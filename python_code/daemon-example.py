#!/usr/bin/env python

from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Pre-release"

""" 
This code is from \ http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ \

This is the script where we will access the Oracle QUEUE table and \
which jobs need to be processed and then the process will be called.
"""

import sys, time
from daemon import Daemon

class MyDaemon(Daemon):
    def run(self):
        
        while True:
            #This is where we will put are function calls
            time.sleep(1)
            file=open('/tmp/test.txt','a')
            file.write('Hello\n')
            file.close()

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
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

