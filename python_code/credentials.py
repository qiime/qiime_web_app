"""
Factored credentials - should never be checked into source control on github
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2012, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

class Credentials(object):
    """ A collection of credential values
    """
    
    liveMetadataDatabaseConnectionString = 'qiime_metadata/m_t_d_t_@thebeast.colorado.edu/thebeast'
    liveOntologyDatabaseConnectionString = 'ontologies/odyssey$@thebeast.colorado.edu/thebeast'
    liveSFFDatabaseConnectionString = 'SFF/SFF454SFF@thebeast.colorado.edu/thebeast'
    
    testMetadataDatabaseConnectionString = 'qiime_metadata/m_t_d_t_@webdev.microbio.me:1521/dbdev'
    testOntologyDatabaseConnectionString = 'ontologies/odyssey$@webdev.microbio.me:1521/dbdev'
    testSFFDatabaseConnectionString = 'SFF/SFF454SFF@webdev.microbio.me:1521/dbdev'