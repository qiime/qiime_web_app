
"""
Centralized database access for the American Gut web portal
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
from threading import Lock
from time import sleep
import csv

class AGDataAccess(object):
    """
    Data Access implementation for all the American Gut web portal
    """
    
    def __init__(self, connections):
        self._metadataDatabaseConnection = None
        self._ontologyDatabaseConnection = None
        self._SFFDatabaseConnection = None
        
        # Set up the connections
        if not connections:
            raise ValueError('connections is None. Cannot instantiate QiimeDataAccess')
            
        self.getMetadataDatabaseConnection = connections.getMetadataDatabaseConnection
        self.getOntologyDatabaseConnection = connections.getOntologyDatabaseConnection
        self.getSFFDatabaseConnection = connections.getSFFDatabaseConnection
        
    #####################################
    # Helper Functions
    #####################################
    
    def testDatabase(self):
        """Attempt to connect to the database
        
        Attempt a database connection. Will throw an exception if it fails. Returns
        "True" if successful.
        """
        con = self.getMetadataDatabaseConnection()
        if con:
            return True
        
    def dynamicMetadataSelect(self, query_string):
        # Make sure no tomfoolery is afoot
        query_string_parts = set(query_string.lower().split())
        verboten = set(['insert', 'update', 'delete'])
        intersection = query_string_parts.intersection(verboten)
        if len(intersection) > 0:
            raise Exception('Only select statements are allowed. Your query: %s' % query_string)
        
        con = self.getMetadataDatabaseConnection()
        return con.cursor().execute(query_string)

    #####################################
    # Users
    #####################################

    def authenticateWebAppUser(self, username, password):
        """ Attempts to validate authenticate the supplied username/password
        
        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        #crypt_pass = crypt(password, username)
        con = self.getMetadataDatabaseConnection()
        user_data = con.cursor()
        con.cursor().callproc('ag_authenticate_user', [username, password, user_data])
        row = user_data.fetchone()
        if row:
            user_data = {'web_app_user_id':row[0], 'email':row[1], 'name':row[2], \
                'address':row[3], 'city':row[4], 'state':row[5], 'zip':row[6], \
                'country':row[7]}
            return user_data
        else:
            return False

    
    
