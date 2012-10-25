#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"
 
from ebi_output_parser import *
from cogent.util.unit_test import TestCase, main

class Tests(TestCase):
    
    def setUp(self):
        """ Setup
        """
        self.parser = ebi_output_parser('support_files/ebi_results.xml')
        pass
        
    def tearDown(self):
        """ Clean up
        """
        pass

    def test_parse_samples(self):
        """ Test instantiation of base services
        """
        samples = self.parser.parse_samples()
        self.assertIsNotNone(samples)
        
if __name__ == "__main__":
    main()