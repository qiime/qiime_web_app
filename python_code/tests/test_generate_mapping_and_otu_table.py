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
from generate_mapping_and_otu_table import (combine_map_header_cols,
                                           get_mapping_data)

class TopLevelTests(TestCase):
    """Tests of top-level functions"""

    def setUp(self):
        
        self.map = [['SampleID','BarcodeSequence','LinkerPrimerSequence',
                     'Description'],['Sample1','AA','GGCC','Test1'],
                     ['Sample2','CC','AAGG','Test2']]
        
        
    def test_combine_map_header_cols(self):
        """ combine_map_header_cols: this combines 2 cols in mapping file"""
        
        
        obs=combine_map_header_cols(['SampleID','Description'],self.map)
        exp = [['SampleID','BarcodeSequence','LinkerPrimerSequence',
                     'Description','SampleID_and_Description'],
                     ['Sample1','AA','GGCC','Test1','Sample1_Test1'],
                     ['Sample2','CC','AAGG','Test2','Sample2_Test2']]
        
        self.assertEqual(obs,exp)
        
    def test_get_mapping_data(self):
        """ get_mapping_data: this gets the metadata from DB """
        
        {'SAMPLE####SEP####COUNTRY####STUDIES####613': '####ALL####'}
        
if __name__ == "__main__":
    main()