#!/usr/bin/env python
# encoding: utf-8
"""
test_metadata_table.py

Created by Doug Wendel on 2010-02-05.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

import unittest
from metadata_table import *
from data_access_connections import data_access_factory
from enums import ServerConfig

# Callback for invalid rows
def is_invalid(column_name, row_index):
    return column_name, row_index

# Global data access
qda = data_access_factory(ServerConfig.data_access_type)

class MetadtaTableTests(unittest.TestCase):
    """ Unit tests for the MetadataTable and related classes
    """
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    ######################################################    
    # Tests for BaseColumn class
    ######################################################
    
    def test_BaseColumnCreate(self):        
        base_column = BaseColumn('depth', is_invalid, True)
        self.assertTrue(base_column)
        self.assertTrue(base_column.column_name)
        self.assertTrue(base_column.is_invalid, True)

    ######################################################    
    # Tests for RegEx column class
    ######################################################
    
    def test_RegExColumnCreate(self):
        regex = '^y$|^Y$|^n$|^N$'
        reg_ex_column = RegExColumn('test_name', is_invalid, True, regex)
        self.assertTrue(reg_ex_column)

    def test_AddRegExColumnCreate(self):
        regex = '^y$|^Y$|^n$|^N$'
        reg_ex_column = RegExColumn('test_name', is_invalid, True, regex)
        reg_ex_column._addValue('y', qda, True)
        self.assertTrue(len(reg_ex_column.values) == 1)
        
    ######################################################    
    # Tests for ColumnFactory class
    ######################################################

    def test_ColumnFactoryCreate(self):
        factory = ColumnFactory(is_invalid, qda)
        self.assertTrue(factory)

    def test_ColumnFactoryCreateNumeric(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('depth', 'numeric', 4000, 0, True)
        self.assertTrue(column)
        
    def test_ColumnFactoryCreateNotInDictionary(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('xyz', 'text', 4000, 0, False)
        self.assertTrue(column)

if __name__ == '__main__':
    unittest.main()


