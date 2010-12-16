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
from run_find_otus_in_database import find_otus
from os import *
from os.path import *

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = """
Checks for existence of OTUs in database given an input fasta file.
"""
script_info['script_description'] = """
This script takes as in put a fasta file and searches the database for OTUs that
have already been selected for exact-match sequences. For those it does match, it will
generate an otu_map.txt file with a list of the otu_id and the sequecnes which map to
it. For those it does not find, it will produce a new fasta file with the sequences which
still need to be run through OTU picking.
"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case")]
script_info['output_description']= "This script produces an otu_map.txt file and a leftover_sequences.fna file."
script_info['required_options'] = [\
    make_option('-i','--input_fasta',help='This is the path to the input fasta file.'),\
    make_option('-f','--leftover_fasta', help='This is the path where the leftover fasta file will be created'),\
    make_option('-m','--otu_map', help='This is the path where the otu_map file will be created')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    input_fasta = opts.input_fasta
    leftover_fasta = opts.leftover_fasta
    otu_map = opts.otu_map
    output_directory = split(leftover_fasta)[0]
    
    # Attempt to create the output dir if it doesn't exist
    if not isdir(output_directory):
        try:
            mkdir(output_directory)
        except IOError, e:
            print 'Could not create output directory. The error was %s' % str(e)
            return
    
    # Do eeet!
    find_otus(input_fasta, leftover_fasta, otu_map)
    
if __name__ == "__main__":
    main()
