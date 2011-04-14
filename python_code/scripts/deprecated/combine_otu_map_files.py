from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable
from qiime.parse import parse_qiime_parameters
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable, create_dir
from run_combine_otu_map_files import combine_otu_files
from os import *
from os.path import *

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = """
Combines a list of sibling OTU map files into a single otu map file.
"""
script_info['script_description'] = """
This script takes in a list of 'like' OTU map files and combines them into a single file.
Another way to think of this is all source files should be siblings, i.e. descended from
the same parent process.
"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i 'otu_map_1.txt,otu_map_2.txt' -o combined_otu_map.txt")]
script_info['output_description']= "This script produces a combined otu_map file."
script_info['required_options'] = [\
    make_option('-i','--input_list',help='This is a comma separated list of input otu map files.'),\
    make_option('-o','--output_otu_file', help='This is the path where the combined otu map file will be written.')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    input_list = opts.input_list
    output_otu_file = opts.output_otu_file
    
    # Do eeet!
    combine_otu_files(input_list, output_otu_file)
    
if __name__ == "__main__":
    main()
