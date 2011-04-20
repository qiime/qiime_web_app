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
from os.path import join, exists, getsize, split, splitext,abspath, dirname
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

allowed_seconds_per_test = 400

def timeout(signum, frame):
    raise TimeExceededError,\
     "Test failed to run in allowed time (%d seconds)."\
      % allowed_seconds_per_test
    
class WorkflowTests(TestCase):
    
    def setUp(self):
        """setup the test values"""
        
        self.qiime_config = load_qiime_config()
        self.dirs_to_remove = []
        self.files_to_remove = []
        

        #this is specific to the web-apps only
        test_dir = abspath(dirname(__file__))
        self.fna_original_fp = os.path.join(test_dir, 'support_files', \
                                        'test.fna')


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
        self.params = parse_qiime_parameters(qiime_parameters_f.split('\n'))

        signal.signal(signal.SIGALRM, timeout)
        # set the 'alarm' to go off in allowed_seconds seconds
        signal.alarm(allowed_seconds_per_test)
        
    
    def tearDown(self):
        """remove all the files after completing tests """
        # turn off the alarm
        signal.alarm(0)
        
        remove_files(self.files_to_remove)
        # remove directories last, so we don't get errors
        # trying to remove files which may be in the directories
        for d in self.dirs_to_remove:
            if exists(d):
                rmtree(d)
    
    def test_run_chain_pick_otus(self):
        """run_chain_pick_otus runs serially without error"""
        run_chain_pick_otus(self.fna_original_fp, self.wf_out,\
                    call_commands_serially, \
                    self.params, self.qiime_config, False,\
                    no_status_updates)
        
        #load the exact match OTUs and check if they are valid
        exact_otus_fp=join(self.wf_out,'pick_otus_exact',\
                           'test_otus.txt')
        obs_exact_otus=open(exact_otus_fp).read()
        
        self.assertEqual(obs_exact_otus,exp_exact_otus)
        
        #load the uclust_ref picked OTUs and check if they are valid
        uclust_ref_otus_fp=join(self.wf_out,'picked_otus_UCLUST_REF_97',
                            'leftover_otus.txt')
        obs_uclust_ref_otus=open(uclust_ref_otus_fp).read()
        
        self.assertEqual(obs_uclust_ref_otus,exp_uclust_ref_otus)
        
        #load the merged OTUs and check if they are valid
        all_otus_fp=uclust_ref_otus_fp=join(self.wf_out,
                                            'exact_uclust_ref_otus.txt')
        obs_all_otus=open(all_otus_fp).read()
        
        self.assertEqual(obs_all_otus,exp_all_otus)
        
        #load the sample failures and check if they are valid
        otus_failures_fp=join(self.wf_out, 'all_failures.txt')
        obs_otu_failures=open(otus_failures_fp).read()
        
        self.assertEqual(obs_otu_failures,exp_otu_failures)
        
        #load the otu table and check if they are valid
        otus_table_fp=join(self.wf_out, 'exact_uclust_ref_otu_table.txt')
        obs_otu_table=open(otus_table_fp).read()
        
        self.assertEqual(obs_otu_table,exp_otu_table)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)
    
    '''
    # CURRENTLY: we do not allow for parallel otu-picking
    def test_run_chain_pick_otus_parallel(self):
        """run_chain_pick_otus runs without error"""
        run_chain_pick_otus(self.fna_original_fp, self.wf_out,\
                    call_commands_serially, \
                    self.params, self.qiime_config, True,\
                    no_status_updates)
        
        #load the exact match OTUs and check if they are valid
        exact_otus_fp=join(self.wf_out,'pick_otus_exact',\
                           'test_otus.txt')
        obs_exact_otus=open(exact_otus_fp).read()
        
        self.assertEqual(obs_exact_otus,exp_exact_otus)
        
        #load the uclust_ref picked OTUs and check if they are valid
        uclust_ref_otus_fp=join(self.wf_out,'picked_otus_UCLUST_REF_97',
                            'leftover_otus.txt')
        obs_uclust_ref_otus=open(uclust_ref_otus_fp).read()
        
        self.assertEqual(obs_uclust_ref_otus,exp_uclust_ref_otus)
        
        #load the merged OTUs and check if they are valid
        all_otus_fp=uclust_ref_otus_fp=join(self.wf_out,
                                            'exact_uclust_ref_otus.txt')
        obs_all_otus=open(all_otus_fp).read()
        
        self.assertEqual(obs_all_otus,exp_all_otus)
        
        #load the sample failures and check if they are valid
        otus_failures_fp=join(self.wf_out, 'all_failures.txt')
        obs_otu_failures=open(otus_failures_fp).read()
        
        self.assertEqual(obs_otu_failures,exp_otu_failures)
        
        #load the otu table and check if they are valid
        otus_table_fp=join(self.wf_out, 'exact_uclust_ref_otu_table.txt')
        obs_otu_table=open(otus_table_fp).read()
        
        self.assertEqual(obs_otu_table,exp_otu_table)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)
        
    '''
        
  
exp_otu_failures='''\
test.PCx634.281501_20
test.PCx635.281504_16
test.PCx634.281501_14
test.PCx634.281501_19'''

exp_otu_table='''\
# QIIME v1.2.1-dev OTU table
#OTU ID	test.PCx354.281499	test.PCx355.281497	test.PCx356.281498	test.PCx481.281500	test.PCx593.281502	test.PCx634.281501	test.PCx635.281504	test.PCx636.281503
204144	0	0	0	0	1	0	0	0
230364	0	0	0	0	0	1	0	0
264035	0	0	0	0	0	0	0	1
266771	1	1	0	0	0	0	0	0
268947	0	0	0	1	0	0	0	0
299668	0	0	0	0	0	1	0	0
331820	0	0	0	0	0	2	0	0
332311	0	0	0	0	0	1	0	0
343906	0	0	0	0	0	1	0	0
355771	0	0	1	0	0	0	0	0
362383	0	0	0	0	0	1	0	0
469832	0	0	0	0	0	2	0	0
568692	0	0	0	0	0	0	1	0'''

exp_exact_otus='''\
0	test.PCx635.281504_16
1	test.PCx634.281501_19
2	test.PCx354.281499_3
3	test.PCx634.281501_8
4	test.PCx636.281503_6
5	test.PCx634.281501_18
6	test.PCx355.281497_13
7	test.PCx634.281501_1
8	test.PCx635.281504_15
9	test.PCx634.281501_2
10	test.PCx634.281501_10
11	test.PCx634.281501_9
12	test.PCx481.281500_4
13	test.PCx634.281501_20
14	test.PCx634.281501_14
15	test.PCx634.281501_11
16	test.PCx634.281501_7
17	test.PCx356.281498_17
18	test.PCx634.281501_5
19	test.PCx593.281502_12
'''

exp_uclust_ref_otus=''''''

exp_all_otus='''\
355771	test.PCx356.281498_17
362383	test.PCx634.281501_1
268947	test.PCx481.281500_4
204144	test.PCx593.281502_12
230364	test.PCx634.281501_8
469832	test.PCx634.281501_11	test.PCx634.281501_2
332311	test.PCx634.281501_7
343906	test.PCx634.281501_5
299668	test.PCx634.281501_18
331820	test.PCx634.281501_10	test.PCx634.281501_9
264035	test.PCx636.281503_6
568692	test.PCx635.281504_15
266771	test.PCx354.281499_3	test.PCx355.281497_13
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

test_dir = abspath(dirname(__file__))
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
pick_otus:refseqs_fp    %s/gg_97_otus_4feb2011.fasta
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

""" % os.path.join(test_dir, 'support_files')

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
