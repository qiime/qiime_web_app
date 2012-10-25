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
    # Tests for ColumnFactory class
    ######################################################

    def test_ColumnFactoryCreate(self):
        factory = ColumnFactory(is_invalid, qda)
        self.assertTrue(factory)
    
    ######################################################    
    # Tests for RegEx column class
    ######################################################
    
    def test_NumericColumnCreate(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('depth', 'numeric', 8000, 0, True)
        self.assertTrue(column)
        
    def test_NumericColumnWriteJSValidation(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('depth', 'numeric', 8000, 0, True)
        validation_text = column.writeJSValidation()
        self.assertTrue(validation_text)
        
    ######################################################    
    # Tests for List column class
    ######################################################    

    def test_ListColumnCreate(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('age', 'list', 8000, 0, True)
        self.assertTrue(column)
        
    def test_ListColumnWriteJSValidation(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('age', 'list', 8000, 0, True)
        validation_text = column.writeJSValidation()
        self.assertTrue(validation_text)  
    
    ######################################################    
    # Tests for Ontology column class
    ######################################################
    
    def test_OntologyColumnCreate(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('country', 'ontology', 8000, 0, True)
        self.assertTrue(column)
        
    def test_OntologyColumnWriteJSValidation(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('country', 'ontology', 8000, 0, True)
        validation_text = column.writeJSValidation()
        self.assertTrue(validation_text)
    
    ######################################################    
    # Tests for Text column class
    ######################################################

    def test_TextColumnCreate(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('project_name', 'text', 8000, 0, True)
        self.assertTrue(column)
        
    def test_TextColumnWriteJSValidation(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('project_name', 'text', 8000, 0, True)
        validation_text = column.writeJSValidation()
        self.assertTrue(validation_text)

    ######################################################    
    # Tests for columns not in dictionary
    ######################################################
        
    def test_ColumnFactoryCreateNotInDictionary(self):
        factory = ColumnFactory(is_invalid, qda)
        column = factory.createColumn('xyz', 'text', 8000, 0, False)
        self.assertTrue(column)
        

if __name__ == '__main__':
    unittest.main()


