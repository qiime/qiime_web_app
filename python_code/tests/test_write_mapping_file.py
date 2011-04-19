#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename
from write_mapping_file import write_mapping_file
from os.path import join,exists
from os import makedirs,listdir
from shutil import rmtree
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

class writeMappingFile(TestCase):
    
    def setUp(self):
        """setup the test values"""
        self.dirs_to_remove = []
        self.files_to_remove = []
        self.tmp_dir='/tmp/'
        
        #generate random fnames for OTU maps
        self.output_dir=get_tmp_filename(tmp_dir=self.tmp_dir,
         prefix='tmp_mapping_files',suffix='',result_constructor=str)
        
        if not exists(self.output_dir):
            makedirs(self.output_dir)
            # if test creates the temp dir, also remove it
            self.dirs_to_remove.append(self.output_dir)
        
    def tearDown(self):
        """remove all the files after completing tests """

        # remove directories last, so we don't get errors
        # trying to remove files which may be in the directories
        for d in self.dirs_to_remove:
            if exists(d):
                rmtree(d)

    def test_write_mapping_file(self):
        """ test_write_mapping_file: This function writes a QIIME-formatted 
            mapping file
        """
        
        write_mapping_file(609,False,self.output_dir,True)
        open_fpath=open(join(self.output_dir,'study_609_run_Fasting_subset_mapping.txt')).read()
        
        self.assertEqual(open_fpath,exp_mapping)

exp_mapping="""\
#SampleID	BarcodeSequence	LinkerPrimerSequence	STUDY_ID	RUN_PREFIX	Description
test.PCx481.281527	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx634.281528	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx355.281524	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx607.281523	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx636.281530	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx635.281531	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx593.281529	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx356.281525	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test
test.PCx354.281526	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	609	Fasting_subset	fasting_mice_test"""

if __name__ == "__main__":
    main()