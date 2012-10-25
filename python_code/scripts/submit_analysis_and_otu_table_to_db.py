#!/usr/bin/env python
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
from os.path import split, join
from submit_job_to_qiime import submitQiimeJob
from qiime.util import load_qiime_config
from load_analysis_seqs_through_otu_table import submit_sff_and_split_lib, \
                                             submit_illumina_and_split_lib,\
                                             load_otu_mapping,\
                                             submit_fasta_and_split_lib,\
                                             load_split_lib_sequences
                                             
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Submit OTU-table data into DB"
script_info['script_description'] = """\
Create an analysis and submit the OTU-table data into the QIIME-DB"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i /path/to/files/processed_data_/454_Reads.fna -t False -s 0 -u 0 -o /path/to/files/processed_data_/ -p FLX")]
script_info['output_description']= "There is no output from the script, since it puts the processed data into the QIIME-DB."
script_info['required_options'] = [\
    make_option('-i','--fasta_file_paths',help='This is the processed fasta filepath(s) from process_sff.py'),\
    make_option('-t','--submit_to_test_db',help='By setting this parameter, the data will be submitted to the test database.'),\
    make_option('-s','--study_id',help='This is the study id assigned from loading the metadata'),\
    make_option('-u','--user_id',help='user id'),\
    make_option('-o','--output_dir',help='output directory'),\
    make_option('-p','--platform',help='sequencing platform'),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    
    submit_to_test_db=opts.submit_to_test_db
    fasta_file_paths=opts.fasta_file_paths
    study_id=opts.study_id
    output_dir=opts.output_dir
    platform=opts.platform
    user_id=opts.user_id
    
    if submit_to_test_db == 'False':
        # Load the data into the database
        data_access = data_access_factory(ServerConfig.data_access_type)
    else:
        # Load the data into the database 
        data_access = data_access_factory(DataAccessType.qiime_test)

    # Get all of the fasta files
    if (platform=='FLX' or platform=='TITANIUM'):
        print 'Submitting SFF data to database...'
        analysis_id, input_dir, seq_run_id, split_lib_input_md5sum = \
            submit_sff_and_split_lib(data_access, fasta_file_paths, study_id)
    elif platform=='ILLUMINA':
        print 'Submitting Illumina data to database...'
        analysis_id, input_dir, seq_run_id, split_lib_input_md5sum = \
            submit_illumina_and_split_lib(data_access, fasta_file_paths,
                                          study_id,output_dir)
    elif platform=='FASTA':
        print 'Submitting FASTA data to database...'
        analysis_id, input_dir, seq_run_id, split_lib_input_md5sum = \
            submit_fasta_and_split_lib(data_access, fasta_file_paths, 
                                       study_id, output_dir)
    
    '''
    # Submit Split-library loading job
    split_library_id=load_split_lib_sequences(data_access,input_dir,
                                              analysis_id, seq_run_id,
                                              split_lib_input_md5sum)
    '''

    # verify that these are not metagenomic sequences
    # otherwise load the OTU table
    study_info=data_access.getStudyInfo(study_id,user_id)
    if study_info['investigation_type'].lower() == 'metagenome':
        # skip OTU loading
        pass
    else:
        print 'Submitting OTU data to database...'
        load_otu_mapping(data_access, output_dir, analysis_id)
    

    params=[]
    params.append('OutputDir=%s' % output_dir)
    params.append('UserId=%s' % user_id)
    params.append('StudyId=%s' % study_id)
    params.append('TestDB=%s' % submit_to_test_db)
    params.append('ProcessedFastaFilepath=%s' % (fasta_file_paths))
    params.append('AnalysisId=%s' % analysis_id)
    params.append('SeqRunId=%s' % seq_run_id)
    params.append('MDchecksum=%s' % split_lib_input_md5sum)
    job_input='!!'.join(params)
    job_type='LoadSplitLibSeqsHandler'


    submitQiimeJob(study_id, user_id, job_type, job_input, data_access)
    
    print 'Completed database loading.'

if __name__ == "__main__":
    main()
