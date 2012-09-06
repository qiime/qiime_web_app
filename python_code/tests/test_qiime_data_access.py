#!/usr/bin/env python

"""
Unit tests for qiime_data_access.py
"""

import unittest
from cogent.util.unit_test import TestCase, main
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
        self._qiime_data_access = None
        
        
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
    def test_registerWebAppUser(self):
        """ test_registerWebAppUser: Attempt to register the user. If 
            successful, a dict with user innformation is
            returned. If not, the function returns False.
        """        
        result = self._qiime_data_access.registerWebAppUser('test_user1313', 
                                                        'calkd1579','calkd1579')
        
        exp={'verified': 'n', 'is_locked': 0, 'last_login': 
             datetime.datetime(2000, 1, 1, 1, 0), 'web_app_user_id': 12423, 
             'is_admin': 0, 'password': 'te/GxW0xxmgtQ', 'email': 
             'test_user1313'}
        
        self.assertEqual(result['email'],exp['email'])
    
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
        result = self._qiime_data_access.getUserDetails(12423)
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
            Note: Currently using study 0 which may change
        """
        result = self._qiime_data_access.getSampleIDsFromStudy(0)

        self.assertEqual(len(result),9)
        
    def test_createStudy(self):
        """ test_createStudy: test method for creating Study
            Note: this test encapsulates the delete study fxn as well
        """

        values = self._qiime_data_access.createStudy(1, 'test', 3, 'y', 'y',
                                                     'qiime','test_title',
                                                     'test_alias','',
                                                     'test_abstract',
                                                     'test_desc','test_pi',
                                                     'test_pi_con','test_lab',
                                                     'test_lab_con',0)
        self.assertTrue(values)
        values = self._qiime_data_access.deleteStudy(values, 2)

    def test_updateStudy(self):
        """ test_updateStudy: test method for updating Study
            Note: this test encapsulates the delete study fxn as well
        """

        values = self._qiime_data_access.createStudy(1, 'test', 3, 'y', 'y',
                                                     'qiime','test_title',
                                                     'test_alias','',
                                                     'test_abstract',
                                                     'test_desc','test_pi',
                                                     'test_pi_con','test_lab',
                                                     'test_lab_con',0)
                                                     
        values2 = self._qiime_data_access.updateStudy(values, 3, 'y', 'y',
                                                     'qiime','test2','test2','',
                                                     'test2','test2','test2',
                                                      'test2','test2','test2',
                                                      False,0)
    
        values = self._qiime_data_access.deleteStudy(values, 2)

    def test_getStudyNames(self):
        """ test_getStudyNames: test method for getStudyNames 
        """

        study_names = self._qiime_data_access.getStudyNames()
        self.assertTrue(study_names)
        
    def test_getUserStudyNames(self):
        """ test_getUserStudyNames: test method for getStudyUserNames 
        """
        
        study_names = self._qiime_data_access.getUserStudyNames(12171,0,'qiime')
            
        self.assertTrue(len(study_names)>0)
        
    def test_getUserAndPublicStudyNames(self):
        """ test_getUserAndPublicStudyNames: test method for 
            getUserAndPublicStudyNames 
        """
        
        study_names = self._qiime_data_access.getUserAndPublicStudyNames(12171,
                                                                    0,'qiime')
        
        self.assertTrue(len(study_names)>0)

    def test_getStudyInfo(self):
        """ test_getStudyInfo: test method for getStudyInfo
        """
        
        study_info = self._qiime_data_access.getStudyInfo(0,12171)
        
        if study_info['metadata_complete']=='y' and \
                    study_info['sff_complete']=='y' and \
                    study_info['project_name']=='study_0':
            value=True
        else:
            value=False

        self.assertTrue(value)
        
    def test_getStudyPlatform(self):
        """ test_getStudyPlatform: test method for getStudyPlatform
        """
        
        platform = self._qiime_data_access.getStudyPlatform(0)
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
        
    def test_addSeqFile(self):
        """ test_addSeqFile: tries to add SFF, but will fail
        """
        
        result = self._qiime_data_access.addSeqFile(1, '/dev/null/my.sff','SFF')
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
                                                          12423,1,2)
        self.assertTrue(job_id>0)
        
        #Remove the torque job
        self._qiime_data_access.clearTorqueJob(job_id)

    def test_updateTorqueJob(self):
        """ test_updateTorqueJob: updates a torque job and returns the 
            job_id. Note: this also performs the clear torque job
        """
        job_id = self._qiime_data_access.createTorqueJob('poller_test_1','',
                                                          12423,1,2)
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
        """ test_getControlledVocabs: Returns the controlled vocabularies
        """
        
        controlled_vocab_list = self._qiime_data_access.getControlledVocabs('investigation_type')
        self.assertTrue(controlled_vocab_list[0] == 'Investigation Type')

    def test_getControlledVocabValueList(self):
        """ test_getControlledVocabValueList: Returns the controlled 
            vocabulary values
        """

        result = self._qiime_data_access.getControlledVocabValueList(1)
        if result[1]=='air' and result[2]=='host-associated' \
            and result[3]=='human-associated' in result:
            value=True
        else:
            value=False

        self.assertTrue(result)
        
    def test_getOntologies(self):
        """ test_getOntologies: Returns a list of Ontologies
        """
        
        ontology = self._qiime_data_access.getOntologies('body_habitat')
        self.assertTrue(ontology[0] == 'UBERON')

    def test_getListValues(self):
        """ test_getListValues: Returns list values
        """
        
        result = self._qiime_data_access.getListValues('Investigation Type')
        
        self.assertTrue(result)
        
        if (18, 'eukaryote') and (19, 'bacteria_archaea') and (20, 'plasmid') \
           in result:
            value=True
        else: 
            value=False
        
        self.assertTrue(value)

    def test_validateListValue(self):
        """ test_validateListValue: validates a list value
        """
        
        result = self._qiime_data_access.validateListValue('Investigation Type',
                                                           'eukaryote')
        self.assertTrue(result > 0)

    def test_getOntologyValues(self):
        """ test_getOntologyValues: Returns ontology values
        """
        
        result = self._qiime_data_access.getOntologyValues('CL')
        self.assertTrue(result)

    def test_validateOntologyValue(self):
        """ test_validateOntologyValue: validates an ontology value
        """
        
        result = self._qiime_data_access.validateOntologyValue('FMA', 'Hand')
        self.assertTrue(result > 0)


    def test_getTermMatches(self):
        """ test_getTermMatches: Finds close term matches for columns of type 
            ontology or list
        """
        result = self._qiime_data_access.getTermMatches('body_habitat', 
                                     'UBERON:metacarpal bone of hand digit 1')
        self.assertTrue(result==['UBERON:metacarpal bone of hand digit 1'])


    def test_get_list_of_ontologies(self):
        """ test_get_list_of_ontologies: Returns a list of metadata values 
            based on a study type and list
        """
        result = self._qiime_data_access.get_list_of_ontologies()
        self.assertTrue(result)
        
        if (885934180, 'AAO', 'Amphibian Gross Anatomy') and \
           (607506283, 'BS', 'Biosapiens Annotations') in result:
            value=True
        else:
            value=False
            
        self.assertTrue(value)
        
    def test_get_ontology_terms(self):
        """ test_get_ontology_terms: Returns a list of ontology terms if the 
            term contains query as a substring.
        """
        result = self._qiime_data_access.get_ontology_terms('\'UBERON\'',
                                    'METACARPAL BONE OF HAND DIGIT 1')
        self.assertTrue(result==['UBERON:metacarpal bone of hand digit 1'])
        
    def test_validity_of_ontology_term(self):
        """ test_validity_of_ontology_term: Returns a list of ontology terms 
            if the query is exactly equal to the term.
        """
        result = self._qiime_data_access.validity_of_ontology_term('\'UBERON\'',
                                    '\'HAND\'')
        self.assertTrue(result==['hand'])
        
    #####################################
    # Loading
    #####################################
        
    def test_getSFFFiles(self):
        """ test_getSFFFiles: Gets a list of SFF files for this study
        """
        
        result = self._qiime_data_access.getSFFFiles(0)
        self.assertTrue(result==['/home/wwwdevuser/user_data/studies/study_0/Fasting_subset.sff'])
    
    
    def test_getMappingFiles(self):
        """ test_getSFFFiles: Gets a list of metadata files for this study
        """
        
        result = self._qiime_data_access.getMappingFiles(0)
        self.assertTrue(result==['/home/wwwdevuser/user_data/studies/study_0/mapping_files/Fasting_subset__split_libraries_mapping_file.txt'])
    
    def test_getStudyTemplates(self):
        """ test_getStudyTemplates: Gets a list of study template files for 
            this study
        """
        
        result = self._qiime_data_access.getStudyTemplates(0)
        self.assertTrue(result)

    def test_getSplitLibrariesMappingFileData(self):
        """ test_getSplitLibrariesMappingFileData: Gets a list of sff and 
            mapping files for study
        """
        
        result = self._qiime_data_access.getSplitLibrariesMappingFileData(0)
        self.assertTrue(result)
        
    def test_clearSplitLibrariesMappingFiles(self):
        # needs added - tricky since we don't want to delete data
        pass
        
    def test_checkRunPrefixBarcodeLengths(self):
        """ test_checkRunPrefixBarcodeLengths: Checks to make sure all barcode
            lengths are the same for a given run_prefix
        """
        
        result = self._qiime_data_access.checkRunPrefixBarcodeLengths(0,
                                                            'Fasting_subset')
        self.assertTrue(result==12)
    
    def test_clearMetaFiles(self):
        # needs added - tricky since we don't want to delete data
        pass
    
    def test_clearSFFFile(self):
        # needs added - tricky since we don't want to delete data
        pass
        
    def test_loadSplitLibInfo(self):
        """ test_loadSplitLibInfo: uploads the information related to the 
            split_libraries run to the DB
        """
        
        result = self._qiime_data_access.loadSplitLibInfo(False,1,1,1,1,1,1,1)
        self.assertTrue(result[0])
    
    def test_loadAllOTUInfo(self):
        """ test_loadAllOTUInfo: loads the information pertaining to an OTU 
            picking runs
        """
        
        result = self._qiime_data_access.loadAllOTUInfo(False,1,1/1/2000,
                                                        'UCLUST_REF',97,1,
                                                        'test','test','md5',
                                                        'gg_97',97,1)
        self.assertTrue(result[0])
    
    def test_getTestFlowData(self):
        """ test_getTestFlowData: Returns the FLOW TEST Data from DB
        """
        
        result = self._qiime_data_access.getTestFlowData(False,1,'test')
        self.assertTrue(result)

    def test_getTestSplitLibData(self):
        """ test_getTestSplitLibData: Returns the SPLIT_LIBRARY TEST Data
        """
        
        result = self._qiime_data_access.getTestSplitLibData(False,1,'test')
        self.assertTrue(result)
    
    def test_getTestOTUData(self):
        """ test_getTestOTUData: Returns the OTU TEST DATA
        """
        
        result = self._qiime_data_access.getTestOTUData(False,1,'test')
        self.assertTrue(result)
    
    def test_getTestOTUFailureData(self):
        """ test_getTestOTUFailureData: Returns the OTU FAILURE TEST DATA
        """
        
        result = self._qiime_data_access.getTestOTUFailureData(False,1,'test')
        self.assertTrue(result)
    
    def test_deleteTestAnalysis(self):
        """ test_deleteTestAnalysis: Removes rows from the DB given an 
            analysis id
        """
        
        result = self._qiime_data_access.deleteTestAnalysis(False,1)
        self.assertTrue(result)
    
    def test_loadOTUFailuresAll(self):
        """ test_loadOTUFailuresAll: starts process of importing failed otus
        """
        
        result = self._qiime_data_access.loadOTUFailuresAll(False,1)
        self.assertFalse(result)
        
    def test_checkIfSFFExists(self):
        """ test_checkIfSFFExists: determine if the SFF is already in the DB
        """
        
        result = self._qiime_data_access.checkIfSFFExists('314f4000857668d45a413d2e94a755fc')
        self.assertTrue(result)
    
    def test_getSeqRunIDUsingMD5(self):
        """ test_getSeqRunIDUsingMD5: returns the SEQ_RUN_ID given an 
            md5_checksum
        """
        
        result = self._qiime_data_access.getSeqRunIDUsingMD5('314f4000857668d45a413d2e94a755fc')
        self.assertTrue(result>0)

    def test_createAnalysis(self):
        """ test_createAnalysis: creates a row in the ANALYSIS table 
            Difficult to test since adds to table
        """
        
        pass
        
    def test_createSequencingRun(self):
        """ test_createSequencingRun: creates a row in the sequencing_run table
        """
        
        result = self._qiime_data_access.createSequencingRun(False,'test','1',1)
        self.assertFalse(result)
        
    
    def test_loadSFFData(self):
        """ test_loadSFFData: loads the flow data into the READ_454 table
        """
        
        result = self._qiime_data_access.loadSFFData(False,'Test')
        self.assertFalse(result)
    
    def test_loadFNAFile(self):
        """ test_loadFNAFile: starts process of importing fna file data
        """
        
        result = self._qiime_data_access.loadFNAFile(False,'Test')
        self.assertFalse(result)
        
    def test_updateAnalysisWithSeqRunID(self):
        """ test_updateAnalysisWithSeqRunID: updates the ANALYSIS table with 
            the SEQ_RUN_ID
        """
        
        result = self._qiime_data_access.updateAnalysisWithSeqRunID(False,1,1)
        self.assertFalse(result)

    def test_loadOTUMapAll(self):
        """ test_loadOTUMapAll: starts process of importing otus
        """
        
        result = self._qiime_data_access.loadOTUMapAll(False,1)
        self.assertFalse(result) 
    
    def test_loadSeqToSourceMap(self):
        """ test_loadSeqToSourceMap: loads the sequence to source map...for 
            greengenes seqs
        """
        
        result = self._qiime_data_access.loadSeqToSourceMap(False,1)
        self.assertFalse(result)

    def test_getOTUTable(self):
        """ test_getOTUTable: Gets a list otus for a samples
        """
        
        result=self._qiime_data_access.getOTUTable(False,'sample1','UCLUST_REF',
                                                   97,'GREENGENES_REFERENCE',97)
        self.assertFalse(result)
    
    def test_checkIfStudyIdExists(self):
        """ test_checkIfStudyIdExists: Check if the study id already exists
        """
        
        result=self._qiime_data_access.checkIfStudyIdExists(0)
        self.assertTrue(result)
        
        
    def test_checkIfColumnControlledVocab(self):
        """ test_checkIfColumnControlledVocab: checks if column is a 
            controlled column
        """
        result=self._qiime_data_access.checkIfColumnControlledVocab('SEX')
        self.assertTrue(result)
        
    def test_getValidControlledVocabTerms(self):
        """ test_getValidControlledVocabTerms: get controlled vocab values
        """
        result=self._qiime_data_access.getValidControlledVocabTerms('SEX')
        if (47,'male') in result:
            value=True
        else:
            value=False
        self.assertTrue(value)
        
    def test_getPublicColumns(self):
        """ test_getPublicColumns: get public columns for specified user
        """
        result=self._qiime_data_access.getPublicColumns('0')
        self.assertFalse(result)

    def test_getFieldReferenceInfo(self):
        """ test_getFieldReferenceInfo: get public columns for specified user
        """
        result=self._qiime_data_access.getFieldReferenceInfo('SEX')
        self.assertTrue(result==[('list', '[male/female/neuter/hermaphrodite/not determined]', 'physical sex of the host')])

    def test_loadBetaDivDistances(self):
        """ test_loadBetaDivDistances: loads beta-diversity distances
        """
        
        result=self._qiime_data_access.loadBetaDivDistances(0,'test')
        self.assertEqual(result,None)

    def test_loadOTUTable(self):
        """ test_loadOTUTable: loads the OTU table
        """
        
        result=self._qiime_data_access.loadOTUTable(0,'test')
        self.assertEqual(result,None)
        
    def test_getBetaDivDistances(self):
        """ test_getBetaDivDistances: gets the beta-div distance for 2 samples
        """
        
        result=self._qiime_data_access.getBetaDivDistances(0,'s1','s2',
                                                           'weighted_unifrac',0)
        self.assertEqual(result,None)
    
    def test_getBetaDivDistancesArray(self):
        """ test_getBetaDivDistancesArray: gets the beta-div distance for 
            2 samples as array
        """
        
        result=self._qiime_data_access.getBetaDivDistancesArray(0,['','','',''])
        self.assertEqual(result,None)
        
    def test_getFoundOTUArray(self):
        """ test_getFoundOTUArray: Gets a list of found OTU ids based on a list 
            of input sequence MD5s
        """
        
        result=self._qiime_data_access.getFoundOTUArray([''])
        self.assertEqual(result,[[''], [None], [None]])
        
    def test_getQiimeSffSamples(self):
        """ test_getQiimeSffSamples: Gets a list of SFF samples
        """
        
        result=self._qiime_data_access.getQiimeSffSamples(0,0)
        for exp in result:
            self.assertEqual(exp,None)
    
    def test_getQiimeSffReadCounts(self):
        """ test_getQiimeSffReadCounts: Gets the read counts for a sequencing 
            run
        """
        result=self._qiime_data_access.getQiimeSffReadCounts(0)
        for exp in result:
            self.assertEqual(exp[0],0)
    
    def test_getQiimeSffSamplesCount(self):
        """ test_getQiimeSffSamplesCount: Gets the sample count
        """
        result=self._qiime_data_access.getQiimeSffSamplesCount('test')
        self.assertEqual(result[1],0)
    
    def test_getQiimeSffDbSummary(self):
        """ test_getQiimeSffDbSummary: Gets the summary info for an SFF
        """
        
        result=self._qiime_data_access.getQiimeSffDbSummary(0)
        for exp in result:
            self.assertEqual(exp,(0, 'study_0', 'study_0', 'study_0', None))
            
    def test_getGGTaxonomy(self):
        """ test_getGGTaxonomy: gets the gg taxonomy for a prokmsa
        """
        
        result=self._qiime_data_access.getGGTaxonomy(True,1111,'RDP_tax_string')
        exp='Archaea; Crenarchaeota; Thermoprotei; unclassified_Thermoprotei'
        self.assertEqual(result,exp)

    #####################################
    # Meta-Analysis
    #####################################
    def test_addMetaAnalysisFiles(self):
        """ test_addMetaAnalysisFiles: add meta-analysis files
        """
        
        result=self._qiime_data_access.addMetaAnalysisFiles(False,1,'','ARARE',
                                                            '1/1/2000','TXT')
        self.assertTrue(result)
            
    def test_getMetaAnalysisFilepaths(self):
        """ test_getMetaAnalysisFilepaths: gets meta-analysis files
        """
        
        result=self._qiime_data_access.getMetaAnalysisFilepaths(1)
        self.assertFalse(result)
        
    def test_createMetaAnalysis(self):
        """ test_createMetaAnalysis: creates a meta-analysis
            NOTE: this will create a row in the table so may not be useful to 
            test
        """
        
        pass
        
    def test_getMetaAnalysisNames(self):
        """ test_getMetaAnalysisNames: Returns a list of meta-analysis names
        """
        
        result=self._qiime_data_access.getMetaAnalysisNames(12423)
        self.assertFalse(result)

    #####################################
    # MG-RAST Stuff
    #####################################
    
    def test_getSequencesFullDatabase(self):
        """ test_getSequencesFullDatabase: Returns a list of all sequences in DB
        """
        
        result=self._qiime_data_access.getSequencesFullDatabase()
        self.assertTrue(result)
    
    def test_getSequencesFromSample(self):
        """ test_getSequencesFromSample: Returns a list of seqs for a given 
            sample
        """
        
        result=self._qiime_data_access.getSequencesFromSample(0,0)
        self.assertFalse(result)
    #
    def test_getAllSampleFields(self):
        """ test_getAllSampleFields: Finds all filled in sample fields for a 
            given sample_id
        """
        
        result=self._qiime_data_access.getAllSampleFields(0,0)
        self.assertFalse(result)
        
if __name__ == '__main__':
	main()
