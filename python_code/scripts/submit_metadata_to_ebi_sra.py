#!/usr/bin/env python
# File created on 16 Feb 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"


from optparse import make_option
from qiime.util import parse_command_line_parameters
from live_ebi_sra_rest_services import LiveEBISRARestServices

from os.path import join

script_info = {}
script_info['brief_description'] = "This script submits metadata to the EBI SRA based on a study_id"
script_info['script_description'] = "This script takes a study_id and a web service key and performs metadata submission to the EBI SRA system."
script_info['script_usage'] = [("Example","This is an example usage", "python submit_data_to_ebi_sra.py -s 12345")]
script_info['output_description']= "There is no output from the script."
script_info['required_options'] = [make_option('-s','--study_id', help='The study id to be exported')]
script_info['optional_options'] = [\
    make_option('-d','--debug', action='store_true', help='Specifies that verbose debug output should be displayed.',default=True)
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # Some needed variables
    study_id = opts.study_id
    debug = opts.debug
    web_app_user_id = 12169
    root_dir = '/home/wwwuser/user_data/studies'
    study_dir = root_dir + '/study_{0}'.format(str(study_id))
    ebi_export_log_fp = join(study_dir, 'ebi_export_log.txt')
    curl_output_fp = join(study_dir, 'curl_output.xml')

    # Get the live EBI function reference
    live = LiveEBISRARestServices(study_id, web_app_user_id, root_dir, debug)
    live.host_name = ''
    
    # Send the sequence files first - required for metadata to validate. If files have already been
    # sent then skip this step.
    statement = 'select ebi_files_sent from study where study_id = {0}'.format(study_id)
    ebi_files_sent = data_access.dynamicMetadataSelect(statement).fetchone()[0]
    if ebi_files_sent != 1:
        live.submit_files(debug = True)
    
    # Submit the metadata with the VALIDATE attribute first. Performs no other actions
    # on EBI server other than ensuring that XML validates. 
    live.generate_metadata_files(debug = True, action_type = 'VALIDATE')
    curl_output = open(curl_output_fp, 'r')
    curl_output.close()
    
    # If success, then submit with 'ADD' or 'MODIFY'
    # Read output
    # If error then display to user. If success then proceed with actual submit


if __name__ == "__main__":
    main()
