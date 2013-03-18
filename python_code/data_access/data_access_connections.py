
"""
Connection classes for data access classes
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

import cx_Oracle
from qiime_data_access import QiimeDataAccess
from ag_data_access import AGDataAccess
from enums import ServerConfig, DataAccessType
from credentials import Credentials

def data_access_factory(data_access_type, class_type='qiime'):
    """
    Factory method for returning the appropriate data access type. By defalt returns
    the 'qiime' data_access_type, but you can request other data access types for
    specific purposes.
    """

    connections = None
    
    if data_access_type == DataAccessType.qiime_production:
        connections = QiimeDataAccessConnections()
    elif data_access_type == DataAccessType.qiime_test:
        connections = TestDataAccessConnections()
    
    # Throw an exception if the type could not be determined
    if not connections:
        raise TypeError('Could not determine data access type.')
    
    if class_type == 'qiime':
        return QiimeDataAccess(connections)
    elif class_type == 'american_gut':
        return AGDataAccess(connections)
    
class AbstractDataAccessConnections(object):
    """
    Abstract implementation of the data access connections.
    
    The AbstractDataAccessConnections class templates the connections for other uses (live, test, etc...). 
    The only functional code is the destructor which closes any open database connections when teh object
    goes out of scope.
    """
    
    #####################################
    # Connections
    #####################################
    
    def __init__(self):
        self._metadataDatabaseConnection = None
        self._metadataDatabaseConnectionString = ''
        
        self._ontologyDatabaseConnection = None
        self._ontologyDatabaseConnectionString = ''
        
        self._SFFDatabaseConnection = None
        self._SFFDatabaseConnectionString = ''
        
    def getMetadataDatabaseConnection(self):
        """ Obtains a connection to the qiime_production schema

        Get a database connection for the qiime
        """
        
        if self._metadataDatabaseConnection == None:
            self._metadataDatabaseConnection = cx_Oracle.Connection(self._metadataDatabaseConnectionString, cclass='qiime')
                
        return self._metadataDatabaseConnection

    def getOntologyDatabaseConnection(self):
        """ Obtains a connection to the ontologies schema

        Get a database connection.
        """
        if self._ontologyDatabaseConnection == None:
            try:
                self._ontologyDatabaseConnection = cx_Oracle.Connection(self._ontologyDatabaseConnectionString)
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;

        return self._ontologyDatabaseConnection

    def getSFFDatabaseConnection(self):
        """ Obtains a connection to the SFF schema

        Get a database connection. 
        """
        if self._SFFDatabaseConnection == None:
            try:
                self._SFFDatabaseConnection = cx_Oracle.Connection(self._SFFDatabaseConnectionString)
            except Exception, e:
                print 'Exception caught: %s. \nThe error is: %s' % (type(e), e)
                return False;

        return self._SFFDatabaseConnection
        

class QiimeDataAccessConnections(AbstractDataAccessConnections):
    """
    The live implementation of the data access connections
    
    This class implements the abstract methods of the partent class for the live environment
    """

    #####################################
    # Connections
    #####################################

    def __init__(self):
        # Set up the initial values
        super(QiimeDataAccessConnections, self).__init__()
        
        # Now define the actual connection strings
        self._metadataDatabaseConnectionString = Credentials.liveMetadataDatabaseConnectionString
        self._ontologyDatabaseConnectionString = Credentials.liveOntologyDatabaseConnectionString
        self._SFFDatabaseConnectionString = Credentials.liveSFFDatabaseConnectionString

class TestDataAccessConnections(AbstractDataAccessConnections):
    """
    The test implementation of the data access connections

    This class implements the abstract methods of the partent class for the live environment
    """

    #####################################
    # Connections
    #####################################

    def __init__(self):
        # Set up the initial values
        super(TestDataAccessConnections, self).__init__()
        
        # Now define the actual connection strings
        self._metadataDatabaseConnectionString = Credentials.testMetadataDatabaseConnectionString
        self._ontologyDatabaseConnectionString = Credentials.testOntologyDatabaseConnectionString
        self._SFFDatabaseConnectionString = Credentials.testSFFDatabaseConnectionString
