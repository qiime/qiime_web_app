#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from base_mgrast_rest_services import BaseMGRASTRestServices

class MockMGRASTRestServices(BaseMGRASTRestServices):

    def send_data_to_mgrast(self, url_path, file_contents, host, debug):
        success = True
        entity_id = 1
        
        return success, entity_id

