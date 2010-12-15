
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
from os import makedirs
from os.path import exists,splitext,split,join
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable
from qiime.parse import parse_qiime_parameters
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable,\
                       create_dir
from run_process_sff_through_split_lib import run_process_sff_through_split_lib,\
                                           web_app_call_commands_serially
from qiime.workflow import print_commands,\
                           print_to_stdout, no_status_updates
from run_chain_pick_otus import run_chain_pick_otus


qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Process SFF and metadata through picking OTUs"
script_info['script_description'] = """\
This script takes an SFF file and a mapping file and performs the \
following steps:

    1) Process SFFs to generate .fna, .qual and flowgram file. (process_sff.py)
    2) De-multiplex sequences. (split_libraries.py)

"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i 454_Reads.sff -m mapping.txt -p custom_parameters.txt -o Output_Directory")]
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
    make_option('-t','--convert_to_flx',action='store_true',\
           dest='convert_to_flx',default=False,\
           help='Convert the SFF to FLX length reads [default: %default]'),\
    make_option('-c','--write_to_all_fasta',action='store_true',\
           dest='write_to_all_fasta',default=False,\
           help='Copy the split_library seqs to folder for concatenation [default: %default]'),\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    study_id = opts.study_id
    run_prefix=splitext(split(opts.map_fname)[-1])[0].split('_')[0]
    print run_prefix
    #output_dir = '/home/wwwuser/user_data/studies/study_%s/processed_data_%s/' % (study_id,run_prefix)
    output_dir = '/tmp/studies/study_%s/processed_data_%s/' % (study_id,run_prefix)
    
          
    print output_dir
    sff_fname=opts.sff_fname
    map_fname = opts.map_fname
    verbose = opts.verbose
    print_only = opts.print_only
    write_to_all_fasta=opts.write_to_all_fasta
    convert_to_flx=opts.convert_to_flx

    try:
       parameter_f = open(opts.parameter_fp)
    except IOError:
        raise IOError,\
        "Can't open parameters file (%s). Does it exist? Do you have read access?"\
        % opts.parameter_fp

    try:
       makedirs(output_dir)
    except OSError:
        pass

    if print_only:
        command_handler = print_commands
    else:
        command_handler = web_app_call_commands_serially

    if verbose:
        status_update_callback = print_to_stdout
    else:
        status_update_callback = no_status_updates
        
    params=parse_qiime_parameters(parameter_f)
    run_process_sff_through_split_lib(study_id=study_id,\
     run_prefix=run_prefix,\
     sff_input_fp=sff_fname,\
     mapping_fp=map_fname,\
     output_dir=output_dir,\
     command_handler=command_handler,\
     params=params,\
     qiime_config=qiime_config,\
     convert_to_flx=convert_to_flx,\
     write_to_all_fasta=write_to_all_fasta,\
     status_update_callback=status_update_callback)
     
    resulting_fasta=join(output_dir,'split_libraries/seqs.fna')
    otu_output_dir=join(output_dir,'gg_97_otus')
    create_dir(otu_output_dir)
    run_chain_pick_otus(resulting_fasta, otu_output_dir, command_handler, \
                        params, qiime_config, parallel=False, \
                        status_update_callback=status_update_callback)

if __name__ == "__main__":
    main()
