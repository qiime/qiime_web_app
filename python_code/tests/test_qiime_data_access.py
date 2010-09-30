#!/usr/bin/env python

"""
Unit tests for qiime_data_access.py
"""

import unittest
from data_access_connections import data_access_factory
from enums import DataAccessType

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

    # Variables required for all tests
    _qiime_data_access = None

    # Set up and tear downdown
    def setUp(self):
        self._qiime_data_access = data_access_factory(DataAccessType.qiime_production)

    def tearDown(self):
        result = self._qiime_data_access.deactivateWebAppUser('test_user1313', 'calkd1579')

    # The rest of the unit tests
    
    #These two functions are first, because they create a test user acct.
    def test_registerWebAppUser(self):        
        result = self._qiime_data_access.registerWebAppUser('test_user1313', 'calkd1579','calkd1579')
        self.assertFalse(result)

    def test_activateWebAppUser(self):
        result = self._qiime_data_access.activateWebAppUser('test_user1313', 'calkd1579')
        self.assertTrue(result)

    def test_verifyActivationCode(self):
        result = self._qiime_data_access.verifyActivationCode('test_user1313', 'calkd1579')
        self.assertTrue(result)
        
    def test_updateWebAppUserPwd(self):
        
        result = self._qiime_data_access.updateWebAppUserPwd('test_user1313','calkd1579')
        self.assertFalse(result)
    #####
    
    def test_getDatabaseConnection(self):
        
        con = self._qiime_data_access.getDatabaseConnection()
        self.assertTrue(con)\

    def test_getWebAppUserDatabaseConnection(self):
        
        con = self._qiime_data_access.getWebAppUserDatabaseConnection()
        self.assertTrue(con)

    def test_getOntologyDatabaseConnection(self):
        
        con = self._qiime_data_access.getOntologyDatabaseConnection()
        self.assertTrue(con)
        
    def test_getSFFDatabaseConnection(self):
        
        con = self._qiime_data_access.getSFFDatabaseConnection()
        self.assertTrue(con)

    def test_authenticateWebAppUser(self):
        
        result = self._qiime_data_access.authenticateWebAppUser('test_user1313', 'calkd1579')
        self.assertTrue(result)
        #user_info = result = self._qiime_data_access.authenticateWebAppUser('', '')
        #self.assertTrue(type(user_info).name == 'dict')
        
    def test_checkWebAppUserAvailability(self):
        
        result = self._qiime_data_access.checkWebAppUserAvailability('test_user1313')
        self.assertFalse(result)
        
    def test_createStudy(self):
        """ Unit test method for creating Study
        """

        values = self._qiime_data_access.createStudy(1, 'test', 3, 'y', 'y')
        self.assertTrue(values)

    '''
    def test_createQueueJob(self):
        """ Unit test method for creating Queue Job
        """
        
        values = self._qiime_data_access.createQueueJob(1,1,0,'/tmp/')
        self.assertTrue(values)
    '''

    def test_getUserStudyNames(self):
        """ Unit test method for getStudyUserNames 
        """
        
        study_names = self._qiime_data_access.getUserStudyNames(12169)
        self.assertTrue(study_names)
        
    def test_getStudyNames(self):
        """ Unit test method for getStudyNames 
        """
        
        study_names = self._qiime_data_access.getStudyNames()
        self.assertTrue(study_names)

    '''
    def test_getMetadataHeaders(self):
        """ Unit test method for getMetadataHeaders
        """
        
        metadata_headers = self._qiime_data_access.getMetadataHeaders()
        self.assertTrue(metadata_headers)
    '''

    '''
    def test_getMetadataByStudyList(self):
        """ Unit test method for getMetadataByStudyList
        """
        
        metadata = self._qiime_data_access.getMetadataByStudyList('HOST_AGE', '\'GUT\'')
        self.assertTrue(metadata)

    def test_getParameterByScript(self):
        """ Unit test method for getParameterByScript
        """
        
        values = self._qiime_data_access.getParameterByScript('\'otu_picking_method\'','\'pick_otus\'')
        self.assertTrue(values)
    '''

    def test_getColumnDictionary(self):
        """ 
        """
        
        values = self._qiime_data_access.getColumnDictionary()
        self.assertTrue(values)

    def test_getControlledVocabs(self):
        """ 
        """
        
        controlled_vocab_list = self._qiime_data_access.getControlledVocabs('investigation_type')
        self.assertTrue(controlled_vocab_list[0] == 'Investigation Type')

    def test_getOntologies(self):
        """ 
        """
        
        controlled_vocab_list = self._qiime_data_access.getOntologies('body_habitat')
        self.assertTrue(controlled_vocab_list[0] == 'FMA')

    def test_getListValues(self):
        """ 
        """
        
        result = self._qiime_data_access.getListValues('Investigation Type')
        self.assertTrue(result)

    def test_validateListValue(self):
        """ 
        """
        
        result = self._qiime_data_access.validateListValue('Investigation Type', 'eukaryote')
        self.assertTrue(result > 0)

    def test_getOntologyValues(self):
        """ 
        """
        
        result = self._qiime_data_access.getOntologyValues('CL')
        self.assertTrue(result)

    def test_validateOntologyValue(self):
        """ 
        """
        
        result = self._qiime_data_access.validateOntologyValue('FMA', 'Hand')
        self.assertTrue(result > 0)

    def test_getControlledVocabValueList(self):
        """ 
        """
        
        result = self._qiime_data_access.getControlledVocabValueList(1)
        self.assertTrue(result)

    def test_getControlledVocabValueList(self):
        """ 
        """
        
        result = self._qiime_data_access.getPackageColumns(1)
        self.assertTrue(result)

    '''
    def test_disableTableConstraints(self):
        """ 
        """
        exp_run_id=True
        
        obs_run_id = self._qiime_data_access.disableTableConstraints()
        self.assertEqual(obs_run_id,exp_run_id)
    
    def test_enableTableConstraints(self):
        """ 
        """
        exp_run_id=True
        
        obs_run_id = self._qiime_data_access.enable_table_constraints(1)
        self.assertEqual(obs_run_id,exp_run_id)
    '''         

    def test_loadSplitLibFasta(self):
        """ 
        """
        
        result = self._qiime_data_access.loadSplitLibFasta(False,0,'seqs.fna')
        self.assertTrue(result)
        
    def test_loadSplitLibInfo(self):
        """ 
        """
        
        result = self._qiime_data_access.loadSplitLibInfo(False,1,1,1,1,1,1,1)
        self.assertTrue(result)
        
    def test_getTestData(self):
        """ 
        """
        
        result = self._qiime_data_access.getTestData(False,1,'test')
        self.assertTrue(result)
        
    def test_deleteTestAnalysis(self):
        """ 
        """
        
        result = self._qiime_data_access.deleteTestAnalysis(False,1)
        self.assertTrue(result)
    
    def test_loadOTUInfo(self):
        """ 
        """

        result = self._qiime_data_access.loadOTUInfo(False,1,1,1,1,1,1,1,1,1,'test', 97)
        self.assertTrue(result)
        
    def test_getTestFlowData(self):
        """ 
        """
        
        result = self._qiime_data_access.getTestFlowData(False,1,'test')
        self.assertTrue(result)
    #
    def test_getTestSplitLibData(self):
        """ 
        """
        
        result = self._qiime_data_access.getTestSplitLibData(False,1,'test')
        self.assertTrue(result)
    #
    def test_getTestOTUData(self):
        """ 
        """
        
        result = self._qiime_data_access.getTestOTUData(False,1,'test')
        self.assertTrue(result)
    #
    def test_getTestOTUFailureData(self):
        """ 
        """
        
        result = self._qiime_data_access.getTestOTUFailureData(False,1,'test')
        self.assertTrue(result)
    #
    def test_loadOTUFailures(self):
        """ 
        """
        
        result = self._qiime_data_access.loadOTUFailures(False,1)
        self.assertFalse(result)

    def test_checkIfSFFExists(self):
        """ 
        """
        
        result = self._qiime_data_access.checkIfSFFExists('test')
        self.assertFalse(result)
    #
    
    def test_getSeqRunIDUsingMD5(self):
        """ 
        """
        
        result = self._qiime_data_access.getSeqRunIDUsingMD5('test')
        self.assertFalse(result)

    def test_createAnalysis(self):
        """ 
        """
        
        #result = self._qiime_data_access.createAnalysis()
        #self.assertFalse(result)
    #
    def test_addSFFFile(self):
        """ 
        """
        
        result = self._qiime_data_access.addSFFFile(1, '/dev/null/my.sff')
        self.assertFalse(result)
    #
    def test_createSequencingRun(self):
        """ 
        """
        
        result = self._qiime_data_access.createSequencingRun(False,'test','1',1)
        self.assertFalse(result)
        
    #
    def test_loadSFFData(self):
        """ 
        """
        
        result = self._qiime_data_access.loadSFFData(False,'Test')
        self.assertFalse(result)
    #
    def test_updateAnalysisWithSeqRunID(self):
        """ 
        """
        
        result = self._qiime_data_access.updateAnalysisWithSeqRunID(False,1,1)
        self.assertFalse(result)
    #
    def test_loadOTUMap(self):
        """ 
        """
        
        result = self._qiime_data_access.loadOTUMap(False,1)
        self.assertFalse(result) 
    #
    def test_loadSeqToSourceMap(self):
        """ 
        """
        
        result = self._qiime_data_access.loadSeqToSourceMap(False,1)
        self.assertFalse(result)

    def test_convertToOracleHappyName_DateOnly(self):
        """ 
        """
        result = self._qiime_data_access.convertToOracleHappyName('11/25/1973')
        self.assertTrue(result)
        
    def test_convertToOracleHappyName_DateAndTime(self):
        """ 
        """
        result = self._qiime_data_access.convertToOracleHappyName('11/25/1973')
        self.assertTrue(result)


        
if __name__ == '__main__':
	unittest.main()
