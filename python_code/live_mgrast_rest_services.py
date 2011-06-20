#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

import httplib, urllib
from base_mgrast_rest_services import BaseMGRASTRestServices

class LiveMGRASTRestServices(BaseMGRASTRestServices):

    def send_data_to_mgrast(self, url_path, file_contents, host, debug):
        success = None
        entity_id = None
        
        # Output the file contents if debug mode is set
        if debug:
            if len(file_contents) < 10000:
                print file_contents
            print 'Host: %s' % host
            print 'Service URL: %s' % url_path
    
        # Submit file data
        headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
        conn = httplib.HTTPConnection(host)
        conn.request(method = "POST", url = url_path, body = file_contents, headers = headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    
        # Output the status and response if debug mode is set
        if debug:
            print response.status, response.reason
            print str(data)

        # Check for success
        if '<success>0</success>' in data:
            success = False
        elif '<success>1</success>' in data:
            success = True
    
        # Look for a returned identifier in the data
        if '<project_id>' in data:
            entity_id = data[data.find('<project_id>')+len('<project_id>'):data.find('</project_id>')]
        elif '<sample_id>' in data:
            entity_id = data[data.find('<sample_id>')+len('<sample_id>'):data.find('</sample_id>')]

        return success, entity_id