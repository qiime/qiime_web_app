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
from qiime.util import load_qiime_config
from generate_mapping_and_otu_table import write_mapping_and_otu_table
from submit_job_to_qiime import submitQiimeJob
from qiime.parse import parse_qiime_parameters
from qiime.workflow import print_to_stdout,\
                           call_commands_serially,no_status_updates
from handler_workflows import run_beta_diversity,run_principal_coordinates,\
                              run_3d_plots,run_2d_plots,\
                              run_make_distance_histograms
from cogent.app.util import get_tmp_filename

from data_access_connections import data_access_factory
from enums import ServerConfig
from submit_job_to_qiime import submitQiimeJob
from datetime import datetime
from time import strftime

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Submit processed SFF and metadata through picking OTUs into the Oracle DB"
script_info['script_description'] = """\
This script takes an processed sff fasta file and performs the \
following steps:

    1) 
    2) 
    3) 
    4) 
"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i 454_Reads.fna")]
script_info['output_description']= "There is no output from the script is puts the processed data into the Oracle DB."
script_info['required_options'] = [\
    make_option('-f','--fs_fp',help='this is the location of the actual files on the linux box'),\
    make_option('-w','--web_fp',help='this is the location that the webserver can find the files'),\
    make_option('-o','--otu_table_fp',help='this is the path to the otu table'),\
    make_option('-q','--mapping_file_fp',help='this is the path to the qiime mapping file'),\
    make_option('-p','--fname_prefix',help='this is the prefix to append to the users files'),\
    make_option('-u','--user_id',help='this is the user id'),\
    make_option('-m','--meta_id',help='this is the meta analysis id'),\
    make_option('-b','--params_path',help='this is the parameters file used'),\
    make_option('-r','--bdiv_rarefied_at',help='this is the rarefaction number'),\
    make_option('-s','--jobs_to_start',help='these are the jobs that should be started'),\
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
    jobs_to_start=opts.jobs_to_start
    tree_fp=opts.tree_fp
    command_handler=call_commands_serially
    zip_fpath=opts.zip_fpath
    zip_fpath_db=opts.zip_fpath_db
    run_date=opts.run_date
    force=True
    
    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig
        import cx_Oracle
        data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
        
    try:
        parameter_f = open(opts.params_path)
    except IOError:
        raise IOError,\
         "Can't open parameters file (%s). Does it exist? Do you have read access?"\
         % opts.params_path
    
    params=parse_qiime_parameters(parameter_f)
    
    try:
        makedirs(output_dir)
    except OSError:
        if force:
            pass
        else:
            # Since the analysis can take quite a while, I put this check
            # in to help users avoid overwriting previous output.
            print "Output directory already exists. Please choose "+\
             "a different directory, or force overwrite with -f."
            exit(1)

    # run beta-diversity calculations and return fpaths
    bdiv_files=run_beta_diversity(otu_table_fp, mapping_file_fp,
        output_dir, command_handler, params, qiime_config,
        sampling_depth=bdiv_rarefied_at,
        tree_fp=tree_fp, parallel=False, 
        status_update_callback=no_status_updates)


    
    #iterate over files generated and put the paths in the database for display
    for dist_file in bdiv_files:
        
        #zip the distance matrices
        cmd_call='cd %s; zip %s %s' % (output_dir,zip_fpath,dist_file[1].split('/')[-1])
        system(cmd_call)
        
        ''' These files are in zip, so don't need a link
        #convert link into web-link
        web_link=path.join(web_fp,dist_file[1].split('/')[-1])
        #add the distance matrices
        valid=data_access.addMetaAnalysisFiles(True,int(meta_id),web_link,'BDIV',run_date,dist_file[0].upper())
        if not valid:
            raise ValueError, 'There was an issue uploading the filepaths to the DB!'
        '''

    analyses_to_start=jobs_to_start.split(',')
    if '3d_bdiv_plots' in analyses_to_start or '2d_bdiv_plots' in analyses_to_start:
        
        pc_files=run_principal_coordinates(bdiv_files,output_dir, params,
                                           qiime_config,command_handler,
                                           status_update_callback=no_status_updates)
    
        #iterate over files generated and put the paths in the database for display    
        for pc_file in pc_files:
        
            #zip the distance matrices
            cmd_call='cd %s; zip %s %s' % (output_dir,zip_fpath,pc_file[1].split('/')[-1])
            system(cmd_call)
            
            ''' These files are in zip, so don't need a link
            #convert link into web-link
            web_link=path.join(web_fp,pc_file[1].split('/')[-1])
            #add the distance matrices
            valid=data_access.addMetaAnalysisFiles(True,int(meta_id),web_link,'BDIV',run_date,pc_file[0].upper())
            if not valid:
                raise ValueError, 'There was an issue uploading the filepaths to the DB!'
            '''

   

    if '3d_bdiv_plots' in analyses_to_start:
        
        bdiv_3d_fpaths=run_3d_plots(pc_files,mapping_file_fp,output_dir, params,
                                    qiime_config,command_handler,
                                    status_update_callback=no_status_updates)


        #iterate over files generated and put the paths in the database for display
        for bdiv_3d_plots in bdiv_3d_fpaths:

            #zip the distance matrices
            cmd_call='cd %s; zip -r %s %s' % (output_dir,zip_fpath,bdiv_3d_plots[2].split('/')[0])
            system(cmd_call)

            #convert link into web-link
            web_link=path.join(web_fp,bdiv_3d_plots[2])
            #add the distance matrices
            valid=data_access.addMetaAnalysisFiles(True,int(meta_id),web_link,'BDIV',run_date,bdiv_3d_plots[0].upper())
            if not valid:
                raise ValueError, 'There was an issue uploading the filepaths to the DB!'
                
    #
    if '2d_bdiv_plots' in analyses_to_start:
        
        bdiv_2d_fpaths=run_2d_plots(pc_files,mapping_file_fp,output_dir, params,
                                    qiime_config,command_handler,
                                    status_update_callback=no_status_updates)


        #iterate over files generated and put the paths in the database for display
        for bdiv_2d_plots in bdiv_2d_fpaths:

            #zip the distance matrices
            cmd_call='cd %s; zip -r %s %s' % (output_dir,zip_fpath,bdiv_2d_plots[2].split('/')[0])
            system(cmd_call)

            #convert link into web-link
            web_link=path.join(web_fp,bdiv_2d_plots[2])
            #add the distance matrices
            valid=data_access.addMetaAnalysisFiles(True,int(meta_id),web_link,'BDIV',run_date,bdiv_2d_plots[0].upper())
            if not valid:
                raise ValueError, 'There was an issue uploading the filepaths to the DB!'

    #
    if 'disthist_bdiv_plots' in analyses_to_start:
        
        bdiv_disthist_fpaths=run_make_distance_histograms(bdiv_files,mapping_file_fp,
                                    output_dir, params,
                                    qiime_config,command_handler,
                                    status_update_callback=no_status_updates)


        #iterate over files generated and put the paths in the database for display
        for bdiv_disthist_plots in bdiv_disthist_fpaths:

            #zip the distance matrices
            cmd_call='cd %s; zip -r %s %s' % (output_dir,zip_fpath,bdiv_disthist_plots[1].split('/')[-1])
            system(cmd_call)

            #convert link into web-link
            web_link=path.join(web_fp,bdiv_disthist_plots[1].split('/')[-1],'QIIME_Distance_Histograms.html')
            #add the distance matrices
            valid=data_access.addMetaAnalysisFiles(True,int(meta_id),web_link,'BDIV',run_date,bdiv_disthist_plots[0].upper())
            if not valid:
                raise ValueError, 'There was an issue uploading the filepaths to the DB!'
                

    
    
if __name__ == "__main__":
    main()
