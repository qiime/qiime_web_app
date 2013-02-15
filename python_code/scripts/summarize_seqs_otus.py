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
from data_access_connections import data_access_factory
from enums import ServerConfig
from summarize_seqs_otu_hits import summarize_all_stats

script_info = {}
script_info['brief_description'] = "This script summarizes sequence and OTU counts."
script_info['script_description'] = "Reads and summarizes the split_library_log.txt \
    file and the output from per_library_stats.py and genereates summary data for both."
script_info['script_usage'] = [("Example","This is an example usage", "python summarize_seqs_otus.py -s 123")]
script_info['output_description']= "There is no output from the script. It directly updates the Qiime database with the found results."
script_info['required_options'] = [make_option('-s','--study_id', help='The study_id to be summarized')]
script_info['optional_options'] = [\
    make_option('-d','--debug', action='store_true', help='Specifies that verbose debug output should be displayed.',default=True)
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # Some needed variables
    study_id = opts.study_id
    debug = opts.debug
    data_access = data_access_factory(ServerConfig.data_access_type)

    # Get results for all processed_data_ folders in this study's directory
    processed_results = summarize_all_stats(study_id)
    
    # Iterate over each folder's data - can be many processed_data_ folders for a single study
    for directory in processed_results:
        # Unpack the values for each processed_data_ directory
        mapping, seq_header_lines, otu_header_lines = processed_results[directory]

        # Unpack and iterate over each mapping
        for sample_name, sequence_count, otu_count, percent_assignment in mapping:
            sequence_prep_id = sample_name.split('.')[-1]
    	
            # Write values to database for this sequence_prep_id        
            data_access.updateSeqOtuCounts(sequence_prep_id, sequence_count, otu_count, percent_assignment)
    	
            if debug:
        		print 'added to database: prep: {0}, seq_count: {1}, otu_count: {2}'.format(\
        			str(sequence_prep_id), str(sequence_count), str(otu_count))

if __name__ == "__main__":
    main()
