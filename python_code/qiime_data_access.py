
__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"


#/bin/env python
"""
Centralized database access for the Qiime web app
"""

import cx_Oracle
from crypt import crypt
from data_access import AbstractDataAccess

class MockQiimeDataAccesss( AbstractDataAccess ):
    """ 
    The mock data access class for unite testing.
    """

    def __init__(self):
        pass

    def getDatabaseConnection(self):
        pass

    def authenticateWebAppUser(self, session, username, password, ip_addr, web_app_name):
        return True

class QiimeDataAccess( AbstractDataAccess ):
    """
    The actual implementation
    """

    def __init__(self):
        pass
	
    def getDatabaseConnection(self):
        """
        Get a database connection. Note that the consumer is responsible 
        for closing this connection once obtained. This method is intended
        to be used internally by this class.
        """
        try:
            con = cx_Oracle.Connection('qiime_production/odyssey$@microbiome1.colorado.edu/microbe')
            return con
        except Exception as e:
            print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
            return False;
	
    def authenticateWebAppUser( self, username, password ):
        """
        Attempt to authenticate the user against the list of users in
        web_app_user. 


factor out call to database. generic method that passes in name of proc, list of params, then returns both cursor and output params. put this in
	generic data access, move all qiime data access to the qiime svn proj. 
        """
        try:
            crypt_pass = crypt( password, username )
            con = self.getDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('authenticate_user', [username, crypt_pass, user_data] )
            row = user_data.fetchone()
            if ( row ):
                user_data = {'web_app_user_id':row[0], 'email':row[1], 'password':row[2], 'is_admin':row[3], 'is_locked':row[4], 'last_login':row[5]}
                return user_data
            else:
                return False
        except Exception as e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        finally:
            if (con):
                con.cursor().close()
                con.close()


