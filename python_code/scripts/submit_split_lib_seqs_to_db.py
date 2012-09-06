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
from load_analysis_seqs_through_otu_table import submit_sff_and_split_lib, \
                                             submit_illumina_and_split_lib,\
                                             load_otu_mapping,\
                                             submit_fasta_and_split_lib,\
                                             load_split_lib_sequences
                                             
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Submit processed sequence data into the DB"
script_info['script_description'] = """\
This script will submit the demultiplexed data into the QIIME-DB"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i /path/to/files/processed_data_/454_Reads.fna -t False -s 0 -u 0 -o /path/to/files/processed_data_/ -a 0 -r 0 -m c2227d43cf8cf377178e093d2899a9f9")]
script_info['output_description']= "There is no output from the script is puts the processed data into the Oracle DB."
script_info['required_options'] = [\
    make_option('-i','--fasta_file_paths',help='This is the processed fasta filepath(s) from process_sff.py'),\
    make_option('-t','--submit_to_test_db',help='By setting this parameter, the data will be submitted to the test database.'),\
    make_option('-s','--study_id',help='This is the study id assigned from loading the metadata'),\
    make_option('-u','--user_id',help='user id'),\
    make_option('-o','--output_dir',help='output directory'),\
    make_option('-a','--analysis_id',help='analysis id'),\
    make_option('-r','--seq_run_id',help='sequencing run id'),\
    make_option('-m','--split_lib_md5',help='MD5 checksum for input split-lib seqs'),\
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
    analysis_id=opts.analysis_id
    seq_run_id=opts.seq_run_id
    user_id=opts.user_id
    split_lib_md5=opts.split_lib_md5
    
    if submit_to_test_db == 'False':
        # Load the data into the database
        data_access = data_access_factory(ServerConfig.data_access_type)
    else:
        # Load the data into the database 
        data_access = data_access_factory(DataAccessType.qiime_test)

    split_library_id=load_split_lib_sequences(data_access,output_dir,
                                              analysis_id, seq_run_id,
                                              split_lib_md5)
    
    print 'Completed database loading.'

if __name__ == "__main__":
    main()
