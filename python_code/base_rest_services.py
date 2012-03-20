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
import os
import stat
import threading

class BaseRestServices(object):
    def __init__(self, study_id, web_app_user_id):
        self.key = None
        self.hostname = None
        self.study_url = None
        self.sample_url = None
        self.library_url = None
        self.sequence_url = None
        self.study_id = study_id
        self.web_app_user_id = web_app_user_id
        self.rest_data_helper = RestDataHelper(study_id, web_app_user_id)
        self.data_access = data_access_factory(ServerConfig.data_access_type)
        self.errors = []

    def send_post_data(self, url_path, file_contents, debug):
        raise NotImplementedError('Base class method has no implementation')
            
    def generate_metadata_files(self, debug = False):
        raise NotImplementedError('Base class method has no implementation')
        
    def clean_whitespace(self, text):
        return ' '.join(text.split())
    
class RestDataHelper(object):
    def __init__(self, study_id, web_app_user_id):
        self._data_access = data_access_factory(ServerConfig.data_access_type)
        self._study_id = study_id
        self._web_app_user_id = web_app_user_id
        self._invalid_values = set(['', ' ', None, 'None'])
        self._study_info = None
        
    def __del__(self):
        self._data_access = None
        
    def get_study_info(self):
        """ Gets all study-level data
        """
        # If it's already been filled out, just return it
        if self._study_info:
            return self._study_info
        
        # Fill out the study info heirarchy
        self._study_info = self._data_access.getStudyInfo(self._study_id, self._web_app_user_id)
        
        # Remove any columns with invalid data or fields we do not want to submit
        del self._study_info['mapping_file_complete']
        del self._study_info['can_delete']
        del self._study_info['project_id']
        del self._study_info['lab_person_contact']
        del self._study_info['emp_person']
        del self._study_info['has_extracted_data']
        del self._study_info['number_samples_promised']
        del self._study_info['spatial_series']
        del self._study_info['first_contact']
        del self._study_info['has_physical_specimen']
        del self._study_info['avg_emp_score']
        del self._study_info['user_emp_score']
        del self._study_info['lab_person']
        del self._study_info['principal_investigator']
        del self._study_info['principal_investigator_contact']
        del self._study_info['most_recent_contact']

        fields_to_remove = []
        for field in self._study_info:
            if self._study_info[field] in self._invalid_values:
                fields_to_remove.append(field)
        
        for field in fields_to_remove:
            del self._study_info[field]
        
        # Add the list to hold the sample dicts
        self._study_info['samples'] = []
        
        # A few values necessary to run findMetadataTable
        lock = threading.Lock()
        log = []
        field_type = 'text'

        # Get the list of samples and column names for this study
        samples = self._data_access.getSampleList(self._study_id)
        study_columns = self._data_access.getStudyActualColumns(self._study_id)

        # Iterate over all samples in the study
        for sample_id in samples:
            sample_dict = {}
            sample_dict['sample_name'] = samples[sample_id]
            sample_dict['sample_id'] = sample_id
            sample_dict['preps'] = []
            
            # Get all of the sample values stored in a dict
            for column_name in study_columns:
                table_name = self._data_access.findMetadataTable(column_name, field_type, log, self._study_id, lock)
                if not table_name:
                    continue
                    
                table_category = self._data_access.getTableCategory(table_name)
                if table_category in ['study', 'prep']:
                    continue          

                column_value = self._data_access.getSampleColumnValue(sample_id, table_name, column_name)
                if column_value in self._invalid_values:
                    print 'Skipping non-value for column %s in table %s for sample %s (value is: "%s")' % (column_name, table_name, sample_id, str(column_value))
                    continue
                    
                sample_dict[column_name] = column_value
                
            # Fill out the 'preps' list in the sample dict
            for sample_id, row_number in self._data_access.getPrepList(sample_id):
                prep_dict = {}
                prep_dict['row_number'] = row_number
                
                for column_name in study_columns:
                    table_name = self._data_access.findMetadataTable(column_name, field_type, log, self._study_id, lock)
                    table_category = self._data_access.getTableCategory(table_name)
            
                    # Skip the prep and study columns
                    if table_category != 'prep':
                        continue
                    
                    column_value = self._data_access.getPrepColumnValue(sample_id, row_number, table_name, column_name)
                    if column_value in self._invalid_values:
                        continue
                    
                    prep_dict[column_name] = column_value
                    
                # Add this prep dict to the sample's collection
                sample_dict['preps'].append(prep_dict)
                    
            # Add this sample info to the study's collection
            self._study_info['samples'].append(sample_dict)
    
        return self._study_info
        
    def get_study_columns(self):
        """ Get the column for this study and bin them into sample and prep lists
        """
        study_columns = self._data_access.getStudyActualColumns(self._study_id)
        return study_columns
        
    def get_samples(self):
        """ Find the samples for this study
        """
        samples = self._data_access.getSampleList(self._study_id)
        return samples
        
    def get_platform_type(self, sample_id, row_number):
        query = 'select platform from sequence_prep where sample_id = {0} and row_number = {1}'.format(str(sample_id), str(row_number))
        #print query
        platform = self.data_access.dynamicMetadataSelect(query).fetchone()[0].lower()
        
        sff = set(['tit', 'titanium', 'flx', '454', '454 flx'])
        fastq = set(['illumina', 'illumina gaiix'])
        fasta = set(['fasta'])
        
        if platform in sff:
            # Note that even though we start with SFF files, we're actually writing out a fastq file for export
            return SffSequenceWriter(self.data_access, study_id, sample_id, row_number, 'sff', root_dir, '.fastq')
        elif platform in fastq:
            return FastqSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fastq', root_dir, '.fastq')
        elif platform in fasta:
            return FastaSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fasta', root_dir, '.fasta')
        else:
            raise ValueError('Could not determine sequence file writer type based on platform: "%s"' % platform)
            return None


        
        