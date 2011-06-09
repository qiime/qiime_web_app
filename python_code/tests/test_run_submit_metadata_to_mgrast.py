#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"
 

from cogent.util.unit_test import TestCase, main

from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename
from run_submit_metadata_to_mgrast import clean_value_for_mgrast
from os.path import join
from data_access_connections import data_access_factory
from enums import ServerConfig





class runSubmitMetadataToMGRAST(TestCase):
    
    def setUp(self):
        """setup the test values"""
        
        self.dirs_to_remove = []
        self.files_to_remove = []
        self.tmp_dir='/tmp/'
        
        #generate random fnames for OTU maps
        #self.output_fasta = get_tmp_filename(tmp_dir = self.tmp_dir,
        #    prefix = 'seqs_', suffix = '.fna', result_constructor = str)
        
    def tearDown(self):
        """remove all the files after completing tests """
        
        remove_files(self.files_to_remove)

    def test_clean_value_for_mgrast(self):
        test_string = 'This is a < > & test.'
        test_string = clean_value_for_mgrast(test_string)
        self.assertFalse('>' in test_string)
        self.assertFalse('<' in test_string)
        self.assertFalse(' & ' in test_string)
        self.assertTrue('&lt;' in test_string)
        self.assertTrue('&gt;' in test_string)
        self.assertTrue('&amp;' in test_string)

if __name__ == "__main__":
    main()