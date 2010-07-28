#!/usr/bin/env python
# File created on 12 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["GJesse Stombaugh"]
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
        self.dirs_to_remove.append(self.sff_dir)
        
        self.sff_fp = os.path.join(self.sff_dir, 'Fasting_subset.sff')
        copy(sff_original_fp, self.sff_fp)
        self.files_to_remove.append(self.sff_fp)
        
        tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        if not exists(tmp_dir):
            makedirs(tmp_dir)
            # if test creates the temp dir, also remove it
            self.dirs_to_remove.append(tmp_dir)
        
        self.wf_out = get_tmp_filename(tmp_dir=tmp_dir,
         prefix='qiime_wf_out',suffix='',result_constructor=str)
        self.dirs_to_remove.append(self.wf_out)
        
        self.fasting_mapping_fp = get_tmp_filename(tmp_dir=tmp_dir,
         prefix='qiime_wf_mapping',suffix='.txt')
        fasting_mapping_f = open(self.fasting_mapping_fp,'w')
        fasting_mapping_f.write(fasting_map)
        fasting_mapping_f.close()
        self.files_to_remove.append(self.fasting_mapping_fp)
        
        working_dir = self.qiime_config['working_dir'] or './'
        jobs_dir = join(working_dir,'jobs')
        if not exists(jobs_dir):
            # only clean up the jobs dir if it doesn't already exist
            self.dirs_to_remove.append(jobs_dir)
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
        
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        otu_fp = join(self.wf_out,'picked_otus','seqs_otus.txt')
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                 'seqs.fna')
                                 
        input_fname = splitext(split(self.sff_fp)[-1])[0]
        db_input_fp = join(self.wf_out,input_fname)

        analysis_id=submit_processed_data_to_db(db_input_fp+'.fna')
        
        exp_sff_md5='314f4000857668d45a413d2e94a755fc'
        exp_num_seqs=22
        exp_read_id='FLP3FBN01ELBSX'
        exp_instr_code='GS FLX'

        obs_seq_run_id,obs_split_lib_id,obs_pick_otu_id,obs_pick_otu_run_id,\
        obs_sff_file_id,obs_sff_md5,obs_num_of_reads,obs_read_id,obs_read_seq,\
        obs_split_lib_md5,obs_split_lib_log,obs_instrument_code = \
                        data_access.getTestData(True,analysis_id,'test_PCx634_1')
                        
        self.assertEqual(exp_sff_md5,obs_sff_md5,exp_sff_md5)
        self.assertEqual(obs_num_of_reads,exp_num_seqs)
        self.assertEqual(obs_read_id,exp_read_id)
        self.assertEqual(obs_read_seq,exp_read_seq)
        self.assertEqual(obs_split_lib_md5,exp_split_lib_md5)
        self.assertEqual(str(obs_split_lib_log),exp_split_lib_log)
        self.assertEqual(obs_instrument_code,exp_instr_code)
        '''
        valid=data_access.deleteTestAnalysis(True,analysis_id)
        if not valid:
            print "Error: Could not delete data from DB!"
        '''
exp_read_seq='tcagACAGAGTCGGCTCATGCTGCCTCCCGTAGGAGTCTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG'
exp_split_lib_md5='Fasting_subset.fna:fd90ec77f6e426e7eebd5a1c11f3f8ab,Fasting_subset.qual:c992bb0e6dd74b39ec448d87f92a0fb9'
exp_split_lib_log='''Number raw input seqs\t22\n\nLength outside bounds of 0 and 1000\t0\nNum ambiguous bases exceeds limit of 0\t0\nMissing Qual Score\t0\nMean qual score below minimum of 25\t0\nMean window qual score below minimum of 25\t3\nMax homopolymer run exceeds limit of 6\t0\nNum mismatches in primer exceeds limit of 0: 0\n\nRaw len min/max/avg\t240.0/285.0/262.9\nWrote len min/max/avg\t240.0/285.0/263.6\n\nBarcodes corrected/not\t0/0\nUncorrected barcodes will not be written to the output fasta file.\nCorrected barcodes will be written with the appropriate barcode category.\nCorrected but unassigned sequences will be written as such unless disabled via the -r option.\n\nTotal valid barcodes that are not in mapping file\t0\nSequences associated with valid barcodes that are not in the mapping file will not be written. -r option enabled.\n\nBarcodes in mapping file\nNum Samples\t8\nSample ct min/max/mean: 1 / 11 / 2.38\nSample\tSequence Count\tBarcode\ntest_PCx634\t11\tACAGAGTCGGCT\ntest_PCx593\t2\tAGCAGCACTTGT\ntest_PCx354\t1\tAGCACGAGCCTA\ntest_PCx636\t1\tACGGTGAGTGTC\ntest_PCx635\t1\tACCGCAGAGTCA\ntest_PCx481\t1\tACCAGCGACTAG\ntest_PCx356\t1\tACAGACCACTCA\ntest_PCx355\t1\tAACTCGTCGATG\ntest_PCx607\t0\tAACTGTGCGTAC\n\nTotal number seqs written\t19'''


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
pick_otus:refseqs_fp	/home/wwwuser/software/greengenes_core_sets/gg_otus_may2010/inflated_sub_gg/uclust_otus_97/rep_set/gg_97_otus_may2010.fasta
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
