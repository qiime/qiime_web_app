#!/usr/bin/env python
# File created on 28 Mar 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from subprocess import Popen, PIPE, STDOUT
from os import makedirs, listdir
from glob import glob
from os.path import split, splitext, join, dirname, abspath
from datetime import datetime
from numpy import array
from cogent.parse.fasta import MinimalFastaParser
from qiime.parse import parse_mapping_file
from qiime.format import format_otu_table
from qiime.util import (compute_seqs_per_library_stats, 
                        get_qiime_scripts_dir,
                        create_dir)
from qiime.workflow import print_to_stdout,\
                           call_commands_serially,no_status_updates,\
                           WorkflowError,WorkflowLogger,generate_log_fp,\
                           get_params_str


#
def run_make_otu_heatmap_html(otu_table_fp,mapping_fp,output_dir, params,
                              qiime_config,
                              command_handler,tree_fp,
                              status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    
    try:
        params_str = get_params_str(params['make_otu_heatmap_html'])
    except KeyError:
        params_str = ''

    # Build the principal coordinates command
    heatmap_cmd = '%s %s/make_otu_heatmap_html.py -i %s -m %s -t %s -o %s %s' %\
     (python_exe_fp, script_dir, otu_table_fp, mapping_fp,tree_fp, output_dir,params_str)
    commands.append(\
     [('OTU Heatmap' , heatmap_cmd)])
     
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)

    return True

#
def run_summarize_taxa(otu_table_fp, mapping_fp,
    output_dir, command_handler, params, qiime_config, 
    status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    levels_to_summarize=params['summarize_taxa']['level'].split(',')
    
    if params['summarize_taxa'].has_key('absolute_abundance'):
        abs_abund=params['summarize_taxa']['absolute_abundance']
    else:
        abs_abund=False
    
    sum_taxa_files=[]
    sum_levels=[]
    for level in levels_to_summarize:
        # Prep the make distance histograms command
        basename,base_ext=splitext(split(otu_table_fp)[-1])
        output_level_file = '%s/%s_L%s.txt' % (output_dir,basename,str(level))
        sum_taxa_files.append(output_level_file)
    
        if int(level)==1:
            sum_levels.append('Domain')
        elif int(level)==2:
            sum_levels.append('Phylum')
        elif int(level)==3:
            sum_levels.append('Class')
        elif int(level)==4:
            sum_levels.append('Order')
        elif int(level)==5:
            sum_levels.append('Family')
        elif int(level)==6:
            sum_levels.append('Genus')
        elif int(level)==7:
            sum_levels.append('Species')
            
        # Build the make distance histograms command
        if abs_abund:
            sum_taxa_cmd = '%s %s/summarize_taxa.py -i %s -o %s -L %s -a' %\
             (python_exe_fp, script_dir, otu_table_fp, output_dir, \
              str(level))
        else:
            sum_taxa_cmd = '%s %s/summarize_taxa.py -i %s -o %s -L %s' %\
                (python_exe_fp, script_dir, otu_table_fp, output_dir, \
                 str(level))
        commands.append(\
         [('Summarize Taxa (Level %s)' % str(level),sum_taxa_cmd)])
         


    # Prep the plot taxa summary cmd
    try:
        params_str = get_params_str(params['plot_taxa_summary'])
    except KeyError:
        params_str = ''

    # Build the make distance histograms command
    plot_tax_sum_cmd = '%s %s/plot_taxa_summary.py -i %s -l %s -o %s %s' %\
     (python_exe_fp, script_dir, ','.join(sum_taxa_files),','.join(sum_levels),\
      output_dir, params_str)
    commands.append(\
     [('Plot Taxa-Summary',plot_tax_sum_cmd)])

    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)

    plot_files=[]
    plot_types=params['plot_taxa_summary']['chart_type'].split(',')
    
    for i in plot_types:
        plot_files.append('%s_charts.html' % i)
    
    
    return plot_files
    
    
#
def run_summarize_otu_by_cat(otu_table_fp, mapping_fp,
    output_dir, command_handler, params, qiime_config,
    status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    # Prep the summarize by cat command
    try:
        params_str = get_params_str(params['summarize_otu_by_cat'])
    except KeyError:
        params_str = ''

    # Build the make distance histograms command
    sum_by_cat_cmd = '%s %s/summarize_otu_by_cat.py -c %s -i %s -o %s/%s_otu_table.txt %s' %\
     (python_exe_fp, script_dir, otu_table_fp, mapping_fp, output_dir,params_str.split(' ')[-1], params_str)
    commands.append(\
     [('Sum OTU by Category',sum_by_cat_cmd)])
         
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)
    sumcat_files=glob('%s/*_otu_table.txt' % output_dir)
    return sumcat_files
#