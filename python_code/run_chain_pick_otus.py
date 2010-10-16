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
from cogent.util.misc import app_path
from cogent.app.util import ApplicationNotFoundError
from os import system,popen,listdir
from glob import glob
import re
from random import choice
from datetime import datetime
from time import strftime
from qiime.workflow import WorkflowLogger
from os.path import *
from qiime.parse import fields_to_dict
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,generate_log_fp,\
                           get_params_str, WorkflowError
from qiime.util import (compute_seqs_per_library_stats, 
                        get_qiime_scripts_dir,
                        create_dir)
from wrap_files_for_md5 import MD5Wrap

from cogent.parse.flowgram_parser import get_header_info
from hashlib import md5
from cogent.util.misc import safe_md5


## Begin task-specific workflow functions
def run_chain_pick_otus(fasta_files, output_dir, command_handler, params, qiime_config, parallel=False,
    status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
            1) Pick OTUs;

    """

    # Prepare some variables for the later steps
    split_lib_fasta_filenames=fasta_files.split(',')
    otu_maps_to_merge=[]
    commands = []

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()

    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    study_run_prefix_dict={}
    for i in split_lib_fasta_filenames:
        basename,extension=splitext(i)
        fname=split(basename)[-1]
        study_run_prefix=fname.split('_')
        if study_run_prefix[0] not in study_run_prefix_dict:
            study_run_prefix_dict[study_run_prefix[0]]=[]
        study_run_prefix_dict[study_run_prefix[0]].append(study_run_prefix[1])
    
    study_run_prefix_fpath=join(output_dir,'studies_run_prefix_dict.txt')
    study_run_prefix_out=open(study_run_prefix_fpath,'w')
    study_run_prefix_out.write(str(study_run_prefix_dict))
    study_run_prefix_out.close()
    
    #study_run_prefix_str=eval(open(study_run_prefix_fpath,'U').read())
    #print study_run_prefix_str['0']
    
    concated_seqs_fpath=join(output_dir,'all_split_lib_seqs.fna')
    cat_split_lib_files_cmd=cat_files(fasta_files,concated_seqs_fpath)
    commands.append([('Concat sequences', cat_split_lib_files_cmd)])
    

    ###Starting the Choin OTU picking###
    # Perform exact match pre-filtering
    exact_match_otus_dir=join(output_dir,'pick_otus_exact')
    pick_otus_cmd = '%s %s/pick_otus.py -m prefix_suffix -i %s -o %s -p 5000' %\
     (python_exe_fp, script_dir, concated_seqs_fpath, exact_match_otus_dir)
    
    commands.append([('Pick OTUs: Exact match', pick_otus_cmd)])
    
    # Pick Rep set from exact match pre-filtering
    exact_match_basename=splitext(split(concated_seqs_fpath)[-1])[0]
    exact_otu_fp=join(exact_match_otus_dir,exact_match_basename+'_otus.txt')
    otu_maps_to_merge.append(exact_otu_fp)
    
    pick_rep_set_exact_cmd = '%s %s/pick_rep_set.py -i %s -f %s -o %s_exact_rep.fna ' %\
    (python_exe_fp, script_dir, exact_otu_fp, concated_seqs_fpath, \
     join(exact_match_otus_dir,exact_match_basename))

    commands.append([('Pick Rep Set: Exact match', pick_rep_set_exact_cmd)])
    
    # Perform trie pre-filtering
    exact_match_fasta_fp=join(exact_match_otus_dir,exact_match_basename+'_exact_rep.fna')
    trie_otus_dir=join(output_dir,'pick_otus_trie')
    pick_otus_cmd = '%s %s/pick_otus.py -i %s -o %s -m trie' %\
     (python_exe_fp, script_dir, exact_match_fasta_fp, trie_otus_dir)
    
    commands.append([('Pick OTUs: Trie prefilter', pick_otus_cmd)])
    
    # Pick Rep set from trie pre-filtering
    trie_basename=splitext(split(exact_match_fasta_fp)[-1])[0]
    trie_otu_fp=join(trie_otus_dir,trie_basename+'_otus.txt')
    otu_maps_to_merge.append(trie_otu_fp)
    
    pick_rep_set_exact_cmd = '%s %s/pick_rep_set.py -i %s -f %s -o %s_trie_rep.fna' %\
    (python_exe_fp, script_dir, trie_otu_fp, exact_match_fasta_fp, \
     join(trie_otus_dir,trie_basename))

    commands.append([('Pick Rep Set: Trie prefilter', pick_rep_set_exact_cmd)])
    
    # Prep the UCLUST_REF OTU picking command
    otu_picking_method = params['pick_otus']['otu_picking_method'].upper()
    otu_picking_similarity = int(float(params['pick_otus']['similarity'])*100)

    trie_fasta_fp=join(trie_otus_dir,trie_basename+'_trie_rep.fna')
    
    pick_otu_dir = '%s/picked_otus_%s_%s' % (output_dir,otu_picking_method,
                                                otu_picking_similarity)
                                                
    uclust_otu_fp = join(pick_otu_dir,splitext(split(trie_fasta_fp)[-1])[0]+'_otus.txt')
    
    otu_maps_to_merge.append(uclust_otu_fp)

    params_list=[]
    params_list.append('-s '+params['pick_otus']['similarity'])
    params_list.append('-r '+params['pick_otus']['refseqs_fp'])
    params_list.append('--uclust_stable_sort')
    
    if parallel:
        # Grab the parallel-specific parameters
        try:
            params_str = get_params_str(params['parallel'])
        except KeyError:
            params_str = ''
        
        '''
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
        '''
            
        params_list.append('-O '+params['parallel']['jobs_to_start'])
        params_list.append('-Z '+params['parallel']['seconds_to_sleep'])

        # Build the OTU picking command
        pick_otus_cmd = '%s %s/parallel_pick_otus_uclust_ref.py -i %s -o %s -T %s' %\
         (python_exe_fp, script_dir, trie_fasta_fp, pick_otu_dir, ' '.join(params_list))
    else:
        '''
        try:
            params_str = get_params_str(params['pick_otus'])
        except KeyError:
            params_str = ''
        '''
        params_list.append('--suppress_new_clusters')
        params_list.append('-m '+params['pick_otus']['otu_picking_method'])
        # Build the OTU picking command
        pick_otus_cmd = '%s %s/pick_otus.py -i %s -o %s %s' %\
         (python_exe_fp, script_dir, trie_fasta_fp, pick_otu_dir, ' '.join(params_list))
    
    commands.append([('Pick OTUs: uclust_ref', pick_otus_cmd)])
    
    merged_otus_fp=join(output_dir,'exact_trie_uclust_ref_otus.txt')
    merge_otus_cmd = '%s %s/merge_otu_maps.py -i %s -o %s' %\
          (python_exe_fp, script_dir, ','.join(otu_maps_to_merge), merged_otus_fp)
    commands.append([('Merge OTUs', merge_otus_cmd)])
        
    # Call the command handler on the list of commands
    command_handler(commands,status_update_callback,logger=logger)
    
#
def get_fasta_files(fasta_dir):
    """ Gets a list of fasta files from directory
    """
    fasta_files = listdir(fasta_dir)
    #ignore invisible files like .DS_Store
    fasta_filenames = [fname for fname in fasta_files if (not \
        fname.startswith('.') and fname.endswith('.fna'))]
    
    full_path_fasta_filename=[]
    for i in fasta_filenames:
        full_path_fasta_filename.append(join(fasta_dir,i))

    return full_path_fasta_filename
    
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
    print 'cp command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call

def cat_files(filepath,location):
    """concats files together given comma-separated list of files."""
    check_cat()
    files=' '.join(filepath.split(','))
    cmd_call='cat %s > %s' % (files,location)
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

