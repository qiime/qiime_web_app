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
from run_chain_pick_otus import run_chain_pick_otus,web_app_call_commands_serially
from qiime.workflow import (call_commands_serially,
no_status_updates,WorkflowError,print_commands,print_to_stdout)
## The test case timing code included in this file is adapted from
## recipes provided at:
##  http://code.activestate.com/recipes/534115-function-timeout/
##  http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
class TimeExceededError(Exception):
    pass

allowed_seconds_per_test = 240

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
        self.fna_original_fp = '/home/wwwdevuser/qiime_test_dataset/split_libraries/0_FLX_seqs.fna'

        tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        if not exists(tmp_dir):
            makedirs(tmp_dir)
            # if test creates the temp dir, also remove it
            self.dirs_to_remove.append(tmp_dir)
        
        self.wf_out = get_tmp_filename(tmp_dir=tmp_dir,
         prefix='qiime_wf_out',suffix='',result_constructor=str)
        
        if not exists(self.wf_out):
            makedirs(self.wf_out)         
            self.dirs_to_remove.append(self.wf_out)
        
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
    
    def test_run_chain_pick_otus(self):
        """run_chain_pick_otus runs without error"""
        run_chain_pick_otus(self.fna_original_fp, self.wf_out, web_app_call_commands_serially, \
                    self.params, self.qiime_config, False,\
                    no_status_updates)
        
        #load the split lib fasta file and check if it is valid
        cat_split_lib_fp=join(self.wf_out,'all_split_lib_seqs.fna')
        cat_split_lib=open(cat_split_lib_fp).read()
        original_fasta=open(self.fna_original_fp).read()
        
        self.assertEqual(cat_split_lib,original_fasta)
        
        #load the study_run_prefix dictionary and make sure it is valid
        study_run_prefix_dict=eval(open(join(self.wf_out,'studies_run_prefix_dict.txt')).read())
        exp_study_run_prefix={'0': ['FLX']}
        
        self.assertEqual(study_run_prefix_dict,exp_study_run_prefix)
        
        #load the exact match OTUs and check if they are valid
        exact_otus_fp=join(self.wf_out,'pick_otus_exact','all_split_lib_seqs_otus.txt')
        obs_exact_otus=open(exact_otus_fp).read()
        
        self.assertEqual(obs_exact_otus,exp_exact_otus)
        
        #load the trie filtered OTUs and check if they are valid
        trie_otus_fp=join(self.wf_out,'pick_otus_trie','all_split_lib_seqs_exact_rep_otus.txt')
        obs_trie_otus=open(trie_otus_fp).read()
        
        self.assertEqual(obs_trie_otus,exp_trie_otus)
        
        #load the uclust_ref picked OTUs and check if they are valid
        uclust_ref_otus_fp=join(self.wf_out,'picked_otus_UCLUST_REF_97',
                            'all_split_lib_seqs_exact_rep_trie_rep_otus.txt')
        obs_uclust_ref_otus=open(uclust_ref_otus_fp).read()
        
        self.assertEqual(obs_uclust_ref_otus,exp_uclust_ref_otus)
        
        #load the merged OTUs and check if they are valid
        all_otus_fp=uclust_ref_otus_fp=join(self.wf_out,
                                            'exact_trie_uclust_ref_otus.txt')
        obs_all_otus=open(all_otus_fp).read()
        
        self.assertEqual(obs_all_otus,exp_all_otus)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)
        

    def test_run_chain_pick_otus_parallel(self):
        """run_chain_pick_otus parallel runs without error"""
        run_chain_pick_otus(self.fna_original_fp, self.wf_out, web_app_call_commands_serially, \
                    self.params, self.qiime_config, True,\
                    no_status_updates)
        
        #load the split lib fasta file and check if it is valid
        cat_split_lib_fp=join(self.wf_out,'all_split_lib_seqs.fna')
        cat_split_lib=open(cat_split_lib_fp).read()
        original_fasta=open(self.fna_original_fp).read()

        self.assertEqual(cat_split_lib,original_fasta)

        #load the study_run_prefix dictionary and make sure it is valid
        study_run_prefix_dict=eval(open(join(self.wf_out,'studies_run_prefix_dict.txt')).read())
        exp_study_run_prefix={'0': ['FLX']}

        self.assertEqual(study_run_prefix_dict,exp_study_run_prefix)

        #load the exact match OTUs and check if they are valid
        exact_otus_fp=join(self.wf_out,'pick_otus_exact','all_split_lib_seqs_otus.txt')
        obs_exact_otus=open(exact_otus_fp).read()

        self.assertEqual(obs_exact_otus,exp_exact_otus)

        #load the trie filtered OTUs and check if they are valid
        trie_otus_fp=join(self.wf_out,'pick_otus_trie','all_split_lib_seqs_exact_rep_otus.txt')
        obs_trie_otus=open(trie_otus_fp).read()

        self.assertEqual(obs_trie_otus,exp_trie_otus)   
        
        #load the uclust_ref picked OTUs and check if they are valid
        uclust_ref_otus_fp=join(self.wf_out,'picked_otus_UCLUST_REF_97',
                            'all_split_lib_seqs_exact_rep_trie_rep_otus.txt')
        obs_uclust_ref_otus=open(uclust_ref_otus_fp).read()
        
        self.assertEqual(obs_uclust_ref_otus,exp_uclust_ref_otus_parallel)
        
        #load the merged OTUs and check if they are valid
        all_otus_fp=uclust_ref_otus_fp=join(self.wf_out,
                                            'exact_trie_uclust_ref_otus.txt')
        obs_all_otus=open(all_otus_fp).read()
        
        self.assertEqual(obs_all_otus,exp_all_otus_parallel)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)
        
        
        
exp_exact_otus='''\
0	test_PCx634_17
1	test_PCx354_3
2	test_PCx634_8
3	test_PCx636_6
4	test_PCx355_13
5	test_PCx634_1
6	test_PCx635_15
7	test_PCx634_2
8	test_PCx634_10
9	test_PCx634_9
10	test_PCx481_4
11	test_PCx634_18
12	test_PCx634_14
13	test_PCx593_19
14	test_PCx634_11
15	test_PCx634_7
16	test_PCx356_16
17	test_PCx634_5
18	test_PCx593_12
'''

exp_trie_otus='''\
0	11
1	10
2	13
3	12
4	15
5	14
6	17
7	16
8	18
9	1
10	0
11	3
12	2
13	5
14	4
15	7
16	6
17	9
18	8
'''
exp_uclust_ref_otus='''\
231318	6
259499	1
342038	9	14
271150	11
230364	12
204144	8
135567	2
469842	15	5
169379	0
249724	7
568692	16
328623	4
577170	17	18
'''

exp_all_otus='''\
135567	test_PCx593_19
169379	test_PCx634_18
204144	test_PCx593_12
230364	test_PCx634_8
231318	test_PCx634_5
249724	test_PCx356_16
259499	test_PCx481_4
271150	test_PCx636_6
328623	test_PCx634_7
342038	test_PCx354_3	test_PCx355_13
469842	test_PCx634_2	test_PCx634_11
568692	test_PCx635_15
577170	test_PCx634_9	test_PCx634_10
'''

exp_uclust_ref_otus_parallel='''\
259499	1
231318	6
342038	14	9
204144	8
230364	12
135567	2
469842	15	5
169379	0
271150	11
568692	16
328623	4
249724	7
577170	17	18
'''

exp_all_otus_parallel='''\
135567	test_PCx593_19
169379	test_PCx634_18
204144	test_PCx593_12
230364	test_PCx634_8
231318	test_PCx634_5
249724	test_PCx356_16
259499	test_PCx481_4
271150	test_PCx636_6
328623	test_PCx634_7
342038	test_PCx355_13	test_PCx354_3
469842	test_PCx634_2	test_PCx634_11
568692	test_PCx635_15
577170	test_PCx634_9	test_PCx634_10
'''

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
pick_otus:refseqs_fp    /home/wwwdevuser/software/gg_otus_6oct2010/rep_set/gg_97_otus_6oct2010.fasta
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
pick_otus:suppress_new_clusters True
pick_otus:uclust_otu_id_prefix  otu_
pick_otus:uclust_stable_sort    True

# Parallel options
parallel:jobs_to_start	2
parallel:retain_temp_files	False
parallel:seconds_to_sleep	1

""".split('\n')

fasting_map = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
PCx354	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse__I.D._354
PCx355	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse__I.D._355
PCx356	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Control	20061126	Control_mouse__I.D._356
PCx481	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Control	20070314	Control_mouse__I.D._481
PCx593	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Control	20071210	Control_mouse__I.D._593
PCx607	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fast	20071112	Fasting_mouse__I.D._607
PCx634	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._634
PCx635	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._635
PCx636	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._636
"""



if __name__ == "__main__":
    main()
