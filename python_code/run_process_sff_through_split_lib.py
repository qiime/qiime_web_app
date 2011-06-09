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
          3) Optionally denoise the sequences (set sff_input_fp=True);
          4) Pick OTUs;
          
    """
    if write_to_all_fasta:
        split_lib_fastas='%s/user_data/studies/all_split_lib_fastas' % environ['HOME']
        create_dir(split_lib_fastas)
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
    
    copied_mapping=split(mapping_fp)[-1]
    mapping_input_fp_copy=join(output_dir, copied_mapping)
    copy_mapping_cmd='cp %s %s' % (mapping_fp,mapping_input_fp_copy)
    commands.append([('CopyMapping', copy_mapping_cmd)])
    for sff_input_fp in sff_filenames:
        ##### GENERATE THE MD5 HERE AND STORE IN THE DATABASE AFTER FILE SUCCESSFULLY PROCESSED
        
        # Copy the SFF into the processed files directory
        copied_sff=split(sff_input_fp)[-1]
        sff_input_fp_copy=join(output_dir, copied_sff)
        #copy_sff_cmd='cp %s %s' % (sff_input_fp,sff_input_fp_copy)
        #commands.append([('CopySFF', copy_sff_cmd)])
        
        #Generate filenames for split_libraries
        input_dir, input_filename = split(sff_input_fp)
        input_basename, input_ext = splitext(input_filename)
        # Convert sff file into fasta, qual and flowgram file
        if convert_to_flx:
            process_sff_cmd = '%s %s/process_sff.py -i %s -f -o %s -t' %\
                (python_exe_fp, script_dir, sff_input_fp,
                 output_dir)
            split_lib_fasta_input_files.append(join(output_dir,input_basename + '_FLX.fna'))
            split_lib_qual_input_files.append(join(output_dir,input_basename + '_FLX.qual'))
            denoise_flow_input_files.append(join(output_dir,input_basename + '_FLX.txt'))
        else:
            process_sff_cmd = '%s %s/process_sff.py -i %s -f -o %s' %\
            (python_exe_fp, script_dir, sff_input_fp,
             output_dir)
            split_lib_fasta_input_files.append(join(output_dir,input_basename + '.fna'))
            split_lib_qual_input_files.append(join(output_dir,input_basename + '.qual'))
            denoise_flow_input_files.append(join(output_dir,input_basename + '.txt'))
        commands.append([('ProcessSFFs', process_sff_cmd)])
        

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
    
    if write_to_all_fasta:
        copy_split_lib_seqs_location='%s_%s_seqs.fna' % (study_id,run_prefix)
        copy_to_split_lib_fastas_cmd=cp_files(input_fp,join(split_lib_fastas,
                                        copy_split_lib_seqs_location))
        commands.append([('cpSplitLib', copy_to_split_lib_fastas_cmd)])
   
   
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)

    # Return the fasta file paths
    return split_lib_fasta_input_files
    
#
## Begin task-specific workflow functions
def run_process_illumina_through_split_lib(study_id,run_prefix,input_fp,
    mapping_fp, output_dir, 
    command_handler, params, qiime_config,
    write_to_all_fasta=False,
    status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
          1) De-multiplex sequences. (split_libraries.py)
    
    """
    
    #print input_fp
    if write_to_all_fasta:
        split_lib_fastas='%s/user_data/studies/all_split_lib_fastas' \
                            % environ['HOME']
        create_dir(split_lib_fastas)
        
    # Prepare some variables for the later steps
    filenames=input_fp.split(',')
    commands = []
    create_dir(output_dir)
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    

    
    copied_mapping=split(mapping_fp)[-1]
    mapping_input_fp_copy=join(output_dir, copied_mapping)
    copy_mapping_cmd='cp %s %s' % (mapping_fp,mapping_input_fp_copy)
    commands.append([('CopyMapping', copy_mapping_cmd)])

    filenames.sort()

    #fastq_dict={}
    #mapping_file=open(mapping_fp,'U')
    
    # iterate over files and import them
    # both seqs and barcode files are valid fastq files, so we need
    # to look at the length of seq and/or barcode to determine the file types
    #for file in filenames:
    #    fastq_dict[file]=open(file,'U')
    
    input_str=get_split_libraries_fastq_params_and_file_types(filenames,
                                                              mapping_fp)
    
    split_library_output=join(output_dir,'split_libraries')
    create_dir(split_library_output)

    '''
    try:
        params_str = get_params_str(params['split_libraries'])
    except KeyError:
        params_str = ''
    '''
    
    # Build the split libraries command
    split_libraries_cmd = '%s %s/split_libraries_fastq.py -o %s -m %s %s' % \
     (python_exe_fp, script_dir, split_library_output, mapping_input_fp_copy,
      input_str)
    commands.append([('SplitLibraries', split_libraries_cmd)])
    
    input_fp=join(split_library_output,'seqs.fna')
    
    
    if write_to_all_fasta:
        copy_split_lib_seqs_location='%s_%s_seqs.fna' % (study_id,run_prefix)
        copy_to_split_lib_fastas_cmd=cp_files(input_fp,join(split_lib_fastas,
                                        copy_split_lib_seqs_location))
        commands.append([('cpSplitLib', copy_to_split_lib_fastas_cmd)])
    
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)

    # Return the fasta file paths
    return ','.join(filenames)

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
    """Transfers files to another server."""
    check_cp()
    cmd_call='cp %s %s' % (filepath,location)
    #print 'cp command is: %s' % cmd_call
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

