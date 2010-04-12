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
The base code is from \ http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/ \

This Daemon manages controlled vocabularies used in the metadata validation process. Because the loading
times are orders of magnitude slower than lookups, a persistent object was created to maintain one instance
of each requested list. The lists are lazy-loaded on first request.
"""

import sys
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from daemon import Daemon
from qiime_data_access import *

class ListManagerDaemon(Daemon):
    _lists = []
    _ontologies = []

    def checkListValue(self, list_name, value):
        # Make sure list has been loaded
        if list_name not in self._lists:
            self._lists[list_name] = QiimeDataAccess().getListValues(list_name)

        # Check if values is in list
        if value in self._lists[list_name]:
            return True
        else:
            return False

    def checkOntologyValue(self, ontology_name, term):
        # Make sure ontology has been loaded
        if ontology_name not in self._ontologies:
            self._ontologies[ontology_name] = QiimeDataAccess().getOntologyValues(ontology_name)

        # Check if term is in ontology
        if term in self._ontologies[ontology_name]:
            return True
        else:
            return False
    
    def run(self):        
        #server = SimpleXMLRPCServer(("localhost", 8000))
        #print 'Listening on port 8000...'
        #server.register_function(checkListValue, "checkListValue")
        #print 'Registered checkListValue...'
        #server.register_function(checkOntologyValue, "checkOntologyValue")
        #print 'Registered checkOntologyValue...'
        #print 'Starting service...'
        #server.serve_forever()
        print 'running'
        

if __name__ == "__main__":
    daemon = ListManagerDaemon('./ListManagerDaemon.txt')
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
