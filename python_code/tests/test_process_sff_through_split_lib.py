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
from os.path import join, exists, getsize, split, splitext, abspath, dirname
from os import makedirs, environ, system
from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename, ApplicationNotFoundError
from qiime.util import load_qiime_config, create_dir, get_top_fastq_two_lines
from qiime.parse import parse_qiime_parameters
from run_process_sff_through_split_lib import (run_process_sff_through_split_lib,
                                        run_process_illumina_through_split_lib,
                                        run_process_fasta_through_split_lib)
from qiime.workflow import (call_commands_serially, no_status_updates, 
                            WorkflowError, print_commands)

    
class WorkflowTests(TestCase):
    
    def setUp(self):
        """ """
        
        self.qiime_config = load_qiime_config()
        self.dirs_to_remove = []
        self.files_to_remove = []
        
        # create output directory
        self.wf_out="/%s/tmp" % environ['HOME']
        create_dir(self.wf_out)
        
        #this is specific to the web-apps only
        test_dir = abspath(dirname(__file__))
        sff_original_fp = os.path.join(test_dir, 'support_files', \
                                        'Fasting_subset.sff')
        sff_gz_original_fp = os.path.join(test_dir, 'support_files', \
                                        'Fasting_subset.sff.gz')
        
        self.illumina_fps = [os.path.join(test_dir, 'support_files', \
                                        's_8_1_sequence_100_records.txt.gz'),
                             os.path.join(test_dir, 'support_files', \
                                        's_8_2_sequence_100_records.txt.gz')]
        self.illumina_map_fp = os.path.join(test_dir, 'support_files', \
                                        's8_map_incomplete.txt')
        self.fasta_fps=[os.path.join(test_dir,'support_files',
                                   'test_split_lib_seqs.fasta')]
        self.fasta_map_fp = os.path.join(test_dir, 'support_files', \
                                        'fasta_mapping_file.txt')
                                        
        # move SFF into place but also make sure to remove it
        self.sff_fp = os.path.join(environ['HOME'], 'Fasting_subset.sff')
        self.sff_gz_fp = os.path.join(environ['HOME'], 'Fasting_subset.sff.gz')
        copy(sff_original_fp, self.sff_fp)
        copy(sff_gz_original_fp, self.sff_gz_fp)
        self.files_to_remove.append(self.sff_fp)
        self.files_to_remove.append(self.sff_gz_fp)
        
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
        
        # define working directory
        working_dir = self.qiime_config['working_dir'] or '%s/tmp/' % \
                                                                environ['HOME']
        jobs_dir = join(working_dir,'jobs')
        if not exists(jobs_dir):
            # only clean up the jobs dir if it doesn't already exist
            self.dirs_to_remove.append(jobs_dir)

        # remove the default log file
        self.files_to_remove.append(join(self.wf_out,'log.txt'))            

        # parse params file
        self.params = parse_qiime_parameters(qiime_parameters_f.split('\n'))
        
    
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
        """ run_process_sff_through_pick_otus: runs without error """
        
        # remove generated mapping file
        moved_mapping_file=join(self.wf_out,split(self.fasting_mapping_fp)[-1])
        self.files_to_remove.append(moved_mapping_file)
        
        # process the SFF files
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
         
        # get the file basename
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        # get the split-library sequence fpath
        split_lib_seqs_fp = join(self.wf_out,'split_libraries','seqs.fna')
                                    
        sff_seqs_fp = join(self.wf_out,'Fasting_subset.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        
        # define files to remove
        self.files_to_remove.append(sff_seqs_fp)
        self.files_to_remove.append(sff_qual_fp)
        self.files_to_remove.append(sff_flow_fp)
        
        # get the head of files
        split_lib_head=get_top_fastq_two_lines(open(split_lib_seqs_fp,'U'))
        raw_seq_head=get_top_fastq_two_lines(open(sff_seqs_fp,'U'))
        raw_qual_head=get_top_fastq_two_lines(open(sff_qual_fp,'U'))
        raw_flow_head=get_top_fastq_two_lines(open(sff_flow_fp,'U'))
        
        # check results
        self.assertEqual(''.join(split_lib_head),exp_FLX_split_lib_head)
        self.assertEqual(''.join(raw_seq_head),exp_FLX_raw_seq_head)
        self.assertEqual(''.join(raw_qual_head),exp_FLX_raw_qual_head)
        self.assertEqual(''.join(raw_flow_head),exp_FLX_raw_flow_head)

        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

    def test_run_process_sff_gz_through_split_lib(self):
        """ run_process_sff_through_pick_otus: runs without error """
        
        # remove generated mapping file
        moved_mapping_file=join(self.wf_out,split(self.fasting_mapping_fp)[-1])
        self.files_to_remove.append(moved_mapping_file)
        
        # process the SFF files
        run_process_sff_through_split_lib(0,'Fasting_subset',\
         sff_input_fp=self.sff_gz_fp,\
         mapping_fp=self.fasting_mapping_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         convert_to_flx=False,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
         
        # get the file basename
        input_file_basename = splitext(splitext(split(self.sff_fp)[1])[0])[0]
        
        # get the split-library sequence fpath
        split_lib_seqs_fp = join(self.wf_out,'split_libraries','seqs.fna')
                                    
        sff_seqs_fp = join(self.wf_out,'Fasting_subset.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        
        # define files to remove
        self.files_to_remove.append(sff_seqs_fp)
        self.files_to_remove.append(sff_qual_fp)
        self.files_to_remove.append(sff_flow_fp)
        
        # get the head of files
        split_lib_head=get_top_fastq_two_lines(open(split_lib_seqs_fp,'U'))
        raw_seq_head=get_top_fastq_two_lines(open(sff_seqs_fp,'U'))
        raw_qual_head=get_top_fastq_two_lines(open(sff_qual_fp,'U'))
        raw_flow_head=get_top_fastq_two_lines(open(sff_flow_fp,'U'))
        
        # check results
        self.assertEqual(''.join(split_lib_head),exp_FLX_split_lib_head)
        self.assertEqual(''.join(raw_seq_head),exp_FLX_raw_seq_head)
        self.assertEqual(''.join(raw_qual_head),exp_FLX_raw_qual_head)
        self.assertEqual(''.join(raw_flow_head),exp_FLX_raw_flow_head)

        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

    def test_run_process_sff_through_split_lib_FLX(self):
        """run_process_sff_through_pick_otus runs without error: Convert to \
FLX"""
        
        # remove generated mapping file
        moved_mapping_file=join(self.wf_out,split(self.fasting_mapping_fp)[-1])
        self.files_to_remove.append(moved_mapping_file)
        
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
        
        # get the file basename
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        # get the split-library sequence fpath
        split_lib_seqs_fp = join(self.wf_out,'split_libraries','seqs.fna')
                                    
        sff_fp = join(self.wf_out,'Fasting_subset_FLX.sff')
        sff_seqs_fp = join(self.wf_out,'Fasting_subset_FLX.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset_FLX.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset_FLX.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        
        # define files to remove
        self.files_to_remove.append(sff_fp)
        self.files_to_remove.append(sff_seqs_fp)
        self.files_to_remove.append(sff_qual_fp)
        self.files_to_remove.append(sff_flow_fp)
        
        # get the head of files
        split_lib_head=get_top_fastq_two_lines(open(split_lib_seqs_fp,'U'))
        raw_seq_head=get_top_fastq_two_lines(open(sff_seqs_fp,'U'))
        raw_qual_head=get_top_fastq_two_lines(open(sff_qual_fp,'U'))
        raw_flow_head=get_top_fastq_two_lines(open(sff_flow_fp,'U'))
        
        # check results
        self.assertEqual(''.join(split_lib_head),exp_FLX_split_lib_head)
        self.assertEqual(''.join(raw_seq_head),exp_FLX_raw_seq_head)
        self.assertEqual(''.join(raw_qual_head),exp_FLX_raw_qual_head)
        self.assertEqual(''.join(raw_flow_head),exp_Ti_raw_flow_head)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

    
    def test_run_process_sff_gz_through_split_lib_FLX(self):
        """run_process_sff_through_pick_otus runs without error: Convert to \
FLX"""
        
        # remove generated mapping file
        moved_mapping_file=join(self.wf_out,split(self.fasting_mapping_fp)[-1])
        self.files_to_remove.append(moved_mapping_file)
        
        run_process_sff_through_split_lib(0,'Fasting_subset',\
         sff_input_fp=self.sff_gz_fp,\
         mapping_fp=self.fasting_mapping_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         convert_to_flx=True,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
        
        # get the file basename
        input_file_basename = splitext(splitext(split(self.sff_fp)[1])[0])[0]
        
        # get the split-library sequence fpath
        split_lib_seqs_fp = join(self.wf_out,'split_libraries','seqs.fna')
                                    
        sff_fp = join(self.wf_out,'Fasting_subset_FLX.sff')
        sff_seqs_fp = join(self.wf_out,'Fasting_subset_FLX.fna')
        sff_qual_fp = join(self.wf_out,'Fasting_subset_FLX.qual')
        sff_flow_fp = join(self.wf_out,'Fasting_subset_FLX.txt')
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')
        
        # define files to remove
        self.files_to_remove.append(sff_fp)
        self.files_to_remove.append(sff_seqs_fp)
        self.files_to_remove.append(sff_qual_fp)
        self.files_to_remove.append(sff_flow_fp)
        
        # get the head of files
        split_lib_head=get_top_fastq_two_lines(open(split_lib_seqs_fp,'U'))
        raw_seq_head=get_top_fastq_two_lines(open(sff_seqs_fp,'U'))
        raw_qual_head=get_top_fastq_two_lines(open(sff_qual_fp,'U'))
        raw_flow_head=get_top_fastq_two_lines(open(sff_flow_fp,'U'))
        
        # check results
        self.assertEqual(''.join(split_lib_head),exp_FLX_split_lib_head)
        self.assertEqual(''.join(raw_seq_head),exp_FLX_raw_seq_head)
        self.assertEqual(''.join(raw_qual_head),exp_FLX_raw_qual_head)
        self.assertEqual(''.join(raw_flow_head),exp_Ti_raw_flow_head)
        
        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)

    def test_run_process_illumina_through_split_lib(self):
        """run_process_illumina_through_pick_otus: runs without error"""
        
        self.files_to_remove.append(join(self.wf_out,'s8_map_incomplete.txt'))
        
        # process the sequence data
        run_process_illumina_through_split_lib(0,'Fasting_subset',\
         input_fp=','.join(self.illumina_fps),\
         mapping_fp=self.illumina_map_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
        
        # get the file basename
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        # get the split-library sequence fpath
        split_lib_seqs_fp = join(self.wf_out,'split_libraries','seqs.fna')
                                    
        new_map_fp = join(self.wf_out,'Fasting_subset_mapping.txt')

        # get the head of files
        split_lib_head=get_top_fastq_two_lines(open(split_lib_seqs_fp,'U'))
        
        # check results
        self.assertEqual(''.join(split_lib_head),exp_illumina_split_lib_head)

        # Check that the log file is created and has size > 0
        log_fp = glob(join(self.wf_out,'log*.txt'))[0]
        self.assertTrue(getsize(log_fp) > 0)
    
    def test_run_process_fasta_through_split_lib(self):
        """run_run_process_fasta_through_split_lib runs without error"""
        
        self.files_to_remove.append(join(self.wf_out,'fasta_mapping_file.txt'))
        
        # process the sequence data
        run_process_fasta_through_split_lib(0,'Fasting_subset',\
         input_fp=','.join(self.fasta_fps),\
         mapping_fp=self.fasta_map_fp,\
         output_dir=self.wf_out, \
         command_handler=call_commands_serially,\
         params=self.params,\
         qiime_config=self.qiime_config,\
         write_to_all_fasta=False,\
         status_update_callback=no_status_updates)
        
        # get the file basename
        input_file_basename = splitext(split(self.sff_fp)[1])[0]
        
        # get the split-library sequence fpath
        split_lib_seqs_fp = join(self.wf_out,'split_libraries', 'seqs.fna')
        
        # get the head of files
        split_lib_head=get_top_fastq_two_lines(open(split_lib_seqs_fp,'U'))
        
        split_lib_seqs_only=[split_lib_head[1],split_lib_head[3]]
        
        # check results
        self.assertEqual(''.join(split_lib_seqs_only),
                         exp_fasta_split_lib_seqs_only)
        
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

exp_FLX_split_lib_head="""\
>PCx634_1 FLP3FBN01ELBSX orig_bc=ACAGAGTCGGCT new_bc=ACAGAGTCGGCT bc_diffs=0
CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG
>PCx634_2 FLP3FBN01EG8AX orig_bc=ACAGAGTCGGCT new_bc=ACAGAGTCGGCT bc_diffs=0
TTGGACCGTGTCTCAGTTCCAATGTGGGGGCCTTCCTCTCAGAACCCCTATCCATCGAAGGCTTGGTGGGCCGTTACCCCGCCAACAACCTAATGGAACGCATCCCCATCGATGACCGAAGTTCTTTAATAGTTCTACCATGCGGAAGAACTATGCCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTCATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
"""
exp_FLX_raw_seq_head="""\
>FLP3FBN01ELBSX length=250 xy=1766_0111 region=1 run=R_2008_12_09_13_51_01_
ACAGAGTCGGCTCATGCTGCCTCCCGTAGGAGTCTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG
>FLP3FBN01EG8AX length=276 xy=1719_1463 region=1 run=R_2008_12_09_13_51_01_
ACAGAGTCGGCTCATGCTGCCTCCCGTAGGAGTTTGGACCGTGTCTCAGTTCCAATGTGGGGGCCTTCCTCTCAGAACCCCTATCCATCGAAGGCTTGGTGGGCCGTTACCCCGCCAACAACCTAATGGAACGCATCCCCATCGATGACCGAAGTTCTTTAATAGTTCTACCATGCGGAAGAACTATGCCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTCATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
"""
exp_FLX_raw_qual_head="""\
>FLP3FBN01ELBSX length=250 xy=1766_0111 region=1 run=R_2008_12_09_13_51_01_
37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 36 33 33 33 36 37 37 37 37 37 37 40 40 40 39 39 38 40 40 40 40 40 40 40 37 37 37 37 37 35 35 35 37 37 37 37 37 35 35 35 31 31 23 23 23 31 21 21 21 35 35 37 37 37 36 36 36 36 36 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 28 28 28 36 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 36 36 37 37 37 37 37 37 37 37 37 37 37 37 36 36 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 35 32 32 32 32 35 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 32 32 32 36 37 35 32 32 32 32 32 32 32 32 36 37 37 37 37 36 36 31 31 32 32 36 36 36 36 36 36 36 36 36 36 36 28 27 27 27 26 26 26 30 29 30 29 24 24 24 21 15 15 13 13
>FLP3FBN01EG8AX length=276 xy=1719_1463 region=1 run=R_2008_12_09_13_51_01_
37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 38 37 33 33 21 21 21 26 33 37 36 36 40 33 24 24 29 33 33 39 39 39 40 39 39 39 40 37 37 37 37 37 37 37 37 37 37 37 32 32 20 20 20 20 20 35 35 37 37 37 37 37 37 37 36 36 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 36 36 36 36 36 37 37 37 37 37 36 36 36 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 33 28 28 28 28 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 33 33 33 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 36 36 36 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 37 28 28 28 37 28 28 28 37 37 37 37 37 36 36 36 36 36 28 26 26 26 26 28 36 36 36 36 36 36 36 37 38 38 38 38 38 37 37 37 37 37 31 31 31 31 31 31 31 31 31 31 31 31 30 22 22 22 25 25 31 31 31 31 31 31 31 25 25 25 25 25 28
"""
exp_FLX_raw_flow_head="""\
Common Header:
  Magic Number:  0x2E736666
  Version:       0001
  Index Offset:  36488
"""

exp_Ti_raw_flow_head="""\
Common Header:
  Magic Number:  0x2E736666
  Version:       0001
  Index Offset:  0
"""
exp_illumina_split_lib_head="""\
>SSBE24July07_0 HWUSI-EAS552R_0357:8:1:15008:6374#0/2 orig_bc=ATCCTCAGTAGT new_bc=ATCCTCAGTAGT bc_diffs=0
TACGAAGGCCCCGAGCGTTATCCGGATTAATTGGGCGTAAAGCGTTAATAGGCGGTTTGGTAAGTGTCTCGTTAAATCTCATGGCTCAACCATGAGGCCGCGAGACATACTGCCAGACTTGAGGCCGGAAGAGGCAAGCGGAACTACCGG
>HKE08Aug07_1 HWUSI-EAS552R_0357:8:1:15923:6368#0/2 orig_bc=AAGAGATGTCGA new_bc=AAGAGATGTCGA bc_diffs=0
TACGAAGGGAGCTAGCGTTATTCGGAATGATTGGGTGTAAAGAGTTTGTAGATTGCAAAATTTTTGTTATTAGTAAAAAATTGAATTTATTATTTAAAGATGCTTTTAATACAATTTTGCTTGAGTATAGTAGAGGAAAAT
"""

exp_fasta_split_lib_seqs_only="""\
CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTTACCTCACCAACTAGCTAATGCGCCGCAGGTCCATCCATGTTCACGCCTTGATGGGCGCTTTAATATACTGAGCATGCGCTCTGTATACCTATCCGGTTTTAGCTACCGTTTCCAGCAGTTATCCCGGACACATGGGCTAGG
TTGGACCGTGTCTCAGTTCCAATGTGGGGGCCTTCCTCTCAGAACCCCTATCCATCGAAGGCTTGGTGGGCCGTTACCCCGCCAACAACCTAATGGAACGCATCCCCATCGATGACCGAAGTTCTTTAATAGTTCTACCATGCGGAAGAACTATGCCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTCATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
"""

if __name__ == "__main__":
    main()
