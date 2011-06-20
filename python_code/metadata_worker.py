#/bin/env python

"""
Worker thread for metadata insert
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

import threading
import mod_python
from data_access_connections import data_access_factory
from enums import ServerConfig
from metadata_table import *
from threading import Lock

class TestThread(threading.Thread):
    def __init__(self, val):
        threading.Thread.__init__(self)
        self.val = val
    
    def setValues(self, req):
        self.req = req
    
    def run(self):
        print self.val

class MetadataWorkerThread(threading.Thread):
    def __init__(self, form, item_list, sample_key_fields, prep_key_fields, host_key_fields, \
        study_name, study_id, data_access, updateCallback, errorCallback, lock):
        threading.Thread.__init__(self)
        self.item_list = item_list
        self.sample_key_fields = sample_key_fields
        self.prep_key_fields = prep_key_fields
        self.host_key_fields = host_key_fields
        self.study_name = study_name
        self.form = form
        self.study_id = study_id
        self.data_access = data_access
        self.updateCallback = updateCallback
        self.errorCallback = errorCallback
        self.lock = lock
    
    def run(self):
        
        da = data_access_factory(ServerConfig.data_access_type)
        item_count = len(self.item_list)
        
        for item in self.item_list:
            
            # Reset the key_field
            key_field = None
        
            # Put the parts into more meaningful variables
            parts = item.split(':')
            field_type = parts[0]
            row_num = parts[1]
            field_name = parts[3]
            field_value = self.form[item]
        
            # Figure out what the key field is going to be
            if field_type == 'sample':
                key_field = self.sample_key_fields[row_num]
            elif field_type == 'prep':
                key_field = self.prep_key_fields[row_num]
            elif field_type == 'study':
                key_field = self.study_name
        
            if len(self.host_key_fields) > 0 and field_type == 'sample':
                try:
                    host_key_field = self.host_key_fields[row_num]
                except:
                    # Do nothing if not found
                    pass
            else:
                host_key_field = None
        
            # Just in case...
            if key_field == None:
                continue
        
            # For oracle, clean up single quotes
            field_value = field_value.replace('\'', '\'\'')

            try:
                result = da.writeMetadataValue(field_type, key_field, field_name, field_value, \
                    self.study_id, host_key_field, row_num, self.lock)
                # Notify parent that an item was inserted
                self.updateCallback()
            except Exception, e:
                self.errorCallback(e)
