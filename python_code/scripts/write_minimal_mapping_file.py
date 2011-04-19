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
from os import makedirs,path
import os
from qiime.util import load_qiime_config
from write_mapping_file import write_mapping_file

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
    make_option('-s','--study_id',help='This is the study id assigned from loading the metadata'),\
    options_lookup['output_dir']
]
script_info['optional_options'] = [\
    make_option('-t','--get_from_test_db',action='store_true',help='By setting this parameter, the data will be submitted to the test database.',default=False),\
    make_option('-f','--write_full_mapping',action='store_true',help='By setting this parameter, you can write out all metadata for study.',default=False),\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    if opts.output_dir:
        if path.exists(opts.output_dir):
            dir_path=opts.output_dir
        else:
            try:
                makedirs(opts.output_dir)
                dir_path=opts.output_dir
            except OSError:
                pass
    else:
        dir_path='./'

    get_from_test_db=opts.get_from_test_db
    study_id=opts.study_id
    write_full_mapping=opts.write_full_mapping
    run_prefixes=write_mapping_file(study_id,write_full_mapping,dir_path,get_from_test_db)

    
if __name__ == "__main__":
    main()
