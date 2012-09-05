#!/usr/bin/env python
# File created on 12 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

import signal
import os
import tempfile
import shutil
from shutil import rmtree,copy
from glob import glob
from os.path import join, exists, getsize, split, splitext, abspath, dirname
from os import makedirs,environ,removedirs,remove
from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename, ApplicationNotFoundError
from qiime.util import load_qiime_config,get_qiime_project_dir,create_dir
from qiime.parse import parse_qiime_parameters
from load_analysis_seqs_through_otu_table import (submit_sff_and_split_lib,
                                              submit_illumina_and_split_lib,
                                              submit_fasta_and_split_lib,
                                              load_otu_mapping,
                                              load_split_lib_sequences)
from qiime.workflow import (call_commands_serially,
                            no_status_updates,
                            WorkflowError,
                            print_commands)
from run_process_sff_through_split_lib import (run_process_sff_through_split_lib,
run_process_illumina_through_split_lib,run_process_fasta_through_split_lib,
cp_files)
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType
from run_chain_pick_otus import run_chain_pick_otus
data_access = data_access_factory(DataAccessType.qiime_test)

    
class WorkflowTests(TestCase):
    
    def setUp(self):
        """ set up the default values """
        
        self.qiime_config = load_qiime_config()
        self.dirs_to_remove = []
        self.files_to_remove = []
        
        # define study_id
        self.study_id=-1
        
        # create output directory
        self.wf_out="/%s/tmp" % environ['HOME']
        create_dir(self.wf_out)
        
        # this is specific to the web-apps only
        test_dir = abspath(dirname(__file__))
        sff_original_fp = os.path.join(test_dir, 'support_files', \
                                        'Fasting_subset.sff')
        
        # move SFF into place but also make sure to remove it
        self.sff_fp = os.path.join(environ['HOME'], 'Fasting_subset.sff')
        copy(sff_original_fp, self.sff_fp)
        self.files_to_remove.append(self.sff_fp)
        
        # define illumina filepaths
        self.illumina_fps = [os.path.join(test_dir, 'support_files', \
                                        's_8_1_sequence_100_records.txt.gz'),
                             os.path.join(test_dir, 'support_files', \
                                        's_8_2_sequence_100_records.txt.gz')]
        self.illumina_map_fp = os.path.join(test_dir, 'support_files', \
                                        's8_map_incomplete.txt')
        
        # define fasta filepaths
        self.fasta_fps=[os.path.join(test_dir,'support_files',
                                   'test_split_lib_seqs.fasta')]
        self.fasta_map_fp = os.path.join(test_dir, 'support_files', \
                                        'fasta_mapping_file.txt')
        
        # create the gg_97_otus folder
        self.gg_out=os.path.join(self.wf_out,'gg_97_otus')
        create_dir(self.gg_out)
        self.dirs_to_remove.append(self.gg_out)
        
        # create the split_libraries folder
        self.split_lib_out=os.path.join(self.wf_out,'split_libraries')
        create_dir(self.split_lib_out)
        self.dirs_to_remove.append(self.split_lib_out)
        
        # write SFF/Fasta mapping files
        self.fasting_mapping_fp = get_tmp_filename(tmp_dir='/tmp/',
         prefix='qiime_wf_mapping',suffix='.txt')
        fasting_mapping_f = open(self.fasting_mapping_fp,'w')
        fasting_mapping_f.write(fasting_map)
        fasting_mapping_f.close()
        self.files_to_remove.append(self.fasting_mapping_fp)
        
        # remove the default log file
        self.files_to_remove.append(join(self.wf_out,'log.txt'))
        
        # parse params file
        self.params = parse_qiime_parameters(qiime_parameters_f)
        
        
    def tearDown(self):
        '''This function removes the generated files'''

        map(remove,self.files_to_remove)
        map(rmtree,self.dirs_to_remove)
        
    def test_submit_processed_data_to_db(self):
        """run_process_sff_through_pick_otus runs without error"""
        
        self.files_to_remove.append(join(self.wf_out,'Fasting_subset.fna'))
        self.files_to_remove.append(join(self.wf_out,'Fasting_subset.qual'))
        self.files_to_remove.append(join(self.wf_out,'Fasting_subset.txt'))
        
        # remove generated mapping file
        moved_mapping_file=join(self.wf_out,split(self.fasting_mapping_fp)[-1])
        self.files_to_remove.append(moved_mapping_file)
        
        # process the sequence data first before loading
        run_process_sff_through_split_lib(0,'Fasting_subset',
          sff_input_fp=self.sff_fp, 
          mapping_fp=self.fasting_mapping_fp,
          output_dir=self.wf_out,
          command_handler=call_commands_serially,
          params=self.params,
          qiime_config=self.qiime_config,convert_to_flx=False,
          write_to_all_fasta=False,
          status_update_callback=no_status_updates)
        
        # get the file basename
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        # get key filepaths
        otu_fp = join(self.wf_out,'picked_otus','seqs_otus.txt')
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                 'seqs.fna')
        
        # run chained OTU-picking
        run_chain_pick_otus(split_lib_seqs_fp,
                            output_dir=self.gg_out,
                            command_handler=call_commands_serially,
                            params=self.params,
                            qiime_config=self.qiime_config,parallel=False,
                            status_update_callback=no_status_updates)
                                 
        input_fname = splitext(split(self.sff_fp)[-1])[0]
        db_input_fp = join(self.wf_out,input_fname)

        # submit the data
        analysis_id, input_dir, seq_run_id, split_lib_input_md5sum = \
            submit_sff_and_split_lib(data_access,db_input_fp+'.fna',
                                     self.study_id)
        # load OTU picking
        load_otu_mapping(data_access,self.wf_out,analysis_id)
        
        # load split-lib sequences
        split_library_id=load_split_lib_sequences(data_access,input_dir,
                                                analysis_id, seq_run_id,
                                                split_lib_input_md5sum)
        
        ### TEST raw sequence data load
        # expected results
        print 'Analysis ID is: %s' % str(analysis_id)
        print 'Testing the FLOW_DATA loading!'
        exp_sff_md5='314f4000857668d45a413d2e94a755fc'
        exp_num_seqs=22
        exp_read_id='FLP3FBN01ELBSX'
        exp_instr_code='GS FLX'
        exp_sff_fname='Fasting_subset'
        
        # define the query to pull data from DB
        con = data_access.getSFFDatabaseConnection()
        cur = con.cursor()
        seq_run_info="""select j.seq_run_id,f.sff_filename,f.number_of_reads,f.md5_checksum,
              h.instrument_code
              from analysis j
              inner join seq_run_to_sff_file s on j.seq_run_id=s.seq_run_id
              inner join sff_file f on f.sff_file_id=s.sff_file_id
              inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id
              inner join sequencing_run h on h.seq_run_id=s.seq_run_id"""
        seq_run_info+=" where j.analysis_id=%s and slrm.sequence_name=\'test.PCx634_1\'" % (str(analysis_id))
        results = cur.execute(seq_run_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_sff_filename,obs_num_of_reads,obs_sff_md5,\
            obs_instrument_code = data
        
        # check results
        self.assertEqual(obs_sff_filename,exp_sff_fname)
        self.assertEqual(obs_num_of_reads,exp_num_seqs)
        self.assertEqual(obs_sff_md5,exp_sff_md5)
        self.assertEqual(obs_instrument_code,exp_instr_code)
        
        # TEST split-library data load
        # expected results
        print 'Testing Split-Library Data'
        exp_split_lib_seq='CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG'
        exp_split_lib_md5='2c67e0acf745bef73e26c36f0b3bd00a'
        exp_split_lib_seq_md5='008918f7469f8e33d5dd6e01075d5194'

        # define the query to pull data from DB
        split_lib_info="""select distinct j.seq_run_id,slrm.ssu_sequence_id,l.command,l.md5_checksum,
              s.sequence_string,s.md5_checksum
              from analysis j
              inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id and j.split_library_run_id=slrm.split_library_run_id
              inner join ssu_sequence s on slrm.ssu_sequence_id=s.ssu_sequence_id
              inner join split_library_run l on j.split_library_run_id=l.split_library_run_id"""
        split_lib_info+=" where j.analysis_id=%s and slrm.sequence_name=\'test.PCx634_1\'" % (str(analysis_id))
        results = cur.execute(split_lib_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_seq_id,obs_split_lib_cmd,obs_split_lib_md5,\
            obs_split_lib_seq,obs_split_lib_seq_md5 = data
        
        # check results                                            
        self.assertEqual(obs_split_lib_md5,exp_split_lib_md5)
        self.assertEqual(obs_split_lib_seq,exp_split_lib_seq)
        self.assertEqual(obs_split_lib_seq_md5,exp_split_lib_seq_md5)
        
        # TEST OTU-table data load
        # expected results
        print 'Testing OTU Data!'
        exp_otu_md5='0b8edcf8a4275730001877496b41cf55'
        exp_threshold=97
        
        # define the query to pull data from DB
        otu_info="""select distinct j.seq_run_id,slrm.ssu_sequence_id,ot.reference_id,gr.ssu_sequence_id,
            ot.reference_id,j.otu_picking_run_id,p.command,p.md5_sum_input_file,
            p.threshold
            from analysis j
            inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id and j.split_library_run_id=slrm.split_library_run_id
            inner join otu_table ot on j.otu_run_set_id=ot.otu_run_set_id
            inner join gg_plus_denovo_reference gr on ot.reference_id=gr.reference_id
            inner join otu_picking_run p on j.otu_picking_run_id=p.otu_picking_run_id"""
        otu_info+=" where j.analysis_id=%s and slrm.sequence_name=\'test.PCx634_2\'" % (str(analysis_id))
        results = cur.execute(otu_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_seq_id,obs_otu_id,obs_otu_ssu_id,\
            obs_prokmsa,obs_otu_picking_run_id,obs_pick_otu_cmd,\
            obs_otu_md5,obs_threshold = data
        
        # check results  
        self.assertEqual(obs_otu_md5,exp_otu_md5)
        self.assertEqual(obs_threshold,exp_threshold)
        
        # TEST OTU-failures data load
        # define the query to pull data from DB
        otu_fail_info="""select distinct j.seq_run_id,f.ssu_sequence_id
              from analysis j
              inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id
              inner join otu_picking_failures f on slrm.ssu_sequence_id=f.ssu_sequence_id"""
        otu_fail_info+=" where j.analysis_id=%s and slrm.sequence_name=\'test.PCx634_14\'" % (str(analysis_id))
    
        results = cur.execute(otu_fail_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_id= data
        
        # check results  
        self.failIfEqual(obs_seq_run_id,0)
        self.failIfEqual(obs_ssu_id,0)
        
        # delete the loaded data
        valid=data_access.deleteTestAnalysis(True,analysis_id)
        if not valid:
            print "Error: Could not delete data from DB!"
    
    
    def test_submit_processed_data_to_db_illumina(self):
        """run_process_illumina_through_pick_otus runs without error"""
        
        self.files_to_remove.append(join(self.wf_out,'s8_map_incomplete.txt'))
        
        # process the sequence data first before loading
        run_process_illumina_through_split_lib(0,'Fasting_subset',\
         input_fp=','.join(self.illumina_fps),\
         mapping_fp=self.illumina_map_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
        
        # get the filepaths of key files
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        otu_fp = join(self.wf_out,'picked_otus','seqs_otus.txt')
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                 'seqs.fna')
        
        # run chained OTU-picking
        run_chain_pick_otus(split_lib_seqs_fp,
                            output_dir=self.gg_out,
                            command_handler=call_commands_serially,
                            params=self.params,
                            qiime_config=self.qiime_config,parallel=True,
                            status_update_callback=no_status_updates)
                                 
        input_fname = splitext(split(self.sff_fp)[-1])[0]
        db_input_fp = join(self.wf_out,input_fname)
        
        # load the study
        analysis_id, input_dir, seq_run_id, split_lib_input_md5sum = \
            submit_illumina_and_split_lib(data_access,
                                          ','.join(self.illumina_fps),
                                          self.study_id, self.wf_out)
        
        # load the OTU table data
        load_otu_mapping(data_access,self.wf_out,analysis_id)

        # load the split-library sequence data
        split_library_id=load_split_lib_sequences(data_access,input_dir,
                                              analysis_id, seq_run_id,
                                              split_lib_input_md5sum)
        
        ### TEST raw sequence data load
        # get expected results 
        print 'Analysis ID is: %s' % str(analysis_id)
        print 'Testing the SEQ_RUN loading!'
        exp_fastq_md5=['6e3c114cec9bdc8708aaa9077fd71aa6','685cac31968b74c5d99b294ac29e9fd9']
        exp_num_seqs=100
        exp_instr_code='ILLUMINA'
        exp_fastq_fname=['s_8_2_sequence_100_records.txt','s_8_1_sequence_100_records.txt']
        
        # define the query to pull data from DB
        con = data_access.getSFFDatabaseConnection()
        cur = con.cursor()
        seq_run_info="""select j.seq_run_id,f.sff_filename,f.number_of_reads,f.md5_checksum,
              h.instrument_code
              from analysis j
              inner join seq_run_to_sff_file s on j.seq_run_id=s.seq_run_id
              inner join sff_file f on f.sff_file_id=s.sff_file_id
              inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id
              inner join sequencing_run h on h.seq_run_id=s.seq_run_id"""
        seq_run_info+=" where j.analysis_id=%s and slrm.sample_name=\'HKE08Aug07\'" % (str(analysis_id))
        results = cur.execute(seq_run_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_fastq_filename,obs_num_of_reads,obs_fastq_md5,\
            obs_instrument_code = data
            
        # check results
        self.assertTrue(obs_fastq_filename in exp_fastq_fname)
        self.assertEqual(obs_num_of_reads,exp_num_seqs)
        self.assertTrue(obs_fastq_md5 in exp_fastq_md5)
        self.assertEqual(obs_instrument_code,exp_instr_code)
        
        print 'Done testing SEQ_RUN!'
        
        # TEST split-library sequence data
        # get expected results 
        print 'Testing Split-Library Data'
        exp_split_lib_seq='TACGAAGGGAGCTAGCGTTATTCGGAATGATTGGGTGTAAAGAGTTTGTAGATTGCAAAATTTTTGTTATTAGTAAAAAATTGAATTTATTATTTAAAGATGCTTTTAATACAATTTTGCTTGAGTATAGTAGAGGAAAAT'
        exp_split_lib_md5='700a9b08947589cfdd96525c97f9bcb4'
        exp_split_lib_seq_md5='7e8278ef1f5561d997cad48eabe40847'
        
        # define the query to pull data from DB
        split_lib_info="""select distinct j.seq_run_id,slrm.ssu_sequence_id,l.command,l.md5_checksum,
              s.sequence_string,s.md5_checksum
              from analysis j
              inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id and j.split_library_run_id=slrm.split_library_run_id
              inner join ssu_sequence s on slrm.ssu_sequence_id=s.ssu_sequence_id
              inner join split_library_run l on j.split_library_run_id=l.split_library_run_id"""
        split_lib_info+=" where j.analysis_id=%s and slrm.sample_name=\'HKE08Aug07\'" % (str(analysis_id))
        results = cur.execute(split_lib_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_seq_id,obs_split_lib_cmd,obs_split_lib_md5,\
            obs_split_lib_seq,obs_split_lib_seq_md5 = data
        
        # check results                                                    
        self.assertEqual(obs_split_lib_md5,exp_split_lib_md5)
        self.assertEqual(obs_split_lib_seq,exp_split_lib_seq)
        self.assertEqual(obs_split_lib_seq_md5,exp_split_lib_seq_md5)
        
        ### TEST OTU table load
        # get expected results
        print 'Testing OTU Data!'
        exp_otu_md5='6bc1d4693d57ddfa6abe9bd94103476d'
        exp_threshold=97
        
        # define the query to pull data from DB
        otu_info="""select distinct j.seq_run_id,slrm.ssu_sequence_id,ot.reference_id,gr.ssu_sequence_id,
            ot.reference_id,j.otu_picking_run_id,p.command,p.md5_sum_input_file,
            p.threshold
            from analysis j
            inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id and j.split_library_run_id=slrm.split_library_run_id
            inner join otu_table ot on j.otu_run_set_id=ot.otu_run_set_id
            inner join gg_plus_denovo_reference gr on ot.reference_id=gr.reference_id
            inner join otu_picking_run p on j.otu_picking_run_id=p.otu_picking_run_id"""
        otu_info+=" where j.analysis_id=%s and slrm.sample_name=\'SSBH05July07\'" % (str(analysis_id))
        results = cur.execute(otu_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_seq_id,obs_otu_id,obs_otu_ssu_id,\
            obs_prokmsa,obs_otu_picking_run_id,obs_pick_otu_cmd,\
            obs_otu_md5,obs_threshold = data
        
        # check results 
        self.assertEqual(obs_otu_md5,exp_otu_md5)
        self.assertEqual(obs_threshold,exp_threshold)
        
        ### TEST OTU failures load
        # define the query to pull data from DB
        otu_fail_info="""select distinct j.seq_run_id,f.ssu_sequence_id
              from analysis j
              inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id
              inner join otu_picking_failures f on slrm.ssu_sequence_id=f.ssu_sequence_id"""
        otu_fail_info+=" where j.analysis_id=%s and slrm.sample_name=\'HKE08Aug07\'" % (str(analysis_id))
        results = cur.execute(otu_fail_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_id= data
        
        # check results 
        self.failIfEqual(obs_seq_run_id,0)
        self.failIfEqual(obs_ssu_id,0)
        
        # delete loaded study data
        valid=data_access.deleteTestAnalysis(True,analysis_id)
        if not valid:
            print "Error: Could not delete data from DB!"
    
    
    def test_submit_processed_data_to_db_fasta(self):
        """submit_processed_data_to_db_fasta runs without error"""
          
        self.files_to_remove.append(join(self.wf_out,'fasta_mapping_file.txt'))
        # process the sequence data first before loading
        run_process_fasta_through_split_lib(0,'Fasting_subset',\
                                input_fp=','.join(self.fasta_fps),\
                                mapping_fp=self.fasta_map_fp,\
                                output_dir=self.wf_out, \
                                command_handler=call_commands_serially,\
                                params=self.params,\
                                qiime_config=self.qiime_config,\
                                write_to_all_fasta=False,\
                                status_update_callback=no_status_updates)

        # get key filepaths
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        otu_fp = join(self.wf_out,'picked_otus','seqs_otus.txt')
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                 'seqs.fna')
        
        # run chained OTU-picking
        run_chain_pick_otus(split_lib_seqs_fp,
                           output_dir=self.gg_out,
                           command_handler=call_commands_serially,
                           params=self.params,
                           qiime_config=self.qiime_config,parallel=True,
                           status_update_callback=no_status_updates)

        input_fname = splitext(split(self.sff_fp)[-1])[0]
        db_input_fp = join(self.wf_out,input_fname)

        # submit raw data to DB
        analysis_id, input_dir, seq_run_id, split_lib_input_md5sum = \
            submit_fasta_and_split_lib(data_access,
                                       ','.join(self.fasta_fps),
                                       self.study_id, self.wf_out)
        
        # Load OTU table data
        load_otu_mapping(data_access,self.wf_out,analysis_id)
        
        # load split-library data
        split_library_id=load_split_lib_sequences(data_access,input_dir,
                                               analysis_id, seq_run_id,
                                               split_lib_input_md5sum)
        
        ### TEST raw sequence data load
        # get expected results
        print 'Analysis ID is: %s' % str(analysis_id)
        print 'Testing the SEQ_RUN loading!'
        exp_sff_md5=['412eee0be168a285415d9e4db3dbbf2f']
        exp_num_seqs=22
        exp_instr_code='FASTA'
        exp_sff_fname=['test_split_lib_seqs']
        
        # define the query to pull data from DB
        con = data_access.getSFFDatabaseConnection()
        cur = con.cursor()
        seq_run_info="""select j.seq_run_id,f.sff_filename,f.number_of_reads,f.md5_checksum,
             h.instrument_code
             from analysis j
             inner join seq_run_to_sff_file s on j.seq_run_id=s.seq_run_id
             inner join sff_file f on f.sff_file_id=s.sff_file_id
             inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id
             inner join sequencing_run h on h.seq_run_id=s.seq_run_id"""
        seq_run_info+=" where j.analysis_id=%s and slrm.sample_name=\'test.PCx354.281526\'" % (str(analysis_id))
        results = cur.execute(seq_run_info)

        # get observed values
        for data in results:
            obs_seq_run_id,obs_sff_filename,obs_num_of_reads,obs_sff_md5,\
            obs_instrument_code = data

        # check results
        self.assertTrue(obs_sff_filename in exp_sff_fname)
        self.assertEqual(obs_num_of_reads,exp_num_seqs)
        self.assertTrue(obs_sff_md5 in exp_sff_md5)
        self.assertEqual(obs_instrument_code,exp_instr_code)

        ### TEST split-library sequence load
        # get expected results
        print 'Testing Split-Library Data'
        exp_split_lib_seq='TTGGGCCGTGTCTCAGTCCCAATGTGGCCGATCAGTCTCTTAACTCGGCTATGCATCATTGCCTTGGTAAGCCGTTACCTTACCAACTAGCTAATGCACCGCAGGTCCATCCAAGAGTGATAGCAGAACCATCTTTCAAACTCTAGACATGCGTCTAGTGTTGTTATCCGGTATTAGCATCTGTTTCCAGGTGTTATCCCAGTCTCTTGGG'
        exp_split_lib_md5='412eee0be168a285415d9e4db3dbbf2f'
        exp_split_lib_seq_md5='59843d3394983f2caa26f583014a3389'

        # define the query to pull data from DB
        split_lib_info="""select distinct j.seq_run_id,slrm.ssu_sequence_id,l.command,l.md5_checksum,
             s.sequence_string,s.md5_checksum
             from analysis j
             inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id and j.split_library_run_id=slrm.split_library_run_id
             inner join ssu_sequence s on slrm.ssu_sequence_id=s.ssu_sequence_id
             inner join split_library_run l on j.split_library_run_id=l.split_library_run_id"""
        split_lib_info+=" where j.analysis_id=%s and slrm.sample_name=\'test.PCx354.281526\'" % (str(analysis_id))
        results = cur.execute(split_lib_info)

        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_seq_id,obs_split_lib_cmd,obs_split_lib_md5,\
            obs_split_lib_seq,obs_split_lib_seq_md5 = data

        # check results
        self.assertEqual(obs_split_lib_md5,exp_split_lib_md5)
        self.assertEqual(obs_split_lib_seq,exp_split_lib_seq)
        self.assertEqual(obs_split_lib_seq_md5,exp_split_lib_seq_md5)
        
        ### TEST OTU table load
        # get expected results
        print 'Testing OTU Data!'
        exp_otu_md5='cec9b6c184ffdb12d9de4450034ab775'
        exp_threshold=97
        
        # define the query to pull data from DB
        otu_info="""select distinct j.seq_run_id,slrm.ssu_sequence_id,ot.reference_id,gr.ssu_sequence_id,
           ot.reference_id,j.otu_picking_run_id,p.command,p.md5_sum_input_file,
           p.threshold
           from analysis j
           inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id and j.split_library_run_id=slrm.split_library_run_id
           inner join otu_table ot on j.otu_run_set_id=ot.otu_run_set_id
           inner join gg_plus_denovo_reference gr on ot.reference_id=gr.reference_id
           inner join otu_picking_run p on j.otu_picking_run_id=p.otu_picking_run_id"""
        otu_info+=" where j.analysis_id=%s and slrm.sample_name=\'test.PCx354.281526\'" % (str(analysis_id))
        results = cur.execute(otu_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_seq_id,obs_otu_id,obs_otu_ssu_id,\
            obs_prokmsa,obs_otu_picking_run_id,obs_pick_otu_cmd,\
            obs_otu_md5,obs_threshold = data

        # check results
        self.assertEqual(obs_otu_md5,exp_otu_md5)
        self.assertEqual(obs_threshold,exp_threshold)
        
        ### TEST OTU failures load
        # define the query to pull data from DB
        otu_fail_info="""select distinct j.seq_run_id,f.ssu_sequence_id
             from analysis j
             inner join split_library_read_map slrm on j.seq_run_id=slrm.seq_run_id
             inner join otu_picking_failures f on slrm.ssu_sequence_id=f.ssu_sequence_id"""
        otu_fail_info+=" where j.analysis_id=%s and slrm.sample_name=\'test.PCx635.281531\'" % (str(analysis_id))
        results = cur.execute(otu_fail_info)
        
        # get observed values
        for data in results:
            obs_seq_run_id,obs_ssu_id= data

        # check results
        self.failIfEqual(obs_seq_run_id,0)
        self.failIfEqual(obs_ssu_id,0)
        
        # delete study data from DB
        valid=data_access.deleteTestAnalysis(True,analysis_id)
        if not valid:
            print "Error: Could not delete data from DB!"
            
            
            
exp_read_seq='tcagACAGAGTCGGCTCATGCTGCCTCCCGTAGGAGTCTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG'
exp_split_lib_md5='Fasting_subset.fna:fd90ec77f6e426e7eebd5a1c11f3f8ab,Fasting_subset.qual:c992bb0e6dd74b39ec448d87f92a0fb9'
exp_split_lib_log='''Number raw input seqs\t22\n\nLength outside bounds of 0 and 1000\t0\nNum ambiguous bases exceeds limit of 0\t0\nMissing Qual Score\t0\nMean qual score below minimum of 25\t0\nMean window qual score below minimum of 25\t3\nMax homopolymer run exceeds limit of 6\t0\nNum mismatches in primer exceeds limit of 0: 0\n\nRaw len min/max/avg\t240.0/285.0/262.9\nWrote len min/max/avg\t240.0/285.0/263.6\n\nBarcodes corrected/not\t0/0\nUncorrected barcodes will not be written to the output fasta file.\nCorrected barcodes will be written with the appropriate barcode category.\nCorrected but unassigned sequences will be written as such unless disabled via the -r option.\n\nTotal valid barcodes that are not in mapping file\t0\nSequences associated with valid barcodes that are not in the mapping file will not be written. -r option enabled.\n\nBarcodes in mapping file\nNum Samples\t8\nSample ct min/max/mean: 1 / 11 / 2.38\nSample\tSequence Count\tBarcode\ntest_PCx634\t11\tACAGAGTCGGCT\ntest_PCx593\t2\tAGCAGCACTTGT\ntest_PCx354\t1\tAGCACGAGCCTA\ntest_PCx636\t1\tACGGTGAGTGTC\ntest_PCx635\t1\tACCGCAGAGTCA\ntest_PCx481\t1\tACCAGCGACTAG\ntest_PCx356\t1\tACAGACCACTCA\ntest_PCx355\t1\tAACTCGTCGATG\ntest_PCx607\t0\tAACTGTGCGTAC\n\nTotal number seqs written\t19'''
exp_flow_string='''1.04	0.13	1.07	0.19	0.21	0.86	0.20	0.97	0.20	1.01	1.06	0.13	0.11	0.95	0.15	1.05	0.15	1.03	0.15	1.04	1.08	0.06	1.01	1.89	0.14	0.05	1.04	0.15	1.00	0.10	0.98	0.15	0.16	1.02	0.18	0.15	1.00	0.13	0.19	0.95	0.18	0.14	1.03	0.16	1.04	0.11	0.17	1.00	0.14	0.11	1.81	0.14	1.05	0.13	2.79	0.94	1.01	1.02	0.19	1.87	0.13	0.99	0.18	1.01	1.03	0.13	1.06	0.10	1.01	0.10	0.08	2.89	0.12	0.09	1.95	0.87	0.94	0.10	0.10	1.05	1.01	0.08	1.04	0.13	0.98	0.10	1.06	0.15	0.08	1.03	0.11	1.03	0.97	0.11	2.84	0.13	0.08	1.95	0.13	0.13	1.01	0.01	0.18	0.83	1.02	0.10	0.09	1.74	0.11	0.09	1.80	1.07	2.75	1.11	2.72	0.13	0.94	0.12	0.84	0.15	1.05	0.13	1.02	0.16	0.12	1.03	0.06	1.88	0.20	0.06	1.85	1.88	0.10	0.08	0.87	0.05	1.09	1.07	0.91	1.06	0.10	0.07	0.99	0.11	0.06	1.00	0.11	0.11	1.07	0.06	1.05	0.09	0.03	1.09	0.07	0.03	0.93	0.06	1.04	0.95	0.02	0.11	2.09	0.00	1.91	0.09	0.03	1.94	0.92	0.06	0.00	2.78	0.08	0.13	2.14	1.04	2.08	1.16	1.95	0.14	1.04	0.06	0.81	0.19	0.11	0.93	2.02	0.13	0.12	1.83	1.08	0.04	1.12	0.83	0.08	1.04	0.08	0.00	1.06	0.16	1.01	1.90	0.06	0.10	1.06	0.00	0.09	0.98	0.13	0.11	0.97	0.96	0.17	0.09	1.91	1.02	0.10	0.12	0.95	0.00	0.18	1.07	0.06	2.20	1.08	0.09	2.03	0.10	0.09	0.96	0.00	0.17	1.05	0.08	2.01	0.16	0.01	1.04	0.08	0.09	1.00	0.03	0.11	1.06	1.85	0.03	1.10	0.00	0.08	0.92	0.78	1.12	0.01	0.04	2.01	0.01	1.93	0.00	0.04	1.04	0.10	1.04	0.16	0.00	1.10	0.00	0.04	3.00	0.12	0.10	1.13	0.82	0.13	0.05	0.99	0.09	2.88	1.87	0.16	0.13	0.76	0.61	0.12	0.17	0.92	0.99	1.18	0.06	1.04	0.00	0.09	1.03	0.10	1.03	0.07	1.02	0.14	0.08	1.10	0.10	0.04	1.03	0.13	0.01	1.02	0.03	0.09	1.08	0.06	0.07	0.96	0.97	0.07	0.09	1.00	0.10	0.98	0.11	1.05	0.11	0.93	0.10	0.15	1.21	1.06	0.99	0.03	0.06	1.04	0.92	2.32	0.06	1.04	0.99	0.01	0.15	0.78	0.00	2.28	2.11	4.18	1.11	0.00	0.90	0.13	0.13	1.14	0.04	0.85	1.05	1.87	1.15	2.85	0.00	1.79	0.00	0.11	1.01	0.02	1.07	0.09	0.12	1.14	0.00	0.11	0.98	0.08	1.20	2.03	0.97	0.16	0.00	1.02	0.00	3.20	2.20	0.14	0.89	0.72	0.07	0.17	0.93	1.20	0.08	0.02	0.98	0.17	0.12	1.21	0.12	0.09	3.20	0.05	0.00	1.14	0.00	0.64	1.33	0.35	2.36'''
exp_qual_string='''37	36	36	36	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	36	36	33	33	33	36	37	37	37	37	37	37	40	40	40	39	39	38	40	40	40	40	40	40	40	37	37	37	37	37	35	35	35	37	37	37	37	37	35	35	35	31	31	23	23	23	31	21	21	21	35	35	37	37	37	36	36	36	36	36	36	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	28	28	28	36	36	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	36	36	36	37	37	37	37	37	37	37	37	37	37	37	37	36	36	36	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	35	32	32	32	32	35	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	36	32	32	32	36	37	35	32	32	32	32	32	32	32	32	36	37	37	37	37	36	36	31	31	32	32	36	36	36	36	36	36	36	36	36	36	36	28	27	27	27	26	26	26	30	29	30	29	24	24	24	21	15	15	13	13'''
qiime_parameters_f = """# qiime_parameters.txt
# WARNING: DO NOT EDIT OR DELETE Qiime/qiime_parameters.txt. Users should copy this file and edit copies of it.

# Split libraries parameters
split_libraries:min-seq-length	0
split_libraries:max-seq-length	1000
split_libraries:trim-seq-length	False
split_libraries:min-qual-score	25
split_libraries:max-ambig	0
split_libraries:max-homopolymer	6
split_libraries:max-primer	0
split_libraries:barcode-type	12
split_libraries:max-barcode-errors	1.5
split_libraries:start-numbering	1
split_libraries:remove_unassigned	True
split_libraries:disable_bc_correction	False
split_libraries:qual_score_window	50
split_libraries:disable_primers	False
split_libraries:reverse_primers	disable
split_libraries:record_qual_scores True

# Split libraries parameters
split_libraries_fastq:retain_unassigned_reads
split_libraries_fastq:max_bad_run_length
split_libraries_fastq:min_per_read_length
split_libraries_fastq:sequence_max_n
split_libraries_fastq:start_seq_id
split_libraries_fastq:rev_comp_mapping_barcodes
split_libraries_fastq:rev_comp
split_libraries_fastq:barcode_type	golay_12
split_libraries_fastq:last_bad_quality_char
split_libraries_fastq:max_barcode_errors	1.5
split_libraries_fastq:store_qual_scores True

# OTU picker parameters
pick_otus:otu_picking_method	uclust_ref
pick_otus:clustering_algorithm	furthest
pick_otus:refseqs_fp	~/software/gg_otus_4feb2011/rep_set/gg_97_otus_4feb2011.fasta
pick_otus:similarity	0.97
pick_otus:suppress_new_clusters True
pick_otus:enable_rev_strand_match True

# Parallel options
parallel:jobs_to_start	20
parallel:retain_temp_files	False
parallel:seconds_to_sleep	60
""".split('\n')

fasting_map = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
test.PCx354	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Control	20061218	1
test.PCx355	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Control	20061218	2
test.PCx356	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Control	20061126	3
test.PCx481	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Control	20070314	4
test.PCx593	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Control	20071210	5
test.PCx607	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fast	20071112	6
test.PCx634	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	7
test.PCx635	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	8
test.PCx636	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	9
"""



if __name__ == "__main__":
    main()
