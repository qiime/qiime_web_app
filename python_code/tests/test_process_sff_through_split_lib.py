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
from qiime.util import load_qiime_config
from qiime.parse import parse_qiime_parameters
from run_process_sff_through_split_lib import (run_process_sff_through_split_lib,
                                        run_process_illumina_through_split_lib,
                                        run_process_fasta_through_split_lib)
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
        
        #this is specific to the web-apps only
        test_dir = abspath(dirname(__file__))
        sff_original_fp = os.path.join(test_dir, 'support_files', \
                                        'Fasting_subset.sff')
        
        self.illumina_fps = [os.path.join(test_dir, 'support_files', \
                                        's_8_1_sequence_100_records.txt'),
                             os.path.join(test_dir, 'support_files', \
                                        's_8_2_sequence_100_records.txt')]
        self.illumina_map_fp = os.path.join(test_dir, 'support_files', \
                                        's8_map_incomplete.txt')
        self.fasta_fps=[os.path.join(test_dir,'support_files',
                                   'test_split_lib_seqs.fasta')]
        self.fasta_map_fp = os.path.join(test_dir, 'support_files', \
                                        'fasta_mapping_file.txt')
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
        self.params = parse_qiime_parameters(qiime_parameters_f.split('\n'))

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
        run_process_sff_through_split_lib(0,'Fasting_subset',\
         sff_input_fp=self.sff_fp,\
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
                                    
        #sff_fp = join(self.wf_out,'Fasting_subset.sff')
        sff_seqs_fp = join(self.wf_out,'Fasting_subset.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        # check that the two final output files have non-zero size
        self.assertTrue(getsize(split_lib_seqs_fp) > 0)
        #self.assertTrue(getsize(sff_fp) > 0)
        self.assertTrue(getsize(sff_qual_fp) > 0)
        self.assertTrue(getsize(sff_flow_fp) > 0)
        
        #new_map_str=open(new_map_fp,'U').read()
        
        #self.assertTrue(new_map_str,exp_new_fasting_map)
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)


    def test_run_process_sff_through_split_lib_FLX(self):
        """run_process_sff_through_pick_otus runs without error: Convert to FLX"""
        run_process_sff_through_split_lib(0,'Fasting_subset',\
         sff_input_fp=self.sff_fp,\
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
        
        #new_map_str=open(new_map_fp,'U').read()
        
        #self.assertTrue(new_map_str,exp_new_fasting_map)
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

    #
    def test_run_process_illumina_through_split_lib(self):
        """run_process_illumina_through_pick_otus runs without error"""
        run_process_illumina_through_split_lib(0,'Fasting_subset',\
         input_fp=','.join(self.illumina_fps),\
         mapping_fp=self.illumina_map_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
        
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                    'seqs.fna')
                                    
        #sff_fp = join(self.wf_out,'Fasting_subset.sff')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        
        # check that the two final output files have non-zero size
        self.assertTrue(getsize(split_lib_seqs_fp) > 0)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)
    #
    def test_run_process_fasta_through_split_lib(self):
        """run_run_process_fasta_through_split_lib runs without error"""
        run_process_fasta_through_split_lib(0,'Fasting_subset',\
         input_fp=','.join(self.fasta_fps),\
         mapping_fp=self.fasta_map_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
        
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        split_lib_seqs_fp = join(self.wf_out,'split_libraries',\
                                    'seqs.fna')
        
        # check that the two final output files have non-zero size
        self.assertTrue(getsize(split_lib_seqs_fp) > 0)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

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
split_libraries:record_qual_scores True

# OTU picker parameters
pick_otus:otu_picking_method	uclust_ref
pick_otus:clustering_algorithm	furthest
pick_otus:refseqs_fp    %s/gg_97_otus_4feb2011.fasta
pick_otus:similarity	0.97
pick_otus:suppress_new_clusters True
pick_otus:enable_rev_strand_match True

# Parallel options
parallel:jobs_to_start	2
parallel:retain_temp_files	False
parallel:seconds_to_sleep	1

"""

fasting_map = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
PCx354	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Control	20061218	1
PCx355	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Control	20061218	2
PCx356	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Control	20061126	3
PCx481	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Control	20070314	4
PCx593	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Control	20071210	5
PCx607	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fast	20071112	6
PCx634	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	7
PCx635	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	8
PCx636	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	9
"""

exp_new_fasting_map = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
PCx354.Fasting_subset	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Control	20061218	1
PCx355.Fasting_subset	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Control	20061218	2
PCx356.Fasting_subset	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Control	20061126	3
PCx481.Fasting_subset	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Control	20070314	4
PCx593.Fasting_subset	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Control	20071210	5
PCx607.Fasting_subset	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fast	20071112	6
PCx634.Fasting_subset	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	7
PCx635.Fasting_subset	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	8
PCx636.Fasting_subset	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fast	20080116	9
"""

if __name__ == "__main__":
    main()
