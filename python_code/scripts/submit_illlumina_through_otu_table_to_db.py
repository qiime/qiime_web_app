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
from os import makedirs
from os.path import split, join
from qiime.util import load_qiime_config
from load_sff_through_split_lib_to_db import submit_illumina_and_split_lib, \
                                             load_otu_mapping
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

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
    make_option('-i','--fasta_file_paths',help='This is the processed fasta filepath(s) from process_sff.py'),\
    make_option('-t','--submit_to_test_db',help='By setting this parameter, the data will be submitted to the test database.'),\
    make_option('-s','--study_id',help='This is the study id assigned from loading the metadata'),\
    make_option('-u','--user_id',help='user id'),\
    make_option('-o','--output_dir',help='output directory'),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    
    submit_to_test_db=opts.submit_to_test_db
    fasta_file_paths=opts.fasta_file_paths
    study_id=opts.study_id
    output_dir=opts.output_dir
    
    if submit_to_test_db == 'False':
        # Load the data into the database
        data_access = data_access_factory(ServerConfig.data_access_type)
    else:
        # Load the data into the database 
        data_access = data_access_factory(DataAccessType.qiime_test)


    # Get all of the fasta files
    print 'Submitting SFF data to database...'
    analysis_id = submit_sff_and_split_lib(data_access, fasta_file_paths, study_id)
    print 'Submitting OTU data to database...'
    load_otu_mapping(data_access, output_dir, analysis_id)
    print 'Completed database loading.'

if __name__ == "__main__":
    main()
