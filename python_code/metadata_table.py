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
import csv
import re
import os

class ColumnFactory(object):
    """ Factory class for producing metadata columns
    """
    _qiimeDataAccess = None
    
    def __init__(self, isInvalid):
        self._isInvalid = isInvalid
        self._qiimeDataAccess = QiimeDataAccess()

    def _columnExists(self, column_name):
        found = False
        column_detail_list = QiimeDataAccess().getColumnDictionary()
        for row in column_detail_list:
            if row[0].upper() == column_name:
                found = True
                break
                      
        return found
        
    def _validateNumeric(self, value):
        """ return true if number, false otherwise
        """
        # Matches number of the form 234, 2.34, or .234
        if re.match('^\-*[0-9]+$|^\-*[0-9]*\.[0-9]+$', value) == None:
            return False
        else:
            return True
        
    def _validateText(self, value):
        """ return true if number, false otherwise
        """
        if isinstance(value, str):
            return True
        else:
            return False

    # Consider refactoring with _validateOntology()
    def _validateList(self, value, list_names):
        """ returns true if value is in list designated by list_name, 
        false otherwise
        """
        for list_name in list_names:
            if self._qiimeDataAccess.validateListValue(list_name, value) > 0:
                return True
        
        #for list_name in list_names:
        #    if (ListManager().checkListValue(list_name, value)):
        #        return True
                
        # Not found in any list
        return False
        
        #return True
        
    def _validateOntology(self, term, ontology_names):
        """ returns true if term is in ontology designated by ontology_name, 
        false otherwise 
        """
        for ontology_name in ontology_names:
            term_values = term.split(':')
            if len(term_values) != 2:
                return False
            
            if self._qiimeDataAccess.validateOntologyValue(ontology_name, term_values[1]) > 0:
                return True
        
        #for ontology_name in ontology_names:
        #    if (ListManager().checkOntologyValue(ontology_name, term)):
        #        return True
                
        # Not found in any list
        return False
        
        #return True

    def _validateDate(self, date):
        """ returns true if provided date is in a valid format, false otherwise 
        """
        return True

    def _getControlledVocabs(self, column_name, datatype):
        if datatype == 'list':
            return QiimeDataAccess().getControlledVocabs(column_name)
        elif datatype == 'ontology':
            return QiimeDataAccess().getOntologies(column_name)

    def createColumn(self, column_name, datatype):
        """ Creates a column of the right type based on the column name
        """
        column = None
        controlled_vocab_list = None

        # Deterine if this column is associated with a list or ontology
        if datatype == 'list' or datatype == 'ontology':
            controlled_vocab_list = self._getControlledVocabs(column_name, datatype)
            if controlled_vocab_list == None:
                print 'Error: No controlled vocabulary or ontology found even though column is listed as ' + datatype + '.'
                return None
        
        # Create the appropriate type of column
        if datatype == 'numeric':
            column = NumericColumn(column_name, self._validateNumeric, self._isInvalid)
        elif datatype == 'text':
            column = TextColumn(column_name, self._validateText, self._isInvalid)
        elif datatype == 'list':
            column = ListColumn(column_name, self._validateList, self._isInvalid, controlled_vocab_list)
        elif datatype == 'ontology':
            column = OntologyColumn(column_name, self._validateOntology, self._isInvalid, controlled_vocab_list)

        return column

class BaseColumn(object):
    """ The base class for all column types in the metadata table. This class 
    implements common functionality for all column classes.
    """
    def __init__(self, column_name, validate, isInvalid):
        # Name of this column. Should be unique in MetadataTable object
        self.column_name = column_name
        
        # Validation function pointer
        self.validate = validate
        
        # Callback to notify parent of an invalid value entry
        self.isInvalid = isInvalid
        
        # List of values in this column
        self.values = []
        
        # List of invalid indicies in this column
        self._invalid_indicies = []
        
    def writeJSValidation(self):
        """ Writes the Javascript validation funciton if necessary
        """
        return ''
    
    def addValue(self, value):
        status = 'good'
        if not self.validate(value):
            status = 'bad'
            self.isInvalid(self.column_name, len(self.values))     
        self.values.append((value, status))
        
class NumericColumn(BaseColumn):
    """ Numeric implementation of BaseColumn class
    """
    def __init__(self, column_name, validate, isInvalid):
        super(NumericColumn, self).__init__(column_name, validate, isInvalid)
        
    def writeJSValidation(self):
        function_string = 'validateNumericField(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
        
class ListColumn(BaseColumn):
    """ List implementation of BaseColumn class
    """
    def __init__(self, column_name, validate, isInvalid, list_names):
        super(ListColumn, self).__init__(column_name, validate, isInvalid)
        self.list_names = list_names
        
    def addValue(self, value):
        status = 'good'
        if not self.validate(value, self.list_names):
            status = 'bad'
            self.isInvalid(self.column_name, len(self.values))
        self.values.append((value, status))
        
    def writeJSValidation(self):
        function_string = 'findListTerms(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
        
class OntologyColumn(BaseColumn):
    """ Ontology implementation of BaseColumn class
    """
    def __init__(self, column_name, validate, isInvalid, ontology_names):
        super(OntologyColumn, self).__init__(column_name, validate, isInvalid)
        self.ontology_names = ontology_names

    def addValue(self, value):
        status = 'good'
        if not self.validate(value, self.ontology_names):
            status = 'bad'
            self.isInvalid(self.column_name, len(self.values))
        self.values.append((value, status))
        
    def writeJSValidation(self):
        function_string = 'findListTerms(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
    
class TextColumn(BaseColumn):
    """ Text implementation of BaseColumn class
    """
    def __init__(self, column_name, validate, isInvalid):
        super(TextColumn, self).__init__(column_name, validate, isInvalid)
        
class DateColumn(BaseColumn):
    """ Date implementation of BaseColumn class
    """
    def __init__(self, column_name, validate, isInvalid):
        super(DateColumn, self).__init__(column_name, validate, isInvalid)
        
class MetadataTable(object):
    """ The parent class which represents a metadata table object
    
    This class encapsulates the functionality of a metadata table
    for use with the Qiime database. It ties together the concept
    of a metadata file along with the validation associated with
    each type of column.
    """

    _metadataFile = None

    def __init__(self, metadataFile):
        global _metadataFile
        
        self._invalid_rows = []
        self._columns = []
        self._metadataFile = metadataFile
        #self._template_id = template_id
        self._readMetadataFile()
        
    def getInvalidRows(self):
        return self._invalid_rows
        
    def writeToDatabase(self, data_access):
        if len(self._invalid_rows) > 0:
            raise Exception('Data cannot be written while invalid rows still exist')
        else:
            data_access.writeTableToDatabase()
            
    def _isInvalid(self, column_name, invalid_row):
        """ A callback that is fired when an invalid field has been found
        """
        self._invalid_rows.append((column_name, invalid_row))

    def _readMetadataFile(self):
        global _metadataFile
        column_factory = ColumnFactory(self._isInvalid)
        data_file = open(self._metadataFile, "rU")
        reader = csv.reader(data_file,  delimiter='\t')

        # Obtain the list of metadata columns for validation
        column_detail_list = QiimeDataAccess().getColumnDictionary()
        column_name_list = {}
        for item in column_detail_list:
            column_name_list[item[0]] = item[3]

        # Create the header columns
        headers = reader.next()
        for column in headers:
            try:
                # First column starts with a #, make sure to strip it
                if column.startswith('#'):
                    column = column[1:]
                if column in column_name_list:
                    result = column_factory.createColumn(column, column_name_list[column])
                    if result:
                        self._addColumn(result)
                    else:
                        raise ValueError('Column creation failed for \'' + column + '\' however the column does exist in the column dictionary')
            except Exception as err:
                raise err

        # Read the column values
        for row in reader:
            
            # If a row is incomplete, probably means end of file whitespace
            if len(row) < len(self._columns):
                continue
            
            # Skip any additional rows starting with a #
            if str(row[0]).startswith('#'):
                continue
            
            i = 0
            for column in row:
                # Skip any rows starting with white space
                if column.startswith('\t') or column.startswith(' '):
                    continue
                self._columns[i].addValue(column)
                i += 1

        #self._printTable()
        self._printInvalidRows()

    def _addColumn(self, column):
        self._columns.append(column)

    def _printInvalidRows(self):
        print 'Invalid Rows:'
        for row in self._invalid_rows:
            print row

    def _printTable(self):
        print '\n\n'
        column_count = len(self._columns)
        row_count = len(self._columns[0].values)

        x = 0

        while x < column_count:
            print self._columns[x].column_name + '\t',
            x += 1

        y = 0
        
        while y < row_count:
            x = 0
            print '\n',
            while x < column_count:
                for column in self._columns:
                    print str(column.values[y]) + '\t',
                    x += 1
            y += 1 
            
        print '\n\n'

    def printHTMLTable(self):
        # Determine the type of file we're dealing with
        file_type = ''
        if os.path.basename(self._metadataFile).startswith('study'):
            file_type = 'study'
        elif os.path.basename(self._metadataFile).startswith('sample'):
            file_type = 'sample'
        elif os.path.basename(self._metadataFile).startswith('prep'):
            file_type = 'prep'
        else:
            return
        
        html_table = '<table class="metadata_table">'
        
        column_count = len(self._columns)
        row_count = len(self._columns[0].values)

        # Print the column headers
        x = 0
        while x < column_count:
            html_table += '<th class="meta_th">' + self._columns[x].column_name + '</th>\n'
            x += 1
        
        #####################################
        # Print the table rows
        #####################################
        
        # Max length for text columns
        max_text_length = 50
        
        # Index for rows
        y = 0
        
        while y < row_count:
            x = 0
            html_table += '<tr>\n'
            while x < column_count:
                for column in self._columns:
                    # Create a unique column name for processing later
                    unique_column_name = file_type + ':' + str(y) + ':' + str(x) + ':' + column.column_name

                    value_output = str(column.values[y][0])
                    
                    #For fields that are valid:
                    if column.values[y][1] == 'good':
                        # If this is a text column, truncate the length of the string to keep the display reasonable
                        if type(column) == TextColumn:
                            if len(value_output) > max_text_length:
                                value_output = value_output[:max_text_length] + '...'
                            
                        hidden_field_text = '<input type=\"hidden\" id=\"%s\" name=\"%s\" value=\"%s\">\n' % (unique_column_name, unique_column_name, value_output)
                        cell_color = '#FFFFFF'
                        html_table += '<td style=\"background-color:%s;\">%s%s</td>\n' % (cell_color, hidden_field_text, value_output)
                    
                    # For fields that are not valid
                    else:
                        cell_color = '#FF8888'
                        html_table += '<td><input style="background-color:%s;" type="text" id="%s" name="%s" value="%s" %s> <br/> \
                            <a href="" onclick="replaceWithCurrent(\'%s\');return false;">replace all</a></td>\n' \
                            % (cell_color, unique_column_name, unique_column_name, value_output, column.writeJSValidation(), unique_column_name)
                    x += 1
                    
            html_table +='</tr>\n'
            y += 1 
        
        html_table += '</table>\n'
        
        return html_table
