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
from data_access_connections import data_access_factory
from enums import ServerConfig

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
    curl_command_fp = join(study_dir, 'ebi_curl_command_{0}.sh'.format(study_id))

    # Get the live EBI function reference
    live = LiveEBISRARestServices(study_id, web_app_user_id, root_dir, debug)
    live.host_name = ''

    # Make one pass through metadata to generate files to validate. Also
    # necessary to populate the list of sequence files to send.
    live.generate_metadata_files(debug = True, action_type = 'VALIDATE')
    if len(live.errors):
        print 'Errors found while generating metadata files. Aborting. Errors are:'
        for error in live.errors:
            print 'Error: {0}'.format(error)
        return
    
    # Send the sequence files first - required for metadata to validate. If files have already been
    # sent then skip this step.
    data_access = data_access_factory(ServerConfig.data_access_type)
    statement = 'select case when ebi_files_sent is null then 0 else ebi_files_sent end as ebi_files_sent from study where study_id = {0}'.format(study_id)
    ebi_files_sent = data_access.dynamicMetadataSelect(statement).fetchone()[0]
    if ebi_files_sent != 1:
        try:
            live.submit_files(debug = True)
        except Exception, e:
            print 'Error encountered while submitting files. Aborting. Error was:'
            print str(e)
            return
    
    # Submit the metadata with the VALIDATE attribute first. Performs no other actions
    # on EBI server other than ensuring that XML validates. 

    # Check if valid, if so regenerate with ADD attribute and send again for reals
    result, curl_result = live.send_curl_data(curl_output_fp, curl_command_fp)
    if result == 'VALID':
        print 'VALID, resending to EBI with ADD attribute.'
        live.generate_metadata_files(debug = True, action_type = 'ADD')
        result, curl_result = live.send_curl_data(curl_output_fp, curl_command_fp)
        print curl_result
        print 'SUCCESS'
    else:
        print 'INVALID'
        print curl_result
        PRINT 'FAILED'


if __name__ == "__main__":
    main()
