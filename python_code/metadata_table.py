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
    
    def __init__(self, isInvalid):
        self._isInvalid = isInvalid

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

    def createColumn(self, column_name, datatype, length):
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
            column = NumericColumn(column_name, self._isInvalid)
        elif datatype == 'text':
            column = TextColumn(column_name, self._isInvalid, length)
        elif datatype == 'yn':
            column = YesNoColumn(column_name, self._isInvalid)
        elif datatype == 'date':
            column = DateColumn(column_name, self._isInvalid)
        elif datatype == 'list':
            column = ListColumn(column_name, self._isInvalid, controlled_vocab_list)
        elif datatype == 'ontology':
            column = OntologyColumn(column_name, self._isInvalid, controlled_vocab_list)

        return column

class BaseColumn(object):
    """ The base class for all column types in the metadata table. This class 
    implements common functionality for all column classes.
    """
    def __init__(self, column_name, isInvalid):
        # Name of this column. Should be unique in MetadataTable object
        self.column_name = column_name
        
        # Callback to notify parent of an invalid value entry
        self.isInvalid = isInvalid
        
        # List of values in this column
        self.values = []
        
        # List of invalid indicies in this column
        self._invalid_indicies = []
        
        # RegEx validation string (if applicable)
        self.reg_exp = ''
        
    def writeJSValidation(self):
        """ Writes the Javascript validation funciton if necessary
        """
        return ''
    
    def _addValue(self, value):
        status = 'good'
        if not self._validate(value):
            status = 'bad'
            self.isInvalid(self.column_name, len(self.values))     
        self.values.append((value, status))
        
    def _validate(self, value):
        """ Validates a value of this column type
        """
        return True

class NumericColumn(BaseColumn):
    """ Numeric implementation of BaseColumn class
    """
    def __init__(self, column_name, isInvalid):
        super(NumericColumn, self).__init__(column_name, isInvalid)
        self.reg_exp = '^\-*[0-9]+$|^\-*[0-9]*\.[0-9]+$'
        
    def writeJSValidation(self):
        function_string = 'validateNumericField(this, \'%s\', \'%s\')' % (self.column_name, self.reg_exp.replace('\\', '\\\\'))
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
        
    def _validate(self, value):
        """ return true if number, false otherwise
        """
        # Matches number of the form 234, 2.34, or .234
        if re.match(self.reg_exp, value) == None:
            return False
        else:
            return True
        
class YesNoColumn(BaseColumn):
    """ Yes/No implementation of BaseColumn class
    """
    def __init__(self, column_name, isInvalid):
        super(YesNoColumn, self).__init__(column_name, isInvalid)
        self.reg_exp = '^y$|^Y$|^n$|^N$'
        
    def writeJSValidation(self):
        function_string = 'validateYesNoField(this, \'%s\', \'%s\')' % (self.column_name, self.reg_exp.replace('\\', '\\\\'))
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
    
    def _validate(self, value):
        """ return true if y/Y/n/N, false otherwise
        """
        if re.match(self.reg_exp, value):
            return True
        else:
            return False

class ListColumn(BaseColumn):
    """ List implementation of BaseColumn class
    """
    def __init__(self, column_name, isInvalid, list_names):
        super(ListColumn, self).__init__(column_name, isInvalid)
        self.list_names = list_names
        
    def _addValue(self, value):
        status = 'good'
        if not self._validate(value, self.list_names):
            status = 'bad'
            self.isInvalid(self.column_name, len(self.values))
        self.values.append((value, status))
        
    def writeJSValidation(self):
        function_string = 'findListTerms(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string

    # Consider refactoring with _validateOntology()
    def _validate(self, value, list_names):
        """ returns true if value is in list designated by list_name, 
        false otherwise
        """
        for list_name in list_names:
            if QiimeDataAccess().validateListValue(list_name, value) > 0:
                return True
        
        # Not found in any list
        return False

class OntologyColumn(BaseColumn):
    """ Ontology implementation of BaseColumn class
    """
    def __init__(self, column_name, isInvalid, ontology_names):
        super(OntologyColumn, self).__init__(column_name, isInvalid)
        self.ontology_names = ontology_names

    def _addValue(self, value):
        status = 'good'
        if not self._validate(value, self.ontology_names):
            status = 'bad'
            self.isInvalid(self.column_name, len(self.values))
        self.values.append((value, status))
        
    def writeJSValidation(self):
        function_string = 'findListTerms(this, \'%s\')' % self.column_name 
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
    
    def _validate(self, term, ontology_names):
        """ returns true if term is in ontology designated by ontology_name, 
        false otherwise 
        """
        for ontology_name in ontology_names:
            term_values = term.split(':')
            if len(term_values) != 2:
                return False
            
            if QiimeDataAccess().validateOntologyValue(ontology_name, term_values[1]) > 0:
                return True
        
        # Not found in any list
        return False
    
class TextColumn(BaseColumn):
    """ Text implementation of BaseColumn class
    """
    def __init__(self, column_name, isInvalid, length):
        super(TextColumn, self).__init__(column_name, isInvalid)
        self.maxLength = length
        
    def _validate(self, value):
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

        
class DateColumn(BaseColumn):
    """ Date implementation of BaseColumn class
    """
    def __init__(self, column_name, isInvalid):
        super(DateColumn, self).__init__(column_name, isInvalid)
        self.reg_exp = '^((((((0?[13578])|(1[02]))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\-\/\s]?((0?[1-9])|([1-2][0-9]))))[\-\/\s]?\d{2}(([02468][048])|([13579][26])))|(((((0?[13578])|(1[02]))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\-\/\s]?((0?[1-9])|(1[0-9])|(2[0-8]))))[\-\/\s]?\d{2}(([02468][1235679])|([13579][01345789]))))(\s(((0?[1-9])|(1[0-2]))\:([0-5][0-9])((\s)|(\:([0-5][0-9])\s))([AM|PM|am|pm]{2,2})))?$'
        
    def writeJSValidation(self):
        function_string = 'validateDateField(this, \'%s\', \'%s\')' % (self.column_name, self.reg_exp.replace('\\', '\\\\'))
        validation_string = ' onclick="%s;" ' % (function_string)
        validation_string += ' onkeyup="%s;" ' % (function_string)
        return validation_string
    
    def _validate(self, date):
        """Returns true if provided date is in a valid format, false otherwise
        
        Borrowed from http://regexlib.com/DisplayPatterns.aspx?cattabindex=4&categoryId=5
        
        Description: Following expression can be used to validate a datetime column from SQL Server.
        This expression is an enhanced version of Scott Watermasysk's date/time submission. It now
        accepts leading zeros in months, days, and hours. In addition, this expression properly handles
        the 11th hour. Watermasysk's would take the 10th and 12th hour but not the 11th. This regex has
        been tweaked to do so. Does not handle the February 29th problem on non-leap years yet. Will
        learn a little more about RegEx and do so in later submission. 
        
        Matches: 11/30/2003 10:12:24 am | 2/29/2003 08:14:56 pm | 5/22/2003
        Non-Matches: 11/31/2003 10:12:24 am | 2/30/2003 08:14:56 pm | 5/22/2003 14:15
        """
        if re.match(self.reg_exp, date) == None:
            return True
        else:
            return False
        
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
        column_details = {}
        for item in column_detail_list:
            # Store off the data type and data length for each column name
            column_details[item[0]] = (item[3], item[4])

        # Create the header columns
        headers = reader.next()
        for column in headers:
            try:
                if column in column_details:
                    result = column_factory.createColumn(column, column_details[column][0], column_details[column][1])
                    if result:
                        self._addColumn(result)
                    else:
                        raise ValueError('Column creation failed for \'' + column + '\' however the column does exist in the column dictionary')
            except Exception as err:
                raise err

        # Read the column values
        for row in reader:
            
            # Skip any rows starting with white space
            if row[0].startswith('\t') or row[0].startswith(' '):
                continue

            # If a row is incomplete, probably means end of file whitespace
            if len(row) < len(self._columns):
                continue
            
            i = 0
            for column in row:
                self._columns[i]._addValue(column)
                i += 1

        #self._printTable()
        self._printInvalidRows()

    def _addColumn(self, column):
        self._columns.append(column)

    def _printInvalidRows(self):
        print 'Invalid Rows:'
        for row in self._invalid_rows:
            print row

    """ depreciated
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
    """

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
                    #print 'column_count: ' + str(column_count) + ', row_count: ' + str(row_count)
                    #print unique_column_name
                    #print str(column.values)
                    
                    # This is the output value for the HTML page. It may be truncated for display if the
                    # text is very long.
                    value_output = str(column.values[y][0])
                    # This will always hold the full value of the field. Used for submission to database.
                    actual_value = str(column.values[y][0])
                    
                    #For fields that are valid:
                    if column.values[y][1] == 'good':
                        # If this is a text column, truncate the length of the string to keep the display reasonable
                        if type(column) == TextColumn:
                            if len(value_output) > max_text_length:
                                value_output = value_output[:max_text_length] + '...'
                            
                        hidden_field_text = '<input type=\"hidden\" id=\"%s\" name=\"%s\" value=\"%s\">\n' % (unique_column_name, unique_column_name, actual_value)
                        cell_color = '#FFFFFF'
                        html_table += '<td style=\"background-color:%s;\">%s%s</td>\n' % (cell_color, hidden_field_text, value_output)
                    
                    # For fields that are not valid
                    else:
                        cell_color = '#EEEEFF'
                        html_table += '<td style="background-color:#DDDDDD;"><input style="background-color:%s;" type="text" id="%s" name="%s" value="%s" %s> <br/> \
                            <a href="" onclick="replaceWithCurrent(\'%s\');return false;"><div style="font-size:11px">replace all</div></a></td>\n' \
                            % (cell_color, unique_column_name, unique_column_name, actual_value, column.writeJSValidation(), unique_column_name)
                    x += 1
                    
            html_table +='</tr>\n'
            y += 1 
        
        html_table += '</table>\n'
        
        return html_table
