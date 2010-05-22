#!/usr/bin/env python
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, Qiime Web Analysis"
__credits__ = ["Jesse Stombaugh","Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Jesse Stombaugh"]
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Production"

"""
Centralized database access for the Qiime web app
"""

import cx_Oracle
from crypt import crypt
from data_access import AbstractDataAccess

class OntologyDataAccess( AbstractDataAccess ):
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
            con = cx_Oracle.Connection('ontologies/odyssey$@microbiome1.colorado.edu/microbe')
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
                user_data = {'web_app_user_id':row[0], 'email':row[1], \
                'password':row[2], 'is_admin':row[3], 'is_locked':row[4], \
                'last_login':row[5]}
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

                
    def get_list_of_ontologies(self):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getDatabaseConnection()
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

    
    def get_ontology_terms(self, ontology,query):
        """ Returns a list of ontology terms if the term contains query as a
            substring.
        """
        try:
            con = self.getDatabaseConnection()		
            column_values = con.cursor()
            con.cursor().callproc('get_ontology_terms', [ontology, query, \
                                                            column_values])
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
            con = self.getDatabaseConnection()		
            column_values = con.cursor()
            con.cursor().callproc('validity_of_ontology_term', [ontology, \
                                                        query, column_values])
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