#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

import sys
import httplib, urllib

# Variables that describe where the data is going
url_path = '/r/cv/23'
host = '192.168.56.101'
file_contents = """
{
	"vocabulary_name":"Coffee Side Effects",
	"side_effects":["The Jitters", "Real Sense of Euphoria", "Invincibility"]
}
"""

debug = True
success = None
entity_id = None

# Output the file contents if debug mode is set
if debug:
    print 'File Contents: "{0}"'.format(file_contents)
    print 'Host: %s' % host
    print 'Service URL: %s' % url_path

# Submit file data
#headers = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/xml", "User-Agent":"qiime_website"}
headers = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/html", "User-Agent":"qiime_website"}
conn = httplib.HTTPConnection(host)
conn.request(method = "POST", url = url_path, body = file_contents, headers = headers)
response = conn.getresponse()
data = response.read()
print '\n\nRequest output:\n\n{0}'.format(str(data))

"""
print '==============================================='

print 'Response data is: ' + data
print 'Connecting to poll url...'
url_path = data

conn.request(method = "GET", url = url_path, body = file_contents, headers = headers)
response = conn.getresponse()
data = response.read()

print data

conn.close()

# Output the status and response if debug mode is set
if debug:
    print '\n\nDEBUG INFO'
    print response.status, response.reason
    print str(data)
    print 'END DEBUG INFO\n\n'

"""
