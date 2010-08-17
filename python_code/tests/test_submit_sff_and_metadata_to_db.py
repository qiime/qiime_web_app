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
from os.path import join, exists, getsize, split, splitext
from os import makedirs
from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename, ApplicationNotFoundError
from qiime.util import load_qiime_config,get_qiime_project_dir
from qiime.parse import parse_qiime_parameters
from process_sff_and_metadata_workflow import (run_process_sff_through_pick_otus,submit_processed_data_to_db)
from qiime.workflow import (call_commands_serially,
no_status_updates,WorkflowError,print_commands)

from qiime_data_access import QiimeDataAccess
data_access = QiimeDataAccess()
## The test case timing code included in this file is adapted from
## recipes provided at:
##  http://code.activestate.com/recipes/534115-function-timeout/
##  http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
class TimeExceededError(Exception):
    pass

allowed_seconds_per_test = 600

def timeout(signum, frame):
    raise TimeExceededError,\
     "Test failed to run in allowed time (%d seconds)."\
      % allowed_seconds_per_test
    
class WorkflowTests(TestCase):
    
    def setUp(self):
        """ """
        
        self.qiime_config = load_qiime_config()
        self.dirs_to_remove = []
        self.files_to_remove = []
        
        # Cannot use get_qiime_project_dir() due to test errors in virtual box
        test_dir = os.path.join(get_qiime_project_dir(),'tests')
        sff_original_fp = os.path.join(test_dir, 'support_files', \
                                        'Fasting_subset.sff')

        # copy sff file to working directory
        self.sff_dir = tempfile.mkdtemp()
        #self.dirs_to_remove.append(self.sff_dir)
        
        self.sff_fp = os.path.join(self.sff_dir, 'Fasting_subset.sff')
        copy(sff_original_fp, self.sff_fp)
        #self.files_to_remove.append(self.sff_fp)
        
        tmp_dir = "/home/wwwuser/qiime_test_dataset/"#self.qiime_config['temp_dir'] or '/tmp/'
        if not exists(tmp_dir):
            makedirs(tmp_dir)
            # if test creates the temp dir, also remove it
            #self.dirs_to_remove.append(tmp_dir)
        self.wf_out="/home/wwwuser/qiime_test_dataset/"
        '''
        self.wf_out = get_tmp_filename(tmp_dir=tmp_dir,
         prefix='qiime_wf_out',suffix='',result_constructor=str)
        self.dirs_to_remove.append(self.wf_out)
        '''
        self.fasting_mapping_fp = get_tmp_filename(tmp_dir=tmp_dir,
         prefix='qiime_wf_mapping',suffix='.txt')
        fasting_mapping_f = open(self.fasting_mapping_fp,'w')
        fasting_mapping_f.write(fasting_map)
        fasting_mapping_f.close()
        #self.files_to_remove.append(self.fasting_mapping_fp)
        
        working_dir = self.qiime_config['working_dir'] or './'
        jobs_dir = join(working_dir,'jobs')
        '''
        if not exists(jobs_dir):
            # only clean up the jobs dir if it doesn't already exist
            self.dirs_to_remove.append(jobs_dir)
        '''
        self.params = parse_qiime_parameters(qiime_parameters_f)

        signal.signal(signal.SIGALRM, timeout)
        # set the 'alarm' to go off in allowed_seconds seconds
        signal.alarm(allowed_seconds_per_test)
        
    
    def tearDown(self):
        """ """
        # turn off the alarm
        signal.alarm(0)
        
        remove_files(self.files_to_remove)
        # remove directories last, so we don't get errors
        # trying to remove files which may be in the directories
        for d in self.dirs_to_remove:
            if exists(d):
                rmtree(d)
        
    def test_submit_processed_data_to_db(self):
        """run_process_sff_through_pick_otus runs without error"""
        '''
        run_process_sff_through_pick_otus(
          sff_input_fp=self.sff_fp, 
          mapping_fp=self.fasting_mapping_fp,
          output_dir=self.wf_out, 
          denoise=False,
          command_handler=call_commands_serially,
          params=self.params,
          qiime_config=self.qiime_config, 
          parallel=False,
          status_update_callback=no_status_updates)
        '''
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        otu_fp = join(self.wf_out,'picked_otus','seqs_otus.txt')
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                 'seqs.fna')
                                 
        input_fname = splitext(split(self.sff_fp)[-1])[0]
        db_input_fp = join(self.wf_out,input_fname)

        analysis_id=submit_processed_data_to_db(db_input_fp+'.fna',0)
        print 'Analysis ID is: %s' % str(analysis_id)
        print 'Testing the FLOW_DATA loading!'
        exp_sff_md5='314f4000857668d45a413d2e94a755fc'
        exp_num_seqs=22
        exp_read_id='FLP3FBN01ELBSX'
        exp_instr_code='GS FLX'
        exp_sff_fname='Fasting_subset'
       
        #print 'Calling getTestFlowData...' 
        obs_seq_run_id,obs_sff_filename,obs_num_of_reads,obs_sff_md5,\
        obs_instrument_code,obs_read_id,obs_read_seq,obs_flow_string,\
        obs_qual_string = data_access.getTestFlowData(True,analysis_id,
                                                            'test_PCx634_1')

        #print 'After getTestFlowData...'
                                                            
        self.assertEqual(obs_sff_filename,exp_sff_fname)    
        self.assertEqual(obs_num_of_reads,exp_num_seqs)            
        self.assertEqual(obs_sff_md5,exp_sff_md5)
        self.assertEqual(obs_instrument_code,exp_instr_code)
        self.assertEqual(obs_read_id,exp_read_id)
        self.assertEqual(obs_read_seq,exp_read_seq)
        self.assertEqual(str(obs_flow_string),exp_flow_string)
        self.assertEqual(str(obs_qual_string),exp_qual_string)
        
        print 'Done testing Flow_Data!'
        
        print 'Testing Split-Library Data'
        exp_split_lib_cmd='python /home/wwwuser/software/Qiime/scripts/split_libraries.py -f /home/wwwuser/qiime_test_dataset/Fasting_subset.fna -q /home/wwwuser/qiime_test_dataset/Fasting_subset.qual -m "/home/wwwuser/qiime_test_dataset/qiime_wf_mappingfgHtBGBCGsqINRl64WxD.txt" -o /home/wwwuser/qiime_test_dataset/split_libraries --reverse_primers disable --max-seq-length 1000 --max-ambig 0 --start-numbering 1 --max-primer 0 --min-qual-score 25 --max-homopolymer 6 --barcode-type 12 --max-barcode-errors 1.5 --remove_unassigned --min-seq-length 0 --qual_score_window 50\n'
        exp_split_lib_md5='Fasting_subset.fna:fd90ec77f6e426e7eebd5a1c11f3f8ab,Fasting_subset.qual:c992bb0e6dd74b39ec448d87f92a0fb9'
        exp_split_lib_seq='CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG'
        exp_split_lib_md5='4a369b42e8fc542a4896ef1d1106162b'
        exp_split_lib_seq_md5='008918f7469f8e33d5dd6e01075d5194'

        
        obs_seq_run_id,obs_ssu_seq_id,obs_split_lib_cmd,obs_split_lib_md5,\
        obs_split_lib_seq,obs_split_lib_seq_md5 = \
                    data_access.getTestSplitLibData(True,analysis_id,
                                                            'test_PCx634_1')
                                                            
        self.assertEqual(obs_split_lib_cmd,exp_split_lib_cmd)
        self.assertEqual(obs_split_lib_md5,exp_split_lib_md5)
        self.assertEqual(obs_split_lib_seq,exp_split_lib_seq)
        self.assertEqual(obs_split_lib_seq_md5,exp_split_lib_seq_md5)
        
        print 'Testing OTU Data!'
        
        exp_prokmsa=176564
        exp_otu_md5='a990fad228b5eaad9bce75b41ba40564'
        exp_threshold=97
        exp_pick_otu_cmd='python /home/wwwuser/software/Qiime/scripts/pick_otus.py -i /home/wwwuser/qiime_test_dataset/split_libraries/seqs.fna -o /home/wwwuser/qiime_test_dataset//picked_otus --otu_picking_method uclust_ref --similarity 0.97 --uclust_otu_id_prefix otu_ --max_cdhit_memory 400 --suppress_new_clusters --refseqs_fp /home/wwwuser/software/greengenes_core_sets/gg_otus_may2010/inflated_sub_gg/uclust_otus_97/rep_set/gg_97_otus_may2010.fasta --clustering_algorithm furthest --max_e_value 1e-10\n'
        
        obs_seq_run_id,obs_ssu_seq_id,obs_otu_id,obs_otu_ssu_id,\
        obs_prokmsa,obs_otu_picking_run_id,obs_pick_otu_cmd,\
        obs_otu_md5,obs_threshold = \
                    data_access.getTestOTUData(True,analysis_id,
                                                            'test_PCx634_2')
        
        self.assertEqual(obs_prokmsa,exp_prokmsa)
        self.assertEqual(obs_pick_otu_cmd,exp_pick_otu_cmd)
        self.assertEqual(obs_otu_md5,exp_otu_md5)
        self.assertEqual(obs_threshold,exp_threshold)
        
        obs_seq_run_id,obs_ssu_id = \
                    data_access.getTestOTUFailureData(True,analysis_id,
                                                            'test_PCx634_1')
        
        self.failIfEqual(obs_seq_run_id,0)
        self.failIfEqual(obs_ssu_id,0)
        
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

# OTU picker parameters
pick_otus:otu_picking_method	uclust_ref
pick_otus:clustering_algorithm	furthest
pick_otus:max_cdhit_memory	400
pick_otus:refseqs_fp	/home/wwwuser/software/greengenes_core_sets/gg_otus_9aug2010/inflated_sub_gg/uclust_otus_97/rep_set/gg_97_otus_9aug2010.fasta
pick_otus:blast_db
pick_otus:similarity	0.97
pick_otus:max_e_value	1e-10
pick_otus:prefix_prefilter_length
pick_otus:trie_prefilter
pick_otus:prefix_length
pick_otus:suffix_length
pick_otus:optimal_uclust
pick_otus:exact_uclust
pick_otus:user_sort
pick_otus:suppress_presort_by_abundance_uclust
pick_otus:suppress_new_clusters	True
pick_otus:uclust_otu_id_prefix  otu_

# Parallel options
parallel:jobs_to_start	2
parallel:retain_temp_files	False
parallel:seconds_to_sleep	1

""".split('\n')

fasting_map = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
test_PCx354	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse__I.D._354
test_PCx355	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse__I.D._355
test_PCx356	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Control	20061126	Control_mouse__I.D._356
test_PCx481	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Control	20070314	Control_mouse__I.D._481
test_PCx593	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Control	20071210	Control_mouse__I.D._593
test_PCx607	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fast	20071112	Fasting_mouse__I.D._607
test_PCx634	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._634
test_PCx635	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._635
test_PCx636	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._636
"""



if __name__ == "__main__":
    main()
