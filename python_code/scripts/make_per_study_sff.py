#!/usr/bin/env python
# File created on 09 Feb 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

from os.path import abspath
from os import makedirs
from sys import argv, exit, stderr, stdout
from qiime.util import parse_command_line_parameters, get_options_lookup,\
                       create_dir,make_option
from per_study_sff import make_study_sffs
options_lookup = get_options_lookup()


script_info={}
script_info['brief_description']="""Make SFFs for a particular DB study"""
script_info['script_description']=""" """
script_info['script_usage']=[]
script_info['script_usage'].append(("","""""",""""""))
script_info['output_description']=""""""
script_info['required_options']=[\
    make_option('-s', '--study_id', help='Database study_id'),
    options_lookup['output_dir'],
]
script_info['optional_options']=[\
    make_option('-f','--force',action='store_true',\
           dest='force',help='Force overwrite of existing output directory'+\
           ' (note: existing files in output_dir will not be removed)'+\
           ' [default: %default]'),\
]

script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    
    output_dir=abspath(opts.output_dir)
    study_id=int(opts.study_id)
    try:
        makedirs(output_dir)
    except OSError:
        if opts.force:
            pass
        else:
            # Since the analysis can take quite a while, I put this check
            # in to help users avoid overwriting previous output.
            print "Output directory already exists. Please choose "+\
             "a different directory, or force overwrite with -f."
            exit(1)
    make_study_sffs(output_dir,study_id)

if __name__ == "__main__":
    main()