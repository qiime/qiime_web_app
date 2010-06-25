
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
        self._testDatabaseConnection = None
        self._ontologyDatabaseConnection = None
    
    def getDatabaseConnection(self):
        """ Obtains a connection to the qiime_production schema
        """
        if self._databaseConnection == None:
            try:
                self._databaseConnection = cx_Oracle.Connection('qiime_production/odyssey$@microbiome1.colorado.edu:1523/microbe')
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
                self._ontologyDatabaseConnection = cx_Oracle.Connection('ontologies/odyssey$@microbiome1.colorado.edu:1523/microbe')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
                
        return self._ontologyDatabaseConnection

    def getTestDatabaseConnection(self):
        """ Obtains a connection to the qiime_test schema

        Get a database connection. 
        """
        if self._testDatabaseConnection == None:
            try:
                print 'No active connection - obtaining new connection to qiime_test.'
                self._testDatabaseConnection = cx_Oracle.Connection('qiime_test/odyssey$@microbiome1.colorado.edu:1523/microbe')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
        
        return self._testDatabaseConnection
    
    #####################################
    # Helper Functions
    #####################################
    
    def testDatabase(self):
        con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_delete', [study_id, full_delete])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getStudyNames(self):
        """ Returns a list of study names
        """
        try:
            con = self.getTestDatabaseConnection()
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

    def getUserStudyNames(self, user_id):
        """ Returns a list of study names
        """
        try:
            con = self.getTestDatabaseConnection()
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

    def getStudyInfo(self, study_id):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_packages_insert', [study_id, env_package])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getStudyPackages(self, study_id):
        """ Returns a list env_package types associated to this study
        """
        try:
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.update_metadata_flag', [study_id, status])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addSFFFile(self, study_id, sff_file_path):
        """ adds a new SFF file to the study
        """
        try:
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_sff_file', [study_id, sff_file_path])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addMappingFile(self, study_id, mapping_file_path):
        """ adds a new mapping file to the study
        """
        try:
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_mapping_file', [study_id, mapping_file_path])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    #def updateSFFFlag(self, study_id, status):
    #    """ Updates the status of the sff submission flag (y/n)
    #    """
    #    try:
    #        con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.sample_insert', [study_id, sample_name])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createPrepKey(self, study_id, sample_name):
        """ Writes a prep key row to the database
        """
        try:
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.prep_insert', [study_id, sample_name])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createHostKey(self, study_id, sample_name, host_subject_id):
        """ Writes a host key row to the database
        """
        try:
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.host_insert', [study_id, sample_name, host_subject_id])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def handleExtraData(self, study_id, field_name, field_type, log, con):
        
        # Define the names of the 'extra' tables
        extra_table = ''
        key_table = ''
        
        # Other required values
        schema_owner = 'QIIME_TEST'
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
            statement = 'alter table %s add %s clob default \'\'' % (extra_table, field_name)
            log.append(statement)
            results = con.cursor().execute(statement)
        
        # Return the proper table name
        return extra_table
    
    def writeMetadataValue(self, field_type, key_field, field_name, field_value, study_id, host_key_field):
        """ Writes a metadata value to the database
        """
        
        # This is a mess and it's slow right now. In need of serious speed improvements and cleanup.
        
        statement = ''
        log = []
        pk_name = ''
        
        try:
            
            con = self.getTestDatabaseConnection()
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
            named_params = {'key_column_value':key_column_value}
            statement = 'select * from %s where %s = :key_column_value' % (table_name, key_column)
            log.append(statement)
            results = con.cursor().execute(statement, named_params).fetchone()
            if results == None:
                log.append('No row found, inserting new row:')
                named_params = {'key_column_value':key_column_value}
                statement = 'insert into %s (%s) values (:key_column_value)' % (table_name, key_column)
                log.append(statement)
                con.cursor().execute(statement, named_params)
            
            # Attempt to write the metadata field
            log.append('Writing metadata value...')
            if database_data_type == 'date':
                statement = 'update %s set %s = %s where %s = %s' % (table_name, field_name, self.convertToOracleHappyName(field_value), key_column, key_column_value)
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
            con.cursor().callproc('qiime_assets.update_job_status', [job_id, status])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def createQueueJob(self, study_id, user_id, mapping_file_path, sff_path):
        """ Returns submits a job to the queue and returns the job_id
        """
        try:
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
            con = self.getTestDatabaseConnection()
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
                con = self.getTestDatabaseConnection()
                results = con.cursor()
                con.cursor().callproc('qiime_assets.get_list_matches', [column_name, term_value, results])
                for row in results:
                    matches.append(row[1])
            elif column_type == 'ontology':
                con = self.getTestDatabaseConnection()
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
    
    def loadSFFData(self,start_job,basename,run_id):
        """ starts process of importing processed sff file data into the DB
        """
        try:
            con = self.getTestDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc(\
                        'sff.process_sff_files.sff_main',[basename,run_id,\
                                                          error_flag])
                if db_output[2]==0:
                    return True,db_output[1]
                else:
                    return False,db_output[1]
            else:
                return True,run_id
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def loadSplitLibFasta(self,start_job,run_id):
        """ starts process of importing processed split-library data into the DB
        """
        try:
            con = self.getTestDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('sff.load_fna_file',[run_id,\
                                                                    error_flag])
                if db_output[1]==0:
                    return True
                else:
                    return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def loadSplitLibInfo(self,start_job,run_id,run_date, cmd, svn_version,
                            log_str,hist_str, md5_input_file):
        """ uploads the information related to the split_libraries run to the DB
        """
        try:
            con = self.getTestDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('sff.register_split_library_run',
                                        [run_id,run_date, cmd, svn_version,\
                                         log_str, hist_str, md5_input_file,\
                                         error_flag])
                if db_output[7]==0:
                    return True
                else:
                    return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False