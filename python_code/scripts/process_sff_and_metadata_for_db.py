
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2011, The QIIME WebApp project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from os import makedirs
from os.path import exists
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable
from qiime.parse import parse_qiime_parameters
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable
from run_sample_export import export_samples

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Exports samples to a fasta file."
script_info['script_description'] = """\
This script takes in a list of sample names and writes the to a new fasta file \
"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -s 454_Reads.sff -m mapping.txt -p custom_parameters.txt -o Output_Directory")]
script_info['output_description']= "The output of this script produces the FNA, QUAL, and flowgram files, the output of split_libraries.py and pick_otus.py."
script_info['required_options'] = [\
    make_option('-i','--sff_fname',help='This is the input sff filepath(s)'),\
    make_option('-s','--study_id',help='This is the study id assigned by the web-interface'),\
    make_option('-m', '--map_fname', dest='map_fname', \
      help='This is the metadata mapping file'), \
    make_option('-p','--parameter_fp',\
             help='path to the parameter file [REQUIRED]. E.g. /python_code/')
]
script_info['optional_options'] = [\
    make_option('-f','--force',action='store_true',\
           dest='force',help='Force overwrite of existing output directory'+\
           ' (note: existing files in output_dir will not be removed)'+\
           ' [default: %default]'),\
    make_option('-w','--print_only',action='store_true',\
           dest='print_only',help='Print the commands but don\'t call them -- '+\
           'useful for debugging [default: %default]',default=False),\
    make_option('-d','--denoise',action='store_true',\
           dest='denoise',help='Denoise the supplied dataset'+\
           '[default: %default]',default=False),\
    make_option('-a','--parallel',action='store_true',\
           dest='parallel',default=False,\
           help='Run in parallel where available [default: %default]'),\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    study_id = opts.study_id

    for i in range(1,25):
        output_dir='/home/wwwdevuser/user_data/studies/study_%s/processed_data_%s/' % (study_id,i)
        if not exists(output_dir):
            break
        else:
            continue
            
    print output_dir
    sff_fname=opts.sff_fname
    map_fname = opts.map_fname
    verbose = opts.verbose
    print_only = opts.print_only
    parallel = opts.parallel
    denoise=opts.denoise
    
    if parallel: 
        raise_error_on_parallel_unavailable()

    try:
       parameter_f = open(opts.parameter_fp)
    except IOError:
        raise IOError,\
        "Can't open parameters file (%s). Does it exist? Do you have read access?"\
        % opts.parameter_fp

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

    if print_only:
        command_handler = print_commands
    else:
        command_handler = web_app_call_commands_serially

    if verbose:
        status_update_callback = print_to_stdout
    else:
        status_update_callback = no_status_updates

    run_process_sff_through_pick_otus(sff_input_fp=sff_fname,\
     mapping_fp=map_fname,\
     output_dir=output_dir,\
     denoise=denoise,\
     command_handler=command_handler,\
     params=parse_qiime_parameters(parameter_f),\
     qiime_config=qiime_config,\
     parallel=parallel,\
     status_update_callback=status_update_callback)

if __name__ == "__main__":
    main()
