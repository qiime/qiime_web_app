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
    
    _testDatabaseConnection = None
    _ontologyDatabaseConnection = None

    def __init__(self):
        pass
	
    def getDatabaseConnection(self):
        """ Obtains a connection to the qiime_production schema
        
        Get a database connection. Note that the consumer is responsible 
        for closing this connection once obtained. This method is intended
        to be used internally by this class.
        """
        try:
            con = cx_Oracle.Connection('qiime_production/odyssey$@microbiome1.colorado.edu/microbe')
            return con
        except Exception, e:
            print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
            return False;

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
        finally:
            if con:
                con.cursor().close()
                con.close()

    def getStudyNames(self):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
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
        finally:
            if con:
                con.cursor().close()
                con.close()

    def getUserStudyNames(self, user_id):
        """ Returns a list of study names
        """
        try:
            con = self.getDatabaseConnection()
            study_names = con.cursor()
            con.cursor().callproc('get_user_study_names', [user_id, study_names])
            study_name_list = []
            for row in study_names:
                if row[0] is None:
                    continue
                else:
                    study_name_list.append([row[0],row[1]])
            return study_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if con:
                con.cursor().close()
                con.close()

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
        finally:
            if (con):
                con.cursor().close()
                con.close()

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
        finally:
            if (con):
                con.cursor().close()
                con.close()

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
        finally:
            if (con):
                con.cursor().close()
                con.close()
            
    def createStudy(self, user_id, study_name, public_data):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            study_id=0
            study_id=con.cursor().callproc('create_study', [user_id, study_name, public_data, study_id])
            return study_id[3]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if (con):
                con.cursor().close()
                con.close()
                
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
        finally:
            if (con):
                con.cursor().close()
                con.close()
        
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
        finally:
            if (con):
                con.cursor().close()
                con.close()

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
                list_item = row[0], row[1], row[2], row[3]
                column_dictionary.append(list_item)
            return column_dictionary
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()

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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()
        
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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()

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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()

    def getListValues(self, list_name):
        """ Returns the full column dictionary
        """
        try:
            list_values = []
            con = self.getTestDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_list_values', [results, list_name])
            
            for row in results:
                list_values.append(row[0])
                    
            return list_values
            
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()
                
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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()
                
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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()

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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()

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
        #finally:
        #    if (con):
        #        con.cursor().close()
        #        con.close()
