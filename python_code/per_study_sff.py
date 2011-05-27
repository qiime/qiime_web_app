#!/usr/bin/env python
# File created on 27 May 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.workflow import print_commands,generate_log_fp,\
    call_commands_serially, print_to_stdout, no_status_updates,WorkflowLogger
from write_mapping_file import write_mapping_file
from data_access_connections import data_access_factory
from enums import ServerConfig
from qiime.util import load_qiime_config,create_dir,get_qiime_scripts_dir
qiime_config = load_qiime_config()
data_access = data_access_factory(ServerConfig.data_access_type)
from os.path import splitext,join,basename,split
from os import listdir,environ

def make_study_sffs(output_dir,study_id):
    #get run prefixes and SFF files, then write mapping files
    run_prefixes=write_mapping_file(study_id,False,output_dir,False)
    sff_files = data_access.getSFFFiles(study_id)
    
    # set command handler params
    command_handler = call_commands_serially
    status_update_callback = no_status_updates
    
    file_map={}
    for run_prefix in run_prefixes:
        
        mapping_file='study_%s_run_%s_mapping.txt' % (str(study_id),run_prefix)
        matching_sff_files=[]
    
        for sff_file in sff_files:
            sff_file_basename = splitext(basename(sff_file))[0].upper()
            # If the run_prefix matches the SFF file name exactly, assume only
            # one SFF for this run
            if run_prefix.upper() == splitext(sff_file_basename)[0].upper():
                matching_sff_files.append(sff_file)
                file_map[mapping_file] = matching_sff_files
            # If the run_prefix is contained in the file name, find all that 
            # match and submit them together with the current mapping file
            elif run_prefix.upper() in sff_file_basename:
                # If it's the first item for this mapping file name, assign the 
                # list
                if not file_map.get(mapping_file):
                    file_map[mapping_file] = matching_sff_files
                file_map[mapping_file].append(sff_file)
            # If we get here, there are extra SFF files with no matching mapping  
            # file. For now, do nothing... may need to add some handling code 
            # at a later date.
            else:
                pass
                
        #get barcode length
        barcode_length = data_access.checkRunPrefixBarcodeLengths(study_id, 
                                                                    run_prefix)
        params={}
    
        sff_working_dir=split(file_map[mapping_file][0])[0]
    
        #prepare commands to run
        commands = []
        python_exe_fp = qiime_config['python_exe_fp']
        script_dir = get_qiime_scripts_dir()

        #create log file
        logger = WorkflowLogger(generate_log_fp(output_dir),
                                params=params,
                                qiime_config=qiime_config)
                        
        # Step 1
        process_sff_cmd = '%s %s/process_sff.py -i %s' %\
         (python_exe_fp,script_dir, sff_working_dir)
        
        commands.append([(
            'Process SFF files to create FASTA and QUAL files.',
            process_sff_cmd)])
        
        # Step 1: split libraries
        map_fp = join(output_dir,mapping_file)
        sff_filenames = file_map[mapping_file]
        sff_basepaths = [splitext(x)[0] for x in sff_filenames]
        fna_string = ','.join([b + '.fna' for b in sff_basepaths])
        library_dir = join(output_dir, '%s_demultiplex' % run_prefix)
        create_dir(library_dir)

        # set barcode type based on length
        if barcode_length==12:
            barcode_type='golay_12'
        elif barcode_length==8:
            barcode_type='hamming_8'
        else:
            barcode_type=str(barcode_length)
        
        split_libraries_cmd = \
         '%s %s/split_libraries.py -m %s -f %s -o %s -b %s -H 2000 -w 0 -l 0 -L 3000' %\
         (python_exe_fp,script_dir,map_fp,fna_string,
         library_dir,barcode_type)
    
        commands.append([(
            'Demultiplex run %s.' % run_prefix, split_libraries_cmd)])
    
        seqs_fp = join(library_dir, 'seqs.fna')
    
        # Step 2 - make per library id lists
        per_lib_sff_dir = join(library_dir, 'per_lib_info')
        create_dir(per_lib_sff_dir)
    
        make_library_id_lists_cmd = \
         '%s %s/make_library_id_lists.py -i %s -o %s' % \
         (python_exe_fp, script_dir, seqs_fp,per_lib_sff_dir)

        commands.append([(
            'Create per-library id lists to use when splitting SFF files.',
            make_library_id_lists_cmd)])
        
    
        # Step 3 -- make per library sff files
        sff_string = ','.join(
                    [join(sff_working_dir, x) for x in sff_filenames])
        #params_str = get_params_str(params['make_per_library_sff'])
        make_per_library_sff_cmd = \
         '%s %s/make_per_library_sff.py -i %s -l %s' %\
         (python_exe_fp, script_dir, sff_string, per_lib_sff_dir)
        commands.append([(
            'Create per-library SFF files.', make_per_library_sff_cmd)])
    

        # Call the command handler on the list of commands
        command_handler(commands, status_update_callback, logger)
    
        # need results from first command run to set params, so have to run
        # command_handler again
        logger = WorkflowLogger(generate_log_fp(output_dir),
                                params=params,
                                qiime_config=qiime_config)
        
        #get list of SFFs produced minus the unassigned seqs
        commands=[]
        sff_cat_list=[]
        for fname in listdir(per_lib_sff_dir):
            if fname.endswith('.sff') and fname!='Unassigned.sff':
                outpath_name=join(per_lib_sff_dir,fname)
                sff_cat_list.append(outpath_name)
    
        # Step 4 -- Concatenate SFFSs
        output_sff_dir=join(output_dir,'filtered_sffs')
        create_dir(output_sff_dir)
    
        make_sff_cmd = \
            'cd %s; sfffile %s; cd %s' % (output_sff_dir,' '.join(sff_cat_list),
                                          environ['HOME'])
    
        commands.append([(
         'cat SFF files into study', make_sff_cmd)])
    
        # Step 5 -- rename the concatenated SFF
        output_sff_fname=join(output_sff_dir,'454Reads.sff')
        new_output_sff_fname=join(output_sff_dir,'study_%s_%s.sff' % (study_id,
                                                                    run_prefix))
    
        mv_sff_file_cmd = \
            'mv %s %s' % (output_sff_fname,new_output_sff_fname)
    
        commands.append([('cat SFF files into study', mv_sff_file_cmd)])

        # Call the command handler on the list of commands
        command_handler(commands, status_update_callback, logger)
        