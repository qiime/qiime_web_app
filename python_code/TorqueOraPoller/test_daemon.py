#!/usr/bin/env python

from daemon import Daemon, sys
from time import sleep

class TestDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        self.interval = 0
        super(TestDaemon, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            self.interval += 1
            sleep(5)
            print self.interval

            sys.stdout.flush()
            sys.stderr.flush()
if __name__ == '__main__':
    daemon = TestDaemon('/tmp/testdaemon.pid',
            stdout='/tmp/testdaemon.stdout',
            stderr='/tmp/testdaemon.stderr')

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        else:
            print "needs start or stop"
            sys.exit(2)
    else:
        print "wtf... gimme a start or stop"
