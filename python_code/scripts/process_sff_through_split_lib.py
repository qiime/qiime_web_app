
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Doug Wendel"
__email__ = "jesse.stombaugh@colorado.edu, wendel@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from os import makedirs, environ, listdir, remove
from os.path import exists,splitext,split,join
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable
from qiime.parse import parse_qiime_parameters
from qiime.util import load_qiime_config, raise_error_on_parallel_unavailable,\
                       create_dir
from run_process_sff_through_split_lib import run_process_sff_through_split_lib,\
                                    web_app_call_commands_serially,\
                                    run_process_illumina_through_split_lib,\
                                    run_process_fasta_through_split_lib
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates
from run_chain_pick_otus import run_chain_pick_otus
from load_analysis_seqs_through_otu_table import submit_sff_and_split_lib, \
                                                 load_otu_mapping
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType
from submit_job_to_qiime import submitQiimeJob
from qiime.validate_demultiplexed_fasta import run_fasta_checks
from shutil import rmtree
from time import sleep
from summarize_seqs_otu_hits import summarize_all_stats, submit_mapping_to_database

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Process Sequences and metadata through picking OTUs"
script_info['script_description'] = """\
This script takes Sequence file(s) and a mapping file and performs the \
following steps:
    
    454:
    1) Process SFFs to generate .fna, .qual and flowgram file. (process_sff.py)
    2) De-multiplex sequences. (split_libraries.py)
    3) Chained OTU-picking
    
    Illumina:
    1) De-multiplex sequences. (split_libraries_fastq.py)
    2) Chained OTU-picking
    
    FASTA:
    1) Associate DB accesions to sequence_names provided
    2) Chained OTU-picking

"""
script_info['script_usage'] = [("Example:","454 FLX", "%prog -i 454_Reads.sff -s 0 -m mapping.txt -p custom_parameters.txt -q FLX -r -u 0")]
script_info['script_usage'].append(("","454 Ti", "%prog -i 454_Reads.sff -s 0 -m mapping.txt -p custom_parameters.txt -q TITANIUM -rt -u 0"))
script_info['script_usage'].append(("","Illumina", "%prog -i s_1_1_sequences.fastq.gz,s_1_1_sequences_barcodes.fastq.gz -s 0 -m mapping.txt -p custom_parameters.txt -q ILLUMINA -r -u 0"))
script_info['script_usage'].append(("","FASTA", "%prog -i seqs.fna -s 0 -m mapping.txt -p custom_parameters.txt -q FASTA -r -u 0"))
script_info['output_description']= "The output of this script produces the output of demultiplexing and chained OTU-picking"
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
    make_option('-d','--submit_to_test_db',help='Choose to submit data to Test DB [default: %default]',default='False'),\
    make_option('-q','--sequencing_platform',help='This is the sequencing technology used.',default='FLX'),\
    make_option('-r','--process_only',help='This is whether to only process the data without loading [default: %default]',default='False'),\
    make_option('-u','--user_id',help='user-id'),\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    study_id = opts.study_id
    run_prefix ='_'.join(splitext(split(opts.map_fname)[-1])[0].split('_')[:-4])
    print run_prefix
    output_dir = '%s/user_data/studies/study_%s/processed_data_%s/' % (environ['HOME'],study_id, run_prefix)
    base_dir = '%s/user_data/studies/study_%s/' % (environ['HOME'], study_id)
    
    sff_fname=opts.sff_fname
    map_fname = opts.map_fname
    verbose = opts.verbose
    print_only = opts.print_only
    write_to_all_fasta=opts.write_to_all_fasta
    convert_to_flx=opts.convert_to_flx
    submit_to_test_db=opts.submit_to_test_db
    sequencing_platform=opts.sequencing_platform
    process_only=opts.process_only
    user_id=opts.user_id

    # Get our copy of data_access
    if submit_to_test_db == 'False':
        # Load the data into the database
        data_access = data_access_factory(ServerConfig.data_access_type)
    else:
        # Load the data into the database 
        data_access = data_access_factory(DataAccessType.qiime_test)

    # Remove the processed data directory if it exists
    if exists(output_dir):
        rmtree(output_dir)

    # determine if platform is Titanium. If so, then convert_to_flx
    if sequencing_platform=='TITANIUM':
        convert_to_flx=True
    else:
        convert_to_flx=False
        
    # parse the params file
    try:
        parameter_f = open(opts.parameter_fp)
    except IOError:
        raise IOError,\
        "Can't open parameters file (%s). Does it exist? Do you have read access?"\
        % opts.parameter_fp

    # create the output directory
    try:
        print 'output dir is: %s ' % output_dir 
        makedirs(output_dir)
        print 'made output dir'
    except OSError:
        pass

    # determine command_handler to use
    if print_only:
        command_handler = print_commands
    else:
        command_handler = call_commands_serially

    if verbose:
        status_update_callback = print_to_stdout
    else:
        status_update_callback = no_status_updates
        
    # Process the SFF file
    params=parse_qiime_parameters(parameter_f)
    print 'Running run_process_sff_through_split_lib...'
    
    if (sequencing_platform=='TITANIUM' or sequencing_platform=='FLX'):
        fasta_file_paths = run_process_sff_through_split_lib(study_id=study_id,\
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
    elif (sequencing_platform=='ILLUMINA'):
        fasta_file_paths = run_process_illumina_through_split_lib(\
         study_id=study_id,\
         run_prefix=run_prefix,\
         input_fp=sff_fname,\
         mapping_fp=map_fname,\
         output_dir=output_dir,\
         command_handler=command_handler,\
         params=params,\
         qiime_config=qiime_config,\
         write_to_all_fasta=write_to_all_fasta,\
         status_update_callback=status_update_callback)
    elif (sequencing_platform=='FASTA'):
        # this will most likely be a clean fasta step, since it should be
        # demultiplexed
        fasta_file_paths = run_process_fasta_through_split_lib(\
         study_id=study_id,\
         run_prefix=run_prefix,\
         input_fp=sff_fname,\
         mapping_fp=map_fname,\
         output_dir=output_dir,\
         command_handler=command_handler,\
         params=params,\
         qiime_config=qiime_config,\
         write_to_all_fasta=False,\
         status_update_callback=status_update_callback)
    else:
        raise ValueError, 'Platform (%s) defined in metadata is not supported!'\
            % (sequencing_platform)
        
    print 'Completed run_process_sff_through_split_lib.'
    
    """
    ####TOO SLOW FOR ILLUMINA
    print 'Check Demultiplexed sequences'
    split_lib_seqs_fp=join(output_dir,'split_libraries','seqs.fna')
    
    fasta_check=run_fasta_checks(split_lib_seqs_fp,map_fname)
    
    if float(fasta_check['invalid_labels']) > 0:
        raise ValueError, "There are invalid sequence names in the split-library sequence file"
    #elif float(fasta_check['barcodes_detected']) > 0:
    #    raise ValueError, "There are barcode sequences found in the split-library sequence file"
    elif float(fasta_check['duplicate_labels']) > 0:
        raise ValueError, "There are duplicate sequence names in the split-library sequence file"
    elif float(fasta_check['invalid_seq_chars']) > 0:
        raise ValueError, "There are invalid nucleotides in the split-library sequence file (i.e. not A,C,G,T or N)"
    elif float(fasta_check['linkerprimers_detected']) > 0.05:
        raise ValueError, "There are linker primer sequences in split-library the sequence file"
    elif float(fasta_check['nosample_ids_map']) > 0.20:
        raise ValueError, "More than 20% of the samples in the mapping file do not have split-library sequences"
        
    print 'Demultiplexed sequences appear to be valid'
    """
    
    
    study_info=data_access.getStudyInfo(study_id,user_id)
    if study_info['investigation_type'].lower() == 'metagenome':
        # skip OTU picking
        pass
    else:
        # Chain Pick OTUS
        resulting_fasta=join(output_dir,'split_libraries/seqs.fna')
        otu_output_dir=join(output_dir,'gg_97_otus')
        create_dir(otu_output_dir)
        print 'Running run_chain_pick_otus...'
        if (sequencing_platform=='ILLUMINA'):
            run_chain_pick_otus(resulting_fasta, otu_output_dir, command_handler, \
                                params, qiime_config, parallel=True, \
                                status_update_callback=status_update_callback)
        else:
            run_chain_pick_otus(resulting_fasta, otu_output_dir, command_handler, \
                                params, qiime_config, parallel=False, \
                                status_update_callback=status_update_callback)
        print 'Completed run_chain_pick_otus.'

    # Define the loading parameters
    params=[]
    params.append('OutputDir=%s' % output_dir)
    params.append('UserId=%s' % user_id)
    params.append('StudyId=%s' % study_id)
    params.append('TestDB=%s' % submit_to_test_db)
    params.append('ProcessedFastaFilepath=%s' % ','.join(fasta_file_paths))
    params.append('Platform=%s' % sequencing_platform)
    job_input='!!'.join(params)
    job_type='LoadAnalysisOTUTableHandler'
    
    # submit loading job to DB
    if process_only == 'False':
        submitQiimeJob(study_id, user_id, job_type, job_input, data_access)
    else:
        submitQiimeJob(study_id, user_id, job_type, job_input, data_access,\
                       job_state=-2)
    
    # generate and store seqs and otu stats for database
    print 'Summarizing results...'
    processed_results = summarize_all_stats(output_dir)
    print 'Writing seqs and otu summary to database...'
    submit_mapping_to_database(processed_results)
    print 'Seq and OTU summary results successfully added to database.'
    

if __name__ == "__main__":
    main()
