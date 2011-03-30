
"""
Functions for page of same name
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from data_access_connections import data_access_factory
from enums import ServerConfig
import os

def exportStudyToMGRAST(study_id, user_id):
    # Instantiate one copy of data access for this process
    data_access = data_access_factory(ServerConfig.data_access_type)

    # Submit the job
    job_id = data_access.createTorqueJob('ExportToMGRASTHandler', 'StudyID=%s' % study_id, user_id, study_id)
    
    # Make sure a legit job_id was created. If not, inform the user there was a problem
    if job_id < 0:
        raise Exception('There was an error creating the job. Please contact the system administrator.')
