#/bin/env python

"""
Classes to represent metadata table information
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from qiime_data_access import QiimeDataAccess
import re

class ColumnFactory(object):
    """ Factory class for producing metadata columns
    """
    
    def __init__(self, is_invalid):
        self._is_invalid = is_invalid

    def _columnExists(self, column_name):
        found = False
        column_detail_list = QiimeDataAccess().getColumnDictionary()
        for row in column_detail_list:
            if row[0].upper() == column_name:
                found = True
                break
                      
        return found

    def _getControlledVocabs(self, column_name, datatype):
        if datatype == 'list':
            return QiimeDataAccess().getControlledVocabs(column_name)
        elif datatype == 'ontology':
            return QiimeDataAccess().getOntologies(column_name)

    def createColumn(self, column_name, datatype, length, in_dictionary):
        """ Creates a column of the right type based on the column name
        """
        _column = None
        _controlled_vocab_list = None

        # Deterine if this column is associated with a list or ontology
        if datatype == 'list' or datatype == 'ontology':
            _controlled_vocab_list = self._getControlledVocabs(column_name, datatype)
            if _controlled_vocab_list == None:
                print 'Error: No controlled vocabulary or ontology found even though column is listed as ' + datatype + '.'
                return None
        
        # Create the appropriate type of column
        if datatype == 'numeric':
            regex = '^\-*[0-9]+$|^\-*[0-9]*\.[0-9]+$'
            _column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex)
        elif datatype == 'range':
            regex = '^((\-?[0-9]+)|(\-?[0-9]*\.[0-9]+))(\-((\-?[0-9]+)|(\-?[0-9]*\.[0-9]+)))?$'
            _column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex)
        elif datatype == 'yn':
            regex = '^y$|^Y$|^n$|^N$'
            _column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex)
        elif datatype == 'date':
            regex = '^((((((0?[13578])|(1[02]))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\-\/\s]?((0?[1-9])|([1-2][0-9]))))[\-\/\s]?\d{2}(([02468][048])|([13579][26])))|(((((0?[13578])|(1[02]))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\-\/\s]?((0?[1-9])|(1[0-9])|(2[0-8]))))[\-\/\s]?\d{2}(([02468][1235679])|([13579][01345789]))))(\s(((0?[1-9])|(1[0-9])|(2[0-3]))\:([0-5][0-9])((\s)|(\:([0-5][0-9])))))?$'
            _column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex)
        elif datatype == 'text':
            _column = TextColumn(column_name, self._is_invalid, in_dictionary, length)
        elif datatype == 'list':
            _column = ListColumn(column_name, self._is_invalid, in_dictionary, _controlled_vocab_list)
        elif datatype == 'ontology':
            _column = OntologyColumn(column_name, self._is_invalid, in_dictionary, _controlled_vocab_list)

        return _column

class BaseColumn(object):
    """ The base class for all column types in the metadata table. This class 
    implements common functionality for all column classes.
    """
    def __init__(self, column_name, is_invalid, in_dictionary):
        # Name of this column. Should be unique in MetadataTable object
        self.column_name = column_name
        
        # Callback to notify parent of an invalid value entry
        self.is_invalid = is_invalid
        
        # List of values in this column
        self.values = []
        
        # List of invalid indicies in this column
        self._invalid_indicies = []
        
        # RegEx validation string (if applicable)
        self.reg_exp = ''
        
        # Variable to store whether or not this column exists in the column dictionary
        self._in_dictionary = in_dictionary
    
    def _addValue(self, value, data_access):
        status = 'good'
        if not self._validate(value, data_access):
            status = 'bad'
            self.is_invalid(self.column_name, len(self.values))     
        self.values.append((value, status))

class RegExColumn(BaseColumn):
    """ RegExColumn implementation of BaseColumn class
    """
    def __init__(self, column_name, is_invalid, in_dictionary, regex):
        super(RegExColumn, self).__init__(column_name, is_invalid, in_dictionary)
        self.reg_exp = regex
        
    def writeJSValidation(self):
        function_string = 'validateRegExField(this, \'%s\', \'%s\')' % (self.column_name, self.reg_exp.replace('\\', '\\\\'))
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
        
    def _validate(self, value, data_access):
        """ return true if number, false otherwise
        """
        if re.match(self.reg_exp, value) == None:
            return False
        else:
            return True

class ListColumn(BaseColumn):
    """ List implementation of BaseColumn class
    """
    def __init__(self, column_name, is_invalid, in_dictionary, list_names):
        super(ListColumn, self).__init__(column_name, is_invalid, in_dictionary)
        self.list_names = list_names
        
    def _addValue(self, value, data_access):
        status = 'good'
        if not self._validate(value, self.list_names, data_access):
            status = 'bad'
            self.is_invalid(self.column_name, len(self.values))
        self.values.append((value, status))
        
    def writeJSValidation(self):
        function_string = 'findListTerms(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string

    # Consider refactoring with _validateOntology()
    def _validate(self, value, list_names, data_access):
        """ returns true if value is in list designated by list_name, 
        false otherwise
        """
        for list_name in list_names:
            if data_access.validateListValue(list_name, value) > 0:
                return True
        
        # Not found in any list
        return False

class OntologyColumn(BaseColumn):
    """ Ontology implementation of BaseColumn class
    """
    def __init__(self, column_name, is_invalid, in_dictionary, ontology_names):
        super(OntologyColumn, self).__init__(column_name, is_invalid, in_dictionary)
        self.ontology_names = ontology_names

    def _addValue(self, value, data_access):
        status = 'good'
        if not self._validate(value, self.ontology_names, data_access):
            status = 'bad'
            self.is_invalid(self.column_name, len(self.values))
        self.values.append((value, status))
        
    def writeJSValidation(self):
        function_string = 'findListTerms(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
    
    def _validate(self, term, ontology_names, data_access):
        """ returns true if term is in ontology designated by ontology_name, 
        false otherwise 
        """
        for ontology_name in ontology_names:
            term_values = term.split(':')
            if len(term_values) != 2:
                return False
        
            if data_access.validateOntologyValue(ontology_name, term_values[1]) > 0:
                return True
        
        # Not found in any list
        return False
    
class TextColumn(BaseColumn):
    """ Text implementation of BaseColumn class
    """
    def __init__(self, column_name, is_invalid, in_dictionary, length):
        super(TextColumn, self).__init__(column_name, is_invalid, in_dictionary)
        self.maxLength = length
        
    def _validate(self, value, data_access):
        """ return true if number, false otherwise
        """
        if self.maxLength == '':
            return False
        elif len(value) > self.maxLength:
            return False
        else:
            return True
        
    def writeJSValidation(self):
        function_string = 'validateTextLength(this, \'%s\', \'%s\')' % (self.column_name, self.maxLength)
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string