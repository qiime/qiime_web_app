#!/usr/bin/env python
# File created on 16 Feb 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from optparse import make_option
from qiime.util import parse_command_line_parameters
from run_submit_metadata_to_mgrast import submit_metadata_for_study

script_info = {}
script_info['brief_description'] = "This script submits metadata to MG-RAST based on a study_id"
script_info['script_description'] = "This script takes a study_id and an MG-RAST web service key and performs metadata submission to the MG-RAST system."
script_info['script_usage'] = [("Example","This is an example usage", "python submit_data_to_mgrast.py -s 12345")]
script_info['output_description']= "There is no output from the script is puts the processed data into the Oracle DB."
script_info['required_options'] = [make_option('-s','--study_id', help='The study id to be exported')]
script_info['optional_options'] = []
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # define the variables
    study_id = opts.study_id
    
    # call the main function
    key = 'y7x2G29QEbuEyTYbLr7pjavtA'
    result = submit_metadata_for_study(key, study_id)
    
        
if __name__ == "__main__":
    main()
