
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from os import makedirs,mkdir

from os.path import exists,join,exists,isdir
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable
from qiime.parse import parse_qiime_parameters
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable,\
                        create_dir
from run_chain_pick_otus import run_chain_pick_otus,get_fasta_files,\
web_app_call_commands_serially
from qiime.workflow import print_commands,\
                           print_to_stdout, no_status_updates

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Perform chain picking OTUs on split-library fasta files."
script_info['script_description'] = """\
This script takes an SFF file and a mapping file and performs the \
following steps:

    1) Pick OTUs
"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i 454_Reads.sff -m mapping.txt -p custom_parameters.txt -o Output_Directory")]
script_info['output_description']= "The output of this script produces the FNA, QUAL, and flowgram files, the output of split_libraries.py and pick_otus.py."
script_info['required_options'] = [\
    make_option('-i','--split_lib_seqs',help='This is the input split-lib sequence filepath(s)'),\
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
    make_option('-a','--parallel',action='store_true',\
           dest='parallel',default=False,\
           help='Run in parallel where available [default: %default]'),\
    options_lookup['output_dir']
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)


    verbose = opts.verbose
    print_only = opts.print_only
    parallel = opts.parallel
    output_dir=opts.output_dir
    if output_dir:
        if exists(output_dir):
            dir_path=output_dir
        else:
            try:
                mkdir(output_dir)
                dir_path=output_dir
            except OSError:
                pass
    else:
        dir_path='./'
        
    
    if isdir(opts.split_lib_seqs):
        fasta_files = ','.join(get_fasta_files(opts.split_lib_seqs))
    else:
        fasta_files = opts.split_lib_seqs
    

    if parallel: 
        raise_error_on_parallel_unavailable()

    try:
       parameter_f = open(opts.parameter_fp)
    except IOError:
        raise IOError,\
        "Can't open parameters file (%s). Does it exist? Do you have read access?"\
        % opts.parameter_fp

    try:
        makedirs(dir_path)
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

    new_output_dir=join(dir_path,'chain_picked_otus')
    create_dir(new_output_dir)
    
    run_chain_pick_otus(fasta_files=fasta_files,\
     output_dir=new_output_dir,\
     command_handler=command_handler,\
     params=parse_qiime_parameters(parameter_f),\
     qiime_config=qiime_config,\
     parallel=parallel,\
     status_update_callback=status_update_callback)

if __name__ == "__main__":
    main()
