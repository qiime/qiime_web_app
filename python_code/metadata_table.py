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

from data_access_connections import data_access_factory
from enums import ServerConfig
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
    
    def __init__(self, metadataFile, study_id):
        self._invalid_rows = []
        self._columns = []
        self._log = []
        self._metadataFile = metadataFile
        self._data_access = data_access_factory(ServerConfig.data_access_type)
        self._study_id = study_id

    #############################################
    # Getter and setter methods
    #############################################
    
    def getColumnNames(self):
        if self._columns == None:
            self._buildMetadataTable(False, False)
        return self._columns;
    
    def getInvalidRows(self):
        return self._invalid_rows
        
    def getUserDefinedColumns(self):
        # Build the table with only column headers
        self._buildMetadataTable(False, False)
        user_defined_columns = []
        for column in self._columns:
            if not column.in_dictionary:
                user_defined_columns.append(column)
        return user_defined_columns 
    
    def getColumn(self, column_name):
        column = None
        
        if len(self._columns) == 0:
            self._buildMetadataTable(True, False)
        
        # Find the column
        for c in self._columns:
            if c.column_name.lower() == column_name.lower():
                column = c
                break
                        
        # If the column was not found, return an error
        if not column:
            raise ValueError('Could not locate column with column name "%s"' % column_name)
            
        return column;

    #############################################
    # Private methods
    #############################################
        
    def _is_invalid(self, column_name, invalid_row):
        """ A callback that is fired when an invalid field has been found
        """
        self._invalid_rows.append((column_name, invalid_row))
        
    def checkForDuplicateColumns(self, headers):
        errors = []
        names = []
        dupes = []
        
        for column in headers:
            if column in names:
                dupes.append(column)
            else:
                names.append(column)
            
            for column in dupes:
                errors.append('Column names must be unique within the file: %s' % column)
                
        return errors
        
    def _createColumnHeaders(self, reader, process_all_data, validate_contents):
        self._log.append('Entering _createColumnHeaders()...')

        # Get a column factory
        column_factory = ColumnFactory(self._is_invalid, self._data_access)
        
        # Obtain the list of metadata columns for validation
        column_detail_list = self._data_access.getColumnDictionary()
        column_details = {}
        # list of items must match length of list - maybe a way to only grab parts look
        # for (x, y) in coords:
            #do whatever with x and y
        for item in column_detail_list:
            # Store off the data type and data length for each column name
            # item[3] = data_type
            # item[4] = max_length
            # item[5] = min_length
            column_details[item[0]] = (item[3], item[4], item[5])

        # Create the header columns
        headers = reader.next()
        
        # Make sure there are no duplicates
        errors = self.checkForDuplicateColumns(headers)
        if errors:
            return errors
            
        # Check for bad columns
        errors, bad_columns = self.validateColumnNames()
        
        self._log.append('Column headers: %s<br/>' % str(headers))
        for column in headers:
            column = column.lower()
            
            # Skip known bad columns
            if column in bad_columns:
                continue
                
            self._log.append('Checking if column "%s" exists in column dictionary...' % column)
            try:
                # If column exists in dictionary, pass the name to the column factory and get back
                # a valid column object
                if column in column_details:
                    self._log.append('Column exists in dictionary.')
                    self._log.append('Creating column with details: %s...' % str(column_details[column]))
                    result = column_factory.createColumn(column)
                    self._log.append('Existing column successfully created.')
                    if result:
                        self._addColumn(result)
                    else:
                        self._log.append('Column creation failed for \'' + column + '\' however the column does exist in the column dictionary')
                        return self._log

                # Column not in dictionary - was added by user. Capture this field and store as metadata and
                # request a new text column from the column factory.
                else:
                    # Only check if these are in the database if a full processing run is requested
                    if process_all_data and validate_contents:
                        # Figure out the data type of for each column
                        extra_column_details = self._data_access.getExtraColumnMetadata(self._study_id)
                        if not extra_column_details:
                            raise ValueError('Expected extra_column_details however none were found.')
                        data_type = extra_column_details[column]['data_type']
                        if not data_type:
                            raise ValueError('Expected data type for extra column however none was found.')
                        result = column_factory.createColumn(column)
                    else:
                        result = column_factory.createColumn(column)
                    if result:
                        self._addColumn(result)

            except Exception, e:
                message = 'Could not create column. The reason was:\n%s' % (str(e))
                self._log.append(message)
                raise Exception(message)

    def _processRows(self, reader, validate_contents):
        self._log.append('Entering _processsRows()...')

        # Read the column values
        try:
            for row in reader:
                self._log.append('Reading row:')
                #self._log.append(str(row))

                # If row is entirely whitespace, get rid of it
                data_found = False
                for item in row:
                    if item.strip():
                        data_found = True
                if not data_found:
                    continue

                # Skip any rows starting with white space
                if len(row) == 0:
                    print 'Skipping row due to zero lengh'
                    print str(row)
                    continue
                if row[0].startswith('\t') or row[0].startswith(' '):
                    self._log.append('Skipping row due to leading white space')
                    continue

                # There is data but not enough to fill the columns - pad out data
                self._log.append('row_length: %s' % str(len(row)))
                self._log.append('header_length: %s' % str(len(self._columns)))
                if len(row) > 1 and len(row) < len(self._columns):
                    self._log.append('Row contains data but insufficient number of columns. Assuming blanks for remaining column values.')
                    j = 0
                    orig_row_length = len(row)
                    while j < (len(self._columns) - orig_row_length):
                        row.append('')
                        j += 1

                i = 0
                for column in row:
                    # Some files contain extra whitespace characters beyond the bounds of the last column.
                    # Skip over these values.
                    if (i > len(self._columns) - 1):
                        self._log.append('Extra whitespace found beyond column list boundary. Ignoring...')
                        continue

                    # Add the current value to the appropriate metadata table column
                    self._log.append('Adding new value to metadata column %s: "%s"' % (self._columns[i].column_name, column.strip()))
                    self._columns[i]._addValue(column.strip(), validate_contents)
                    i += 1

        except Exception, e:
            raise Exception( 'Error in _processRows: %s. \nError Log:\n%s' % (str(e), self._log) )
            
    def _buildMetadataTable(self, process_all_data, validate_contents):
        self._log.append('Entering _buildMetadataTable()...')

        data_file = None
        reader = None

        try:
            self._log.append('Opening data file...')
            data_file = open(self._metadataFile, "rU")
            self._log.append('Obtaining reader...')
            reader = csv.reader(data_file,  delimiter='\t')

            # Read the column headers and create columns for each column name in the file
            self._log.append('Creating column headers...')
            
            errors = self._createColumnHeaders(reader, process_all_data, validate_contents)
            if errors:
                message = 'Errors were found while processing column headers: %s' % ', '.join(errors)
                raise Exception(message)

            # Fill in the rest of the data values for each row
            if process_all_data:
                self._log.append('Processing all rows...')
                self._processRows(reader, validate_contents)

        except Exception, e:
            self._log.append('Error opening metadata file "%s". The error was:\n%s' % (self._metadataFile, str(e)))
            raise Exception('Error: Could not build metadata table.\nError Log: %s\nThe error is: %s' % (self._log, str(e)))            

    def _addColumn(self, column):
        self._columns.append(column)

    def _printInvalidRows(self):
        print 'Invalid Rows:'
        for row in self._invalid_rows:
            print row
    
    #############################################
    # Public methods
    #############################################

    def validateColumnNames(self):
        global _metadataFile
        bad_columns = []
        errors = []
        expression = '^[A-Za-z][A-Za-z0-9_]*$'
        max_column_length = 30
        
        try:
            data_file = open(self._metadataFile, "rU")
            reader = csv.reader(data_file,  delimiter='\t')
            headers = reader.next()
            for column in headers:
                bad = False
                # Check the length of the column
                if len(column) > max_column_length:
                    errors.append('"%s": Column name is too long. Names must be %s characters or less.<br/>' % (column, str(max_column_length)))
                    bad = True
                # Check for invalid characters
                if re.match(expression, column) == None:
                    errors.append('\n"%s": Column name contains invalid characters. Column names must start with a letter and may only contain letters, numbers, and the underscore ("_") character. Spaces are not allowed.<br/>' % column)
                    bad = True
                # If the column fails initial validation, add to the bad list. These
                # will not be checked for further errors until name is fixed.
                if bad:
                    bad_columns.append(column)
                    
        except Exception, e:
            errors.append('The file "%s" is in an invalid format. Make sure you didn\'t save it as a binary Excel file. Template files must be in tab-delimited format.<br/>' % (data_file))
        finally:
            data_file.close()
            return errors, bad_columns

    def processMetadataFile(self):
        # Build the table with columns and full data
        self._buildMetadataTable(True, True)
    
    def fillValidItems(self, file_type, column_count, row_count, rows_to_draw, validated_items):
        y = 0
        while y < row_count:
            # If this is a visible row (i.e. it has errors), skip it...
            if y in rows_to_draw:
                y += 1
                continue
            
            x = 0
            while x < column_count:
                for column in self._columns:
                    unique_column_name = file_type + ':' + str(y) + ':' + str(x) + ':' + column.column_name
                    actual_value = str(column.values[y][0])
                    validated_items[unique_column_name] = actual_value
                    x += 1
            y += 1
        
    def renderVisibleTable(self, file_type, column_count, row_count, rows_to_draw):
        html_table = '<table class="metadata_table">'
        
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
                html_table += '<th class="meta_th" style="background:#00FFFF">' + \
                    self._columns[x].column_name + '</th>\n'
                self._log.append('Column is not in dictionary - assuming user-defined column.')
            x += 1
    
        # Max length for text columns
        max_text_length = 50
        
        # Row color
        row_color = '#FFFFFF'
    
        # Index for rows
        y = 0
        while y < row_count:
            
            # Skip all rows that are already valid
            if y not in rows_to_draw:
                y += 1
                continue
                
            x = 0            
            
            html_table += '<tr style="background-color:%s;">\n' % (row_color)
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
                        self._log.append('Field value is valid.')
                        # If this is a text column, truncate the length of the string to keep the display reasonable
                        if type(column) == TextColumn:
                            if len(value_output) > max_text_length:
                                value_output = value_output[:max_text_length] + '...'

                        hidden_field_text = '<input type="hidden" id="{unique_column_name}"\
                            name="{unique_column_name}" value="{actual_value}">\n'.format(unique_column_name = \
                            unique_column_name, actual_value = actual_value)
                            
                        cell_color = '#FFFFFF'
                        html_table += '<td>%s%s</td>\n' % (hidden_field_text, value_output)
                        
                    # For fields that are not valid
                    else:
                        self._log.append('Field value is invalid')
                        cell_color = '#EEEEFF'
                        html_table += '<td style="background-color:#FFFF00;">\
                            <input style="background-color:{cell_color};" type="text" id="{unique_column_name}" \
                            name="{unique_column_name}" value="{actual_value}" {js_validation}> \
                            <br/> \
                            <a href="" onclick="replaceWithCurrent(\'{unique_column_name}\', \
                            \'{actual_value}\');return false;">\
                            <div style="font-size:11px">update all like values\
                            </div>\
                            </a>\
                            </td>'.format(\
                                cell_color = cell_color, \
                                unique_column_name = unique_column_name, \
                                actual_value = actual_value, \
                                js_validation = column.writeJSValidation())
                    x += 1
                
            html_table +='</tr>\n'
            y += 1 
    
        html_table += '</table>\n'
        
        return html_table

    def printHTMLTable(self):
        # Log which function we're in
        self._log.append('Entering printHTMLTable()...')
        
        # Return variables
        html_table = ''
        visible_elements = False
        
        # Rows to visibly draw
        rows_to_draw = []
        
        # Dict of validated items
        validated_items = {}

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

            column_count = len(self._columns)
            row_count = len(self._columns[0].values)

            # Figure out if there are any rows to visibly draw            
            y = 0
            while y < row_count:
                x = 0
                while x < column_count:
                    for column in self._columns:
                        if column.values[y][1] == 'good':
                            continue
                        else:
                            rows_to_draw.append(y)
                            break
                    x += 1
                y += 1
            
            # Fill in validated_items. These are not rendered - only written to file later.
            self.fillValidItems(file_type, column_count, row_count, rows_to_draw, validated_items)
            
            # If there are rows to draw (i.e. there are validation errors), render the HTML...
            if rows_to_draw:
                html_table = self.renderVisibleTable(file_type, column_count, row_count, rows_to_draw)
                visible_elements = True

            # Return the table and an empty error log
            return validated_items, html_table, None, visible_elements
        
        except Exception, e:            
            self._log.append('Error caught in printHTMLTable: %s' % str(e))
            return html_table, self._log, False

