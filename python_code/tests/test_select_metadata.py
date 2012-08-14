#!/usr/bin/env python
# File created on 10 Sep 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME Web App"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from cogent.util.unit_test import TestCase, main
from select_metadata import public_cols_to_dict,unique_cols_to_select_box_str,\
                            print_metadata_info_and_values_table,\
                            get_selected_column_values,\
                            get_table_col_values_from_form,get_otu_table

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
        self.table='TEST'
        self.col='TEST_COL'
        self.studies='100'
        self.col_values=['y','n']
        
    def test_public_cols_to_dict(self):
        ''' test_public_cols_to_dict: convert array of oracle public columns 
            into a dictionary for use in web page
         '''
        obs=public_cols_to_dict(self.public_columns)
        
        exp=({'HOST####SEP####HOST_TAXID': [89], 
             'SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG': [77], 
             'SEQUENCE_PREP####SEP####POOL_MEMBER_NAME': [77], 
             'SEQUENCE_PREP####SEP####RUN_DATE': [77], 
             'SAMPLE####SEP####ELEVATION': [77], 
             'STUDY####SEP####STUDY_ALIAS': [89, 77], 
             'SEQUENCE_PREP####SEP####KEY_SEQ': [77], 
             'HOST_ASSOC_VERTIBRATE####SEP####DIET': [77], 
             'SEQUENCE_PREP####SEP####RUN_CENTER': [89], 
             'SEQUENCE_PREP####SEP####EXPERIMENT_TITLE': [77]}, ['77', '89'])
             
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
        obs=get_selected_column_values(controlled_vocab,col_name,table_name,1,'609',data_access)

        self.assertEqual(obs,exp_values)
        
    def test_get_table_col_values_from_form(self):
        ''' test_get_selected_column_values: get a list of column values for a
            given table and column name
        '''
        form1={'fname_prefix': [StringField('fname_prefix:')]}
        
        form2={'fname_prefix': [StringField('fname_prefix:')], 
               'HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289': StringField('HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289:####ALL####')}
        form3={'fname_prefix': [StringField('fname_prefix')], 
               'HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289': StringField('HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289:female')}
        
        exp1={}
        exp2={'HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289': StringField('HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289:####ALL####')}
        exp3={'HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289': StringField('HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####89S101S77S289:female')}
        exp_values=['female', 'hermaphrodite', 'male', 'neuter', \
                    'not determined']
                
        obs1=get_table_col_values_from_form(form1)
        self.assertEqual(obs1,exp1)
        
        obs2=get_table_col_values_from_form(form2)
        self.assertEqual(obs2,exp2)

        obs3=get_table_col_values_from_form(form3)
        self.assertEqual(obs3,exp3)
        
    #
    def test_get_otu_table(self):
        ''' test_get_otu_table: get OTU table for given set of params
        '''
    
        obs1=get_otu_table(data_access, {'HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####0': StringField('HOST_ASSOC_VERTIBRATE####SEP####SEX####STUDIES####0:female')},'12171',0,'PHPR')
        self.assertEqual(obs1,'# QIIME v1.5.0-dev OTU table\n#OTU ID')
        
        
exp_select_box_str='''\
available_cols=new Array();
available_cols["HOST####SEP####HOST_TAXID"]=new Array();
available_cols["HOST####SEP####HOST_TAXID"]=["unique_study","ADD#ENDGRP#HOST####SEP####HOST_TAXID","HOST####SEP####HOST_TAXID####STUDIES####77S89","HOST_TAXID"]
available_cols["SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG"]=new Array();
available_cols["SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG"]=["unique_study","ADD#ENDGRP#SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG","SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG####STUDIES####77S89","PRIMER_READ_GROUP_TAG"]
available_cols["SEQUENCE_PREP####SEP####POOL_MEMBER_NAME"]=new Array();
available_cols["SEQUENCE_PREP####SEP####POOL_MEMBER_NAME"]=["unique_study","ADD#ENDGRP#SEQUENCE_PREP####SEP####POOL_MEMBER_NAME","SEQUENCE_PREP####SEP####POOL_MEMBER_NAME####STUDIES####77S89","POOL_MEMBER_NAME"]
available_cols["SEQUENCE_PREP####SEP####RUN_DATE"]=new Array();
available_cols["SEQUENCE_PREP####SEP####RUN_DATE"]=["unique_study","PREP#ENDGRP#SEQUENCE_PREP####SEP####RUN_DATE","SEQUENCE_PREP####SEP####RUN_DATE####STUDIES####77S89","RUN_DATE"]
available_cols["SAMPLE####SEP####ELEVATION"]=new Array();
available_cols["SAMPLE####SEP####ELEVATION"]=["unique_study","SAMPLE#ENDGRP#SAMPLE####SEP####ELEVATION","SAMPLE####SEP####ELEVATION####STUDIES####77S89","ELEVATION"]
available_cols["STUDY####SEP####STUDY_ALIAS"]=new Array();
available_cols["STUDY####SEP####STUDY_ALIAS"]=["common_study","STUDY#ENDGRP#STUDY####SEP####STUDY_ALIAS","STUDY####SEP####STUDY_ALIAS####STUDIES####77S89","STUDY_ALIAS"]
available_cols["SEQUENCE_PREP####SEP####KEY_SEQ"]=new Array();
available_cols["SEQUENCE_PREP####SEP####KEY_SEQ"]=["unique_study","PREP#ENDGRP#SEQUENCE_PREP####SEP####KEY_SEQ","SEQUENCE_PREP####SEP####KEY_SEQ####STUDIES####77S89","KEY_SEQ"]
available_cols["HOST_ASSOC_VERTIBRATE####SEP####DIET"]=new Array();
available_cols["HOST_ASSOC_VERTIBRATE####SEP####DIET"]=["unique_study","ADD#ENDGRP#HOST_ASSOC_VERTIBRATE####SEP####DIET","HOST_ASSOC_VERTIBRATE####SEP####DIET####STUDIES####77S89","DIET"]
available_cols["SEQUENCE_PREP####SEP####RUN_CENTER"]=new Array();
available_cols["SEQUENCE_PREP####SEP####RUN_CENTER"]=["unique_study","PREP#ENDGRP#SEQUENCE_PREP####SEP####RUN_CENTER","SEQUENCE_PREP####SEP####RUN_CENTER####STUDIES####77S89","RUN_CENTER"]
available_cols["SEQUENCE_PREP####SEP####EXPERIMENT_TITLE"]=new Array();
available_cols["SEQUENCE_PREP####SEP####EXPERIMENT_TITLE"]=["unique_study","PREP#ENDGRP#SEQUENCE_PREP####SEP####EXPERIMENT_TITLE","SEQUENCE_PREP####SEP####EXPERIMENT_TITLE####STUDIES####77S89","EXPERIMENT_TITLE"]
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
    
    
