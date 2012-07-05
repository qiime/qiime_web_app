#!/usr/bin/env python
# File created on 06 Jun 2012
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2012, The QIIME-DB Project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, make_option,create_dir
from os.path import join
from os import environ,remove,removedirs,system

from collate_per_study_seqs_lib import (write_full_mapping_file,
                                        generate_full_split_lib_seqs,
                                        generate_full_split_lib_fastq,
                                        generate_split_lib_log,
                                        generate_full_otu_table,
                                        scp_files_to_thebeast)
                                        
script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 # Example required option
 make_option('-s','--study_ids',type="string",
             help='comma-separated list of study ids'),\
 
]
script_info['optional_options'] = [\
 make_option('-p','--public',action="store_true",
             help='is the study public [%default]', default=False),\
 make_option('-f','--generate_fastq',action="store_true",
             help='generate a split-lib fastq file [%default]', default=False),\
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    # command-line options
    studies=opts.study_ids.split(',')
    public=opts.public
    generate_fastq=opts.generate_fastq
    
    # define the input location of all studies
    input_dir='%s/user_data/studies/' % environ['HOME']
    
    for study in studies:
        # create a list of files to remove
        files_to_remove=[]
        print study
        # define study input directory
        study_input_dir=join(input_dir,'study_%s' % (str(study)))
        output_dir=join(study_input_dir,'study_%s_split_library_seqs_and_mapping'  % (str(study)))
        create_dir(output_dir)
        
        # define the zip file where all files will be compressed
        folder_name="study_%s_split_library_seqs_and_mapping" % (str(study))
        zip_fname="study_%s_split_library_seqs_and_mapping.tgz" % (str(study))
        zip_fp=join(study_input_dir,zip_fname)
        # add to list of files to remove
        files_to_remove.append(zip_fp)
        
        files_to_remove=write_full_mapping_file(study, study_input_dir,
                                                zip_fname, files_to_remove,
                                                output_dir)
        
        if generate_fastq:
            files_to_remove, biom_files, samples = \
                generate_full_split_lib_fastq(study, study_input_dir, zip_fname,
                                             files_to_remove,output_dir)
        else:
            files_to_remove, biom_files, samples = \
                generate_full_split_lib_seqs(study, study_input_dir, zip_fname,
                                             files_to_remove,output_dir)
        
        files_to_remove=generate_split_lib_log(study, study_input_dir,
                                               zip_fname, files_to_remove,
                                               samples,output_dir)
        
        files_to_remove=generate_full_otu_table(study, study_input_dir, 
                                                zip_fname, files_to_remove,
                                                biom_files,output_dir)
        
        # zip the full split-library sequence file
        cmd_call='cd %s; tar czvf %s %s' % (study_input_dir,zip_fname,folder_name)
        system(cmd_call)
        
        scp_files_to_thebeast(study,zip_fp,zip_fname,public)
        # remove all files generated to reduce space
        map(remove,files_to_remove)
        removedirs(output_dir)
        

if __name__ == "__main__":
    main()
