#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"
 
from data_access_connections import data_access_factory
from enums import ServerConfig
from cogent.util.unit_test import TestCase, main
from live_ebi_sra_rest_services import LiveEBISRARestServices

class Tests(TestCase):
    
    def setUp(self):
        """ Setup
        """
        self.study_id = 717
        self.web_app_user_id = 12169

    def tearDown(self):
        """ Clean up
        """
        pass

    def test_instantiate_object(self):
        """ Test instantiation of base services
        """
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id)
        self.assertNotEqual(live, None)

    def test_live_values(self):
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id)
        self.assertIsNotNone(live.hostname)
        self.assertIsNotNone(live.study_url)
        self.assertIsNotNone(live.sample_url)
        self.assertIsNotNone(live.library_url)
        self.assertIsNotNone(live.sequence_url)
        self.assertIsNotNone(live.key)
        self.assertIsNotNone(live.study_id)
        self.assertIsNotNone(live.web_app_user_id)

    def test_send_post_data(self):
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id)
        live.host_name = ''
        
        file_contents = 'I am the file contents'
        url_path = '/the/url/path'
        debug = True
        
        success, entity_id = live.send_post_data(url_path, file_contents, debug)
        self.assertIsNotNone(success)

    def test_generate_metadata_files(self):
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id)
        live.host_name = ''
        live.generate_metadata_files(debug = True)

if __name__ == "__main__":
    main()