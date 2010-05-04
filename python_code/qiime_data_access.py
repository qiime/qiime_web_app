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

class QiimeDataAccess( AbstractDataAccess ):
    """
    The actual implementation
    """
    
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
                self._databaseConnection = cx_Oracle.Connection('qiime_production/odyssey$@microbiome1.colorado.edu/microbe')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
                
        return self._databaseConnection

    def getOntologyDatabaseConnection(self):
        """ Obtains a connection to the ontologies schema

        Get a database connection. Note that the consumer is responsible 
        for closing this connection once obtained. This method is intended
        to be used internally by this class.
        """
        if self._ontologyDatabaseConnection == None:
            try:
                self._ontologyDatabaseConnection = cx_Oracle.Connection('ontologies/odyssey$@microbiome1.colorado.edu/microbe')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
                
        return self._ontologyDatabaseConnection

    def getTestDatabaseConnection(self):
        """ Obtains a connection to the qiime_test schema

        Get a database connection. Note that the consumer is responsible 
        for closing this connection once obtained. This method is intended
        to be used internally by this class.
        """
        if self._testDatabaseConnection == None:
            try:
                self._testDatabaseConnection = cx_Oracle.Connection('qiime_test/odyssey$@microbiome1.colorado.edu/microbe')
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;
        
        return self._testDatabaseConnection

    def authenticateWebAppUser( self, username, password ):
        """ Attempts to validate authenticate the supplied username/password
        
        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('authenticate_user', [username, crypt_pass, user_data])
            row = user_data.fetchone()
            if row:
                user_data = {'web_app_user_id':row[0], 'email':row[1], 'password':row[2], 'is_admin':row[3], 'is_locked':row[4], 'last_login':row[5]}
                return user_data
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getStudyNames(self):
        """ Returns a list of study names
        """
        try:
            con = self.getTestDatabaseConnection()
            study_names = con.cursor()
            con.cursor().callproc('get_study_names', [study_names])
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
            con.cursor().callproc('get_user_study_names', [user_id, study_names])
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
            con.cursor().callproc('get_study_info', [study_id, results])
            study_info = {}
            for row in results:
                print row
                study_info['public'] = row[0]
                study_info['submit_to_insdc'] = row[1]
                study_info['investigation_type'] = row[2]
                study_info['project_name'] = row[3]
                study_info['experimental_factor'] = row[4]
                study_info['env_package_id'] = row[5]
                study_info['study_complt_stat'] = row[6]
                study_info['study_alias'] = row[7]
                study_info['study_title'] = row[8]
                study_info['study_type'] = row[9]
                study_info['study_abstract'] = row[10]
                study_info['study_description'] = row[11]
                study_info['center_name'] = row[12]
                study_info['center_project_name'] = row[13]
                study_info['project_id'] = row[14]
                study_info['pmid'] = row[15]
            return study_info
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createStudy(self, user_id, study_name, investigation_type, environmental_package, study_completion_status, submit_to_insdc, public_data):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getTestDatabaseConnection()
            study_id = 0
            study_id = con.cursor().callproc('study_insert', [user_id, study_name, investigation_type, environmental_package, study_completion_status, submit_to_insdc, public_data, study_id])
            return study_id[7]
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
            con.cursor().callproc('get_column_dictionary', [column_values])
            for row in column_values:
                if row[0] is None:
                    continue
                
                if row[1] == None:
                    row[1] == ''
                elif row[2] == None:
                    row[2] == ''
                elif row[3] == None:
                    row[3] = ''
                    
                list_item = (row[0], row[1], row[2], row[3])
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
            con.cursor().callproc('get_controlled_vocab_list', [results, column_name])
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
            con.cursor().callproc('get_controlled_vocab_values', [controlled_vocab_id, results])
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
            con.cursor().callproc('get_ontology_list', [results, column_name])
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
            con.cursor().callproc('get_list_values', [results, list_name])
            
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
            results = con.cursor().callproc('validate_list_value', [list_name, list_value, results])
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
            con.cursor().callproc('get_package_columns', [package_type_id, results])

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
            con.cursor().callproc('find_metadata_table', [column_name, results])

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
            con.cursor().callproc('get_field_details', [field_name, results])
            
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
            matches = []
            details = self.getFieldDetails(column_name)
            if len(details) == 0:
                return None
            column_type = details[1]
            
            if column_type == 'list':
                con = self.getTestDatabaseConnection()
                results = con.cursor()
                con.cursor().callproc('get_list_matches', [column_name, term_value, results])
                for row in results:
                    matches.append(row[1])
            elif column_type == 'ontology':
                con = self.getTestDatabaseConnection()
                ontologies = con.cursor()
                con.cursor().callproc('get_column_ontologies', [column_name, ontologies])
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

    def createKeyField(self, study_id, study_name, field_type, field_value):
        """ Writes a key row to the database
        """
        try:
            con = self.getTestDatabaseConnection()
            if field_type == 'sample':
                con.cursor().callproc('sample_insert', [study_id, field_value])
            elif field_type == 'prep':
                con.cursor().callproc('prep_insert', [study_name, field_value])

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def writeMetadataValue(self, field_type, key_field, field_name, field_value, study_id):
        """ Writes a metadata value to the database
        """
        statement = ''
        log = []
        pk_name = ''
        
        try:
            con = self.getTestDatabaseConnection()
            table_name = None
            
            # Find the table name
            log.append('Locating table name...')
            table_name = self.findMetadataTable(field_name)
            if table_name == None or table_name == '':
                log.append('Could not determine table for field "%s" with value "%s"' % (field_name, field_value))
                raise Exception
            table_name = '"' + table_name + '"'
            log.append('Table name found: %s' % (table_name))
            
            # Figure out if this needs to be an integer ID instead of a text value
            log.append('Determing if field value exists in controlled_vocab_values:')
            statement = 'select vocab_value_id from controlled_vocab_values where term = \'%s\'' % (field_value)
            log.append(statement)
            results = con.cursor().execute(statement).fetchone()
            if results != None:
                # If found, set the field_value to its numeric identifier for storage
                log.append('Value found in controlled_vocab_values. Old field value: "%s", new field value: "%s".' % (field_value, results[0]))
                field_value = results[0]
            
            ########################################
            ### For STUDY
            ########################################
            
            # Study is special - handle separately since row is guaranteed to exist and there
            # can only be one row
            if table_name == '"STUDY"':
                log.append('Updating study field...')
                statement = 'update study set %s = \'%s\' where study_id = %s' % (field_name, field_value, study_id)
                log.append(statement)
                results = con.cursor().execute(statement)
                con.cursor().execute('commit')
                return
            
            # Find the assocaited sample_id
            log.append('Determining if required key row exists...')
            statement = 'select sample_id from "SAMPLE" where sample_name = \'%s\'' % (key_field)
            log.append(statement)
            results = con.cursor().execute(statement).fetchone()
            if results != None:
                sample_id = results[0]
                log.append('Found sample_id: %s' % str(sample_id))
            else:
                log.append('Could not determine sample_id. Skipping write for field "%s" with value "%s".' % (field_name, field_value))
                raise Exception

            ########################################
            ### For SAMPLE and SEQUENCE_PREP
            ########################################

            if table_name in ['"SAMPLE"', '"SEQUENCE_PREP"']:
                # If it ain't there, create it
                log.append('Attempting to create new key row...')
                statement = 'select * from %s where sample_id = %s' % (table_name, sample_id)
                log.append(statement)
                results = con.cursor().execute(statement).fetchone()
                if results == None:
                    log.append('No row found, inserting new row:')
                    statement = 'insert into %s (sample_id) values (%s)' % (table_name, field_value)
                    log.append(statement)
                    con.cursor().execute(statement)
                
                # Attempt to write the metadata field
                log.append('Writing metadata value...')
                statement = 'update %s set %s=\'%s\' where sample_id = %s' % (table_name, field_name, field_value, sample_id)
                log.append(statement)
                results = con.cursor().execute(statement)
            
            ########################################
            ### For SAMPLE and SEQUENCE_PREP
            ########################################
            
            else:
                return table_name
            
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
