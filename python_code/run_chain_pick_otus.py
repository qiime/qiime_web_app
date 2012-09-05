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
from os import system, popen, listdir, mkdir,environ
from glob import glob
import re, sys
from random import choice
from datetime import datetime
from time import strftime
from qiime.workflow import WorkflowLogger
from os.path import split, join, splitext, abspath, realpath
from qiime.parse import fields_to_dict
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,\
                           get_params_str, WorkflowError
from qiime.util import (compute_seqs_per_library_stats, 
                        get_qiime_scripts_dir,
                        create_dir)
from wrap_files_for_md5 import MD5Wrap
from cogent.parse.flowgram_parser import get_header_info
from hashlib import md5
from cogent.util.misc import safe_md5

def generate_log_fp(output_dir,
                    basefile_name='log',
                    suffix='txt',
                    timestamp_pattern='%Y%m%d%H%M%S'):
    """ Generate a log filepath """
    
    timestamp = datetime.now().strftime(timestamp_pattern)
    filename = '%s.%s' % (basefile_name,suffix)
    
    return join(output_dir,filename)

## Begin task-specific workflow functions
def run_chain_pick_otus(fasta_file, output_dir, command_handler, params, 
                        qiime_config, parallel=False,
                        status_update_callback=print_to_stdout):
    """ NOTE: Parts of this function are a directly copied from the
        run_qiime_data_preparation function from the workflow.py library file 
        in QIIME.
    
        The steps performed by this function are:
            1) Pick OTUs;

    """
    
    # Prepare some variables for the later steps
    #split_lib_fasta_filenames=fasta_files.split(',')
    otu_maps_to_merge=[]
    commands = []

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()

    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    ###Starting the Chain OTU picking###
    # Perform exact match pre-filtering
    exact_match_otus_dir=join(output_dir,'pick_otus_exact')
    pick_otus_cmd = '%s %s/pick_otus.py -m prefix_suffix -i %s -o %s -p 5000' %\
        (python_exe_fp, script_dir, fasta_file, exact_match_otus_dir)
    
    commands.append([('Pick OTUs: Exact match', pick_otus_cmd)])
    
    # Pick Rep set from exact match pre-filtering
    exact_match_basename=splitext(split(fasta_file)[-1])[0]
    exact_otu_fp=join(exact_match_otus_dir,exact_match_basename+'_otus.txt')
    exact_match_fna = join(exact_match_otus_dir,exact_match_basename) + \
                                                                '_exact_rep.fna'
    otu_maps_to_merge.append(exact_otu_fp)
    
    pick_rep_set_exact_cmd = '%s %s/pick_rep_set.py -i %s -f %s -o %s ' %\
        (python_exe_fp, script_dir, exact_otu_fp, fasta_file, exact_match_fna)

    commands.append([('Pick Rep Set: Exact match', pick_rep_set_exact_cmd)])

    # Do exact-match database pre-filtering
    leftover_fasta = join(output_dir, 'leftover.fasta')
    db_otu_map = join(output_dir, 'otu_map.txt')
    web_app_scripts_dir = join(split(realpath(__file__))[0], 'scripts')
    find_db_otus_command = '%s %s/find_otus_in_database.py -i %s -f %s -m %s' %\
        (python_exe_fp, web_app_scripts_dir, exact_match_fna, leftover_fasta,\
         db_otu_map)
        
    commands.append([('Find Database OTU Hits', find_db_otus_command)])
    
    # Prep the UCLUST_REF OTU picking command
    otu_picking_method = params['pick_otus']['otu_picking_method'].upper()
    otu_picking_similarity = int(float(params['pick_otus']['similarity'])*100)
    pick_otu_dir = '%s/picked_otus_%s_%s' % (output_dir,otu_picking_method,\
                                             otu_picking_similarity)
    uclust_otu_fp = join(pick_otu_dir,\
                         splitext(split(leftover_fasta)[-1])[0]+'_otus.txt')
    uclust_failure_fp = join(pick_otu_dir,\
                        splitext(split(leftover_fasta)[-1])[0]+'_failures.txt')

    # Grab the OTU picker parameters
    try:
        # Want to find a cleaner strategy for this: the parallel script
        # is method-specific, so doesn't take a --otu_picking_method
        # option. This works for now though.
        d = params['pick_otus'].copy()
        del d['otu_picking_method']
        params_str = ' %s' % get_params_str(d)
    except KeyError:
        pass
        
    if parallel:
        # Grab the parallel-specific parameters
        
        # Grab the OTU picker parameters
        try:
            # Want to find a cleaner strategy for this: the parallel script
            # is method-specific, so doesn't take a --otu_picking_method
            # option. This works for now though.
            d = params['pick_otus'].copy()
            del d['otu_picking_method']
            del d['clustering_algorithm']
            del d['suppress_new_clusters']
            params_str = ' %s' % get_params_str(d)
        except KeyError:
            pass
        
        try:
            params_str += ' %s' % get_params_str(params['parallel'])
        except KeyError:
            params_str += ''
        
        # Build the OTU picking command
        pick_otus_cmd = '%s %s/parallel_pick_otus_uclust_ref.py -i %s -T -o %s %s' %\
         (python_exe_fp, script_dir, leftover_fasta, pick_otu_dir, params_str)
        
    else:
        try:
            # Want to find a cleaner strategy for this: the parallel script
            # is method-specific, so doesn't take a --otu_picking_method
            # option. This works for now though.
            d = params['pick_otus'].copy()
            params_str = ' %s' % get_params_str(d)
        except KeyError:
            pass
            
        # Build the OTU picking command
        pick_otus_cmd = '%s %s/pick_otus.py -i %s -o %s %s' %\
         (python_exe_fp, script_dir, leftover_fasta, pick_otu_dir, params_str)
    
    commands.append([('Pick OTUs: uclust_ref', pick_otus_cmd)])
    
    # Must now merge the otu file produced from database matching and the file
    # produced by uclust_ref - they are of the same kind but need to be mashed
    # together
    combined_otu_file = join(output_dir, 'combined_otu_map.txt')
    otu_map_files = [db_otu_map, uclust_otu_fp]
    otu_maps_to_merge.append(combined_otu_file)
    combine_otu_maps_cmd = '%s %s/combine_otu_map_files.py -i %s -o %s' %\
          (python_exe_fp, web_app_scripts_dir, ','.join(otu_map_files), 
           combined_otu_file)
        
    commands.append([('Combine OTU maps', combine_otu_maps_cmd)])
    
    # Run merge_otu_maps.py on the newly combined file and the originally 
    # produced otu map
    merged_otus_fp = join(output_dir,'exact_uclust_ref_otus.txt')
    merge_otus_cmd = '%s %s/merge_otu_maps.py -i %s -o %s' %\
          (python_exe_fp, script_dir, ','.join(otu_maps_to_merge), 
           merged_otus_fp)
          
    commands.append([('Merge OTUs', merge_otus_cmd)])
    
    # Deal with failures produced in uclust_ref
    all_failures_fp = join(output_dir,'all_failures.txt')
    merge_otus_failures_cmd = '%s %s/merge_otu_maps.py -f %s -i %s -o %s' %\
          (python_exe_fp, script_dir, uclust_failure_fp, exact_otu_fp, 
           all_failures_fp)
          
    commands.append([('Merge OTUs - Failures', merge_otus_failures_cmd)])
    
    # Make OTU Table
    otu_biom_fp = join(output_dir,'exact_uclust_ref_otu_table.biom')
    make_otu_biom_cmd='%s %s/make_otu_table.py -i %s -o %s' %\
            (python_exe_fp, script_dir, merged_otus_fp, otu_biom_fp)

    commands.append([('Make Biom File', make_otu_biom_cmd)])
    
    # Convert to classic OTU table
    otu_table_fp = join(output_dir,'exact_uclust_ref_otu_table.txt')
    make_otu_table_cmd='%s %s/software/biom-format/scripts/convert_biom.py -i %s -o %s -b' %\
            (python_exe_fp, environ['HOME'], otu_biom_fp, otu_table_fp)

    commands.append([('Make OTU Table', make_otu_table_cmd)])
    
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger=logger)
    
