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
from run_process_sff_through_split_lib import (run_process_sff_through_split_lib)
from qiime.workflow import (call_commands_serially,
no_status_updates,WorkflowError,print_commands)
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
        
        '''
        self.fasting_seqs_fp = get_tmp_filename(tmp_dir=tmp_dir,
            prefix='qiime_wf_seqs',suffix='.fasta')
        fasting_seqs_f = open(self.fasting_seqs_fp,'w')
        fasting_seqs_f.write(fasting_seqs_subset)
        fasting_seqs_f.close()
        self.files_to_remove.append(self.fasting_seqs_fp)
        
        self.fasting_seqs_denoiser_fp = get_tmp_filename(tmp_dir=tmp_dir,
            prefix='qiime_wf_seqs',suffix='.fasta')
        fasting_seqs_f = open(self.fasting_seqs_denoiser_fp,'w')
        fasting_seqs_f.write('\n'.join(fasting_seqs_subset.split('\n')[:44]))
        fasting_seqs_f.close()
        self.files_to_remove.append(self.fasting_seqs_denoiser_fp)
        '''
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
        
    def test_run_process_sff_through_split_lib(self):
        """run_process_sff_through_pick_otus runs without error"""
        run_process_sff_through_split_lib(0,sff_input_fp=self.sff_fp,\
         mapping_fp=self.fasting_mapping_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         convert_to_flx=False,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
         
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                    'seqs.fna')
                                    
        sff_fp = join(self.wf_out,'Fasting_subset.sff')
        sff_seqs_fp = join(self.wf_out,'Fasting_subset.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        # check that the two final output files have non-zero size
        self.assertTrue(getsize(split_lib_seqs_fp) > 0)
        self.assertTrue(getsize(sff_fp) > 0)
        self.assertTrue(getsize(sff_qual_fp) > 0)
        self.assertTrue(getsize(sff_flow_fp) > 0)
        
        new_map_str=open(new_map_fp,'U').read()
        
        self.assertTrue(new_map_str,exp_new_fasting_map)
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)


    def test_run_process_sff_through_split_lib_FLX(self):
        """run_process_sff_through_pick_otus runs without error: Convert to FLX"""
        run_process_sff_through_split_lib(0,sff_input_fp=self.sff_fp,\
         mapping_fp=self.fasting_mapping_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         convert_to_flx=True,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
         
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                    'seqs.fna')
                                    
        sff_fp = join(self.wf_out,'Fasting_subset_FLX.sff')
        sff_seqs_fp = join(self.wf_out,'Fasting_subset_FLX.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset_FLX.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset_FLX.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        # check that the two final output files have non-zero size
        self.assertTrue(getsize(split_lib_seqs_fp) > 0)
        self.assertTrue(getsize(sff_fp) > 0)
        self.assertTrue(getsize(sff_qual_fp) > 0)
        self.assertTrue(getsize(sff_flow_fp) > 0)
        
        new_map_str=open(new_map_fp,'U').read()
        
        self.assertTrue(new_map_str,exp_new_fasting_map)
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

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
pick_otus:refseqs_fp    /home/wwwuser/software/greengenes_core_sets/gg_otus_9aug2010/inflated_sub_gg/uclust_otus_97/rep_set/gg_97_otus_9aug2010.fasta
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
pick_otus:suppress_new_clusters
pick_otus:uclust_otu_id_prefix  otu_

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

exp_new_fasting_map = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
PCx354-Fasting_subset	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse__I.D._354
PCx355-Fasting_subset	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse__I.D._355
PCx356-Fasting_subset	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Control	20061126	Control_mouse__I.D._356
PCx481-Fasting_subset	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Control	20070314	Control_mouse__I.D._481
PCx593-Fasting_subset	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Control	20071210	Control_mouse__I.D._593
PCx607-Fasting_subset	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fast	20071112	Fasting_mouse__I.D._607
PCx634-Fasting_subset	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._634
PCx635-Fasting_subset	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._635
PCx636-Fasting_subset	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse__I.D._636
"""

if __name__ == "__main__":
    main()
