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
from qiime.util import load_qiime_config
from qiime.util import load_qiime_config
from load_sff_through_split_lib_to_db import load_otu_mapping


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
    make_option('-i','--input_otu_dir',help='This is the folder containing chained otu mapping'),\
    make_option('-t','--submit_to_test_db',action='store_true',help='By setting this parameter, the data will be submitted to the test database.',default=False),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig
        import cx_Oracle
        if opts.submit_to_test_db:
            data_access = data_access_factory(DataAccessType.qiime_test)
        else:
            data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
        
    input_dir=opts.input_otu_dir

    load_otu_mapping(data_access,input_dir)

if __name__ == "__main__":
    main()
