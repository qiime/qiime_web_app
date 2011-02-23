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
from qiime.util import parse_command_line_parameters, get_options_lookup
from qiime.submit_to_mgrast import parse_and_submit_params
from os import mkdir
from os.path import exists
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "This script submits metadata to MG-RAST based on a study_id"
script_info['script_description'] = "This script takes a study_id and an MG-RAST web service key and performs metadata submission to the MG-RAST system."
script_info['script_usage'] = [("Example","The user can submit a post-split-library FASTA file, which will be loaded and processed into MG-RAST under the users account ('-w') and project ('-p'), as follows:","submit_metadata_to_mgrast.py -i split_lib_seqs.fna -w user_mgrast_auth_key -p qiime_test_dataset -o ./output_dir")]
script_info['output_description']= "The resulting directory will contain all of the sample-separated FASTA files, along with a log html file, which informs the user of the jobs started on MG-RAST"
script_info['required_options'] = [\
 options_lookup['fasta_as_primary_input'],
 make_option('-w','--web_key_auth',help='the web services authorization key from MG-RAST'),
 make_option('-p','--project_id',help='the title to be used for the project'),
 options_lookup['output_dir'],
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__


def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    #define the variables
    project_id = opts.project_id
    files = opts.input_fasta_fp
    key = opts.web_key_auth
    
    #create directory path
    if opts.output_dir:
        if exists(opts.output_dir):
            output_dir=opts.output_dir
        else:
            try:
                mkdir(opts.output_dir)
                output_dir=opts.output_dir
            except OSError:
                pass
    else:
        dir_path='./'
    
    #call the main function
    log_info=parse_and_submit_params(key, project_id, files,output_dir)
    
        
if __name__ == "__main__":
    main()