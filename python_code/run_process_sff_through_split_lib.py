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

import time 
from subprocess import Popen, PIPE, STDOUT
from qiime.parse import parse_mapping_file
from cogent.parse.fastq import MinimalFastqParser
from cogent.parse.fasta import MinimalFastaParser
from qiime.format import format_map_file
from cogent.util.misc import app_path
from cogent.app.util import ApplicationNotFoundError
from os import system,popen,environ
from glob import glob
import re
from random import choice
from datetime import datetime
from time import strftime
from qiime.workflow import WorkflowLogger
from os.path import *
from qiime.parse import fields_to_dict
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,\
                           get_params_str, WorkflowError
from qiime.util import (compute_seqs_per_library_stats, 
                        get_qiime_scripts_dir,
                        create_dir,
                        get_split_libraries_fastq_params_and_file_types)
from wrap_files_for_md5 import MD5Wrap
from cogent.parse.flowgram_parser import get_header_info
from hashlib import md5
from cogent.util.misc import safe_md5
from qiime.validate_demultiplexed_fasta import run_fasta_checks
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

def generate_log_fp(output_dir,
                    basefile_name='log',
                    suffix='txt',
                    timestamp_pattern='%Y%m%d%H%M%S'):
    timestamp = datetime.now().strftime(timestamp_pattern)
    filename = '%s.%s' % (basefile_name,suffix)
    return join(output_dir,filename)
    
## Begin task-specific workflow functions
def run_process_sff_through_split_lib(study_id,run_prefix,sff_input_fp,
    mapping_fp, output_dir, 
    command_handler, params, qiime_config,
    convert_to_flx=False, write_to_all_fasta=False,
    status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
          1) Process SFFs to generate .fna, .qual and flowgram file.
             (process_sff.py)
          2) De-multiplex sequences. (split_libraries.py)
          
    """

    # Prepare some variables for the later steps
    sff_filenames=sff_input_fp.split(',')
    commands = []
    create_dir(output_dir)
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    
    # generate a log file
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    make_flowgram=True
    split_lib_fasta_input_files=[]
    split_lib_qual_input_files=[]
    denoise_flow_input_files=[]

    # make a copy of the mapping file
    copied_mapping=split(mapping_fp)[-1]
    mapping_input_fp_copy=join(output_dir, copied_mapping)
    copy_mapping_cmd='cp %s %s' % (mapping_fp,mapping_input_fp_copy)
    commands.append([('CopyMapping', copy_mapping_cmd)])
    
    # iterate over SFFs and match to the mapping file
    for sff_input_fp in sff_filenames:
        # GENERATE THE MD5 HERE AND STORE IN THE DATABASE AFTER FILE 
        # SUCCESSFULLY PROCESSED
        
        # Copy the SFF into the processed files directory
        copied_sff=split(sff_input_fp)[-1]
        sff_input_fp_copy=join(output_dir, copied_sff)

        #Generate filenames for split_libraries
        input_dir, input_filename = split(sff_input_fp)
        input_basename, input_ext = splitext(input_filename)
        # Convert sff file into fasta, qual and flowgram file
        if convert_to_flx:
            if study_id in ['496','968','969','1069','1002','1066','1194','1195','1457','1458','1460','1536']:
                ### this function is for handling files where the barcode and
                ### linkerprimer are all lowercase (i.e. HMP data or SRA data)
                
                # write process_sff command
                process_sff_cmd = '%s %s/process_sff.py -i %s -f -o %s -t --no_trim --use_sfftools' %\
                                  (python_exe_fp, script_dir, sff_input_fp,
                                   output_dir)
                
                commands.append([('ProcessSFFs', process_sff_cmd)])
                
                # define output fasta from process_sff
                no_trim_fasta_fp=join(output_dir,input_basename + '_FLX.fna')
                
                # define pprospector scripts dir
                pprospector_scripts_dir=join(ServerConfig.home,'software',
                                                 'pprospector','scripts')
                
                # clean fasta - basically converting lowercase to uppercase
                clean_fasta_cmd = '%s %s/clean_fasta.py -f %s -o %s' %\
                                      (python_exe_fp, pprospector_scripts_dir, 
                                       no_trim_fasta_fp,output_dir)
                
                commands.append([('CleanFasta', clean_fasta_cmd)])
                
                # move the cleaned file to be consistent with other processes
                cleaned_fasta_fp=join(output_dir,input_basename + \
                                      '_FLX_filtered.fasta')
                moved_fasta_fp=join(output_dir,input_basename + '_FLX.fna')
                mv_cmd='mv %s %s' %  (cleaned_fasta_fp,moved_fasta_fp)

                commands.append([('RenameFasta',mv_cmd)])
                
                # update the split-lib files to use the cleaned file
                split_lib_fasta_input_files.append(moved_fasta_fp)
                split_lib_qual_input_files.append(join(output_dir,
                                                input_basename + '_FLX.qual'))
                denoise_flow_input_files.append(join(output_dir,
                                                input_basename + '_FLX.txt'))
            else:
                # write process_sff command
                process_sff_cmd = '%s %s/process_sff.py -i %s -f -o %s -t' %\
                                  (python_exe_fp, script_dir, sff_input_fp,
                                   output_dir)
                
                commands.append([('ProcessSFFs', process_sff_cmd)])
                
                # get filepaths for generated files
                split_lib_fasta_input_files.append(join(output_dir,
                                                input_basename + '_FLX.fna'))
                split_lib_qual_input_files.append(join(output_dir,
                                                input_basename + '_FLX.qual'))
                denoise_flow_input_files.append(join(output_dir,
                                                input_basename + '_FLX.txt'))
                
                
        else:
            # write process_sff command
            process_sff_cmd = '%s %s/process_sff.py -i %s -f -o %s' %\
                                (python_exe_fp, script_dir, sff_input_fp,
                                 output_dir)
            
            commands.append([('ProcessSFFs', process_sff_cmd)])
            
            # get filepaths for generated files
            split_lib_fasta_input_files.append(join(output_dir,input_basename + '.fna'))
            split_lib_qual_input_files.append(join(output_dir,input_basename + '.qual'))
            denoise_flow_input_files.append(join(output_dir,input_basename + '.txt'))
        

    split_lib_fasta_input=','.join(split_lib_fasta_input_files)
    split_lib_qual_input=','.join(split_lib_qual_input_files)
    denoise_flow_input=','.join(denoise_flow_input_files)
    
    # If dataset is metagenomic disable primer check
    data_access = data_access_factory(ServerConfig.data_access_type)
    study_info=data_access.getStudyInfo(study_id,12171)
    if study_info['investigation_type'].lower() == 'metagenome':
        params['split_libraries']['disable_primers']=None
    
    # create split-libraries folder
    split_library_output=join(output_dir,'split_libraries')
    create_dir(split_library_output)
    
    # get params string
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
    
    # create per sample fastq files
    fastq_output=join(split_library_output,'per_sample_fastq')
    create_dir(fastq_output)
    try:
        params_str = get_params_str(params['convert_fastaqual_fastq'])
    except KeyError:
        params_str = ''
        
    input_qual_fp=join(split_library_output,'seqs_filtered.qual')
    
    # build the convert fasta/qual to fastq command
    create_fastq_cmd = '%s %s/convert_fastaqual_fastq.py -f %s -q %s -o %s %s'%\
     (python_exe_fp, script_dir, input_fp, input_qual_fp,
      fastq_output, params_str)
      
    commands.append([('Create FASTQ', create_fastq_cmd)])
   
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)
    
    # Return the fasta file paths
    return split_lib_fasta_input_files
    
def run_process_illumina_through_split_lib(study_id,run_prefix,input_fp,
    mapping_fp, output_dir, 
    command_handler, params, qiime_config,
    write_to_all_fasta=False,
    status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
          1) De-multiplex sequences. (split_libraries_fastq.py)
    
    """

    # Prepare some variables for the later steps
    filenames=input_fp.split(',')
    commands = []
    create_dir(output_dir)
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    # copy the mapping file
    copied_mapping=split(mapping_fp)[-1]
    mapping_input_fp_copy=join(output_dir, copied_mapping)
    copy_mapping_cmd='cp %s %s' % (mapping_fp,mapping_input_fp_copy)
    commands.append([('CopyMapping', copy_mapping_cmd)])

    # sort the filenames
    filenames.sort()
    
    # determine which file is seq-file and which is barcode-file and associate
    # to mapping file
    input_str=get_split_libraries_fastq_params_and_file_types(filenames,
                                                              mapping_fp)
    
    # create split_libaries folder
    split_library_output=join(output_dir,'split_libraries')
    create_dir(split_library_output)
    
    # get params string
    try:
        params_str = get_params_str(params['split_libraries_fastq'])
    except KeyError:
        params_str = ''
    
    # Build the split libraries command
    split_libraries_cmd = '%s %s/split_libraries_fastq.py -o %s -m %s %s %s' % \
     (python_exe_fp, script_dir, split_library_output, mapping_input_fp_copy,
      input_str,params_str)
    
    commands.append([('SplitLibraries', split_libraries_cmd)])
    
    # define the generate files
    input_fp=join(split_library_output,'seqs.fna')
    
    # create per sample fastq files
    fastq_output=join(split_library_output,'per_sample_fastq')
    create_dir(fastq_output)
    
    """
    # not used for the one-off
    try:
        params_str = get_params_str(params['convert_fastaqual_fastq'])
    except KeyError:
        params_str = ''
    """
    
    # build the per-sample fastq command
    input_qual_fp=join(split_library_output,'seqs.qual')
    create_fastq_cmd = '%s %s/git/qiime_web_app/python_code/scripts/make_per_sample_fastq.py -i %s -q %s -o %s' % \
    (python_exe_fp, environ['HOME'], input_fp, input_qual_fp, fastq_output)
    
    """
    # TURN ON when convert_fastaqual_fastq can handle Illumina qual file
    create_fastq_cmd = '%s %s/convert_fastaqual_fastq.py -f %s -q %s -o %s %s'%\
     (python_exe_fp, script_dir, input_fp, input_qual_fp,
      fastq_output, params_str)
    """
    commands.append([('Create FASTQ', create_fastq_cmd)])
    
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)

    # Return the fasta file paths
    return filenames


def run_process_fasta_through_split_lib(study_id,run_prefix,input_fp,
    mapping_fp, output_dir, 
    command_handler, params, qiime_config,
    write_to_all_fasta=False,
    status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
          1) Update sequence names using DB accessions
    
    """

    # Prepare some variables for the later steps
    filenames=input_fp.split(',')
    commands = []
    create_dir(output_dir)
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    # copy the mapping file
    copied_mapping=split(mapping_fp)[-1]
    mapping_input_fp_copy=join(output_dir, copied_mapping)
    copy_mapping_cmd='cp %s %s' % (mapping_fp,mapping_input_fp_copy)
    commands.append([('CopyMapping', copy_mapping_cmd)])

    # sort filenames
    filenames.sort()
    
    # create split_libraries directory
    split_library_output=join(output_dir,'split_libraries')
    create_dir(split_library_output)
    
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)
    
    # define output filepath
    output_fp=join(split_library_output,'seqs.fna')
    
    # re-write the sequence file
    outf=open(output_fp,'w')
    
    # get sample-info from mapping file
    map_data,map_header,map_comments=parse_mapping_file(\
                                        open(mapping_input_fp_copy,'U'))
                                        
    # create dictionary of original sample_ids to new sample_ids
    sample_ids_from_mapping=zip(*map_data)[0]
    sample_id_dict={}
    for sample in sample_ids_from_mapping:
        sample_id_dict['.'.join(sample.split('.')[:-1])]=sample
    
    
    # NEED to be able to just pass fasta file, since mapping sample_ids
    # will not match input fasta file ever
    '''
    fasta_check=run_fasta_checks(input_fp,mapping_input_fp_copy)
    
    if float(fasta_check['invalid_labels']) > 0:
        raise ValueError, "There are invalid sequence names in the Original sequence file"
    #elif float(fasta_check['barcodes_detected']) > 0:
    #    raise ValueError, "There are barcode sequences found in the Original sequence file"
    elif float(fasta_check['duplicate_labels']) > 0:
        raise ValueError, "There are duplicate sequence names in the Original sequence file"
    elif float(fasta_check['invalid_seq_chars']) > 0:
        raise ValueError, "There are invalid nucleotides in the sequence Original file (i.e. not A,C,G,T or N)"
    #elif float(fasta_check['linkerprimers_detected']) > 0:
    #    raise ValueError, "There are linker primer sequences in the Original sequence file"
    #elif float(fasta_check['nosample_ids_map']) > 0.20:
    #    raise ValueError, "More than 20% of the samples in the mapping file do not have sequences"
    ''' 
    
    # parse the sequences
    sequences=MinimalFastaParser(open(input_fp),'U')
    
    # update fasta file with new DB SampleIDs and create new split-lib seqs 
    # file
    num=1
    for seq_name,seq in sequences:
        seq_name_arr=seq_name.split()
        updated_seq_name =sample_id_dict['_'.join(seq_name_arr[0].split('_')[:-1])] + \
                '_' + str(num) + ' ' + ' '.join(seq_name_arr[1:])
        num=num+1
        outf.write('>%s\n%s\n' % (updated_seq_name,seq))
    outf.close()
        
        
    # Return the fasta file paths
    return filenames


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
    """Copy files """
    
    check_cp()
    cmd_call='cp %s %s' % (filepath,location)
    #print 'cp command is: %s' % cmd_call
    return cmd_call
    
def zip_files(filepath1,filepath2,directory,location):
    """Zip files"""
    
    check_zip()
    cmd_call='cd %s | zip -jX split_library_input.zip %s' % (directory,filepath1)
    print 'zip command is: %s' % cmd_call
    system(cmd_call)
    cmd_call='cd %s | zip -jX split_library_input.zip %s' % (directory,filepath2)
    print 'zip command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call

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

