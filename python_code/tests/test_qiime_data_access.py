#!/usr/bin/env python

"""
Unit tests for qiime_data_access.py
"""

import unittest
from qiime_data_access import QiimeDataAccess

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

class QiimeDataAccessTests(unittest.TestCase):
    """Unit tests for the QiimeDataAccess class

    QiimeDataAccess unit tests. These tests are designed to validate that
    the various database functions work and return expected values.
    """

    # Global variables required for all tests
    _qiime_data_access = None

    # Set up and tear downdown
    def setUp(self):
        global _qiime_data_access
        _qiime_data_access = QiimeDataAccess()

    def tearDown(self):
        pass

    # The rest of the unit tests
    def test_getDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getDatabaseConnection()
        self.assertTrue(con)
        con.close()

    def test_getOntologyDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getOntologyDatabaseConnection()
        self.assertTrue(con)
        con.close()

    def test_getTestDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getTestDatabaseConnection()
        self.assertTrue(con)
        con.close()

    def test_authenticateWebAppUser(self):
        global _qiime_data_access
        result = _qiime_data_access.authenticateWebAppUser('asdf', '1234')
        self.assertFalse(result)
        #user_info = result = _qiime_data_access.authenticateWebAppUser('', '')
        #self.assertTrue(type(user_info).name == 'dict')

    def test_createStudy(self):
        """ Unit test method for creating Study
        """
        global _qiime_data_access
        values = _qiime_data_access.createStudy(1,'test','Y')
        self.assertTrue(values)
        
    def test_createQueueJob(self):
        """ Unit test method for creating Queue Job
        """
        global _qiime_data_access
        values = _qiime_data_access.createQueueJob(1)
        self.assertTrue(values)

    def test_getUserStudyNames(self):
        """ Unit test method for getStudyUserNames 
        """
        global _qiime_data_access
        study_names = _qiime_data_access.getUserStudyNames(11296)
        self.assertTrue(study_names)
        
    def test_getStudyNames(self):
        """ Unit test method for getStudyNames 
        """
        global _qiime_data_access
        study_names = _qiime_data_access.getStudyNames()
        self.assertTrue(study_names)

    def test_getMetadataHeaders(self):
        """ Unit test method for getMetadataHeaders
        """
        global _qiime_data_access
        metadata_headers = _qiime_data_access.getMetadataHeaders()
        self.assertTrue(metadata_headers)

    def test_getMetadataByStudyList(self):
        """ Unit test method for getMetadataByStudyList
        """
        global _qiime_data_access
        metadata = _qiime_data_access.getMetadataByStudyList('HOST_AGE', '\'GUT\'')
        self.assertTrue(metadata)

    def test_getParameterByScript(self):
        """ Unit test method for getParameterByScript
        """
        global _qiime_data_access
        values = _qiime_data_access.getParameterByScript('\'otu_picking_method\'','\'pick_otus\'')
        self.assertTrue(values)

    def test_getColumnDictionary(self):
        """ Unit test method for getParameterByScript
        """
        global _qiime_data_access
        values = _qiime_data_access.getColumnDictionary()
        self.assertTrue(values)



if __name__ == '__main__':
	unittest.main()
