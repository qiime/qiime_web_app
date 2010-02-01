#!/usr/bin/env python

"""
Unit tests for qiime_data_access.py
"""

import unittest
from qiime_data_access import QiimeDataAccess

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

class QiimeDataAccessTests(unittest.TestCase):
	"""Unit tests for the QiimeDataAccess class
	
	QiimeDataAccess unit tests. These tests are designed to validate that
	the various database functions work and return expected values.
	"""
	
	# Global variables required for all tests
	_qiime_data_access = None

	# Set up and tear downdown
	def setUp(self):
		global _qiime_data_access
		_qiime_data_access = QiimeDataAccess()
		
	def tearDown(self):
		pass
		
	# The rest of the unit tests
	def test_getDatabaseConnection(self):
		global _qiime_data_access
		con = _qiime_data_access.getDatabaseConnection()
		self.assertTrue(con)
		con.close()

	def test_authenticateWebAppUser(self):
		global _qiime_data_access
		result = _qiime_data_access.authenticateWebAppUser('asdf', '1234')
		self.assertFalse(result)
		#user_info = result = _qiime_data_access.authenticateWebAppUser('', '')
		#self.assertTrue(type(user_info).name == 'dict')

if __name__ == '__main__':
	unittest.main()
