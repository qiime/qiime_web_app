
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
Mock database access for the Qiime web app unit testing
"""

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

