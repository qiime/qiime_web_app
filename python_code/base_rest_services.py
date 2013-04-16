#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from data_access_connections import data_access_factory
from enums import ServerConfig
from sample_export import export_fasta_from_sample
from os.path import join
import stat
import threading
import gc
from difflib import SequenceMatcher

class DataLogger(object):
    """ Generic logger for export services
    
    This class will log entries in a list, optionally output to the console if debug = True,
    and can dump the log to a log file.
    """
    def __init__(self, log_file_path, debug = False):
        self._log_file_path = log_file_path
        self._debug = debug
        self._log = []
        self._log_file = open(log_file_path, 'w')
        self._log_file.write('Begin Log\n\n')
        
    def __del__(self):
        self._log_file.write('\n\nEnd log')
        self._log_file.close()
        
    def log_entry(self, entry):
        """ Adds an entry to the log, prints to console if debug = True
        """
        self._log.append(entry)
        self._log_file.write('{0}\n'.format(entry))
        if self._debug:
            print entry

class BaseRestServices(object):
    def __init__(self, study_id, web_app_user_id, debug = False):
        self.hostname = None
        self.study_url = None
        self.sample_url = None
        self.library_url = None
        self.sequence_url = None
        self.study_id = study_id
        self.base_study_path = '/home/wwwuser/user_data/studies/study_{0}'.format(study_id)

        self.web_app_user_id = web_app_user_id
        # Set up a logger so we can see what's going on
        log_file_path = join(self.base_study_path, 'ebi_export_log.txt')
        self.logger = DataLogger(log_file_path, debug)
        
        self.rest_data_helper = RestDataHelper(study_id, web_app_user_id, self.logger)
        self.data_access = data_access_factory(ServerConfig.data_access_type)
        #self.errors = []
        self.debug = debug

    def send_post_data(self, url_path, file_contents, debug):
        raise NotImplementedError('Base class method has no implementation')
            
    def generate_metadata_files(self, debug = False):
        raise NotImplementedError('Base class method has no implementation')
        
    def clean_whitespace(self, text):
        return ' '.join(text.split())

        
    def clean_text_value(self, value):
        # Order matters! Leave & as the first replace
        value = str(value).replace('&', '&amp;')
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        return value

    def controlled_vocab_lookup(self, controlled_vocab, search_term):
        """ Performs a semi-fuzzy search for a term match in specified vocabulary
        """
        search_term = search_term
        best_ratio = 0
        best_term = None
        minimum_ratio = 0.8
        return_value = None

        for term in controlled_vocab:
            # Exact match - exit with value
            if search_term == term:
                return search_term
            elif term.lower() in search_term.lower() or search_term.lower() in term.lower():
                return search_term

            # Let's see how similar the strings are
            s = SequenceMatcher(None, search_term.lower(), term.lower())
            ratio = s.ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_term = term

        # Examine ratio/term and see if we have anything reasonable
        if best_ratio >= minimum_ratio:
            return_value = best_term

        return return_value
    
class RestDataHelper(object):
    """ A class for consolidating complex or commonly used functions
    """
    def __init__(self, study_id, web_app_user_id, logger):
        self.data_access = data_access_factory(ServerConfig.data_access_type)
        self.study_id = study_id
        self.web_app_user_id = web_app_user_id
        self.invalid_values = set(['', ' ', None, 'None'])
        self.required_columns = set(['library_construction_protocol', 'experiment_design_description', 'taxon_id', 'description'])
        self.study_info = None
        self.logger = logger
        
    def __del__(self):
        """ Destructor
        
        Sets data_access to None to guarantee GC finds it. Have had issues in the past;
        this seems to help prevent dangling connections.
        """
        self.data_access = None
        gc.collect()
        
    def get_study_info(self):
        """ Gets all study-level data
        """
        # If it's already been filled out, just return it
        if self.study_info:
            return self.study_info
        
        # Fill out the study info heirarchy
        self.study_info = self.data_access.getStudyInfo(self.study_id, self.web_app_user_id)
        
        # Remove any columns with invalid data or fields we do not want to submit
        del self.study_info['mapping_file_complete']
        del self.study_info['can_delete']
        del self.study_info['project_id']
        del self.study_info['lab_person_contact']
        del self.study_info['emp_person']
        del self.study_info['has_extracted_data']
        del self.study_info['number_samples_promised']
        del self.study_info['spatial_series']
        del self.study_info['first_contact']
        del self.study_info['has_physical_specimen']
        del self.study_info['avg_emp_score']
        del self.study_info['user_emp_score']
        del self.study_info['lab_person']
        del self.study_info['principal_investigator']
        del self.study_info['principal_investigator_contact']
        del self.study_info['most_recent_contact']

        fields_to_remove = []
        for field in self.study_info:
            if self.study_info[field] in self.invalid_values:
                fields_to_remove.append(field)
        
        for field in fields_to_remove:
            del self.study_info[field]
        
        # Add the list to hold the sample dicts
        self.study_info['samples'] = []
        
        # A few values necessary to run findMetadataTable
        lock = threading.Lock()
        log = []
        field_type = 'text'

        # Get the list of samples and column names for this study
        samples = self.data_access.getSampleList(self.study_id)
        study_columns = self.data_access.getStudyActualColumns(self.study_id)

        # Iterate over all samples in the study
        for sample_id in samples:               
            sample_dict = {}
            sample_dict['sample_name'] = samples[sample_id]
            sample_dict['sample_id'] = sample_id
            sample_dict['preps'] = []
            
            # Get all of the sample values stored in a dict
            tables_and_columns = {}
            for column_name in study_columns:
                table_name = self.data_access.findMetadataTable(column_name, field_type, log, self.study_id, lock)
                if not table_name:
                    continue
                    
                table_category = self.data_access.getTableCategory(table_name)
                if table_category in ['study', 'prep']:
                    continue

                # Pre-determine which columns to fetch so we can do it all at once for each table. 
                # Pretty slow to do it for every field individually
                # Will look like this: {table_name : [field1, field2, field3...]}
                if table_name not in tables_and_columns:
                    tables_and_columns[table_name] = []
                # One exception - public is a keyword and must be quoted
                if column_name.lower() in set(['public', 'level']):
                    column_name = '"{0}"'.format(column_name.upper())
                tables_and_columns[table_name].append('{0}'.format(column_name))
                
            for table_name in tables_and_columns:
                column_list = tables_and_columns[table_name]
                if table_name.lower() == 'host':
                    statement = 'select {0} from {1} x inner join host_sample hs on x.host_id = hs.host_id where hs.sample_id = {2}'.format(', '.join(column_list), table_name, sample_id)
                else:
                    statement = 'select {0} from {1} where sample_id = {2}'.format(', '.join(column_list), table_name, sample_id)
                self.logger.log_entry(statement)
                results = self.data_access.dynamicMetadataSelect(statement).fetchone()
                self.logger.log_entry(str(results))
                
                for idx, column_value in enumerate(results):
                    column_name = column_list[idx]
                    if column_value in self.invalid_values:
                        # If the column name is required, give it a default value. Required
                        # columns are those that are explicitly referenced in the XML
                        # generation code.
                        if column_name in self.required_columns:
                            if column_name == 'taxon_id':
                                column_value = '0'
                            else:
                                column_value = ''
                        else:
                            self.logger.log_entry('Skipping non-value for column %s in table %s for sample %s (value is: "%s")' % (column_name, table_name, sample_id, str(column_value)))
                            continue
                    
                    sample_dict[column_name] = column_value
                
            # Fill out the 'preps' list in the sample dict
            for sample_id, row_number, num_sequences in self.data_access.getPrepList(sample_id):
                prep_dict = {}
                tables_and_columns = {}
                prep_dict['row_number'] = row_number
                prep_dict['num_sequences'] = num_sequences

                for column_name in study_columns:
                    table_name = self.data_access.findMetadataTable(column_name, field_type, log, self.study_id, lock)
                    table_category = self.data_access.getTableCategory(table_name)
            
                    # Skip the prep and study columns
                    if table_category != 'prep':
                        continue

                    # Pre-determine which columns to fetch so we can do it all at once for each table. 
                    # Pretty slow to do it for every field individually
                    # Will look like this: {table_name : [field1, field2, field3...]}
                    if table_name not in tables_and_columns:
                        tables_and_columns[table_name] = []
                    tables_and_columns[table_name].append('{0}'.format(column_name))
            
                for table_name in tables_and_columns:
                    column_list = tables_and_columns[table_name]
                    statement = 'select {0} from {1} where sample_id = {2} and row_number = {3}'.format(', '.join(column_list), table_name, sample_id, row_number)
                    self.logger.log_entry(statement)
                    results = self.data_access.dynamicMetadataSelect(statement).fetchone()
                    self.logger.log_entry(str(results))

                    for idx, column_value in enumerate(results):
                        column_name = column_list[idx]
                        self.logger.log_entry('idx: {0}, column: {1}, value: {2}'.format(idx, column_name, column_value))
                        if column_value in self.invalid_values:
                            if column_name in self.required_columns:
                                column_value = ''
                            else:
                                self.logger.log_entry('Skipping non-value for column %s in table %s for sample %s (value is: "%s")' % (column_name, table_name, sample_id, str(column_value)))
                                continue
                        prep_dict[column_name] = column_value
                    
                # Add this prep dict to the sample's collection
                sample_dict['preps'].append(prep_dict)
                    
            # Add this sample info to the study's collection
            self.study_info['samples'].append(sample_dict)
    
        return self.study_info
        
    def get_study_columns(self):
        """ Get the column for this study and bin them into sample and prep lists
        """
        study_columns = self.data_access.getStudyActualColumns(self.study_id)
        return study_columns
        
    def get_samples(self):
        """ Find the samples for this study
        """
        samples = self.data_access.getSampleList(self.study_id)
        return samples
        
