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

def run_beta_diversity(otu_table_fp, mapping_fp,
    output_dir, command_handler, params, qiime_config, sampling_depth=None,
    tree_fp=None, parallel=False, status_update_callback=print_to_stdout):
    """ Run the data preparation steps of Qiime 
    
        The steps performed by this function are:
         1) Compute a beta diversity distance matrix;
         2) Peform a principal coordinates analysis on the result of
          Step 1;
         3) Generate a 3D prefs file for optimized coloring of continuous
          variables;
         4) Generate a 3D plot for all mapping fields with colors
          optimized for continuous data;
         5) Generate a 3D plot for all mapping fields with colors
          optimized for discrete data.
    
    """  
    # Prepare some variables for the later steps
    otu_table_dir, otu_table_filename = split(otu_table_fp)
    otu_table_basename, otu_table_ext = splitext(otu_table_filename)
    create_dir(output_dir)
    commands = []
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    mapping_file_header = parse_mapping_file(open(mapping_fp,'U'))[1]
    mapping_fields = ','.join(mapping_file_header)
    
    if sampling_depth:
        # Sample the OTU table at even depth
        even_sampled_otu_table_fp = '%s/%s_even%d%s' %\
         (output_dir, otu_table_basename, 
          sampling_depth, otu_table_ext)
        single_rarefaction_cmd = \
         '%s %s/single_rarefaction.py -i %s -o %s -d %d' %\
         (python_exe_fp, script_dir, otu_table_fp,
          even_sampled_otu_table_fp, sampling_depth)
        commands.append([
         ('Sample OTU table at %d seqs/sample' % sampling_depth,
          single_rarefaction_cmd)])
        otu_table_fp = even_sampled_otu_table_fp
        otu_table_dir, otu_table_filename = split(even_sampled_otu_table_fp)
        otu_table_basename, otu_table_ext = splitext(otu_table_filename)
    
    beta_diversity_metrics = params['beta_diversity']['metrics'].split(',')
    
    dm_fps = []
    for beta_diversity_metric in beta_diversity_metrics:
        
        # Prep the beta-diversity command
        try:
            bdiv_params_copy = params['beta_diversity'].copy()
        except KeyError:
            bdiv_params_copy = {}
        try:
            del bdiv_params_copy['metrics']
        except KeyError:
            pass
        
        params_str = get_params_str(bdiv_params_copy)
            
        if tree_fp:
            params_str = '%s -t %s ' % (params_str,tree_fp)
            
        # Build the beta-diversity command
        if parallel:
            # Grab the parallel-specific parameters
            try:
                params_str += get_params_str(params['parallel'])
            except KeyError:
                pass
            beta_div_cmd = '%s %s/parallel_beta_diversity.py -i %s -o %s --metrics %s -T %s' %\
             (python_exe_fp, script_dir, otu_table_fp,
              output_dir, beta_diversity_metric, params_str)
            commands.append(\
             [('Beta Diversity (%s)' % beta_diversity_metric, beta_div_cmd)])
        else:
            beta_div_cmd = '%s %s/beta_diversity.py -i %s -o %s --metrics %s %s' %\
             (python_exe_fp, script_dir, otu_table_fp, 
              output_dir, beta_diversity_metric, params_str)
            commands.append(\
             [('Beta Diversity (%s)' % beta_diversity_metric, beta_div_cmd)])
        
        
        beta_div_fp = '%s/%s_%s' % \
         (output_dir, beta_diversity_metric, otu_table_filename)
        dm_fps.append((beta_diversity_metric, beta_div_fp))
        
        
    
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)
    
    return dm_fps
    
def run_principal_coordinates(bdiv_files,output_dir, params,qiime_config,
                              command_handler,
                              status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    pc_files=[]
    for beta_diversity_metric,beta_div_fp in bdiv_files:
        # Prep the principal coordinates command
        pc_fp = '%s/%s_pc.txt' % (output_dir, beta_diversity_metric)
        
        pc_files.append((beta_diversity_metric+'_PC',pc_fp))
        try:
            params_str = get_params_str(params['principal_coordinates'])
        except KeyError:
            params_str = ''
    
        # Build the principal coordinates command
        pc_cmd = '%s %s/principal_coordinates.py -i %s -o %s %s' %\
         (python_exe_fp, script_dir, beta_div_fp, pc_fp, params_str)
        commands.append(\
         [('Principal coordinates (%s)' % beta_diversity_metric, pc_cmd)])
         
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)

    return pc_files
    
def run_3d_plots(pc_files,mapping_fp,output_dir, params,qiime_config,
                 command_handler,
                 status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
                            
    # Prep the 3d prefs file generator command
    prefs_fp = '%s/prefs.txt' % output_dir
    try:
        params_str = get_params_str(params['make_prefs_file'])
    except KeyError:
        params_str = ''
        
    # Build the 3d prefs file generator command
    prefs_cmd = \
     '%s %s/make_prefs_file.py -m %s -o %s %s' %\
     (python_exe_fp, script_dir, mapping_fp, prefs_fp, params_str)
    commands.append([('Build prefs file', prefs_cmd)])
    
    bdiv_3d_plots=[]
    
    for beta_diversity_metric,pc_fp in pc_files:
        # Prep the continuous-coloring 3d plots command
        continuous_3d_dir = '%s/%s_3d_continuous/' %\
         (output_dir, beta_diversity_metric)
         
        bdiv_3d_plots.append(('continuous_'+beta_diversity_metric,continuous_3d_dir,
                               '%s_3d_continuous/%s' % (beta_diversity_metric,
                               pc_fp.split('/')[-1]+'_3D.html')))
         
        try:
            makedirs(continuous_3d_dir)
        except OSError:
            pass
        try:
            params_str = get_params_str(params['make_3d_plots'])
        except KeyError:
            params_str = ''
        # Build the continuous-coloring 3d plots command
        continuous_3d_command = \
         '%s %s/make_3d_plots.py -p %s -i %s -o %s -m %s %s' %\
          (python_exe_fp, script_dir, prefs_fp, pc_fp, continuous_3d_dir,\
           mapping_fp, params_str)
    
        # Prep the discrete-coloring 3d plots command
        discrete_3d_dir = '%s/%s_3d_discrete/' %\
         (output_dir, beta_diversity_metric)
         
        bdiv_3d_plots.append(('discrete_'+beta_diversity_metric,discrete_3d_dir,
                            '%s_3d_discrete/%s' % (beta_diversity_metric,
                            pc_fp.split('/')[-1]+'_3D.html')))
        try:
            makedirs(discrete_3d_dir)
        except OSError:
            pass
        try:
            params_str = get_params_str(params['make_3d_plots'])
        except KeyError:
            params_str = ''
            
        # Build the discrete-coloring 3d plots command
        discrete_3d_command = \
         '%s %s/make_3d_plots.py -i %s -o %s -m %s %s' %\
          (python_exe_fp, script_dir, pc_fp, discrete_3d_dir,\
           mapping_fp, params_str)
       
        commands.append([\
          ('Make 3D plots (continuous coloring, %s)' %\
            beta_diversity_metric,continuous_3d_command),\
          ('Make 3D plots (discrete coloring, %s)' %\
            beta_diversity_metric,discrete_3d_command,)])
    
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)
    
    return bdiv_3d_plots
    
#
def run_2d_plots(pc_files,mapping_fp,output_dir, params,qiime_config,
                 command_handler,
                 status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
                            
    # Prep the 2d prefs file generator command
    prefs_fp = '%s/prefs.txt' % output_dir
    try:
        params_str = get_params_str(params['make_prefs_file'])
    except KeyError:
        params_str = ''
        
    # Build the 2d prefs file generator command
    prefs_cmd = \
     '%s %s/make_prefs_file.py -m %s -o %s %s' %\
     (python_exe_fp, script_dir, mapping_fp, prefs_fp, params_str)
    commands.append([('Build prefs file', prefs_cmd)])
    
    bdiv_2d_plots=[]
    
    for beta_diversity_metric,pc_fp in pc_files:
        # Prep the continuous-coloring 2d plots command
        continuous_2d_dir = '%s/%s_2d_continuous/' %\
         (output_dir, beta_diversity_metric)
         
        bdiv_2d_plots.append(('continuous_'+beta_diversity_metric,continuous_2d_dir,
                               '%s_2d_continuous/%s' % (beta_diversity_metric,
                               '2d_pcoa_plots.html')))
         
        try:
            makedirs(continuous_2d_dir)
        except OSError:
            pass
        try:
            params_str = get_params_str(params['make_2d_plots'])
        except KeyError:
            params_str = ''
            
        # Build the continuous-coloring 2d plots command
        continuous_2d_command = \
         '%s %s/make_2d_plots.py -p %s -i %s -o %s -m %s %s' %\
          (python_exe_fp, script_dir, prefs_fp, pc_fp, continuous_2d_dir,\
           mapping_fp, params_str)
    
        # Prep the discrete-coloring 2d plots command
        discrete_2d_dir = '%s/%s_2d_discrete/' %\
         (output_dir, beta_diversity_metric)
         
        bdiv_2d_plots.append(('discrete_'+beta_diversity_metric,discrete_2d_dir,
                            '%s_2d_discrete/%s' % (beta_diversity_metric,
                            '2d_pcoa_plots.html')))
        try:
            makedirs(discrete_2d_dir)
        except OSError:
            pass
        try:
            params_str = get_params_str(params['make_2d_plots'])
        except KeyError:
            params_str = ''
            
        # Build the discrete-coloring 2d plots command
        discrete_2d_command = \
         '%s %s/make_2d_plots.py -i %s -o %s -m %s %s' %\
          (python_exe_fp, script_dir, pc_fp, discrete_2d_dir,\
           mapping_fp, params_str)
       
        commands.append([\
          ('Make 2D plots (continuous coloring, %s)' %\
            beta_diversity_metric,continuous_2d_command),\
          ('Make 2D plots (discrete coloring, %s)' %\
            beta_diversity_metric,discrete_2d_command,)])
    
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)
    
    return bdiv_2d_plots
    
#
def run_make_distance_histograms(bdiv_files,mapping_file_fp,output_dir, params,
                                 qiime_config,command_handler,
                                 status_update_callback=print_to_stdout):

    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    commands = []
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    dist_hist_files=[]
    for beta_diversity_metric,beta_div_fp in bdiv_files:
        # Prep the make distance histograms command
        output_dist_hist = '%s/%s_distance_histograms' % (output_dir,\
                                                        beta_diversity_metric)
        
        dist_hist_files.append((beta_diversity_metric+'_dist_hist',output_dist_hist))
        try:
            params_str = get_params_str(params['make_distance_histograms'])
        except KeyError:
            params_str = ''
    
        # Build the make distance histograms command
        dist_hist_cmd = '%s %s/make_distance_histograms.py -d %s -m %s -o %s %s' %\
         (python_exe_fp, script_dir, beta_div_fp, mapping_file_fp, output_dist_hist, params_str)
        commands.append(\
         [('Make Distance Histograms (%s)' % beta_diversity_metric,dist_hist_cmd)])
         
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)

    return dist_hist_files

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