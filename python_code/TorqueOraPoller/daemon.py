#!/usr/bin/env python

from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Jesse Stombaugh", "Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Pre-release"

""" 
This code is from \ http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ 
"""

import sys, os, time, atexit
from signal import SIGTERM 
from subprocess import Popen, PIPE

# When stopping, try killing for 30 seconds
KILL_TIMEOUT = 30

class Daemon(object):
    """A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/tmp/daemon_stdout', 
                 stderr='/tmp/daemon_stderr'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def daemonize(self):
        """Unix double-fortk magic to daemonize
        
        see Stevens' "Advanced Programming in the UNIX Environment" for 
        details (ISBN 0201563177)

        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno,e.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno,e.strerror))
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    
    def delpid(self):
        os.remove(self.pidfile)

    def _get_pid_from_file(self):
        """Get PID from file 
        
        return None if no pid file 
        return -1 if unable to read pid file
        """
        # Check for a pidfile to see if the daemon already runs
        pid = None
        if os.path.isfile(self.pidfile):
            pf = open(self.pidfile)
            try:
                pid = int(pf.read().strip())
            except IOError:
                pid = -1
        return pid

    def start(self):
        """
        Start the daemon
        """
        pid = self._get_pid_from_file()
        if pid is not None:
            if pid == -1:
                message = "pidfile %s exists, unable to read PID.\n"
                sys.stderr.write(message % self.pidfile)
                sys.exit(1)
            else:
                message = "pidfile %s with PID %d already exists.\n"
                sys.stderr.write(message % (self.pidfile, pid))
                sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        pid = self._get_pid_from_file()
        
        if pid is None:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        elif pid == -1:
            message = "pidfile %s exists but cannot read it.\t"
            sys.stderr.write(message % self.pidfile)
            return # error?? what would this mean?

        for i in range(KILL_TIMEOUT):
            all_pids = self._get_process_list()
            if pid not in all_pids:
                break

            # its possible the kill from the previous iteration was delayed
            # and the processs terminated between the all_pids population and
            # the try block. Any other OSError is considered bad
            try:
                os.kill(pid, SIGTERM)
            except OSError, err:
                if err.find("No such process") > 0:
                    break
                else:
                    print str(err)
                    sys.exit(1)

            time.sleep(1)

        all_pids = self._get_process_list()
        if pid in all_pids:
            raise OSError, "Time out reached! Cannot kill daemon pid %d" % pid
        
        try:
            self.delpid()
        except:
            raise IOError, "Unable to remove pidfile %s!" % self.pidfile

    def _get_process_list(self):
        """returns a set of PIDs"""
        if 'posix' != os.name:
            raise OSError, "Windows sucks"
        if os.path.exists('/proc'):
            return self._get_process_list_linux()
        else:
            return self._get_process_list_osx()

    def _get_process_list_linux(self):
        """grab all PIDs from the /proc dir""" 
        # taken from http://stackoverflow.com/questions/2703640/process-list-on-linux-via-python
        return set([int(pid) for pid in os.listdir('/proc/') if pid.isdigit()])

    def _get_process_list_osx(self):
        """grab all PIDs from ps"""
        procs = Popen(['ps','aux'], shell=False, stdout=PIPE)
        o, e = procs.communicate()
        o = o.splitlines()

        # idx 1 is PID, skip the first line as it is header
        return set([int(proc.split()[1]) for proc in o[1:]]) 

    def restart(self):
        """Restart the daemon"""
        self.stop()
        self.start()

    def run(self):
        """Method called on daemon start or restart"""
        raise NotImplementedError
