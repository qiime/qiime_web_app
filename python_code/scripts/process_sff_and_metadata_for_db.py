#!/usr/bin/env python
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from optparse import make_option
from qiime.util import parse_command_line_parameters, get_options_lookup

options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 # Example required option
 #make_option('-i','--input_dir',help='the input directory'),\
 #options_lookup['input_fasta']
]
script_info['optional_options'] = [\
 # Example optional option
 #make_option('-o','--output_dir',help='the output directory [default: %default]'),\
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)


if __name__ == "__main__":
    main()