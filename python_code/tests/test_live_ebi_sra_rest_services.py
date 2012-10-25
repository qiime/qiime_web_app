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
        # self.study_id = 717 # doug_test_study
        # self.study_id = 930 # bowers_Spatial_variability
        # self.study_id = 314 # bowers_storm_peak_air
        # self.study_id = 367 # Jesse_test
        self.study_id = 1026 # stahringer_colorado_twin_saliva
        # self.study_id = 850 # Global gut illumina
        # self.study_id = 621 # global gut metagenome
        # self.study_id = 939 # ECUAVIDA
        # self.study_id = 1031 # Alder_Fir_16S (EMP)
        self.study_id = 1566 # Residential_Kitchen_Microbiology

        self.web_app_user_id = 12169
        self.root_dir = '/home/wwwuser/user_data/studies'

    def tearDown(self):
        """ Clean up
        """
        pass

    def test_instantiate_object(self):
        """ Test instantiation of base services
        """
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id, self.root_dir)
        self.assertNotEqual(live, None)

    def test_live_values(self):
        root_dir = '/home/wwwuser/user_data/studies'
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id, self.root_dir)
        self.assertIsNotNone(live.hostname)
        self.assertIsNotNone(live.study_url)
        self.assertIsNotNone(live.sample_url)
        self.assertIsNotNone(live.library_url)
        self.assertIsNotNone(live.sequence_url)
        self.assertIsNotNone(live.key)
        self.assertIsNotNone(live.study_id)
        self.assertIsNotNone(live.web_app_user_id)

    #def test_send_post_data(self):
    #    live = LiveEBISRARestServices(self.study_id, self.web_app_user_id)
    #    live.host_name = ''
    #    
    #    file_contents = 'I am the file contents'
    #    url_path = '/the/url/path'
    #    debug = True
    #    
    #    success, entity_id = live.send_post_data(url_path, file_contents, debug)
    #    self.assertIsNotNone(success)

    def test_generate_metadata_files(self):
        debug = True
        live = LiveEBISRARestServices(self.study_id, self.web_app_user_id, self.root_dir, debug)
        live.host_name = ''
        #live.generate_metadata_files(debug = True, action_type = 'VALIDATE')
        live.generate_metadata_files(debug = True, action_type = 'ADD')
        #live.generate_metadata_files(debug = True, action_type = 'MODIFY')
        #live.submit_files(debug = True)
        pass

if __name__ == "__main__":
    main()
