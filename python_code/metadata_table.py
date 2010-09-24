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
from column_factory import *
import csv
import re
import os

class MetadataTable(object):
    """ Represents a metadata table object
    
    This class encapsulates the functionality of a metadata table
    for use with the Qiime database. It ties together the concept
    of a metadata file along with the validation associated with
    each type of column.
    """

    def __init__(self, metadataFile):
        self._invalid_rows = []
        self._columns = []
        self._log = []
        self._metadataFile = metadataFile
    
    def getInvalidRows(self):
        return self._invalid_rows
        
    def _is_invalid(self, column_name, invalid_row):
        """ A callback that is fired when an invalid field has been found
        """
        self._invalid_rows.append((column_name, invalid_row))

    def validateColumnNames(self):
        global _metadataFile
        errors = []
        expression = '^[A-Za-z][A-Za-z0-9_]*$'
        max_column_length = 30
        
        try:
            data_file = open(self._metadataFile, "rU")
            reader = csv.reader(data_file,  delimiter='\t')
            headers = reader.next()
            for column in headers:
                message = ''
                # Check the length of the column
                if len(column) > max_column_length:
                    message += '"%s": Column name is too long. Names must be %s characters or less.' % (column, str(max_column_length))
                if re.match(expression, column) == None:
                    message += '\n"%s": Column name contains invalid characters. Column names must start with a letter and may only contain letters, numbers, and the underscore ("_") character. Spaces are not allowed.' % column
                if len(message) > 0:
                    errors.append(message)
        except Exception, e:
            errors.append('The file "%s" is in an invalid format. Make sure you didn\'t save it as a binary Excel file. Template files must be in tab-delimited format.' % (data_file))
            return errors
        finally:
            data_file.close()
            return errors      
            
    def getUserDefinedColumns(self):
        if not len(self._columns):
            raise ValueError('No columns have yet been added to the collection.')
            
        user_defined_columns = []
        for column in self._columns:
            if not column.in_dictionary:
                user_defined_columns.append(column)
            
        return user_defined_columns 

    def _createColumnHeaders(self, reader, data_access):
        self._log.append('Entering _createColumnHeaders()...')
        
        # Get a column factory
        column_factory = ColumnFactory(self._is_invalid)
        
        # Obtain the list of metadata columns for validation
        column_detail_list = data_access.getColumnDictionary()
        column_details = {}
        # list of items must match length of list - maybe a way to only grab parts look
        # for (x, y) in coords:
            #do whatever with x and y
        for item in column_detail_list:
            # Store off the data type and data length for each column name
            column_details[item[0]] = (item[3], item[4])

        # Create the header columns
        headers = reader.next()
        for column in headers:
            self._log.append('Checking if column "%s" exists in column dictionary...' % column)
            try:
                # If column exists in dictionary, pass the name to the column factory and get back
                # a valid column object
                if column in column_details:
                    self._log.append('Column exists in dictionary.')
                    result = column_factory.createColumn(column, column_details[column][0], column_details[column][1], True)
                    if result:
                        self._addColumn(result)
                    else:
                        self._log.append('Column creation failed for \'' + column + '\' however the column does exist in the column dictionary')
                        return self._log
                    
                # Column not in dictionary - was added by user. Capture this field and store as metadata and
                # request a new text column from the column factory.
                else:
                    self._log.append('Column does not exist in dictionary. Assuming user-defined column.')
                    result = column_factory.createColumn(column, 'text', '8000', False)
                    if result:
                        self._addColumn(result)
                        
            except Exception, e:
                self._log.append('Could not create column. The reason was:\n%s' % (str(e)))
                return self._log
            
    def _processRows(self, reader, data_access):
        self._log.append('Entering _processsRows()...')
        
        # Read the column values
        try:
            for row in reader:
                self._log.append('Reading header row:')
                self._log.append(str(row))
                
                # Skip any rows starting with white space
                if len(row) == 0:
                    print 'Skipping row due to zero lengh'
                    print str(row)
                    continue
                if row[0].startswith('\t') or row[0].startswith(' '):
                    self._log.append('Skipping row due to leading white space')
                    continue

                # If a row is incomplete, probably means end of file whitespace
                if len(row) < len(self._columns):
                    self._log.append('Skipping row due to insufficient number of columns')
                    continue

                # There is data but not enough to fill the columns - pad out data
                if len(row) > 1 and len(row) < len(self._columns):
                    self._log.append('Row contains data but insufficient number of columns. Assuming blanks for remaining column values.')
                    i = 0
                    while i < len(self._columns) - len(row):
                        row.append('\t')
                        i += 1
                
                i = 0
                for column in row:
                    # Some files contain extra whitespace characters beyond the bounds of the last column.
                    # Skip over these values.
                    if (i > len(self._columns) - 1):
                        self._log.append('Extra whitespace found beyond column list boundary. Ignoring...')
                        continue
                    
                    # Add the current value to the appropriate metadata table column
                    self._log.append('Adding new value to metadata column %s: "%s"' % (self._columns[i].column_name, column.strip()))
                    self._columns[i]._addValue(column.strip(), data_access)
                    i += 1
                    
        except Exception, e:
            self._log.append('Error adding data to column %s. Maximum column index for this metadata table is %s. The error was: \n<p/>%s' % (str(i), str(len(self._columns) - 1), str(e)))
            return self._log

    def processMetadataFile(self):
        self._log.append('Entering processMetadataFile()...')
        
        data_file = None
        reader = None
        
        try:
            data_file = open(self._metadataFile, "rU")
            reader = csv.reader(data_file,  delimiter='\t')    
        except Exception, e:
            log.append('Error opening metadata file "%s". The error was:\n%s' % (self._metadataFile, str(e)))
            return self._log

        # One instance of the data access class for the function
        data_access = QiimeDataAccess()

        # Read the column headers and create columns for each column name in the file
        self._createColumnHeaders(reader, data_access)
        
        # Fill in the rest of the data values for each row
        self._processRows(reader, data_access)

    def _addColumn(self, column):
        self._columns.append(column)

    def _printInvalidRows(self):
        print 'Invalid Rows:'
        for row in self._invalid_rows:
            print row

    def printHTMLTable(self):
        # Log which function we're in
        self._log.append('Entering printHTMLTable()...')
        
        # Return variables
        html_table = ''

        try:
            # Determine the type of file we're dealing with
            file_type = ''
            base_name = os.path.basename(self._metadataFile)
            if 'study_template' in base_name:
                file_type = 'study'
            elif 'sample_template' in base_name:
                file_type = 'sample'
            elif 'prep_template' in base_name:
                file_type = 'prep'
            else:
                self._log.append('Could not determine type of file: "%s". Exiting.' % self._metadataFile)
                return None, log
            
            self._log.append('File type is "%s"' % file_type)
            
            html_table = '<table class="metadata_table">'
            
            column_count = len(self._columns)
            row_count = len(self._columns[0].values)
    
            # Print the column headers
            self._log.append('Print column headers...')
            x = 0
            while x < column_count:
                current_column = self._columns[x]
                self._log.append('Current column is "%s"' % current_column.column_name)
                if current_column.in_dictionary:
                    html_table += '<th class="meta_th">' + self._columns[x].column_name + '</th>\n'
                    self._log.append('Column is in dictionary')
                else:
                    html_table += '<th class="meta_th" style="background:#00FFFF">' + self._columns[x].column_name + '</th>\n'
                    self._log.append('Column is not in dictionary - assuming user-defined column.')
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
                        self._log.append('Unique column name: "%s"' % (unique_column_name))
    
                        # This is the output value for the HTML page. It may be truncated for display if the
                        # text is very long.
                        value_output = str(column.values[y][0])
    
                        # This will always hold the full value of the field. Used for submission to database.
                        actual_value = str(column.values[y][0])
                        self._log.append('Actual value: "%s"' % (actual_value))
                        
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
                            self._log.append('Field is "bad"')
                            cell_color = '#EEEEFF'
                            html_table += '<td style="background-color:#DDDDDD;"><input style="background-color:%s;" type="text" id="%s" name="%s" value="%s" %s> <br/> \
                                <a href="" onclick="replaceWithCurrent(\'%s\', \'%s\');return false;"><div style="font-size:11px">update all like values</div></a></td>\n' \
                                % (cell_color, unique_column_name, unique_column_name, actual_value, column.writeJSValidation(), unique_column_name, actual_value)
                        x += 1
                        
                html_table +='</tr>\n'
                y += 1 
            
            html_table += '</table>\n'

            # Return the table and an empty error log
            return html_table, None
        
        except Exception, e:            
            self._log.append('Error caught in printHTMLTable: %s' % str(e))
            return html_table, self._log

