#!/usr/bin/env python
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from subprocess import Popen, PIPE, STDOUT
from qiime.parse import parse_mapping_file
from cogent.util.misc import app_path
from cogent.app.util import ApplicationNotFoundError
from os import system,popen
from glob import glob
import re
from random import choice
from datetime import datetime
from time import strftime
from qiime.workflow import WorkflowLogger
from os.path import *
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,generate_log_fp,\
                           get_params_str, WorkflowError
from qiime.util import (compute_seqs_per_library_stats, 
                        get_qiime_scripts_dir,
                        create_dir)
from hashlib import md5
from qiime_data_access import QiimeDataAccess
data_access = QiimeDataAccess()

## Begin task-specific workflow functions
def run_process_sff_through_pick_otus(sff_input_fp, mapping_fp, output_dir, 
    denoise, command_handler, params, qiime_config, parallel=False,
    status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
          1) Process SFFs to generate .fna, .qual and flowgram file.
             (process_sff.py)
          2) De-multiplex sequences. (split_libraries.py)
          3) Optionally denoise the sequences (set sff_input_fp=True);
          4) Pick OTUs;

    """
    
    # Prepare some variables for the later steps
    sff_filenames=sff_input_fp.split(',')
    commands = []
    create_dir(output_dir)
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    make_flowgram=True
    split_lib_fasta_input_files=[]
    split_lib_qual_input_files=[]
    denoise_flow_input_files=[]
    for sff_input_fp in sff_filenames:
        ##### GENERATE THE MD5 HERE AND STORE IN THE DATABASE AFTER FILE SUCCESSFULLY PROCESSED
        
        # Copy the SFF into the processed files directory
        copied_sff=split(sff_input_fp)[-1]
        sff_input_fp_copy=join(output_dir, copied_sff)
        copy_sff_cmd='cp %s %s' % (sff_input_fp,sff_input_fp_copy)
        commands.append([('CopySFF', copy_sff_cmd)])
        
        # Convert sff file into fasta, qual and flowgram file
        process_sff_cmd = '%s %s/process_sff.py -i %s -f -o %s' %\
         (python_exe_fp, script_dir, sff_input_fp,
          output_dir)
        commands.append([('ProcessSFFs', process_sff_cmd)])
        
        #Generate filenames for split_libraries
        input_dir, input_filename = split(sff_input_fp)
        input_basename, input_ext = splitext(input_filename)
        split_lib_fasta_input_files.append(join(output_dir,input_basename + '.fna'))
        split_lib_qual_input_files.append(join(output_dir,input_basename + '.qual'))
        denoise_flow_input_files.append(join(output_dir,input_basename + '.txt'))
        
    split_lib_fasta_input=','.join(split_lib_fasta_input_files)
    split_lib_qual_input=','.join(split_lib_qual_input_files)
    denoise_flow_input=','.join(denoise_flow_input_files)
    
    split_library_output=join(output_dir,'split_libraries')
    create_dir(split_library_output)
    try:
        params_str = get_params_str(params['split_libraries'])
    except KeyError:
        params_str = ''
    
    # Build the split libraries command
    split_libraries_cmd = '%s %s/split_libraries.py -f %s -q %s -m %s -o %s %s'%\
     (python_exe_fp, script_dir, split_lib_fasta_input, split_lib_qual_input,
      mapping_fp, split_library_output, params_str)
    commands.append([('SplitLibraries', split_libraries_cmd)])
        
    input_fp=join(split_library_output,'seqs.fna')
    
    # Prep the denoising command
    if denoise:
        assert mapping_fp != None,\
         "Mapping file must be provided for denoising."+\
         " (Need to extract the primer sequence.)"
        denoise_output_dir = '%s/denoised_seqs/' % output_dir
        denoised_seqs_fp = '%s/denoised_seqs.fasta' % denoise_output_dir
        denoised_mapping_fp = '%s/denoiser_mapping.txt' % denoise_output_dir
        
        if parallel:
            parallel_str = '-n %s' % qiime_config['jobs_to_start']
        else:
            parallel_str = ''
            
        try:
            params_str = get_params_str(params['denoise'])
        except KeyError:
            params_str = ''
        
        # build the denoiser command
        denoise_cmd='%s %s/denoise.py -i %s -f %s --method fast -m %s -o %s %s %s' %\
         (python_exe_fp, script_dir, denoise_flow_input, input_fp, mapping_fp,
          denoise_output_dir, parallel_str, params_str)
        commands.append([('Denoise', denoise_cmd)])

        # some values that get passed to subsequent steps change when 
        # denoising -- set those here
        original_input_fp = input_fp
        input_fp = denoised_seqs_fp
        input_basename, input_ext = splitext(split(denoised_seqs_fp)[1])
    
    # Prep the OTU picking command
    otu_picking_method = params['pick_otus']['otu_picking_method']
    pick_otu_dir = '%s/picked_otus' % (output_dir)
    otu_fp = '%s/%s_otus.txt' % (pick_otu_dir,input_basename)
    #We will most likely remove blast otu picking
    if parallel and otu_picking_method == 'blast':
        # Grab the parallel-specific parameters
        try:
            params_str = get_params_str(params['parallel'])
        except KeyError:
            params_str = ''
        
        # Grab the OTU picker parameters
        try:
            # Want to find a cleaner strategy for this: the parallel script
            # is method-specific, so doesn't take a --otu_picking_method
            # option. This works for now though.
            d = params['pick_otus'].copy()
            del d['otu_picking_method']
            params_str += ' %s' % get_params_str(d)
        except KeyError:
            pass
            
        # Build the OTU picking command
        pick_otus_cmd = '%s %s/parallel_pick_otus_blast.py -i %s -o %s -T %s' %\
         (python_exe_fp, script_dir, input_fp, pick_otu_dir, params_str)
    else:
        if denoise:
            # we want to make sure the user is using the right set of commands
            # For now we force to use uclust --user_sort --optimal
            # in the future we might want to do this more clever
            # and force the user to have a good parameter set in the config file
            if 'optimal_uclust' not in params['pick_otus']:
                logger.write("Warning: Setting option pick_otus:optimal_uclust "
                             + "to True "
                             + "for compatibility with denoising\n")
            params['pick_otus']['optimal_uclust']=None

            if 'user_sort' not in params['pick_otus']:
                logger.write("Warning: Setting option pick_otus:user_sort to"\
                                 + " True for compatibility with denoising\n")
            params['pick_otus']['user_sort']=None

            if 'presort_by_abundance_uclust' in params['pick_otus']:
                logger.write("Warning: Disabling option pick_otus:"
                              +"presort_by_abundance_uclust "+
                              +"with uclust OTU picker for compatibility with "
                              +"denoising")
                del params['pick_otus']['presort_by_abundance_uclust']
        try:
            params_str = get_params_str(params['pick_otus'])
        except KeyError:
            params_str = ''
        # Build the OTU picking command
        pick_otus_cmd = '%s %s/pick_otus.py -i %s -o %s %s' %\
         (python_exe_fp, script_dir, input_fp, pick_otu_dir, params_str)

    commands.append([('Pick OTUs', pick_otus_cmd)])
    
    # Prep the merge_denoiser_output.py command, if denoising
    if denoise:
        pick_otu_dir = '%s/denoised_otus/' % pick_otu_dir
        
        try:
            params_str = get_params_str(params['merge_denoiser_output'])
        except KeyError:
            params_str = ''
        merge_denoiser_output_cmd = \
         '%s %s/merge_denoiser_output.py -m %s -p %s -f %s -d %s -o %s %s' %\
         (python_exe_fp, script_dir, denoised_mapping_fp, otu_fp, 
          original_input_fp, denoised_seqs_fp, pick_otu_dir, params_str)
          
        input_fp = '%s/denoised_all.fasta' % pick_otu_dir
        otu_fp = '%s/denoised_otu_map.txt' % pick_otu_dir
        commands.append([('Merge denoiser output', merge_denoiser_output_cmd)])
    
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)
    
    
def web_app_call_commands_serially(commands,
                           status_update_callback,
                           logger):
    """Run list of commands, one after another """
    
    for c in commands:
        for e in c:
            status_update_callback('%s\n%s' % e)
            logger.write('# %s command \n%s\n\n' % e)
            proc = Popen(e[1],shell=True,universal_newlines=True,\
                         stdout=PIPE,stderr=STDOUT)
            return_value = proc.wait()
            if return_value != 0:
                msg = "\n\n*** ERROR RAISED DURING STEP: %s\n" % e[0] +\
                 "Command run was:\n %s\n" % e[1] +\
                 "Command returned exit status: %d\n" % return_value +\
                 "Stdout/stderr:\n%s\n" % proc.stdout.read()
                logger.write(msg)
                logger.close()
                raise WorkflowError, msg
    logger.close()
    
def submit_processed_data_to_db(fasta_files):
    '''
       This function takes the fasta filenames and using that path, determines
       the location of the split-library and picked-otu files.  Once file
       locations have been determined, it moves the files to the DB machine
       and load the files into the DB.
    '''
    alphabet = "ABCDEFGHIJKLMNOPQRSTUZWXYZ"
    alphabet += alphabet.lower()
    alphabet += "01234567890"
    random_fname=''.join([choice(alphabet) for i in range(10)])
    tmp_filename ='_'+random_fname+'_'+strftime("%Y_%m_%d_%H_%M_%S")
    fasta_filenames=fasta_files.split(',')
    run_id=0  
    analysis_id=0    
    split_lib_input_checksums=[]
    
    
    valid = data_access.disableTableConstraints()
    print "Disabled table constraints"
    
    #split the fasta filenames and determine filepaths
    for fasta_fname in fasta_filenames:
        input_fname, input_ext = splitext(split(fasta_fname)[-1])
        input_basename, input_ext = splitext(fasta_fname)
        input_dir = split(input_basename)[:-1][0]
        
        analysis_notes=split(input_basename)[0]
        
        #using the fasta basename, define qual and flow files
        qual_fname=join(input_basename+'.qual')
        flow_fname=join(input_basename+'.txt')
        
        split_lib_fasta_md5sum=md5(open(fasta_fname,\
                                        'rb').read()).hexdigest()
        split_lib_input_checksums.append(input_fname+'.fna:%s' % 
                                            split_lib_fasta_md5sum)
        split_lib_qual_md5sum=md5(open(qual_fname,\
                                        'rb').read()).hexdigest()
        split_lib_input_checksums.append(input_fname+'.qual:%s' % 
                                            split_lib_qual_md5sum)
        
        #move the fna, qual and flow files to the database server
        try:
            '''
            cmd_call=scp_file_transfer(23,fasta_fname,'wwwuser',\
                                        'microbiome1.colorado.edu',\
                                        '/SFF_Files/%s.fna' % (input_fname))
            '''
            cmd_call=scp_file_transfer(23,qual_fname,'wwwuser',\
                                        'microbiome1.colorado.edu',\
                                        '/SFF_Files/%s.qual' % (input_fname))
            cmd_call=scp_file_transfer(23,flow_fname,'wwwuser',\
                                        'microbiome1.colorado.edu',\
                                        '/SFF_Files/%s.txt' % (input_fname))
        except:
            raise ValueError, 'Error: Unable to scp files to database server!'
        print "Finished scp transfer of files!"
        
        #Run the Oracle process_sff_files load package
        ## Get the location and name of the SFF file, get it's MD5. .SFF is one 
        # directory up from the other files
        rev = dirname(fasta_fname)[::-1]
        #sff_file = join(rev[rev.find('/'):][::-1], input_fname + '.sff')
        sff_file=input_basename+'.sff'
        sff_md5 = md5(open(sff_file,'rb').read()).hexdigest()

        # Load the data into the datbase. Will raise an exception if it fails.
        valid, run_id, analysis_id = data_access.loadSFFData(True, input_fname+'.sff',\
                                            run_id, sff_md5, analysis_id,\
                                            analysis_notes)
        if not valid:
            raise ValueError,'Error: Unable to load sff files to database server!'
        
    print 'Finished loading the processed SFF data!'
    print 'Run ID: %s' % run_id
    print 'Analysis ID: %s' % analysis_id
    
    
    #define the split library file paths using the original fasta input 
    #directory
    split_lib_seqs = join(input_dir, 'split_libraries', 'seqs.fna')
    split_lib_hist = join(input_dir, 'split_libraries', 'histograms.txt')
    split_lib_log = join(input_dir, 'split_libraries', 'split_library_log.txt')
    split_hist_str = open(split_lib_hist).read()
    split_log_str = open(split_lib_log).read()
    split_lib_input_md5sum=','.join(split_lib_input_checksums)
    
    #read in the workflow log file and determine timestamp and svn version of
    #Qiime used for the analysis
    svn_version = '1418' # This is temporarily defined, however will use script to dtermine this value
    qiime_revision=get_qiime_svn_version()
    run_date=datetime.now().strftime("%m/%d/%Y/%H/%M/%S")
    full_log_fp = glob(join(input_dir, 'log*.txt'))[0]
    full_log_str = open(full_log_fp, 'U').read()
    log_str = open(full_log_fp, 'U').readlines()
    
    #from the workflow log file get the split-library and pick-otus cmds
    for substr in log_str:
        if 'split_libraries.py' in substr:
            split_lib_cmd=substr
        elif 'pick_otus.py' in substr:
            pick_otus_cmd=substr
    
    #Insert the split-library log information in the DB
    valid=data_access.loadSplitLibInfo(True,analysis_id,run_date, split_lib_cmd, \
                                     svn_version, split_log_str, \
                                     split_hist_str, split_lib_input_md5sum)
    
    if not valid:
        raise ValueError,'Error: Unable to load split-library info to database server!'
    
    print "Finished loading the split-library log information!"
    split_lib_fname='%s.fna' % (('sl_seqs'+ tmp_filename))
    print split_lib_fname
    
    #move the resulting seqs.fna file from split-libraries to the DB server
    try:
        cmd_call=scp_file_transfer(23,split_lib_seqs,'wwwuser',\
                                    'microbiome1.colorado.edu',\
                                    '/SFF_Files/%s' % (split_lib_fname))
    except:
        raise ValueError, 'Error: Unable to scp files to database server!'
    
    print "Finished scp transfer the split-library seqs.fna file!"
    
    #Run the Oracle load_fna_file load procedure
    
    valid = data_access.loadSplitLibFasta(True, run_id,split_lib_fname)
    if not valid:
        raise ValueError, 'Error: Unable to load data into database!'
    
    
    print "Finished loading split-library fasta file!"
    
    # For OTU Tables
    
    #define the picked OTU file paths using the original fasta input 
    #directory
    pattern=re.compile("--similarity (\d+)\.(\d+)")
    pOTUs_threshold='.'.join(pattern.search(pick_otus_cmd).groups())
    
    pattern=re.compile("--otu_picking_method (\w+)")
    pOTUs_method=''.join(pattern.search(pick_otus_cmd).groups()).strip()
    
    pick_otus_map = join(input_dir, 'picked_otus', 'seqs_otus.txt')
    pick_otus_failures = join(input_dir, 'picked_otus', 'seqs_failures.txt')
    pick_otus_log = join(input_dir, 'picked_otus', 'seqs_otus.log')
    otus_log_str = open(pick_otus_log).read()
    
    split_lib_seqs_md5 = md5(open(split_lib_seqs,'rb').read()).hexdigest()
    
    #print run_date, split_lib_cmd, svn_version, split_log_str, split_hist_str, comb_checksums
    
    #Insert the otu-picking log information in the DB
    valid=data_access.loadOTUInfo(True, otu_run_set_id, analysis_id, run_date,
                                  pOTUs_method, pOTUs_threshold,
                                  svn_version, pick_otus_cmd, pick_otus_log,
                                  split_lib_seqs_md5)
    
    """
    print 'Starting transfer of OTU file: %s' % pick_otus_map

    try:
        cmd_call = scp_file_transfer(23, pick_otus_map, 'wwwuser',\
            'microbiome1.colorado.edu',\
            '/SFF_Files/otu.dat' % ())    
    except:
        raise ValueError, 'Error: Unable to scp OTU file to database server!'
        
    print "Finished scp transfer of OTU file!"
                                     
    #Insert the pick_otus information in the DB. 
    print 'Starting load of OTU data into database...'
    valid = data_access.loadOTUData(True, run_id)
    print 'Successfully called data_access.loadOTUData()'
    """
    print 'End of function' 
    
    return analysis_id

            
def check_scp():
    """Raise error if scp is not in $PATH """
    if not app_path('scp'):
        raise ApplicationNotFoundError,\
        "scp is not in $PATH. Is it installed? Have you added it to $PATH?"
         
def scp_file_transfer(port,filepath,username,host,location):
    """Transfers files to another server."""
    check_scp()
    cmd_call='scp -P %d %s %s@%s:%s' % (port,filepath,username,host,location)
    print 'scp command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call
    
    
def cp_files(filepath,location):
    """Transfers files to another server."""
    check_cp()
    cmd_call='cp %s %s' % (filepath,location)
    print 'cp command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call
    
def zip_files(filepath1,filepath2,directory,location):
    """Transfers files to another server."""
    check_zip()
    
    cmd_call='cd %s | zip -jX split_library_input.zip %s' % (directory,filepath1)
    print 'zip command is: %s' % cmd_call
    system(cmd_call)
    cmd_call='cd %s | zip -jX split_library_input.zip %s' % (directory,filepath2)
    print 'zip command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call    

def get_qiime_svn_version():
    """Transfers files to another server."""
    qiime_dir=get_qiime_scripts_dir()
    cmd_call='svn info %s | egrep "Revision: "' % (qiime_dir)
    #print 'svn command is: %s' % cmd_call
    output = popen('svn info %s | egrep "Revision: "' % (qiime_dir)).read()
    revision=output.replace("Revision: ","")

    return revision

def check_cat():
    """Raise error if cat is not in $PATH """
    if not app_path('cat'):
        raise ApplicationNotFoundError,\
        "cat is not in $PATH. Is it installed? Have you added it to $PATH?"\
        
def check_cp():
    """Raise error if cp is not in $PATH """
    if not app_path('cp'):
        raise ApplicationNotFoundError,\
        "cp is not in $PATH. Is it installed? Have you added it to $PATH?"\

def check_zip():
    """Raise error if zip is not in $PATH """
    if not app_path('zip'):
        raise ApplicationNotFoundError,\
        "zip is not in $PATH. Is it installed? Have you added it to $PATH?"\

