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
 

from cogent.util.unit_test import TestCase, main
from base_rest_services import BaseRestServices
from base_rest_services import RestDataHelper

class Tests(TestCase):
    
    def setUp(self):
        """ Setup
        """
        self.study_id = 717
        self.web_app_user_id = 12169
        self.helper = RestDataHelper(self.study_id, self.web_app_user_id)

    def tearDown(self):
        """ Clean up
        """
        pass

    def test_instantiate_object(self):
        """ Test instantiation of base services
        """
        base = BaseRestServices(self.study_id, self.web_app_user_id)
        self.assertNotEqual(base, None)

    def test_send_post_data(self):
        try:
            base = BaseRestServices(self.study_id, self.web_app_user_id)
            url_path = ''
            file_contents = ''
            host = ''
            debug = True
            base.send_post_data(url_path, file_contents, debug)
        except Exception, e:
            self.assertTrue('NotImplementedError' in str(type(e)))

    def test_base_values(self):
        base = BaseRestServices(self.study_id, self.web_app_user_id)
        self.assertEqual(base.hostname, None)
        self.assertEqual(base.study_url, None)
        self.assertEqual(base.sample_url, None)
        self.assertEqual(base.library_url, None)
        self.assertEqual(base.sequence_url, None)
        self.assertEqual(base.study_id, self.study_id)
        self.assertEqual(base.web_app_user_id, self.web_app_user_id)
        
    def test_get_study_info(self):
        study_info = self.helper.get_study_info()
        
        for key in study_info:
            if key == 'samples':
                samples = study_info[key]
                for sample in samples:
                    for sample_key in sample:
                        if sample_key == 'preps':
                            preps = sample[sample_key]
                            for prep in preps:
                                for prep_key in prep:
                                    print '-------- KEY: ' + str(prep_key)
                                    print '-------- VALUE: ' + str(prep[prep_key])
                        else:
                            print'---- KEY: ' + str(sample_key)
                            print '---- VALUE: ' + str(sample[sample_key])
                
            else:
                print 'KEY: ' + str(key)
                print 'VALUE: ' + str(study_info[key])

        self.assertIsNotNone(study_info)

	def test_ebi_controlled_vocab_lookup_nomatch(self):
		live = LiveEBISRARestServices(self.study_id, self.web_app_user_id, self.root_dir)
		controlled_vocabulary = live.existing_study_type
		search_term = 'asdf'
		results = live.controlled_vocab_lookup(controlled_vocabulary, search_term)
		self.assertIsNone(results)

	def test_ebi_controlled_vocab_lookup_other(self):
		live = LiveEBISRARestServices(self.study_id, self.web_app_user_id, self.root_dir)
		controlled_vocabulary = live.existing_study_type
		search_term = 'other'
		results = live.controlled_vocab_lookup(controlled_vocabulary, search_term)
		self.assertIsNotNone(results)

	def test_ebi_controlled_vocab_lookup_match(self):
		live = LiveEBISRARestServices(self.study_id, self.web_app_user_id, self.root_dir)
		controlled_vocabulary = live.existing_study_type
		search_term = 'Metagenomics'
		results = live.controlled_vocab_lookup(controlled_vocabulary, search_term)
		self.assertEqual(results, search_term)

if __name__ == "__main__":
    main()
    
    