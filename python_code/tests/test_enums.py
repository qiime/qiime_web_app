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
from enums import FieldGrouping,DataAccessType,ServerConfig
import getpass

class Tests(TestCase):
    
   
    def test_FieldGrouping(self):
        """ test_FieldGrouping: this is the field groupings
        """
        
        self.assertEqual(FieldGrouping.prep_level,-1)
        self.assertEqual(FieldGrouping.sample_level,-2)
        self.assertEqual(FieldGrouping.study_level,-3)
        
    def test_DataAccessType(self):
        """ test_DataAccessType: this is the data access types
        """
        
        self.assertEqual(DataAccessType.qiime_production,1)
        self.assertEqual(DataAccessType.qiime_test,2)

    def test_ServerConfig(self):
        """ test_ServerConfig: this is the field groupings
        """
        
        self.assertEqual(ServerConfig.home,'/home/%s/' % getpass.getuser())


if __name__ == "__main__":
    main()