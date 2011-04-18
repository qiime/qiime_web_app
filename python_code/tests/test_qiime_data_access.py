#!/usr/bin/env python

"""
Unit tests for qiime_data_access.py
"""

import unittest
from data_access_connections import data_access_factory
from enums import ServerConfig
import datetime

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel","Jesse Stombaugh"]
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
        self._qiime_data_access = data_access_factory(
                                                ServerConfig.data_access_type)

    def tearDown(self):
        result = self._qiime_data_access.deactivateWebAppUser('test_user1313',
                                                              'calkd1579')

    # The rest of the unit tests
    
    #####################################
    # Database Connections
    #####################################

    def test_getOntologyDatabaseConnection(self):
        """ test_getOntologyDatabaseConnection: get a ontology database 
            connection.
        """
        
        con = self._qiime_data_access.getOntologyDatabaseConnection()
        self.assertTrue(con)
        
    def test_getSFFDatabaseConnection(self):
        """ test_getSFFDatabaseConnection: get a SFF database 
            connection.
        """
        
        con = self._qiime_data_access.getSFFDatabaseConnection()
        self.assertTrue(con)
    
    def test_getMetadataDatabaseConnection(self):
        """ test_getMetadataDatabaseConnection: get a metadata database 
            connection.
        """

        con = self._qiime_data_access.getMetadataDatabaseConnection()
        self.assertTrue(con)
    
    #####################################
    # Helper Functions
    #####################################
    
    def test_testDatabase(self):
        """ test_testDatabase: This function just tests a database 
            connection
        """
        result = self._qiime_data_access.testDatabase()
        self.assertTrue(result)
    
    def test_convertToOracleHappyName_DateOnly(self):
        """ test_convertToOracleHappyName_DateOnly: This converts a date to 
            an Oracle date """
        result = self._qiime_data_access.convertToOracleHappyName('11/25/1973')
        self.assertTrue(result)
        
    def test_convertToOracleHappyName_DateAndTime(self):
        """ test_convertToOracleHappyName_DateAndTime: This converts a 
            timestamp to an Oracle Timestamp"""
        result = self._qiime_data_access.convertToOracleHappyName('11/25/1973')
        self.assertTrue(result)
    
    #####################################
    # Users
    #####################################
    def test_authenticateWebAppUser(self):
        """ test_authenticateWebAppUser: Attempt to authenticate the user 
            against the list of users in
            web_app_user table. If successful, a dict with user innformation is
            returned. If not, the function returns False.
        """
        result = self._qiime_data_access.authenticateWebAppUser('test_user1313',
                                                                'calkd1579')
        self.assertTrue(result)

    def test_getUserDetails(self):
        """ test_getUserDetails: Gets the user data from the web_app_user table
        """
        result = self._qiime_data_access.getUserDetails(12173)
        exp={'is_locked': 0, 'last_login': datetime.datetime(2000, 1, 1, 1, 0), 
             'is_admin': 0, 'email': 'test_user1313'}
        self.assertEqual(result,exp)
        
    def test_verifyActivationCode(self):
        """ test_verifyActivationCode: Verify the user's activation code is 
            correct.
        """
        result = self._qiime_data_access.verifyActivationCode('test_user1313',
                                                              'calkd1579')
        self.assertTrue(result)
    
    def test_activateWebAppUser(self):
        """ test_activateWebAppUser: Attempt to activate the user account. 
            If successful, returns True. If not, the function returns False.
        """
        result = self._qiime_data_access.activateWebAppUser('test_user1313',
                                                            'calkd1579')
        self.assertTrue(result)

    def test_checkWebAppUserAvailability(self):
        """ test_checkWebAppUserAvailability: Checks the availability of the 
            supplied username
        """
        result = self._qiime_data_access.checkWebAppUserAvailability(
                                                                'test_user1313')
        self.assertFalse(result)
    
    def test_registerWebAppUser(self):
        """ test_registerWebAppUser: Attempt to register the user. If 
            successful, a dict with user innformation is
            returned. If not, the function returns False.
        """        
        result = self._qiime_data_access.registerWebAppUser('test_user1313', 
                                                        'calkd1579','calkd1579')
        
        exp={'verified': 'n', 'is_locked': 0, 'last_login': 
             datetime.datetime(2000, 1, 1, 1, 0), 'web_app_user_id': 12173, 
             'is_admin': 0, 'password': 'te/GxW0xxmgtQ', 'email': 
             'test_user1313'}
        
        self.assertEqual(result,exp)
        
    def test_updateWebAppUserPwd(self):
        """ test_updateWebAppUserPwd: Attempts to update the users password.
        """
        result = self._qiime_data_access.updateWebAppUserPwd('test_user1313','calkd1579')
        self.assertFalse(result)

    #####################################
    # Study
    #####################################
    
    def test_getSampleIDsFromStudy(self):
        """ test_getSampleIDsFromStudy:get SampleIDs from a study.
            Note: Currently using study 609 which may change
        """
        result = self._qiime_data_access.getSampleIDsFromStudy(609)

        exp=[234891, 234892, 234893, 234894, 234895, 234896, 234897,
             234889, 234890]
        self.assertEqual(result,exp)
        
    def test_createStudy(self):
        """ test_createStudy: test method for creating Study
            Note: this test encapsulates the delete study fxn as well
        """

        values = self._qiime_data_access.createStudy(1, 'test', 3, 'y', 'y',
                                                     'qiime','test','test','',
                                                     'test','test')
        self.assertTrue(values)
        values = self._qiime_data_access.deleteStudy(values, 1)

    def test_updateStudy(self):
        """ test_updateStudy: test method for updating Study
            Note: this test encapsulates the delete study fxn as well
        """

        values = self._qiime_data_access.createStudy(1, 'test', 3, 'y', 'y',
                                                     'qiime','test','test','',
                                                     'test','test')
                                                     
        values2 = self._qiime_data_access.updateStudy(values, 3, 'y', 'y',
                                                     'qiime','test2','test2','',
                                                     'test2','test2')
    
        values = self._qiime_data_access.deleteStudy(values, 1)

    def test_getStudyNames(self):
        """ test_getStudyNames: test method for getStudyNames 
        """

        study_names = self._qiime_data_access.getStudyNames()
        self.assertTrue(study_names)
        
    def test_getUserStudyNames(self):
        """ test_getUserStudyNames: test method for getStudyUserNames 
        """
        
        study_names = self._qiime_data_access.getUserStudyNames(12171,0,'qiime')
        if (609, 'jesse_test') in study_names:
            value=True
        else:
            value=False
            
        self.assertTrue(value)
        
    def test_getUserAndPublicStudyNames(self):
        """ test_getUserAndPublicStudyNames: test method for 
            getUserAndPublicStudyNames 
        """
        
        study_names = self._qiime_data_access.getUserAndPublicStudyNames(12171,
                                                                    0,'qiime')
        if (609, 'jesse_test') in study_names:
            value=True
        else:
            value=False
        
        self.assertTrue(value)

    def test_getStudyInfo(self):
        """ test_getStudyInfo: test method for getStudyInfo
        """
        
        study_info = self._qiime_data_access.getStudyInfo(609,12171)
        
        if study_info['metadata_complete']=='y' and \
                    study_info['sff_complete']=='y' and \
                    study_info['project_name']=='jesse_test':
            value=True
        else:
            value=False
        
        self.assertTrue(value)
        
    def test_getStudyPlatform(self):
        """ test_getStudyPlatform: test method for getStudyPlatform
        """
        
        platform = self._qiime_data_access.getStudyPlatform(609)
        exp='FLX'
        
        self.assertEqual(platform,exp)
        
    #####################################
    # Metadata and EMP Stuff
    #####################################
    
    def test_createEMPStudy(self):
        # needs added
        pass

    def test_updateEMPStudy(self):
        # needs added
        pass
        
    def test_createStudyPackage(self):
        # needs added
        pass
        
    def test_clearStudyPackage(self):
        # needs added
        pass
        
    def test_getStudyPackages(self):
        # needs added
        pass
        
    def test_updateMetadataFlag(self):
        # needs added
        pass
        
    def test_addSFFFile(self):
        """ test_addSFFFile: tries to add SFF, but will fail
        """
        
        result = self._qiime_data_access.addSFFFile(1, '/dev/null/my.sff')
        self.assertFalse(result)
    
    def test_addSFFFileInfo(self):
        """test_addSFFFileInfo: adds information pertaining to SFF file
        """
        
        result = self._qiime_data_access.addSFFFileInfo(False, 'my.sff',10,10,
                                                        4,100,1,10,'ACG','md5',
                                                        10)
        self.assertFalse(result)
        
        
    def test_addMappingFile(self):
        """ test_addMappingFile:adds a new mapping file to the study, but will fail due to key 
            constraint
        """
        result = self._qiime_data_access.addMappingFile(1, 
                                                        '/dev/null/mapping.txt')
                                                        
        self.assertFalse(result)
        
    def test_addTemplateFile(self):
        # needs added
        pass
        
    def test_clearStudyTemplates(self):
        # needs added
        pass
        
    def test_getEMPStudyList(self):
        # needs added
        pass
        
    def test_getEMPSampleList(self):
        # needs added
        pass
        
    def test_updateEMPSampleData(self):
        # needs added
        pass
        
    def test_updateEMPStudyData(self):
        # needs added
        pass
        
    def test_getListFieldValue(self):
        """ test_getListFieldValue: get the list field value
        """
        ###DOES NOT WORK for SOME REASON
        
        #results=self._qiime_data_access.getListFieldValue(1)
        pass
        
    def test_getSampleColumnValue(self):
        # needs added
        pass
        
    def test_getPrepColumnValue(self):
        # needs added
        pass
    
    def test_getMetadataFields(self):
        # needs added
        pass
        
    def test_getSampleList(self):
        # needs added
        pass
        
    def test_getPrepList(self):
        # needs added
        pass
        
    def test_addStudyActualColumn(self):
        # needs added
        pass
        
    def test_getStudyActualColumns(self):
        # needs added
        pass
        
    def test_findExtraColumnMatch(self):
        # needs added
        pass
        
    def test_addExtraColumnMetadata(self):
        # needs added
        pass
        
    def test_getExtraColumnMetadata(self):
        # needs added
        pass
    
    def test_deleteExtraColumnMetadata(self):
        # needs added
        pass
        
    def test_getColumnDictionary(self):
        """ test_getColumnDictionary: Returns the full column dictionary
        """
        
        values = self._qiime_data_access.getColumnDictionary()
        if ('anonymized_name', '[text], example: "subject 1"', 'Anonymized name of the subject, if applicable (e.g. deidentified subject IDs from dbGAP, deidentified subject ids from your study). Only applies to human studies, leave blank if not applicable.', 'text', 500, 0, 1) \
           and ('barcode', '[text]', 'Barcode sequence used for each pool member. Need only be unique for each combination of barcode, primer and plate region.', 'text', 500, 0, 1) \
           in values:
            result=True
        else:
            result=False
        self.assertTrue(result)

    def test_getPackageColumns(self):
        """ test_getPackageColumns: Returns the full package column dictionary
        """
        
        value = self._qiime_data_access.getPackageColumns(1)  
        if ('barometric_press', 'X', 'numeric', '[numeric value]', 'force per unit area exerted against a surface by the weight of air above that surface') \
           and ('carb_dioxide', 'X', 'numeric', '[numeric value]', 'carbon dioxide (gas) amount or concentration at the time of sampling') \
           in value:
            result=True
        else:
            result=False
        
        self.assertTrue(result)
    
    def test_findMetadataTable(self):
        # needs added
        pass
        
    def test_getFieldDetails(self):
        # needs added
        pass
    
    def test_getTableCategory(self):
        # needs added
        pass
        
    def test_createSampleKey(self):
        # needs added
        pass

    def test_createPrepKey(self):
        # needs added
        pass
        
    def test_createHostKey(self):
        # needs added
        pass

    def test_handleExtraData(self):
        # needs added
        pass

    def test_writeMetadataValue(self):
        # needs added
        pass
        
    #####################################
    # Jobs
    #####################################
    def test_createTorqueJob(self):
        """ test_createTorqueJob: submits a job to the queue and returns the 
            job_id. Note: this also performs the clear torque job
        """
        job_id = self._qiime_data_access.createTorqueJob('poller_test_1','',
                                                          12173,1,2)
        self.assertTrue(job_id>0)
        
        #Remove the torque job
        self._qiime_data_access.clearTorqueJob(job_id)

    def test_updateTorqueJob(self):
        """ test_updateTorqueJob: updates a torque job and returns the 
            job_id. Note: this also performs the clear torque job
        """
        job_id = self._qiime_data_access.createTorqueJob('poller_test_1','',
                                                          12173,1,2)
        self.assertTrue(job_id>0)
        
        new_job_id = self._qiime_data_access.updateTorqueJob(job_id,'QIIME_HOLD','')

        self.assertTrue(new_job_id>0)
        
        #Remove the torque job
        self._qiime_data_access.clearTorqueJob(new_job_id)
    
    def test_getJobInfo(self):
        """ test_getJobInfo: returns job information
        """
        results = self._qiime_data_access.getJobInfo(0,2)
        self.assertEqual(results,[])
        
        
    #####################################
    # Ontologies
    #####################################
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
    
    def test_loadOTUInfo(self):
        """ 
        """

        result = self._qiime_data_access.loadAllOTUInfo(False,1,1,1,1,1,1,1,1,'test', 97)
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

    #
    def test_loadOTUFailuresAll(self):
        """ 
        """
        
        result = self._qiime_data_access.loadOTUFailuresAll(False,1)
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

    def test_getOTUGG97Taxonomy(self):
        """
        """
        result=self._qiime_data_access.getOTUGG97Taxonomy(0,'test')
        self.assertFalse(result)
    
    #
    def test_getQiimeSffSamples(self):
        """
        """
        
        result=self._qiime_data_access.getQiimeSffSamples(0,0)
        for exp in result:
            self.assertEqual(exp,None)
    #
    def test_getQiimeSffReadCounts(self):
        """
        """
        result=self._qiime_data_access.getQiimeSffReadCounts(0)
        for exp in result:
            self.assertEqual(exp[0],0)
    #
    def test_getQiimeSffSamplesCount(self):
        """
        """
        result=self._qiime_data_access.getQiimeSffSamplesCount('test')
        self.assertEqual(result[1],0)
    #
    def test_getQiimeSffDbSummary(self):
        """
        """
        
        result=self._qiime_data_access.getQiimeSffDbSummary(0)
        for exp in result:
            self.assertEqual(exp,None)
            
    #
    def test_loadBetaDivDistances(self):
        """
        """
        
        result=self._qiime_data_access.loadBetaDivDistances(0,'test')
        self.assertEqual(result,None)
    #
    def test_loadOTUTable(self):
        """
        """
        
        result=self._qiime_data_access.loadOTUTable(0,'test')
        self.assertEqual(result,None)
            
            
if __name__ == '__main__':
	unittest.main()
