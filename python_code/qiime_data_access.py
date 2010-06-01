#/bin/env python

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
from threading import RLock

class QiimeDataAccess( AbstractDataAccess ):
    """
    The actual implementation
    """
    
    _webAppUserDatabaseConnection = None
    _databaseConnection = None
    _testDatabaseConnection = None
    _ontologyDatabaseConnection = None

    def __init__(self):
        pass
    
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

    def getStudyNames(self):
        """ Returns a list of study names
        """
        try:
            con = self.getTestDatabaseConnection()
            study_names = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_names', [study_names])
            study_name_list = []
            for row in study_names:
                if row is None:
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

    def getMetadataHeaders(self):
        """ Returns a list of metadata headers
        """
        try:
            con = self.getDatabaseConnection()
            metadata_headers = con.cursor()
            con.cursor().callproc('get_metadata_headers', [metadata_headers])
            metadata_headers_list = []
            for row in metadata_headers:
                metadata_headers_list.append(row[0])
            return metadata_headers_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

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
                study_info['env_package_id'] = row[4]
                study_info['study_complt_stat'] = row[5]
                study_info['study_alias'] = row[6]
                study_info['study_title'] = row[7]
                study_info['study_type'] = row[8]
                study_info['study_abstract'] = row[9]
                study_info['study_description'] = row[10]
                study_info['center_name'] = row[11]
                study_info['center_project_name'] = row[12]
                study_info['project_id'] = row[13]
                study_info['pmid'] = row[14]
            return study_info
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def createStudy(self, user_id, study_name, investigation_type, study_completion_status, submit_to_insdc):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getTestDatabaseConnection()
            study_id = 0
            study_id = con.cursor().callproc('qiime_assets.study_insert', [user_id, study_name, investigation_type, study_completion_status, submit_to_insdc, study_id])
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
                
    def createQueueJob(self, user_id,study_id,status,filepath):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            job_id=0
            job_id=con.cursor().callproc('create_queue_job', [user_id,study_id,status,filepath,job_id])
            return job_id[4]
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

    def findMetadataTable(self, column_name):
        """ Finds the target metadata table for the supplied column name
        """
        try:
            table = ''
            con = self.getTestDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.find_metadata_table', [column_name, results])

            for row in results:
                table = row[0]

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
                
            return value_list[0]
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
        
    def writeMetadataValue(self, field_type, key_field, field_name, field_value, study_id, host_key_field):
        """ Writes a metadata value to the database
        """
        
        # This is a mess and it's slow right now. In need of serious speed improvements and cleanup.
        
        statement = ''
        log = []
        pk_name = ''
        
        lock = RLock()
        
        try:
            lock.acquire()
            
            con = self.getTestDatabaseConnection()
            table_name = None
            
            # Find the table name
            log.append('Locating table name...')
            table_name = self.findMetadataTable(field_name)
            
            # If table is not found, assume user-defined column and store appropriately
            if table_name == None or table_name == '':
                # If the table was not found, this is a user-added column.
                if field_type == 'study':
                    statement = 'insert study_extra (sample_id, column_name, value_list) values (%s, \'%s\', \'%s\')' % (study_id, field_name, field_value)
                    pass
                elif field_type == 'sample':
                    pass
                elif field_type == 'prep':
                    pass
                else:
                    # Unknown field type - return with log message
                    log.append('Could not determine table for user-specified field "%s" with value "%s"' % (field_name, field_value))
                    raise Exception
                
            table_name = '"' + table_name + '"'
            log.append('Table name found: %s' % (table_name))
            
            # Get extended field info from the database
            field_details = self.getFieldDetails(field_name)
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
            if table_name == '"STUDY"':
                log.append('Updating study field...')
                named_params = {'field_value':field_value, 'study_id':study_id}
                statement = 'update study set %s = :field_value where study_id = :study_id' % (field_name)
                log.append(statement)
                results = con.cursor().execute(statement, named_params)
                con.cursor().execute('commit')
                return
            
            ########################################
            ### For other tables
            ########################################
            
            if table_name in ['"AIR"', '"COMMON_FIELDS"', '"MICROBIAL_MAT_BIOFILM"', '"OTHER_ENVIRONMENT"', \
            '"SAMPLE"', '"SEDIMENT"', '"SOIL"', '"WASTEWATER_SLUDGE"', '"WATER"', '"SEQUENCE_PREP"']:
                named_params = {'key_field':key_field}
                statement = 'select sample_id from "SAMPLE" where sample_name = :key_field'
                key_column = 'sample_id'
                key_table = '"SAMPLE"'
            elif table_name in ['"HOST"', '"HOST_ASSOC_VERTIBRATE"', '"HOST_ASSOCIATED_PLANT"', '"HUMAN_ASSOCIATED"']:
                named_params = {'key_field':host_key_field}
                statement = 'select host_id from "HOST" where host_subject_id = :key_field'
                key_column = 'host_id'
                key_table = '"HOST"'
            else:
                return 'Unknown table found - no action taken: ' + table_name
            
            # Find the assocaited key column
            log.append('Determining if required key row exists...')
            log.append(statement + ' ::: key_field is ' + key_field)
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
        finally:
            lock.release()


