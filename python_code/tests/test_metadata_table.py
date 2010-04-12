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

# Callback functions
def validate(value):
    if value == 10:
        return True
    else:
        return False
        
def isInvalid(column_name, row_index):
    return column_name, row_index

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
        baseColumn = BaseColumn('depth', validate, isInvalid)
        self.assertTrue(baseColumn)
        self.assertTrue(baseColumn.column_name)
        self.assertTrue(baseColumn.validate)
        self.assertTrue(baseColumn.isInvalid)

    def test_BaseColumnValidate(self):
        baseColumn = BaseColumn('depth', validate, isInvalid)
        self.assertTrue(baseColumn.validate(10))
        self.assertFalse(baseColumn.validate(9))

    def test_AddBaseColumnValue(self):
        baseColumn = BaseColumn('depth', validate, isInvalid)
        baseColumn.addValue(10)
        self.assertTrue(len(baseColumn.values) == 1)
        
    def test_AddValidBaseColumnValue(self):
        baseColumn = BaseColumn('depth', validate, isInvalid)
        baseColumn.addValue(10)
        self.assertTrue(len(baseColumn._invalid_indicies) == 0)

    def test_AddInvalidBaseColumnValue(self):
        baseColumn = BaseColumn('depth', validate, isInvalid)
        baseColumn.addValue(9)
        self.assertTrue(len(baseColumn._invalid_indicies) == 0)

    ######################################################    
    # Tests for ColumnFactory class
    ######################################################

    def test_ColumnFactoryCreate(self):
        factory = ColumnFactory(isInvalid)
        self.assertTrue(factory)

    def test_ColumnFactoryCreateNumeric(self):
        factory = ColumnFactory(isInvalid)
        column = factory.createColumn('depth', 'numeric')
        self.assertTrue(column)

    ######################################################    
    # Tests for MetaddataTable class
    ######################################################

    def test_MetadataTableCreate(self):
        template_id = 1
        #table = MetadataTable(template_id, 'tests/test_data.xls')
        table = MetadataTable(template_id, 'tests/test_data.xls')
        self.assertTrue(table)
        
    #def test_VerifyMetadataColumns(self):
    #    template_id = 1
    #    table = MetadataTable(template_id, 'tests/test_data.xls')
    #    self.assertEqual(len(table._columns), 2)



if __name__ == '__main__':
    unittest.main()


