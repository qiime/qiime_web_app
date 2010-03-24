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
        try:
            con = cx_Oracle.Connection('ontologies/odyssey$@microbiome1.colorado.edu/microbe')
            return con
        except Exception, e:
            print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
            return False;

    def getTestDatabaseConnection(self):
        """ Obtains a connection to the qiime_test schema

        Get a database connection. Note that the consumer is responsible 
        for closing this connection once obtained. This method is intended
        to be used internally by this class.
        """
        try:
            con = cx_Oracle.Connection('qiime_test/odyssey$@microbiome1.colorado.edu/microbe')
            return con
        except Exception, e:
            print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
            return False;

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
                study_name_list.append(row[0])
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
                
    def createQueueJob(self, user_id):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
            job_id=0
            job_id=con.cursor().callproc('create_queue_job', [user_id, job_id])
            return job_id[1]
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
                list_item = row[0], row[1], row[2]
                column_dictionary.append(list_item)
            return column_dictionary
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if (con):
                con.cursor().close()
                con.close()
