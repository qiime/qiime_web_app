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
from linkamafy import *

class LinkTests(TestCase):
    
    def setUp(self):
        """setup the test values"""
        pass
        
        
    def tearDown(self):
        """remove all the files after completing tests """
        pass

    def test_link_urls(self):
        """ Tests that the passed string contains new hyperlinks when processed
        """
        test_string = 'Yo. This is a test of the http://linka.ma.fy/proce.ess. It should look good.'
        expected_result = 'Yo. This is a test of the <a href="http://linka.ma.fy/proce.ess" target="_blank">http://linka.ma.fy/proce.ess</a>. It should look good.'
        result = link_urls(test_string)
        self.assertEqual(result, expected_result)
        
if __name__ == "__main__":
    main()