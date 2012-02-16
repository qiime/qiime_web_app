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
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from os import makedirs,path,system
from qiime.util import load_qiime_config,get_qiime_scripts_dir,create_dir
from generate_mapping_and_otu_table import write_mapping_and_otu_table
from submit_job_to_qiime import submitQiimeJob
from qiime.parse import parse_qiime_parameters
from qiime.workflow import print_to_stdout,WorkflowLogger,generate_log_fp,\
                           call_commands_serially,no_status_updates,\
                           WorkflowError,get_params_str
from cogent.app.util import get_tmp_filename
from data_access_connections import data_access_factory
from enums import ServerConfig
from submit_job_to_qiime import submitQiimeJob
from datetime import datetime
from time import strftime

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "This script call the beta_diversity_through_plots workflow script in QIIME"
script_info['script_description'] = """\
This script call the beta_diversity_through_plots workflow script in QIIME
"""
script_info['script_usage'] = [("","","")]
script_info['output_description']= "Output beta diversity plots and puts links in the DB associated to the files generated"
script_info['required_options'] = [\
    make_option('-f','--fs_fp',
        help='this is the location of the actual files on the linux box'),\
    make_option('-w','--web_fp',
        help='this is the location that the webserver can find the files'),\
    make_option('-o','--otu_table_fp',
        help='this is the path to the otu table'),\
    make_option('-q','--mapping_file_fp',
        help='this is the path to the qiime mapping file'),\
    make_option('-p','--fname_prefix',
        help='this is the prefix to append to the users files'),\
    make_option('-u','--user_id',help='this is the user id'),\
    make_option('-m','--meta_id',help='this is the meta analysis id'),\
    make_option('-b','--params_path',help='this is the parameters file used'),\
    make_option('-r','--bdiv_rarefied_at',
        help='this is the rarefaction number'),\
    make_option('-s','--jobs_to_start',
        help='these are the jobs that should be started'),\
    make_option('-g','--tree_fp',help='this is the gg tree to use'),\
    make_option('-d','--run_date',help='this is the run date'),\
    make_option('-z','--zip_fpath',help='this is the zip fpath'),\
    make_option('-x','--zip_fpath_db',help='this is the zip_fpath_db'),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    #get all the options
    tmp_prefix=get_tmp_filename('',suffix='').strip()
    output_dir=path.join(opts.fs_fp,'bdiv',tmp_prefix)
    web_fp=path.join(opts.web_fp,'bdiv',tmp_prefix)
    otu_table_fp=opts.otu_table_fp
    mapping_file_fp=opts.mapping_file_fp
    file_name_prefix=opts.fname_prefix
    user_id=int(opts.user_id)
    meta_id=int(opts.meta_id)
    bdiv_rarefied_at=int(opts.bdiv_rarefied_at)
    jobs_to_start=opts.jobs_to_start.split(',')
    tree_fp=opts.tree_fp
    command_handler=call_commands_serially
    status_update_callback=no_status_updates
    zip_fpath=opts.zip_fpath
    zip_fpath_db=opts.zip_fpath_db
    run_date=opts.run_date
    force=True
    
    # Connect to the database for adding fpaths
    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig
        import cx_Oracle
        data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
    
    # open and get params
    try:
        parameter_f = open(opts.params_path)
    except IOError:
        raise IOError,\
         "Can't open parameters file (%s). Does it exist? Do you have read access?"\
         % opts.params_path
    
    params=parse_qiime_parameters(parameter_f)
    
    create_dir(output_dir)
    commands = []
    
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    # get the beta_diversity metrics, so we can determine the filepaths based
    # on these
    beta_diversity_metrics = params['beta_diversity']['metrics'].split(',')
    
    if 'disthist_bdiv_plots' in jobs_to_start:
        #start preparing the script call
        beta_div_cmd='%s %s/beta_diversity_through_plots.py -i %s -m %s -o %s -t %s -p %s -c %s -a -O 100 -f' %\
            (python_exe_fp, script_dir, otu_table_fp, mapping_file_fp, \
             output_dir,tree_fp,opts.params_path, \
             params['make_distance_histograms']['fields'])
    else:
        #start preparing the script call
        beta_div_cmd='%s %s/beta_diversity_through_plots.py -i %s -m %s -o %s -t %s -p %s -a -O 100 -f' %\
            (python_exe_fp, script_dir, otu_table_fp, mapping_file_fp, output_dir,\
             tree_fp,opts.params_path)
    
    # add in optional parameters depending on whether they are supplied
    if bdiv_rarefied_at:
        beta_div_cmd+=" -e %s" % (str(bdiv_rarefied_at))
    
    html_fpaths=[]
    
    # add 3d plots params
    if '3d_bdiv_plots' not in jobs_to_start:  
        beta_div_cmd+=" --suppress_3d_plots"
    else:
        for met in beta_diversity_metrics:
            html_fpaths.append((path.join(web_fp,'%s_3d_discrete' % (met),
                                '%s_pc_3D_PCoA_plots.html' % (met)),
                                '3D_DISCRETE_PLOT'))
            html_fpaths.append((path.join(web_fp,'%s_3d_continuous' % (met),
                                         '%s_pc_3D_PCoA_plots.html' % (met)), 
                                         '3D_CONTINUOUS_PLOT'))
                                         
    # add 2d plots params
    if '2d_bdiv_plots' not in jobs_to_start:
        beta_div_cmd+=" --suppress_2d_plots"
    else:
        for met in beta_diversity_metrics:
            html_fpaths.append((path.join(web_fp,'%s_2d_discrete' % (met),
                                         '%s_pc_2D_PCoA_plots.html' % (met)),
                                         '2D_DISCRETE_PLOT'))
            html_fpaths.append((path.join(web_fp,'%s_2d_continuous' % (met),
                                         '%s_pc_2D_PCoA_plots.html' % (met)),
                                          '2D_CONTINUOUS_PLOT'))
    
    # add distance histograms params
    if 'disthist_bdiv_plots' not in jobs_to_start:
        #beta_div_cmd+=" --suppress_distance_histograms"
        pass
    else:
        for met in beta_diversity_metrics:
            html_fpaths.append((path.join(web_fp,'%s_histograms' % (met),
                                    '%s_dm_distance_histograms.html' % (met)),
                                         'DISTANCE_HISTOGRAM'))
    
    commands.append([('Beta Diversity Through Plots',beta_div_cmd)])

    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)
    
    
    #zip the files produced
    cmd_call='cd %s; zip -r %s %s' % (output_dir,\
                                      zip_fpath, './*')
    system(cmd_call)

    #add html links to DB for easy display
    for i in html_fpaths:
        valid=data_access.addMetaAnalysisFiles(True,int(meta_id),i[0],
                                               'BDIV',run_date,i[1].upper())
        if not valid:
            raise ValueError, 'There was an issue uploading the filepaths to the DB!'

    
if __name__ == "__main__":
    main()
