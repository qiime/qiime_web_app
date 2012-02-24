#!/usr/bin/env python

"""QIIME-webapp poller

Every interval period we query a jobs table in the database to see if there are any
new jobs to be submitted. Submitted jobs are also monitored during this interval
period. Status is updated internally and in the database table
"""

# we import sys from daemon as to not void stdout/stderr redirection
from daemon import Daemon, sys
from commands import getoutput
import os
from time import sleep
import cx_Oracle
from handler import *
from enums import ServerConfig,DataAccessType
from data_access_connections import data_access_factory

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@@colorado.edu"
__status__ = "Pre-release"

POLL_INTERVAL = 5
STATUS_INTERVAL = 12
QSTAT_NORMAL = "/usr/bin/qstat | grep %s"
QSUB_CMD = 'echo "%s" | /usr/bin/qsub -k oe -N %s -l pvmem=%s -q %s'

TORQUE_STATE_LOOKUP = {'R':'RUNNING',
                       'C':'COMPLETING',
                       'E':'EXITING',
                       'Q':'QUEUED',
                       'H':'HALTED'}
JOB_TYPE_LOOKUP = {'PollerTestHandlerOkay':PollerTestHandlerOkay,
                   'PollerTestHandlerErr':PollerTestHandlerErr,
                   'ProcessSFFHandler':ProcessSFFHandler,
                   'ProcessPickOTUHandler':ProcessPickOTUHandler,
                   'LoadOTUMappingHandler':LoadOTUMappingHandler,
                   'TestLoadOTUMappingHandler':TestLoadOTUMappingHandler,
                   'TestLoadSFFAndMetadataHandler':TestLoadSFFAndMetadataHandler,
                   'LoadSFFAndMetadataHandler':LoadSFFAndMetadataHandler,
                   'makeMappingAndOTUFiles':makeMappingAndOTUFiles,
                   'makeMappingFileandPCoAPlots':makeMappingFileandPCoAPlots,
                   'ExportToMGRASTHandler':ExportToMGRASTHandler,
                   'ExportToEBISRAHandlerHandler':ExportToEBISRAHandler,
                   'generateMapOTUTableSubmitJobs':generateMapOTUTableSubmitJobs,
                   'betaDiversityThroughPlots':betaDiversityThroughPlots,
                   'makeOTUHeatmap':makeOTUHeatmap,
                   'alphaRarefaction':alphaRarefaction,
                   'summarizeTaxa':summarizeTaxa,
                   'LoadSFFHandler':LoadSFFHandler,
                   'generateMapSubmitJobs':generateMapSubmitJobs}
                   

class FileDoesNotExistError(IOError):
    pass
class CannotOpenFileError(IOError):
    pass

class Poller(Daemon):
    """Polls TORQUE_JOBS for new jobs, submits, updates status"""
    def __init__(self, *args, **kwargs):
        self.data_access=data_access_factory(ServerConfig.data_access_type)
        self.username = os.environ['USER']
        self.home = os.environ['HOME']
        self.Jobs = {} # pbs job id -> job object
        self.interval = 0
        super(Poller, self).__init__(*args, **kwargs)

    def run(self):
        """This method is called when the daemon is started

        First we check for an event. An event might be to provide a status
        update. Event handling is not in place, but mocked out

        Second, check for new jobs. If there are new jobs, we start them

        Third, update job status
        """
        self.con = self.data_access.getSFFDatabaseConnection()
        iter_count = 0

        while True:
            sleep(POLL_INTERVAL)
            iter_count += 1

            # basic event handling
            event = self.checkForEvent()
            if event:
                self.handleEvent(event)

            # check for new jobs, start if necessary
            new_jobs = self.checkForNewJobs()
            err_jobs = []
            if new_jobs:
                err_jobs = self.submitJobs(new_jobs)

            # update job status, including jobs that failed to start
            self.updateMyJobs(err_jobs)

            # every once and a while dump status
            if iter_count % STATUS_INTERVAL == 0:
                # do we want to "save" state to a file incase of crash?
                sys.stdout.write("Status update: \n")
                job_status = map(str, self.Jobs.values())
                sys.stdout.write('\n'.join(job_status))
                sys.stdout.write('\n')

            # flush each cycle
            sys.stderr.flush()
            sys.stdout.flush()

    def checkForEvent(self):
        """Undefined right now, add for possible communication extension"""
        return None
  
    def handleEvent(self, event):
        """Handles an event"""
        raise NotImplementedError

    def parseQstat(self, input):
        """Parse qstat lines, return job_id -> state"""
        poll_result = {}
        for line in input.splitlines():
            job_id, job_name, user, cput, state, queue = line.strip().split()
            pbs_job_id = job_id.split('.',1)[0]
            poll_result[pbs_job_id] = TORQUE_STATE_LOOKUP[state]
        return poll_result

    def _readfile(self, home, job_name, pbs_job_id, filetype):
        """Returns lines from a file or raises if error
        
        Raises IOError if an incorrect filetype is specified
        Raises FileDoesNotExistError if the file does not exist
        Raises CannotOpenFileError if unable to open a file
        """
        
        # construct expected filename
        if filetype == 'stdout':
            filename = '%s/%d.o%s' % (home, job_name, pbs_job_id)
        elif filetype == 'stderr':
            filename = '%s/%d.e%s' % (home, job_name, pbs_job_id)
        else:
            raise IOError, "Unknown filetype"

        # check if the file actually exists
        if not os.path.isfile(filename):
            raise FileDoesNotExistError, "File %s does not exist"

        # if it exists, attempt to open
        try:
            lines = open(filename).readlines()
        except:
            raise CannotOpenFileError, "Unable to open %s"

        return lines

    def _job_completed_or_errored(self, job):
        """Check err status"""
        job_name = job.OracleJobName
        pbs_id = job.getTorqueJobId()
    
        # try to read stdout
        try:
            stdout_lines = self._readfile(self.home, job_name, pbs_id, 'stdout')
        except IOError, e:
            sys.stderr.write('Job %s errored out with %s\n' % (job_name, e))
            return 'COMPLETED_ERROR'

        # try to read stderr
        try:
            stderr_lines = self._readfile(self.home, job_name, pbs_id, 'stderr')
        except IOError, e:
            sys.stderr.write('Job %s errored out with %s\n' % (job_name, e))
            return 'COMPLETED_ERROR'
 
        err = job.checkJobOutput(stdout_lines, stderr_lines)

        if err:
            sys.stderr.write('Job %s errored out\n' % job_name)
            exit_status = 'COMPLETED_ERROR'
        else:
            sys.stdout.write('Job %s completed successfully\n'% job_name)
            exit_status = 'COMPLETED_OKAY'
            
            # Check for next job in chain. If so, call it
            if job._next_job_handler:
                pass
                
        return exit_status

    def updateMyJobs(self, err_jobs):
        """Checks known jobs, updates state, deletes job if completed
        
        err_jobs contains error information from jobs that failed to start
        """
        output = getoutput(QSTAT_NORMAL % self.username)
        poll_result = self.parseQstat(output)
        completed_job_ids = []
        
        state_feedback = [(ej, 'ERROR_STARTING') for ej in err_jobs]
        for pbs_id, job in self.Jobs.items():
            if pbs_id not in poll_result:
                # job is no longer visible by resource manager
                new_state = self._job_completed_or_errored(job)
                job.updateJobState(new_state)
                job.removeTorqueJobId()
                completed_job_ids.append(pbs_id)
            else:
                # job is visible by resource manager
                new_state = poll_result[pbs_id]
                if job.getJobState() == new_state:
                    continue
                job.updateJobState(new_state)
                
            job_name = job.OracleJobName
            job_notes = job.getJobNotes()
            state_feedback.append((job_name, new_state, job_notes))
        
        # communicate back with ora table
        if state_feedback:
            cur = self.con.cursor()
            for job_name, new_state, notes in state_feedback:
                # the job_notes column is varchar2, limit to last 4000 chars...
                proc_args = [job_name, new_state, job_notes[-4000:]]
                cur.callproc('update_torque_job', proc_args)
            self.con.commit()
            cur.close()

        # remove completed jobs
        for pbs_id in completed_job_ids:
            del self.Jobs[pbs_id]

    def checkForNewJobs(self):
        """Call SFF.get_torque_jobs stored proc"""
        cursor = self.con.cursor()
        jobs_cursor = self.con.cursor()
        cursor.callproc('get_new_torque_jobs',[jobs_cursor])

        new_jobs = jobs_cursor.fetchall()
        cursor.close()
        jobs_cursor.close()

        return new_jobs

    def submitJobs(self, jobs):
        """Submits a single job, updates self.Jobs"""
        err_jobs = set([])
        for job_name, job_type, job_args in jobs:
            job_handler = JOB_TYPE_LOOKUP.get(job_type, None)
            
            if job_handler is None:
                sys.stderr.write("Unknown job type %s for job %s\n" % \
                        (job_type, job_name))
                err_jobs.add(job_name)
                continue
            
            job = job_handler(job_name, job_args)
            cmd = job()
            sys.stdout.write('Job command: %s' % cmd)
           
            #### decompose job submission
            # submit job - if loading into DB use singleq
            if job_type=='LoadSFFHandler':
                submit_queue = 'singleq'
                pvmem='8gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            elif job_type=='ProcessSFFHandler':
                submit_queue = 'no_bad_touching'
                pvmem='8gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            elif job_type=='betaDiversityThroughPlots':
                submit_queue = 'no_bad_touching'
                pvmem='4gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            elif job_type=='makeOTUHeatmap':
                submit_queue = 'no_bad_touching'
                pvmem='4gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            elif job_type=='alphaRarefaction':
                submit_queue = 'no_bad_touching'
                pvmem='4gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            elif job_type=='summarizeTaxa':
                submit_queue = 'no_bad_touching'
                pvmem='4gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            elif job_type=='generateMapOTUTableSubmitJobs':
                submit_queue = 'no_bad_touching'
                pvmem='64gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            else:
                submit_queue = 'no_bad_touching'
                pvmem='8gb'
                res = getoutput(QSUB_CMD % (cmd, job_name,pvmem,submit_queue))
            
            res_lines = res.splitlines()

            if len(res_lines) == 0 or len(res_lines) > 1:
                # job did not start
                err_jobs.add(job_name)
                sys.stderr.write('Unable to start %s\n\tError:%s\n' % \
                        (cmd, res))
            else:
                # job started
                pbs_id = res_lines[0].split('.',1)[0]
                job.setTorqueJobId(pbs_id, 'NEW')
                self.Jobs[pbs_id] = job
                    
                sys.stdout.write('Started PBS job id %s, ORA job id %d\n' %\
                        (pbs_id, job_name))

        return list(err_jobs)

if __name__ == '__main__':
    daemon = Poller('/tmp/qiime-webapp-poller.pid',
                    stdout='/tmp/qiime-webapp-poller.stdout',
                    stderr='/tmp/qiime-webapp-poller.stderr')

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

