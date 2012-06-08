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
import re

class ColumnFactory(object):
	""" Factory class for producing metadata columns
	"""
	
	def __init__(self, is_invalid, data_access):
		self._is_invalid = is_invalid
		self._data_access = data_access
		
		# Obtain the list of metadata columns
		self._column_detail_list = self._data_access.getColumnDictionary()
		self._column_details = {}

		for item in self._column_detail_list:
			# Store off the data type and data length for each column name
			# item[3] = data_type
			# item[4] = max_length
			# item[5] = min_length
			self._column_details[item[0]] = (item[3], item[4], item[5])

	def _columnExists(self, column_name):
		found = False
		for row in self._column_detail_list:
			if row[0].upper() == column_name:
				found = True
				break
					  
		return found

	def _getControlledVocabs(self, column_name):		
		datatype = self._column_details[column_name][0]
		if datatype == 'list':
			return self._data_access.getControlledVocabs(column_name)
		elif datatype == 'ontology':
			return self._data_access.getOntologies(column_name)

	def createColumn(self, column_name):
		""" Creates a column of the right type based on the column name
		"""
		_column = None
		_controlled_vocab_list = None
		
		column_name = column_name.lower()
		
		if column_name not in self._column_details:
			datatype = 'text'
			max_length = '8000'
			min_length = 0
			in_dictionary = False
		else:
			datatype = self._column_details[column_name][0]
			max_length = self._column_details[column_name][1]
			min_length = self._column_details[column_name][2]
			in_dictionary = True
				
		# Deterine if this column is associated with a list or ontology
		if datatype == 'list' or datatype == 'ontology':
			_controlled_vocab_list = self._getControlledVocabs(column_name)
			if _controlled_vocab_list == None:
				print 'Error: No controlled vocabulary or ontology found even though column is listed as ' + datatype + '.'
				return None
		
		# Create the appropriate type of column
		if datatype == 'numeric':
			regex = '^\-*[0-9]+$|^\-*[0-9]*\.[0-9]+$'
			_column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex, self._data_access)
		elif datatype == 'range':
			regex = '^((\-?[0-9]+)|(\-?[0-9]*\.[0-9]+))(\-((\-?[0-9]+)|(\-?[0-9]*\.[0-9]+)))?$'
			_column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex, self._data_access)
		elif datatype == 'yn':
			regex = '^y$|^Y$|^n$|^N$'
			_column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex, self._data_access)
		elif datatype == 'date':
			regex = '^((((((0?[13578])|(1[02]))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\-\/\s]?((0?[1-9])|([1-2][0-9]))))[\-\/\s]?\d{2}(([02468][048])|([13579][26])))|(((((0?[13578])|(1[02]))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\-\/\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\-\/\s]?((0?[1-9])|(1[0-9])|(2[0-8]))))[\-\/\s]?\d{2}(([02468][1235679])|([13579][01345789]))))(\s(((0?[1-9])|(1[0-9])|(2[0-3]))\:([0-5][0-9])((\s)|(\:([0-5][0-9])))))?$'
			_column = RegExColumn(column_name, self._is_invalid, in_dictionary, regex, self._data_access)
		elif datatype == 'text':
			_column = TextColumn(column_name, self._is_invalid, in_dictionary, max_length, min_length, self._data_access)
		elif datatype == 'list':
			_column = ListColumn(column_name, self._is_invalid, in_dictionary, _controlled_vocab_list, self._data_access)
			#_column = OntologyColumn(column_name, self._is_invalid, in_dictionary, _controlled_vocab_list, self._data_access)
		elif datatype == 'ontology':
			_column = OntologyColumn(column_name, self._is_invalid, in_dictionary, _controlled_vocab_list, self._data_access)

		return _column

class BaseColumn(object):
	""" The base class for all column types in the metadata table. This class 
	implements common functionality for all column classes.
	"""
	def __init__(self, column_name, is_invalid, in_dictionary, data_access):
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
		self.in_dictionary = in_dictionary
		
		# Store a global reference to data_access
		self._data_access = data_access
	
	def _addValue(self, value, validate_contents):
		status = 'good'
		if validate_contents:
			if not self._validate(value):
				status = 'bad'
				self.is_invalid(self.column_name, len(self.values))		
		self.values.append((value, status))
		
	def _isUnknown(self, value):
		pass_values = set(['UNKNOWN', 'NA'])
		if str(value).upper() in pass_values:
			return True

class RegExColumn(BaseColumn):
	""" RegExColumn implementation of BaseColumn class
	"""
	def __init__(self, column_name, is_invalid, in_dictionary, regex, data_access):
		super(RegExColumn, self).__init__(column_name, is_invalid, in_dictionary, data_access)
		self.reg_exp = regex
		
	def writeJSValidation(self):
		function_string = 'validateRegExField(this, \'%s\', \'%s\')' % (self.column_name, self.reg_exp.replace('\\', '\\\\'))
		validation_string = ' onclick="%s;" ' % (function_string)
		validation_string += ' onkeyup="%s;" ' % (function_string)
		return validation_string
		
	def _validate(self, value):
		""" return true if number, false otherwise
		"""
		if self._isUnknown(value):
			return True
		
		if re.match(self.reg_exp, value) == None:
			return False
		else:
			return True

class ListColumn(BaseColumn):
	""" List implementation of BaseColumn class
	"""
	def __init__(self, column_name, is_invalid, in_dictionary, list_names, data_access):
		super(ListColumn, self).__init__(column_name, is_invalid, in_dictionary, data_access)
		self.list_names = list_names
		
	def _addValue(self, value, validate_contents):
		status = 'good'
		if validate_contents:
			if not self._validate(value, self.list_names):
				status = 'bad'
				self.is_invalid(self.column_name, len(self.values))
		self.values.append((value, status))
		
	def writeJSValidation(self):
		function_string = 'findListTerms(this, \'%s\')' % self.column_name 
		validation_string = ' onclick="%s;" ' % (function_string)
		validation_string += ' onkeyup="%s;" ' % (function_string)
		return validation_string

	def _validate(self, value, list_names):
		""" returns true if value is in list designated by list_name, 
		false otherwise
		"""
		if self._isUnknown(value):
			return True
		
		for list_name in list_names:
			if self._data_access.validateListValue(list_name, value) > 0:
				return True
		
		# Not found in any list
		return False

class OntologyColumn(BaseColumn):
	""" Ontology implementation of BaseColumn class
	"""
	def __init__(self, column_name, is_invalid, in_dictionary, ontology_names, data_access):
		super(OntologyColumn, self).__init__(column_name, is_invalid, in_dictionary, data_access)
		self.ontology_names = ontology_names
		self.ontology_details = data_access.get_column_ontology_details(column_name)			

	def _addValue(self, value, validate_contents):
		status = 'good'
		if validate_contents:
			if not self._validate(value, self.ontology_names):
				status = 'bad'
				self.is_invalid(self.column_name, len(self.values))
		self.values.append((value, status))
		
	def writeJSValidation(self):
		ontology_ids = []
		ontology_branch_ids = []
		
		for record in self.ontology_details:
			ontology_ids.append(str(record[1]))
			# Only add if the branch_id is actually set
			if record[2]:
				ontology_branch_ids.append(record[2])
		
		validation_string = 'class="bp_form_complete-{0}-ontprefix_name" size="40" data-bp_include_definitions="true"'.format(','.join(ontology_ids))
		if len(ontology_branch_ids) > 0:
			validation_string += ' data-bp_search_branch="{0}"'.format(','.join(ontology_branch_ids))
		
		return validation_string
	
	def _validate(self, term, ontology_names):
		""" returns true if term is in ontology designated by ontology_name, 
		false otherwise 
		"""
		if self._isUnknown(term):
			return True
		
		for ontology_name in ontology_names:
			term_values = term.split(':')
			if len(term_values) != 2:
				return False
		
			if self._data_access.validateOntologyValue(ontology_name, term_values[1]) > 0:
				return True
		
		# Not found in any list
		return False
	
class TextColumn(BaseColumn):
	""" Text implementation of BaseColumn class
	"""
	def __init__(self, column_name, is_invalid, in_dictionary, max_length, min_length, data_access):
		super(TextColumn, self).__init__(column_name, is_invalid, in_dictionary, data_access)
		self.max_length = max_length
		self.min_length = min_length
		
	def _validate(self, value):
		""" return true if number, false otherwise
		"""
		if self._isUnknown(value):
			return True
		
		if (self.max_length == '') or (self.min_length == ''):
			return False
		elif (len(value) > self.max_length) or (len(value) < self.min_length):
			return False
		else:
			return True
		
	def writeJSValidation(self):
		function_string = "validateTextLength(this, '{column_name}', '{max_length}', '{min_length}')".format(\
			column_name = self.column_name, \
			max_length = self.max_length, \
			min_length = self.min_length)
		validation_string = ' onclick="%s;" ' % (function_string)
		validation_string += ' onkeyup="%s;" ' % (function_string)
		return validation_string
		
