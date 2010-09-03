
"""
Centralized database access for the Qiime web app
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

import cx_Oracle
from crypt import crypt
from data_access import AbstractDataAccess
from threading import Lock
from time import sleep

class QiimeDataAccess( AbstractDataAccess ):
    """
    The actual implementation
    """
    
    #####################################
    # Connections
    #####################################
    
    def __init__(self):
        self._webAppUserDatabaseConnection = None
        self._databaseConnection = None
        self._ontologyDatabaseConnection = None
        self._SFFDatabaseConnection = None
    def __del__(self):
        # Make sure we close out our connections when the object goes out of scope
        if self._webAppUserDatabaseConnection:
            self._webAppUserDatabaseConnection.close()
            
        if self._databaseConnection:
            self._databaseConnection.close()
            
        if self._ontologyDatabaseConnection:
            self._ontologyDatabaseConnection.close()
    
    def getDatabaseConnection(self):
        """ Obtains a connection to the qiime_production schema
        """
        if self._databaseConnection == None:
            try:
                self._databaseConnection = cx_Oracle.Connection('qiime_metadata/m_t_d_t_@quarterbarrel.microbio.me:1521/qiimedb.microbio.me')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
                
        return self._databaseConnection

    def getWebAppUserDatabaseConnection(self):
        """ Obtains a connection to the web_app_user schema
        """
        if self._webAppUserDatabaseConnection == None:
            try:
                self._webAppUserDatabaseConnection = cx_Oracle.Connection('web_app_user/WW3bApp...@microbiome1.colorado.edu:1523/microbe')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
                
        return self._webAppUserDatabaseConnection

    def getOntologyDatabaseConnection(self):
        """ Obtains a connection to the ontologies schema

        Get a database connection. Note that the consumer is responsible 
        for closing this connection once obtained. This method is intended
        to be used internally by this class.
        """
        if self._ontologyDatabaseConnection == None:
            try:
                self._ontologyDatabaseConnection = cx_Oracle.Connection('ontologies/odyssey$@quarterbarrel.microbio.me:1521/qiimedb.microbio.me')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
                
        return self._ontologyDatabaseConnection
    
    def getSFFDatabaseConnection(self):
        """ Obtains a connection to the qiime_test schema

        Get a database connection. 
        """
        if self._SFFDatabaseConnection == None:
            try:
                print 'No active connection - obtaining new connection to qiime_test.'
                self._SFFDatabaseConnection = cx_Oracle.Connection('SFF/SFF454SFF@quarterbarrel.microbio.me:1521/qiimedb')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;

        return self._SFFDatabaseConnection
        
    #####################################
    # Helper Functions
    #####################################
    
    def testDatabase(self):
        con = self.getDatabaseConnection()
        sleep(.1)
        sleep(.1)
        sleep(.1)
        sleep(.1)
        sleep(.1)
        return True
    
    def convertToOracleHappyName(self, date_string):
        """ Oracle is picky about dates. This function takes a previously validated
        date format and returns a formatted string for inserting into database
        """
        formatted_date = ''
        
        # First handle the date portion since it must exist for a valid submission
        if date_string.find(' ') == -1:
            # Date only
            formatted_date = 'to_date(\'%s\', \'%s\')' % (date_string, 'MM/DD/YYYY')
        else:
            # Date and time exist
            formatted_date = 'to_date(\'%s\', \'%s\')' % (date_string, 'MM/DD/YYYY HH24:MI:SS')
        
        return formatted_date

    #####################################
    # Users
    #####################################

    def authenticateWebAppUser( self, username, password ):
        """ Attempts to validate authenticate the supplied username/password
        
        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getWebAppUserDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('authenticate_user', [username, crypt_pass, user_data])
            row = user_data.fetchone()
            if row:
                user_data = {'web_app_user_id':row[0], 'email':row[1], 'password':row[2], 'is_admin':row[3], 'is_locked':row[4], 'last_login':row[5],'verified':row[6]}
                return user_data
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def verifyActivationCode( self, username, activation_code ):
        """ Attempts to activate user's account

        Attempt to activate the user account. If successful, returns True. 
        If not, the function returns False.
        """
        try:
            con = self.getWebAppUserDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('verify_user_activation_code', [username, activation_code, user_data])
            row = user_data.fetchone()
            if row:
                return True
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def activateWebAppUser( self, username, activation_code ):
        """ Attempts to activate user's account

        Attempt to activate the user account. If successful, returns True. 
        If not, the function returns False.
        """
        try:
            con = self.getWebAppUserDatabaseConnection()
            user_data = con.cursor()

            con.cursor().callproc('verify_user_activation_code', [username, activation_code, user_data])
            row = user_data.fetchone()
            if row:
                con.cursor().callproc('activate_user_account', [username])
                return True
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def deactivateWebAppUser( self, username, activation_code ):
        """ Attempts to activate user's account

        Attempt to activate the user account. If successful, returns True. 
        If not, the function returns False.
        """
        try:
            con = self.getWebAppUserDatabaseConnection()
            con.cursor().callproc('deactivate_user_account', [username,activation_code])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def checkWebAppUserAvailability(self, username):
        """ Attempts to validate authenticate the supplied username/password

        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            con = self.getWebAppUserDatabaseConnection()
            availability = con.cursor()
            con.cursor().callproc('check_username_availability', [username, availability])
            row = availability.fetchone()
            if row:
                return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def registerWebAppUser( self, username, password ,activation_code):
        """ Attempts to register a new user using the supplied username/password

        Attempt to register the user. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getWebAppUserDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('web_app_user_insert', [username, crypt_pass,activation_code])
            row = user_data.fetchone()
            if row:
                user_data = {'web_app_user_id':row[0], 'email':row[1], 'password':row[2], 'is_admin':row[3], 'is_locked':row[4], 'last_login':row[5]}
                return user_data
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def updateWebAppUserPwd( self, username, password ):
        """ Attempts to validate authenticate the supplied username/password

        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getWebAppUserDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('update_web_app_user_password', [username, crypt_pass])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False  

    #####################################
    # Study
    #####################################

    def deleteStudy(self, study_id, full_delete):
        """ Removes a study from the database
        
        study_id: the numeric identifier for the study in the database
        full_delete: an integer value:
            0 = delete all BUT the study entry
            1 = delete everything including the study
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_delete', [study_id, full_delete])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getStudyNames(self):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_names', [results])
            study_name_list = []
            for row in results:
                if row[0] is None:
                    continue
                else:
                    study_name_list.append(row)
            return study_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    #
    def appendMetaAnalysisStudy(self,inv_id,study_id):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('append_meta_analysis_to_study', [inv_id, \
                                                                    study_id])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    #
    def addMetaAnalysisMapOTUFiles(self, start_job, meta_analysis_id, \
                                    mapping_fpath, otu_fpath,zip_fpath):
        try:
            con = self.getDatabaseConnection()
            if start_job:
                con.cursor().callproc('add_map_and_otu_file_paths', 
                                                    [meta_analysis_id,\
                                                    mapping_fpath,otu_fpath,
                                                    zip_fpath])  
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getMetaAnalysisFilepaths(self, meta_analysis_id):
        try:
            con = self.getDatabaseConnection()
            results=con.cursor()
            con.cursor().callproc('get_meta_analysis_filepaths', 
                                                    [meta_analysis_id,\
                                                    results])
            fpaths=[]
            for row in results:
                if row[0] is None:
                    continue
                else:
                    fpaths.append(row)
            return fpaths
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    def createMetaAnalysis(self,web_app_user_id,inv_name):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            db_output=[]
            inv_id=0
            db_output=con.cursor().callproc('create_meta_analysis', 
                                                    [web_app_user_id, \
                                                     inv_name,inv_id])
                                                                
            return db_output[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getRunPrefixForSample(self,sample_name,study_id):
        """ Returns a Run Prefix for Sample
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            db_output=[]
            con.cursor().callproc('get_run_prefix_for_sample', 
                                                    [sample_name,study_id,\
                                                     results])
                                                                
            run_prefix = ''
            for row in results:
                if row[0] is None:
                    continue
                else:
                    run_prefix=row[0]
            return run_prefix
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getStudiesByMetaAnalysis(self,meta_analysis_id):
        """ Returns a list of study ids by meta_analysis id
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_studies_by_meta_analysis', [meta_analysis_id,\
                                                                results])
            meta_analysis_name_list = []
            for row in results:
                if row[0] is None:
                    continue
                else:
                    meta_analysis_name_list.append(row)
            return meta_analysis_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getMetaAnalysisNames(self,web_app_user_id):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_meta_analysis_names', [web_app_user_id,\
                                                                results])
            meta_analysis_name_list = []
            for row in results:
                if row[0] is None:
                    continue
                else:
                    meta_analysis_name_list.append(row)
            return meta_analysis_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    def getPublicStudyNames(self,web_app_user_id):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_study_names', [web_app_user_id,\
                                                                results])
            study_list = []
            for row in results:
                if row[0] is None:
                    continue
                else:
                    study_list.append(row)
            return study_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getUserStudyNames(self, user_id):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            study_names = con.cursor()
            con.cursor().callproc('qiime_assets.get_user_study_names', [user_id, study_names])
            study_name_list = []
            for row in study_names:
                if row[0] is None:
                    continue
                else:
                    study_name_list.append((row[0], row[1]))
            return study_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getStudyByName(self, study_name):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            values = con.cursor()
            con.cursor().callproc('get_study_by_name', [study_name, study_id])
            value_list = []
            for row in study_id:
                value_list.append(row[0])
            return value_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getStudyById(self, study_id):
        """ Returns a study name using the study_id
        """
        try:
            con = self.getDatabaseConnection()
            values = con.cursor()
            con.cursor().callproc('get_study_by_id', [study_id, values])
            value_list = []
            for row in values:
                value_list.append(row[0])
            return value_list[0]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getStudyInfo(self, study_id):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_info', [study_id, results])
            study_info = {}
            for row in results:
                print row
                study_info['submit_to_insdc'] = row[0]
                study_info['investigation_type'] = row[1]
                study_info['project_name'] = row[2]
                study_info['experimental_factor'] = row[3]
                study_info['study_alias'] = row[4]
                study_info['study_title'] = row[5]
                study_info['study_type'] = row[6]
                study_info['study_abstract'] = row[7]
                study_info['study_description'] = row[8]
                study_info['center_name'] = row[9]
                study_info['center_project_name'] = row[10]
                study_info['project_id'] = row[11]
                study_info['pmid'] = row[12]
                study_info['metadata_complete'] = row[13]
                study_info['sff_complete'] = row[14]
                study_info['mapping_file_complete'] = row[15]
                study_info['miens_compliant'] = row[16]
            return study_info
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def createStudy(self, user_id, study_name, investigation_type, miens_compliant, submit_to_insdc):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            study_id = 0
            study_id = con.cursor().callproc('qiime_assets.study_insert', [user_id, study_name, investigation_type, miens_compliant, submit_to_insdc, study_id])
            return study_id[5]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createStudyPackage(self, study_id, env_package):
        """ 
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_packages_insert', [study_id, env_package])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getStudyPackages(self, study_id):
        """ Returns a list env_package types associated to this study
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_packages', [study_id, results])
            env_packages = []
            for row in results:
                env_packages.append(row[0])
            return env_packages
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def updateMetadataFlag(self, study_id, status):
        """ Updates the status of the metadata submission flag (y/n)
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.update_metadata_flag', [study_id, status])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addSFFFile(self, study_id, sff_file_path):
        """ adds a new SFF file to the study
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_sff_file', [study_id, sff_file_path])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addMappingFile(self, study_id, mapping_file_path):
        """ adds a new mapping file to the study
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_mapping_file', [study_id, mapping_file_path])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    #def updateSFFFlag(self, study_id, status):
    #    """ Updates the status of the sff submission flag (y/n)
    #    """
    #    try:
    #        con = self.getDatabaseConnection()
    #        con.cursor().callproc('qiime_assets.update_sff_flag', [study_id, status])
    #        return True
    #    except Exception, e:
    #        print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
    #        return False

    #####################################
    # Metadata
    #####################################

    #def getMetadataHeaders(self):
    #    """ Returns a list of metadata headers
    #    """
    #    try:
    #        con = self.getDatabaseConnection()
    #        metadata_headers = con.cursor()
    #        con.cursor().callproc('get_metadata_headers', [metadata_headers])
    #        metadata_headers_list = []
    #        for row in metadata_headers:
    #            metadata_headers_list.append(row[0])
    #        return metadata_headers_list
    #    except Exception, e:
    #        print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
    #        return False
        
    def getMetadataFields(self, study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_metadata_fields', [study_id, results])
            metadata_fields = []
            for row in results:
                metadata_fields.append((row[0], row[1]))
            return metadata_fields
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getSampleList(self, study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_sample_list', [study_id, results])
            sample_list = []
            for row in results:
                sample_list.append(row[0])
            return sample_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addStudyActualColumn(self, study_id, column_name, table_name):
        """ inserts a selected metadata column name into the database
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_study_actual_column', [study_id, column_name, table_name])
        except Exception, e:
            
            raise Exception('Exception caught in addStudyActualColumns(): %s.\nThe error is: %s' % (type(e), e))

    def getMetadataByStudyList(self, field_name, study_list):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            metadata_list = []
            con = self.getDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('get_metadata_by_study_list', [field_name, study_list, column_values])
            for row in column_values:
                if row[0] is None:
                    continue
                metadata_list.append(row[0])
            return metadata_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getParameterByScript(self, parameter_type, script_type):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            values = con.cursor()
            con.cursor().callproc('get_parameter_by_script', [parameter_type, script_type, values])
            value_list = []
            for row in values:
                value_list.append(row[0])
            return value_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getColumnDictionary(self):
        """ Returns the full column dictionary
        """
        try:
            column_dictionary = []
            con = self.getDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('qiime_assets.get_column_dictionary', [column_values])
            for row in column_values:
                # Skip if no column name is found
                if row[0] is None:
                    continue

                # Some variables to allow for re-assignment should any of them be None
                column_name = row[0]
                expected_values = row[1]
                description = row[2]
                data_type = row[3]
                data_length = row[4]
                
                if row[1] == None:
                    expected_values == ''
                elif row[2] == None:
                    description == ''
                elif row[3] == None:
                    data_type = ''
                elif row[4] == None:
                    data_length = ''
                    
                list_item = (column_name, expected_values, description, data_type, data_length)
                column_dictionary.append(list_item)
            return column_dictionary
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getPackageColumns(self, package_type_id):
        """ Returns the full column dictionary
        """
        try:
            package_columns = []
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_package_columns', [package_type_id, results])

            for row in results:
                package_columns.append((row[0], row[1], row[2], row[3], row[4]))

            return package_columns

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def findMetadataTable(self, column_name, study_id):
        """ Finds the target metadata table for the supplied column name
        """
        try:
            table = ''
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.find_metadata_table', [column_name, results])

            for row in results:
                # If it's a study table, find the right one
                if row[0].upper().startswith('EXTRA_'):
                    elements = row[0].split('_')
                    # Compare the study_id for each. If they don't match, continue
                    if elements[2] != str(study_id):
                        continue
                    else:
                        table = row[0]
                # Not an extra table, just assign the table name
                else:
                    table = row[0]
            
            # If we find an 'extra' table, make sure it's for the right study. If
            # not, return '' so a new extra table will be created.
            if table.upper().startswith('EXTRA_'):
                elements = table.split('_')
                if elements[2] != str(study_id):
                    return ''
                
            return table

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getFieldDetails(self, field_name):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            value_list = []
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_field_details', [field_name, results])

            for row in results:
                value_list.append((row[0], row[1], row[2], row[3]))
                
            if len(value_list) == 0:
                # If not found in the dictionary, assume this is a user-created column
                value_list.append((field_name, 'text', '', ''))
                
            return value_list[0]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def createSampleKey(self, study_id, sample_name):
        """ Writes a sample key row to the database
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.sample_insert', [study_id, sample_name])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createPrepKey(self, study_id, sample_name, row_num):
        """ Writes a prep key row to the database
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.prep_insert', [study_id, sample_name, row_num])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createHostKey(self, study_id, sample_name, host_subject_id):
        """ Writes a host key row to the database
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.host_insert', [study_id, sample_name, host_subject_id])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def handleExtraData(self, study_id, field_name, field_type, log, con):
        
        # Define the names of the 'extra' tables
        extra_table = ''
        key_table = ''
        
        # Other required values
        schema_owner = 'QIIME_METADATA'
        statement = ''
        
        # Figure out which table we're talking about
        if field_type == 'study':
            extra_table = str('extra_study_' + str(study_id)).upper()
            key_table = 'study'
        elif field_type == 'sample':
            extra_table = str('extra_sample_' + str(study_id)).upper()
            key_table = 'sample'
        elif field_type == 'prep':
            extra_table = str('extra_prep_' + str(study_id)).upper()
            key_table = 'sample'
        else:
            # Error state
            raise Exception('Could not determine "extra" table name. field_type is "%s"' % (field_type))
            
        # Does table exist already?
        log.append('Checking if table %s exists...' % extra_table)
        named_params = {'schema_owner':schema_owner, 'extra_table':extra_table}
        statement = 'select * from all_tables where owner = :schema_owner and table_name = :extra_table'
        log.append(statement)
        results = con.cursor().execute(statement, named_params).fetchone()
        
        # Create if it doesn't exist already
        if not results:
            log.append('Creating "extra" table %s...' % extra_table)
            statement = 'create table %s (%s_id int not null, constraint pk_%s primary key (%s_id), \
                constraint fk_%s_sid foreign key (%s_id) references %s (%s_id))' % \
                (extra_table, key_table, extra_table, key_table, extra_table, key_table, key_table, key_table)
            log.append(statement)
            results = con.cursor().execute(statement)
        
            # In the study case, we must also add the first (and only) row for the subsequent updates to succeed.
            if field_type == 'study':
                log.append('Inserting study extra row...')                        
                statement = 'insert into %s (study_id) values (%s)' % (extra_table, study_id)
                log.append(statement)
                results = con.cursor().execute(statement)
                con.cursor().execute('commit')
                            
        # Check if the column exists
        log.append('Checking if extra column exists: %s' % field_name)
        named_params = {'schema_owner':schema_owner, 'extra_table_name':extra_table, 'column_name':field_name}
        statement = 'select * from all_tab_columns where owner = :schema_owner and table_name = :extra_table_name and column_name = :column_name'
        log.append(statement)
        results = con.cursor().execute(statement, named_params).fetchone()
        
        # If column doesn't exist, add it:
        if not results:
            log.append('Creating extra column: %s' % field_name)
            statement = 'alter table %s add %s varchar2(4000) default \'\'' % (extra_table, field_name)
            log.append(statement)
            results = con.cursor().execute(statement)
        
        # Return the proper table name
        return extra_table
    
    def writeMetadataValue(self, field_type, key_field, field_name, field_value, study_id, host_key_field, row_num):
        """ Writes a metadata value to the database
        """
        
        # This is a mess and it's slow right now. In need of serious speed improvements and cleanup.
        
        statement = ''
        log = []
        pk_name = ''
        
        try:
            
            con = self.getDatabaseConnection()
            table_name = None
            
            # Find the table name
            log.append('Locating table name...')
            table_name = self.findMetadataTable(field_name, study_id)
            
            # If table is not found, assume user-defined column and store appropriately
            if table_name == '' or table_name == None:
                # If the table was not found, this is a user-added column.
                table_name = self.handleExtraData(study_id, field_name, field_type, log, con)
            
            # Double-quote for database safety.    
            table_name = '"' + table_name + '"'
            
            log.append('Table name found: %s' % (table_name))
            
            # Store the field name in the database. These are the field names which will
            # be used later to generate a mapping file. We collect the names here because
            # it's an expensive operation to determine post-commit which fields were
            # actually submitted to the database.
            log.append('Attempting to store values in study_actual_columns: %s, %s, %s' % (study_id, field_name, table_name))
            self.addStudyActualColumn(study_id, field_name, table_name);
            
            # Get extended field info from the database
            log.append('Loading field details...')
            field_details = self.getFieldDetails(field_name)
            log.append(str(field_details))
            if field_details == None:
                log.append('Could not obtain detailed field information. Skipping.')
                raise Exception
            else:
                database_data_type = field_details[1]
                log.append('Read field database data type as "%s"' % database_data_type)
            
            # Figure out if this needs to be an integer ID instead of a text value
            if database_data_type == 'list':
                log.append('Field is of type list. Looking up integer value...')
                named_params = {'field_value':field_value.upper()}
                statement = 'select vocab_value_id from controlled_vocab_values where upper(term) = :field_value'
                log.append(statement)
                results = con.cursor().execute(statement, named_params).fetchone()
                if results != None:
                    # If found, set the field_value to its numeric identifier for storage
                    log.append('Value found in controlled_vocab_values. Old field value: "%s", new field value: "%s".' % (field_value, results[0]))
                    field_value = results[0]
                else:
                    log.append('Could not determine inteteger value for list term "%s" with value "%s". Skipping.' % (field_name, field_value))
                    raise Exception
            
            # Set the field_name to it's quoted upper-case name to avoid key-work issues with Oracle
            field_name = '"%s"' % field_name.upper()
            
            # If the filed value is 'unknown', switch to 'null' (empty string is the same as null)
            if str(field_value).upper() == 'UNKNOWN':
                field_value = ''
            
            ########################################
            ### For STUDY
            ########################################
            
            # Study is special - handle separately since row is guaranteed to exist and there can only be one row
            if table_name == '"STUDY"' or 'EXTRA_STUDY_' in table_name:
                log.append('Updating study field...')
                named_params = {'field_value':field_value, 'study_id':study_id}
                statement = 'update %s set %s = :field_value where study_id = :study_id' % (table_name, field_name)
                log.append(statement)
                log.append('field_value = "%s", study_id = "%s"' % (field_value, study_id))
                results = con.cursor().execute(statement, named_params)
                con.cursor().execute('commit')
                log.append('Study updated.')
                #raise Exception
                return
            
            ########################################
            ### For other tables
            ########################################
            
            if table_name in ['"AIR"', '"COMMON_FIELDS"', '"MICROBIAL_MAT_BIOFILM"', '"OTHER_ENVIRONMENT"', \
            '"SAMPLE"', '"SEDIMENT"', '"SOIL"', '"WASTEWATER_SLUDGE"', '"WATER"', '"SEQUENCE_PREP"'] \
            or 'EXTRA_SAMPLE_' in table_name or 'EXTRA_PREP_' in table_name:
                named_params = {'key_field':key_field, 'study_id':study_id}
                statement = 'select sample_id from "SAMPLE" where sample_name = :key_field and study_id = :study_id'
                key_column = 'sample_id'
                key_table = '"SAMPLE"'
            elif table_name in ['"HOST"', '"HOST_ASSOC_VERTIBRATE"', '"HOST_ASSOCIATED_PLANT"', '"HUMAN_ASSOCIATED"']:
                named_params = {'key_field':host_key_field}
                statement = 'select host_id from "HOST" where host_subject_id = :key_field'
                key_column = 'host_id'
                key_table = '"HOST"'
            else:
                return 'Unknown table found - no action taken. Table name was: "%s". Column name was: "%s"' %  (table_name, field_name)
            
            # Find the assocaited key column
            log.append('Determining if required key row exists...')
            log.append(statement + '", key_field is ' + key_field + ', study_id is ' + str(study_id))
            results = con.cursor().execute(statement, named_params).fetchone()
            if results != None:
                key_column_value = results[0]
                log.append('Found key_column_value: %s' % str(key_column_value))
            else:
                log.append('Could not determine key. Skipping write for field %s with value "%s".' % (field_name, field_value))
                raise Exception

            # If it ain't there, create it
            log.append('Checking if row already exists...')
            
            # Must append row_num if sequence table
            if table_name == '"SEQUENCE_PREP"' or 'EXTRA_PREP_' in table_name:
                named_params = {'key_column_value':key_column_value, 'row_number':row_num}
                statement = 'select * from %s where %s = :key_column_value and row_number = :row_number' % (table_name, key_column)
            else:
                named_params = {'key_column_value':key_column_value}
                statement = 'select * from %s where %s = :key_column_value' % (table_name, key_column)
            log.append(statement)
            results = con.cursor().execute(statement, named_params).fetchone()
                
            if results == None:
                log.append('No row found, inserting new row:')
                if table_name == '"SEQUENCE_PREP"' or 'EXTRA_PREP_' in table_name:
                    named_params = {'key_column_value':key_column_value, 'row_number':row_num}
                    statement = 'insert into %s (%s, row_number) values (:key_column_value, :row_number)' % (table_name, key_column)
                else:
                    named_params = {'key_column_value':key_column_value}
                    statement = 'insert into %s (%s) values (:key_column_value)' % (table_name, key_column)
                log.append(statement)
                con.cursor().execute(statement, named_params)
            
            # Attempt to write the metadata field
            log.append('Writing metadata value...')
            if database_data_type == 'date':
                field_value = self.convertToOracleHappyName(field_value)
            if table_name == '"SEQUENCE_PREP"' or 'EXTRA_PREP_' in table_name:
                statement = 'update %s set %s = \'%s\' where %s = %s and row_number = %s' % (table_name, field_name, field_value, key_column, key_column_value, row_num)
            else:  
                statement = 'update %s set %s = \'%s\' where %s = %s' % (table_name, field_name, field_value, key_column, key_column_value)
            log.append(statement)
            results = con.cursor().execute(statement)
            
            # Finally, commit the changes
            results = con.cursor().execute('commit')
            
        except Exception, e:
            call_string = 'writeMetadataValue(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (field_type, key_field, field_name, field_value, study_id)
            log_string = '<br/>'.join(log)
            error_msg = 'Exception caught attempting to store field "%s" with value "%s" into \
                table "%s".<br/>Method signature: %s<br/>Full error log:<br/>%s<br/>Oracle says: %s' % \
                (field_name, field_value, table_name, call_string, log_string, str(e))
            print error_msg
            return error_msg

            
    #####################################
    # Jobs
    #####################################
    
    def checkForNewJobs(self):
        """ Returns a list of jobs that are ready to start
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_new_queue_jobs', [results])
            jobs = []
            for row in results:
                jobs.append((row[0], row[1], row[2]))
            return jobs
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def updateJobStatus(self, job_id, status):
        """ Updates the status message for a job
        """
        try:
            con = self.getDatabaseConnection()
            con.cursor().callproc('qiime_assets.update_job_status', [job_id, status])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def createQueueJob(self, study_id, user_id, mapping_file_path, sff_path):
        """ Returns submits a job to the queue and returns the job_id
        """
        try:
            con = self.getDatabaseConnection()
            job_id = 0
            job_id = con.cursor().callproc('qiime_assets.create_queue_job', [study_id, user_id, sff_path, mapping_file_path, job_id])
            return job_id[4]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return -1
        
    def getSFFFiles(self, study_id):
        """ Gets a list of SFF files for this study
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            items = []
            con.cursor().callproc('qiime_assets.get_sff_files', [study_id, results])
            for row in results:
                items.append(row[0])
            return items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getMappingFiles(self, study_id):
        """ Gets a list of mapping files for this study
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            items = []
            con.cursor().callproc('qiime_assets.get_mapping_files', [study_id, results])
            for row in results:
                items.append(row[0])
            return items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getJobInfo(self, study_id):
        """ Returns submits a job to the queue and returns the job_id
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            jobs = []
            con.cursor().callproc('qiime_assets.get_job_info', [study_id, results])
            for row in results:
                jobs.append((row[0], row[1], row[2]))
            return jobs
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    #####################################
    # Ontologies and Lists
    #####################################

    def getControlledVocabs(self, column_name):
        """ Returns the full column dictionary
        """
        controlled_vocabs = []
        
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_controlled_vocab_list', [results, column_name])
            for row in results:
                controlled_vocabs.append(row[0])

            return controlled_vocabs
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getControlledVocabValueList(self, controlled_vocab_id):
        """ Returns the full column dictionary
        """
        vocab_items = {}

        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_controlled_vocab_values', [controlled_vocab_id, results])
            for row in results:
                vocab_items[row[0]] = row[1]

            return vocab_items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getOntologies(self, column_name):
        """ Returns the full column dictionary
        """
        ontologies = []
        
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_ontology_list', [results, column_name])
            for row in results:
                ontologies.append(row[0])

            return ontologies
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getListValues(self, list_name):
        """ Returns the full column dictionary
        """
        try:
            list_values = []
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_list_values', [results, list_name])
            
            for row in results:
                list_values.append((row[0], row[1]))
                    
            return list_values
            
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    def validateListValue(self, list_name, list_value):
        """ Returns the full column dictionary
        """
        try:
            con = self.getDatabaseConnection()
            results = 0
            results = con.cursor().callproc('qiime_assets.validate_list_value', [list_name, list_value, results])
            return results[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    def getOntologyValues(self, ontology_name):
        """ Returns the full column dictionary
        """
        try:
            ontology_values = []
            con = self.getOntologyDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_ontology_values', [results, ontology_name])

            for row in results:
                ontology_values.append(row[0])

            return ontology_values

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def validateOntologyValue(self, ontology_name, identifier_value):
        """ Returns the full column dictionary
        """
        try:
            con = self.getOntologyDatabaseConnection()
            results = 0
            results = con.cursor().callproc('validate_ontology_value', [ontology_name, identifier_value, results])
            return results[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    def getTermMatches(self, column_name, term_value):
        """ Finds close term matches for columns of type onotlogy or list
        """
        try:
            # Handle the ontology prefix:
            term_parts = term_value.split(':')
            if len(term_parts) > 1:
                term_value = term_parts[1]
            
            details = self.getFieldDetails(column_name)
            if len(details) == 0:
                return None
            
            matches = []
            column_type = details[1]
            
            if column_type == 'list':
                con = self.getDatabaseConnection()
                results = con.cursor()
                con.cursor().callproc('qiime_assets.get_list_matches', [column_name, term_value, results])
                for row in results:
                    matches.append(row[1])
            elif column_type == 'ontology':
                con = self.getDatabaseConnection()
                ontologies = con.cursor()
                con.cursor().callproc('qiime_assets.get_column_ontologies', [column_name, ontologies])
                for row in ontologies:
                    con_tology = self.getOntologyDatabaseConnection()
                    results = con_tology.cursor()
                    con_tology.cursor().callproc('get_ontology_terms', ['\'' + row[0] + '\'', term_value.upper(), results])
                    for row in results:
                        matches.append(row[1])
            else:
                # Do nothing for all other types
                return None
            
            return matches
        
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def get_list_of_ontologies(self):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getOntologyDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('get_list_of_ontologies', [column_values])
            query_results=[]
            for row in column_values:
                if row[0] is None:
                    continue
                query_results.append(row)
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if (con):
                con.cursor().close()
                con.close()
    
    def get_ontology_terms(self, ontology, query):
        """ Returns a list of ontology terms if the term contains query as a
            substring.
            
            Note: ontology can be a list of ontologies, and as such the value, whether
            singular or multiple, must be quoted: e.g. '\'FMA\'', or '\'FMA\', \'OBI\''
        """
        try:
            con = self.getOntologyDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('get_ontology_terms', [ontology, query, column_values])
            query_results=[]
            for row in column_values:
                if row[1] is None:
                    continue
                query_results.append(row[1])
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if (con):
                con.cursor().close()
                con.close()
    
    def validity_of_ontology_term(self, ontology, query):
        """ Returns a list of ontology terms if the query is exactly equal to 
            the term.
        """
        try:
            con = self.getOntologyDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('validity_of_ontology_term', [ontology, query, column_values])
            query_results=[]
            for row in column_values:
                if row[1] is None:
                    continue
                query_results.append(row[1])
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if (con):
                con.cursor().close()
                con.close()
                
    #####################################
    # Loading
    #####################################
    
    def disableTableConstraints(self):
        """ disable the table constraints
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            db_output=con.cursor().callproc('disable_table_constraints', \
                                                [error_flag])
            if db_output[0]==0:
                return True
            else:
                return False
        except Exception, e:
            err = 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            print err
            raise Exception(err)

    def loadSplitLibFasta(self,start_job,run_id,fname):
        """ starts process of importing processed split-library data into the DB
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            warning_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_fna_file',[fname,run_id,\
                                                    error_flag,warning_flag])
                if db_output[3]==-1:
                    print "Warning: some of the samples are already in the DB!"
                
                if db_output[2]==0:
                    return True
                else:
                    return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def loadSplitLibInfo(self, start_job, analysis_id, run_date, cmd, svn_version,
                            log_str, hist_str, md5_input_file):
        """ uploads the information related to the split_libraries run to the DB
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            split_lib_run_id=1
            if start_job:
                db_output=con.cursor().callproc('register_split_library_run',
                                        [analysis_id,run_date, cmd, svn_version,\
                                         log_str, hist_str, md5_input_file,\
                                         split_lib_run_id,error_flag])
                if db_output[8]==0:
                    return True,db_output[7]
                else:
                    return False,db_output[7]
            else:
                return True,0
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False,0
        
    def loadOTUInfo(self, start_job, otu_run_set_id, analysis_id, run_date,
                    pOTUs_method, pOTUs_threshold, svn_version, pick_otus_cmd, 
                    otus_log_str,split_lib_seqs_md5,ref_set_name,
                    ref_set_threshold):
        """ loads the information pertaining to an OTU picking runls
        
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            otu_picking_run_id=0
            if start_job:
                db_output=con.cursor().callproc(\
                        'register_otu_picking_run',[otu_run_set_id, \
                                analysis_id, run_date, pOTUs_method, \
                                pOTUs_threshold, svn_version, pick_otus_cmd, \
                                otus_log_str,split_lib_seqs_md5,ref_set_name, \
                                ref_set_threshold, error_flag, \
                                otu_picking_run_id])
                if db_output[11]==0:
                    return True,db_output[0],db_output[12]
                else:
                    return False,db_output[0],db_output[12]
            else:
                return True,0
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def getTestData(self, start_job,analysis_id, sample_id):
        """ Returns the data from the TEST data from DB
        """
        analysis_data = []
    
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_analysis_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getTestFlowData(self, start_job,analysis_id, sample_id):
        """ Returns the FLOW TEST Data from DB
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_flow_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getTestSplitLibData(self, start_job,analysis_id, sample_id):
        """ Returns the SPLIT_LIBRARY TEST Data
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_split_lib_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getTestOTUData(self, start_job,analysis_id, sample_id):
        """ Returns the OTU TEST DATA
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_otu_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getTestOTUFailureData(self, start_job,analysis_id, sample_id):
        """ Returns the OTU FAILURE TEST DATA
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_otu_failure_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                    
    def deleteTestAnalysis(self, start_job,analysis_id):
        """ Removes rows from the DB given an analysis id
        """
        analysis_data = []
        error_flag = 1
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('delete_test_analysis', 
                                        [analysis_id, error_flag])
                if db_output[1]==0:
                    return True
                else:
                    return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def loadOTUFailures(self, start_job, input_set):
        """ starts process of importing failed otus
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_otu_failures_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def checkIfSFFExists(self, md5_checksum):
        """ determine if the SFF is already in the DB
        """
        try:
            con = self.getSFFDatabaseConnection()
            sff_exists=0
            db_output=con.cursor().callproc('check_if_sff_file_exists',
                                            [str(md5_checksum),sff_exists])
            if db_output[1]==1:
                return True
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def getSeqRunIDUsingMD5(self, md5_checksum):
        """ returns the SEQ_RUN_ID given an md5_checksum
        """
        try:
            con = self.getSFFDatabaseConnection()
            seq_run_id=0
            db_output=con.cursor().callproc('get_seq_run_id_using_md5',
                                            [md5_checksum,seq_run_id])
            return db_output[1]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def createAnalysis(self, study_id):
        """ creates a row in the ANALYSIS table 
        """
        try:
            con = self.getSFFDatabaseConnection()
            analysis_id=0
            db_output=con.cursor().callproc('create_analysis',
                                            [study_id,analysis_id])
            return db_output[1]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def addSFFFile(self, start_job, sff_filename, number_of_reads,header_length,
                    key_length, number_of_flows, flowgram_code, flow_characters,
                    key_sequence, md5_checksum, seq_run_id):
        """ appends the SFF info into the SFF_FILE table
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('add_sff_file',
                                                [sff_filename, number_of_reads,
                                                 header_length,key_length, 
                                                 number_of_flows, flowgram_code, 
                                                 flow_characters, key_sequence, 
                                                 md5_checksum,seq_run_id])
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    def createSequencingRun(self,start_job,instrument_code,version,seq_run_id):
        """ creates a row in the sequencing_run table
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('create_sequencing_run',
                                                [instrument_code, version,
                                                 seq_run_id])
                return db_output[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def loadSFFData(self, start_job, input_set):
        """ loads the flow data into the READ_454 table
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_flow_data.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def loadFNAFile(self, start_job, input_set):
        """ starts process of importing fna file data
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag = 1
            if start_job:
                db_output=con.cursor().callproc('load_fna_file_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False


    def updateAnalysisWithSeqRunID(self, start_job, analysis_id,seq_run_id):
        """ updates the ANALYSIS table with the SEQ_RUN_ID
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                con.cursor().callproc('update_analysis_w_seq_run_id',
                                                [analysis_id,seq_run_id])
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def loadOTUMap(self, start_job, input_set):
        """ starts process of importing otus
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('load_otu_map_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def loadSeqToSourceMap(self, start_job, input_set):
        """ starts process of importing otus
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('load_seq_to_source_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def getOTUMap(self,sample_name,study_id,otu_threshold,otu_method,\
                  source_name,ref_threshold):
        """ Gets a list otus for a samples
        """
        try:
            con = self.getSFFDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('get_otu_map', [sample_name,study_id,\
                                                  otu_threshold,otu_method,\
                                                  source_name,ref_threshold,\
                                                  user_data])
            
            return user_data
        except Exception, e:
            return 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    #
    #
    def getOTUMap2(self,sample_names_and_seq_runs):
        """ Gets a list otus for a samples
        """
        try:
            con = self.getSFFDatabaseConnection()
            user_data = con.cursor()
            sample_ids=[]
            con.cursor().callproc('get_otu_table_package.array_return',\
                                            (sample_names_and_seq_runs,user_data))
            return user_data
        except Exception, e:
            return 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False


    def checkIfStudyIdExists(self, study_id):
        """ starts process of importing otus
        """
        try:
            con = self.getSFFDatabaseConnection()
            study_id_cnt=0
            db_output=con.cursor().callproc('check_if_study_id_exists',
                                            [study_id,study_id_cnt])
            if db_output[1]==0:
                return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    #
    def getSampleRunPrefixList(self, study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_sample_run_prefix_list', [study_id, results])
            sample_list = []
            for row in results:
                sample_list.append(row)
            return sample_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getSeqRunIdFromRunPrefix(self, run_prefix,study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_seq_run_id_from_run_prefix', [run_prefix,\
                                                                     study_id,\
                                                                     results])
            for row in results:
                seq_run_id=row[0]
            return seq_run_id
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getRunPrefixFromSeqRunId(self,study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_sff_basename_from_run_id', [study_id,\
                                                                     results])
            run_prefix = []
            for row in results:
                run_prefix.append(row[0])
            return run_prefix
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def checkIfColumnControlledVocab(self, column_name):
        """ starts process of importing otus
        """
        try:
            con = self.getDatabaseConnection()
            valid_controlled_column=0
            db_output=con.cursor().callproc('check_if_column_controlled',
                                            [column_name.upper(),\
                                             valid_controlled_column])
            if db_output[1]==0:
                return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    #
    #
    def getValidControlledVocabTerms(self,column_name):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_valid_control_vocab_terms', \
                                     [column_name.upper(), results])
            valid_terms = []
            for row in results:
                valid_terms.append(row)
            return valid_terms
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getPublicColumns(self):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_public_study_columns', \
                                     [results])
            public_cols = []
            for row in results:
                public_cols.append(row)
            return public_cols
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    #
    def getFieldReferenceInfo(self,column_name):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_field_reference_info', \
                                     [column_name,results])
            field_reference = []
            for row in results:
                field_reference.append(row)
            return field_reference
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
