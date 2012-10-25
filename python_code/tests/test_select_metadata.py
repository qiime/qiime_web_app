#!/usr/bin/env python
# File created on 10 Sep 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME-DB Project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from cogent.util.unit_test import TestCase, main
from select_metadata import public_cols_to_dict,unique_cols_to_select_box_str,\
                            print_metadata_info_and_values_table,\
                            get_selected_column_values,\
                            get_table_col_values_from_form

from types import *
from exceptions import *

from data_access_connections import data_access_factory
from enums import ServerConfig
data_access = data_access_factory(ServerConfig.data_access_type)

'''
The following StringField class was pulled out of the util script in the mod_python 
library.  A few modifications were made to allow for the generation of a 
Field class for form posting. Here is one link to this function via the svn
repository:

https://svn.apache.org/repos/asf/quetzalcoatl/mod_python/trunk/lib/python/mod_python/util.py

This function should be maintained in mod_python 3.3.1 as well:

http://www.apache.org/dist/httpd/modpython/

'''

""" The classes below are a (almost) a drop-in replacement for the
    standard cgi.py FieldStorage class. They should have pretty much the
    same functionality.

    These classes differ in that unlike cgi.FieldStorage, they are not
    recursive. The class FieldStorage contains a list of instances of
    Field class. Field class is incapable of storing anything in it.

    These objects should be considerably faster than the ones in cgi.py
    because they do not expect CGI environment, and are
    optimized specifically for Apache and mod_python.
"""

class StringField(str):
    """ This class is basically a string with
    added attributes for compatibility with std lib cgi.py. Basically, this
    works the opposite of Field, as it stores its data in a string, but creates
    a file on demand. Field creates a value on demand and stores data in a file.
    """
    filename = None
    headers = {}
    ctype = "text/plain"
    type_options = {}
    disposition = None
    disp_options = None
    name='test'
    
    # I wanted __init__(name, value) but that does not work (apparently, you
    # cannot subclass str with a constructor that takes >1 argument)
    def __init__(self,value):
        '''Create StringField instance. You'll have to set name yourself.'''
        str.__init__(self)
        self.value = value

   
    def __getattr__(self, name):
        if name != 'file':
            raise AttributeError, name
        self.file = cStringIO.StringIO(self.value)
        return self.file
        
    def __repr__(self):
        """Return printable representation (to pass unit tests)."""
        output=self.value.split(':')
        return "Field(%s,%s)" % (`output[0]`,`output[1]`)


## The test case timing code included in this file is adapted from
## recipes provided at:
##  http://code.activestate.com/recipes/534115-function-timeout/
##  http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
class TimeExceededError(Exception):
    pass

allowed_seconds_per_test = 600

def timeout(signum, frame):
    raise TimeExceededError,\
     "Test failed to run in allowed time (%d seconds)."\
      % allowed_seconds_per_test
    
class SelectMetadataTests(TestCase):
    
    def setUp(self):
        self.public_columns=[('EXPERIMENT_TITLE', '"SEQUENCE_PREP"', 77), 
                             ('PRIMER_READ_GROUP_TAG', '"SEQUENCE_PREP"', 77), 
                             ('POOL_MEMBER_NAME', '"SEQUENCE_PREP"', 77), 
                             ('ELEVATION', '"SAMPLE"', 77), 
                             ('RUN_DATE', '"SEQUENCE_PREP"', 77), 
                             ('KEY_SEQ', '"SEQUENCE_PREP"', 77), 
                             ('DIET', '"HOST_ASSOC_VERTIBRATE"', 77), 
                             ('HOST_TAXID', '"HOST"', 89), 
                             ('STUDY_ALIAS', '"STUDY"', 89),
                             ('STUDY_ALIAS', '"STUDY"', 77), 
                             ('HOST', '"EXTRA_SAMPLE_89"', 89), 
                             ('RUN_CENTER', '"SEQUENCE_PREP"', 89), 
                             ('DONOR', '"EXTRA_SAMPLE_89"', 89)]
        self.public_columns=[('run_date','"SEQUENCE_PREP"',0),
                             ('dob','"EXTRA_SAMPLE_0"',0),
                             ('longitude','"SAMPLE"',0),
                             ('platform','"SEQUENCE_PREP"',0),
                             ('host_subject_id','"HOST"',0)]
        self.table='TEST'
        self.col='TEST_COL'
        self.studies='100'
        self.col_values=['y','n']
        
    def test_public_cols_to_dict(self):
        ''' test_public_cols_to_dict: convert array of oracle public columns 
            into a dictionary for use in web page
         '''
        obs=public_cols_to_dict(self.public_columns)
        
        exp=({'SAMPLE####SEP####longitude': [0], 
              'SEQUENCE_PREP####SEP####platform': [0], 
              'SEQUENCE_PREP####SEP####run_date': [0], 
              'HOST####SEP####host_subject_id': [0]}, ['0'])
             
        self.assertEqual(obs,exp)

    def test_unique_cols_to_select_box_str(self):
        ''' test_unique_cols_to_select_box_str: convert the oracle public 
            dictionary columns into the option string for the select box in the 
            web-interface
        '''
        
        obs=unique_cols_to_select_box_str(self.public_columns,data_access)
        self.assertEqual(obs,exp_select_box_str)
        
        
    def test_print_metadata_info_and_values_table(self):
        ''' test_print_metadata_info_and_values_table: this function writes out
            the information table below the select metadata boxes
        '''
        query_results1=[['TEST','TEST_COL','This is a test']]
        query_results2=[]
        show_values1='0'
        show_values2='1'
        
        # test if the values are not to be shown and there are query results
        obs1=print_metadata_info_and_values_table(query_results1,show_values1,\
                                             self.table,self.col,self.studies,\
                                             self.col_values)

        self.assertEqual(obs1,exp_info_table1)
        
        # test if the values are not to be shown and there are no query results
        obs2=print_metadata_info_and_values_table(query_results2,show_values1,\
                                             self.table,self.col,self.studies,\
                                             self.col_values)
        
        self.assertEqual(obs2,exp_info_table2)
        
        # test if the values are shown and there are query results
        obs3=print_metadata_info_and_values_table(query_results1,show_values2,\
                                             self.table,self.col,self.studies,\
                                             self.col_values)
        self.assertEqual(obs3,exp_info_table3)
    
    def test_get_selected_column_values(self):
        ''' test_get_selected_column_values: get a list of column values for a
            given table and column name
        '''
        controlled_vocab=True
        col_name='SEX'
        table_name='HOST_ASSOC_VERTIBRATE' # this table is mispelled in the DB
        exp_values=['female', 'hermaphrodite', 'male', 'neuter', \
                    'not determined']
        obs=get_selected_column_values(controlled_vocab,col_name,table_name,1,
                                       '0',data_access)

        self.assertEqual(obs,exp_values)
        
    def test_get_table_col_values_from_form(self):
        ''' test_get_selected_column_values: get a list of column values for a
            given table and column name
        '''
        form1={'fname_prefix': [StringField('fname_prefix:')]}
        
        form2={'fname_prefix': [StringField('fname_prefix:')], 
               'HOST####SEP####host_subject_id####STUDIES####0': StringField('HOST####SEP####host_subject_id####STUDIES####0:####ALL####')}
        form3={'fname_prefix': [StringField('fname_prefix')], 
               'HOST####SEP####host_subject_id####STUDIES####0': StringField('HOST####SEP####host_subject_id####STUDIES####0:Input1')}
        
        exp1={}
        exp2={'HOST####SEP####host_subject_id####STUDIES####0': 'HOST####SEP####host_subject_id####STUDIES####0:####ALL####'}
        exp3={'HOST####SEP####host_subject_id####STUDIES####0': 'HOST####SEP####host_subject_id####STUDIES####0:Input1'}

                
        obs1=get_table_col_values_from_form(form1)
        self.assertEqual(obs1,exp1)
        
        obs2=get_table_col_values_from_form(form2)
        self.assertEqual(obs2,exp2)

        obs3=get_table_col_values_from_form(form3)
        self.assertEqual(obs3,exp3)
        
        
exp_select_box_str='''\
available_cols=new Array();
available_cols["SAMPLE####SEP####longitude"]=new Array();
available_cols["SAMPLE####SEP####longitude"]=["common_study","ADD#ENDGRP#SAMPLE####SEP####longitude","SAMPLE####SEP####longitude####STUDIES####0","longitude"]
available_cols["SEQUENCE_PREP####SEP####platform"]=new Array();
available_cols["SEQUENCE_PREP####SEP####platform"]=["common_study","ADD#ENDGRP#SEQUENCE_PREP####SEP####platform","SEQUENCE_PREP####SEP####platform####STUDIES####0","platform"]
available_cols["SEQUENCE_PREP####SEP####run_date"]=new Array();
available_cols["SEQUENCE_PREP####SEP####run_date"]=["common_study","ADD#ENDGRP#SEQUENCE_PREP####SEP####run_date","SEQUENCE_PREP####SEP####run_date####STUDIES####0","run_date"]
available_cols["HOST####SEP####host_subject_id"]=new Array();
available_cols["HOST####SEP####host_subject_id"]=["common_study","ADD#ENDGRP#HOST####SEP####host_subject_id","HOST####SEP####host_subject_id####STUDIES####0","host_subject_id"]
'''

exp_info_table1='''\
<tr>\
<td><em>Column Name:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
</tr>\
<tr>\
<td><em>Data Type:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr>\
<td><em>Definition:</em></td>\
<td style="color:black;text-decoration:none">This is a test</td>\
</tr>\
'''

exp_info_table2='''\
<tr>\
<td><em>Column Name:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
</tr>\
<tr>\
<td colspan=2 style="color:black;text-decoration:none">This is a study-specific column defined by the user, field-specific information is not available.</td>\
</tr>\
'''

exp_info_table3='''\
<tr>\
<td><em>Column Name:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
<td rowspan=3><b>Select Values</b><br><select onchange="window.location.href=this.options[this.selectedIndex].value;reset_select(this);saveSelection(\'TEST####SEP####TEST_COL####STUDIES####100\')"><option value="javascript:"><option value="javascript:select_all_col_values(\'TEST####SEP####TEST_COL####STUDIES####100\');">All<option value="javascript:select_none_col_values(\'TEST####SEP####TEST_COL####STUDIES####100\');">None<option value="Javascript:select_invert_col_values(\'TEST####SEP####TEST_COL####STUDIES####100\');">Invert</select><select style="width:300px;" id="TEST####SEP####TEST_COL####STUDIES####100" multiple onchange="saveSelection(this.id)"><option id="y" value="y" onmouseover="return overlib(\'y\',WIDTH, 300);" onmouseout="return nd();">y</option><option id="n" value="n" onmouseover="return overlib(\'n\',WIDTH, 300);" onmouseout="return nd();">n</option></select></td>\
</tr>\
<tr>\
<td><em>Data Type:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr>\
<td><em>Definition:</em></td>\
<td style="color:black;text-decoration:none">This is a test</td>\
</tr>\
'''

if __name__ == "__main__":
    main()
    
    
