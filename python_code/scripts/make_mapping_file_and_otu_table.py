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
from generate_mapping_and_otu_table import write_mapping_and_otu_table


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
    make_option('-q','--query',help='this is the path to the users query'),\
    make_option('-t','--tax_class',help='this is the taxonomy assignment to use.'),\
    make_option('-p','--fname_prefix',help='this is the prefix to append to the users files'),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    try:
        from data_access_connections import data_access_factory
        from enums import DataAccessType
        import cx_Oracle
        data_access = data_access_factory(DataAccessType.qiime_production)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
        
    table_col_value=eval(open(opts.query).read())
    fs_fp=opts.fs_fp
    web_fp=opts.web_fp
    tax_class=opts.tax_class
    file_name_prefix=opts.fname_prefix

    write_mapping_and_otu_table(data_access, table_col_value, fs_fp, web_fp, tax_class, file_name_prefix)

if __name__ == "__main__":
    main()
