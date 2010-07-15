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
    
    #These two functions are first, because they create a test user acct.
    def test_registerWebAppUser(self):
        global _qiime_data_access
        result = _qiime_data_access.registerWebAppUser('test_user1313', 'calkd1579','calkd1579')
        self.assertFalse(result)

    def test_deactivateWebAppUser(self):
        global _qiime_data_access
        result = _qiime_data_access.deactivateWebAppUser('test_user1313', 'calkd1579')
        self.assertTrue(result)

    def test_activateWebAppUser(self):
        global _qiime_data_access
        result = _qiime_data_access.activateWebAppUser('test_user1313', 'calkd1579')
        self.assertTrue(result)

    def test_verifyActivationCode(self):
        global _qiime_data_access
        result = _qiime_data_access.verifyActivationCode('test_user1313', 'calkd1579')
        self.assertTrue(result)
        
    def test_updateWebAppUserPwd(self):
        global _qiime_data_access
        result = _qiime_data_access.updateWebAppUserPwd('test_user1313','calkd1579')
        self.assertFalse(result)
    #####
    
    def test_getDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getDatabaseConnection()
        self.assertTrue(con)\

    def test_getWebAppUserDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getWebAppUserDatabaseConnection()
        self.assertTrue(con)

    def test_getOntologyDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getOntologyDatabaseConnection()
        self.assertTrue(con)

    def test_getTestDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getTestDatabaseConnection()
        self.assertTrue(con)
        
    def test_getSFFDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getSFFDatabaseConnection()
        self.assertTrue(con)

    def test_getTestDatabaseConnection(self):
        global _qiime_data_access
        con = _qiime_data_access.getTestDatabaseConnection()
        self.assertTrue(con)

    def test_authenticateWebAppUser(self):
        global _qiime_data_access
        result = _qiime_data_access.authenticateWebAppUser('test_user1313', 'calkd1579')
        self.assertTrue(result)
        #user_info = result = _qiime_data_access.authenticateWebAppUser('', '')
        #self.assertTrue(type(user_info).name == 'dict')
        
    def test_checkWebAppUserAvailability(self):
        global _qiime_data_access
        result = _qiime_data_access.checkWebAppUserAvailability('test_user1313')
        self.assertFalse(result)
        
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
        values = _qiime_data_access.createQueueJob(1,1,0,'/tmp/')
        self.assertTrue(values)

    def test_getUserStudyNames(self):
        """ Unit test method for getStudyUserNames 
        """
        global _qiime_data_access
        con = _qiime_data_access.getDatabaseConnection()
        study_names = con.getUserStudyNames(11296)
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
        """ 
        """
        global _qiime_data_access
        values = _qiime_data_access.getColumnDictionary()
        self.assertTrue(values)

    def test_getControlledVocabs(self):
        """ 
        """
        global _qiime_data_access
        controlled_vocab_list = _qiime_data_access.getControlledVocabs('investigation_type')
        self.assertTrue(controlled_vocab_list[0] == 'Investigation Type')

    def test_getOntologies(self):
        """ 
        """
        global _qiime_data_access
        controlled_vocab_list = _qiime_data_access.getOntologies('body_habitat')
        self.assertTrue(controlled_vocab_list[0] == 'FMA')

    def test_getListValues(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.getListValues('Investigation Type')
        self.assertTrue(result)

    def test_validateListValue(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.validateListValue('Investigation Type', 'eukaryote')
        self.assertTrue(result > 0)

    def test_getOntologyValues(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.getOntologyValues('CL')
        self.assertTrue(result)

    def test_validateOntologyValue(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.validateOntologyValue('FMA', 'FMA:86707')
        self.assertTrue(result > 0)

    def test_getControlledVocabValueList(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.getControlledVocabValueList(1)
        self.assertTrue(result)

    def test_getControlledVocabValueList(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.getPackageColumns(1)
        self.assertTrue(result)

    def test_disableTableConstraints(self):
        """ 
        """
        exp_run_id=True
        global _qiime_data_access
        obs_run_id = _qiime_data_access.disableTableConstraints()
        self.assertEqual(obs_run_id,exp_run_id)
    
    '''
    def test_enableTableConstraints(self):
        """ 
        """
        exp_run_id=True
        global _qiime_data_access
        obs_run_id = _qiime_data_access.enable_table_constraints(1)
        self.assertEqual(obs_run_id,exp_run_id)
    '''
                    
    def test_loadSFFData(self):
        """ 
        """
        exp_run_id=0
        global _qiime_data_access
        result,obs_run_id,analysis_id = _qiime_data_access.loadSFFData(False,\
                                            'Test',0,0,0,'')
        self.assertEqual(obs_run_id,exp_run_id)
        self.assertTrue(result)

    def test_loadSplitLibFasta(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.loadSplitLibFasta(False,0,'seqs.fna')
        self.assertTrue(result)
        
    def test_loadSplitLibInfo(self):
        """ 
        """
        global _qiime_data_access
        result = _qiime_data_access.loadSplitLibInfo(False,1,1,1,1,1,1,1)
        self.assertTrue(result)

if __name__ == '__main__':
	unittest.main()
