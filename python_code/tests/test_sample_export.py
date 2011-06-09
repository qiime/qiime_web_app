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
from sample_export import export_full_db_to_fasta, export_db_to_fasta,\
                          export_fasta_from_study, export_fasta_from_sample
from os.path import join
import os
import stat
from data_access_connections import data_access_factory
from enums import ServerConfig

class sampleExport(TestCase):
    
    def setUp(self):
        """setup the test values"""
        
        self.dirs_to_remove = []
        self.files_to_remove = []
        self.tmp_dir='/tmp/'
        
        #generate random fnames for OTU maps
        self.output_fasta = get_tmp_filename(tmp_dir = self.tmp_dir,
            prefix = 'seqs_', suffix = '.fna', result_constructor = str)
        
    def tearDown(self):
        """remove all the files after completing tests """
        
        remove_files(self.files_to_remove)

    def test_export_full_db_to_fasta(self):
        export_full_db_to_fasta(self.output_fasta, False)
        file_size = os.stat(self.output_fasta)[stat.ST_SIZE]
        self.assertTrue(file_size > 0)
        
    def test_export_db_to_fasta(self):
        export_db_to_fasta(self.output_fasta, 12161)
        file_size = os.stat(self.output_fasta)[stat.ST_SIZE]
        self.assertTrue(file_size > 0)

    def test_export_fasta_from_study(self):
        export_fasta_from_study(389, self.output_fasta)
        file_size = os.stat(self.output_fasta)[stat.ST_SIZE]
        self.assertTrue(file_size > 0)

    def test_export_fasta_from_sample(self):
        export_fasta_from_sample(389, 240083, self.output_fasta)
        file_size = os.stat(self.output_fasta)[stat.ST_SIZE]
        self.assertTrue(file_size > 0)
        
if __name__ == "__main__":
    main()