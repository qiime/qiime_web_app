#!/usr/bin/env python
# File created on 16 Feb 2011
from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from optparse import make_option
from qiime.util import parse_command_line_parameters
from enums import ServerConfig
from summarize_seqs_otu_hits import summarize_all_stats, submit_mapping_to_database

script_info = {}
script_info['brief_description'] = "This script summarizes sequence and OTU counts."
script_info['script_description'] = "Reads and summarizes the split_library_log.txt \
    file and the output from per_library_stats.py and genereates summary data for both."
script_info['script_usage'] = [("Example","This is an example usage", "python summarize_seqs_otus.py -s 123")]
script_info['output_description']= "There is no output from the script. It directly updates the Qiime database with the found results."
script_info['required_options'] = [make_option('-p','--processed_data_dir', help='The processed data directory')]
script_info['optional_options'] = [\
    make_option('-d','--debug', action='store_true', help='Specifies that verbose debug output should be displayed.',default=True)
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # Some needed variables
    processed_data_dir = opts.processed_data_dir
    debug = opts.debug

    # Get results for all processed_data_ folders in this study's directory
    processed_results = summarize_all_stats(processed_data_dir)
    submit_mapping_to_database(processed_results, debug)

if __name__ == "__main__":
    main()
