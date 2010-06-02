#!/usr/bin/env python

from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Pre-release"

""" 
This Daemon manages the Qiime queue. It monitors SFF and metadata submission status and
fires off Qiime jobs when all elements are in place.
"""

import sys, time
from daemon import Daemon
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from qiime_data_access import *

class QueueDaemon(Daemon):
    def run(self):
        #server = SimpleXMLRPCServer(("localhost", 8000))
        #print 'Listening on port 8000...'
        #server.register_function(checkListValue, "checkListValue")
        #print 'Registered checkListValue...'
        #server.register_function(checkOntologyValue, "checkOntologyValue")
        #print 'Registered checkOntologyValue...'
        #print 'Starting service...'
        #server.serve_forever()
        
        data_access = QiimeDataAccess()
        
        while True:
            # Sleep...
            time.sleep(10)
            
            # Check the database queue for new jobs. Start a new job for each that
            # that is found with a status of 'new'
            for job_info in data_access.checkForNewJobs():
                # How will we fire this off on a new thread or simply offload to
                # another python instance? 
                self.startNewJob(job_info, data_access)
                
            # Next look for jobs that have already started but have not yet completed.
            # if a job has reported an error or has completed but the user has not yet
            # been notified (vie email probably), take the appropriate action and mark
            # job as completed (if successful) or failed (if not successful but done).
            #for job_info in qda.checkUnfinishedJobs():
            #    pass
    
    def startNewJob(self, job_info, data_access):
        data_access.updateJobStatus(job_info[0], 'started')

if __name__ == "__main__":
    daemon = QueueDaemon('/tmp/queue_daemon.pid')
    if len(sys.argv) == 2:
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

