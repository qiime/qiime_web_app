__author__ = "Zhenjiang Xu"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Jesse Stombaugh", "Doug Wendel", "Zhenjiang Xu"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

"""
This script is the upload handler for uploading metadata files using JumpLoader'
"""

from data_access_connections import data_access_factory
from enums import ServerConfig
from commands import getoutput
import re

# Get a copy of data_acess
data_access = data_access_factory(ServerConfig.data_access_type)

def clearJob(job_id, queue_content):
    # Clear the job from the database
    data_access.clearTorqueJob(job_id)
    result = ''

    # Clear the job from the torque queue
    prev_item = ''
    torque_job_id = ''

    for line in queue_content.splitlines()[2:]: # skip header and --- line
        fields = line.strip().split()

        if fields[1] == str(job_id):
            torque_job_id = fields[0]

    if torque_job_id != '':
        clear_cmd = 'qdel %s' % torque_job_id
        result = getoutput(clear_cmd)

    return result

def clearJobs(job_locator_id,  job_type_ids):
    """
    Clear all the jobs for the types of jobs listed in tuple job_type_ids.
    job_locator_id is either a study_id or meta_analysis_id.
    """
    results = []
    queue_content = getoutput('qstat')
    for jobid in job_type_ids:
        #req.write('<p/>looking up jobs<p/>')
        jobs = data_access.getJobInfo(job_locator_id, jobid)
        #req.write('<p/>jobs: %s<p/>' % str(jobs))
        if not jobs:
            continue
        for job in jobs:
            # Clear the job
            results.append(clearJob(job['job_id'], queue_content))

    from time import sleep
    sleep(5)
    return results

