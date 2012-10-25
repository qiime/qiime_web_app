#!/usr/bin/env python
# File created on 28 Mar 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2012, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from os.path import split, splitext, join, dirname, abspath
from qiime.util import get_qiime_scripts_dir
from qiime.workflow import print_to_stdout,\
                           call_commands_serially,no_status_updates,\
                           WorkflowError,WorkflowLogger,generate_log_fp,\
                           get_params_str


def run_make_otu_heatmap_html(otu_table_fp,mapping_fp,output_dir, params,
                              qiime_config,
                              command_handler,tree_fp,
                              status_update_callback=print_to_stdout):
    """ This function calls the make_otu_heatmap_html script """
    
    # define upper-level values
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    # get the user-defined parameters
    try:
        params_str = get_params_str(params['make_otu_heatmap_html'])
    except KeyError:
        params_str = ''

    # Build the make_otu_heatmap_html command
    heatmap_cmd = '%s %s/make_otu_heatmap_html.py -i %s -m %s -t %s -o %s %s' %\
     (python_exe_fp, script_dir, otu_table_fp, mapping_fp,tree_fp, output_dir, 
      params_str)
    
    commands.append([('OTU Heatmap' , heatmap_cmd)])
     
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)

    return True
