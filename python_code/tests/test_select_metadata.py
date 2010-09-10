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
                            get_selected_column_values

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
        '''
            test_public_cols_to_dict: convert array of oracle public columns 
            into a dictionary for use in web page
         '''
        obs=public_cols_to_dict(self.public_columns)
        
        exp={'SEQUENCE_PREP####SEP####EXPERIMENT_TITLE': [77],
             'SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG': [77],
             'SEQUENCE_PREP####SEP####POOL_MEMBER_NAME': [77], 
             'SAMPLE####SEP####ELEVATION': [77], 
             'SEQUENCE_PREP####SEP####RUN_DATE': [77], 
             'SEQUENCE_PREP####SEP####KEY_SEQ': [77], 
             'HOST_ASSOC_VERTIBRATE####SEP####DIET': [77], 
             'HOST####SEP####HOST_TAXID': [89],  
             'STUDY####SEP####STUDY_ALIAS': [89, 77], 
             'EXTRA_SAMPLE_89####SEP####HOST': [89], 
             'SEQUENCE_PREP####SEP####RUN_CENTER': [89], 
             'EXTRA_SAMPLE_89####SEP####DONOR': [89]}
             
        self.assertEqual(obs,exp)

    def test_unique_cols_to_select_box_str(self):
        '''
            test_unique_cols_to_select_box_str: convert the oracle public 
            dictionary columns into the option string for the select box in the 
            web-interface
        '''
        
        obs=unique_cols_to_select_box_str(self.public_columns)
        self.assertEqual(obs,exp_select_box_str)
        
        
    def test_print_metadata_info_and_values_table(self):
        '''
            test_print_metadata_info_and_values_table: this function writes out
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
        '''
            test_get_selected_column_values: get a list of column values for a
            given table and column name
        '''
        controlled_vocab=True
        col_name='SEX'
        table_name='HOST_ASSOC_VERTIBRATE' # this table is mispelled in the DB
        exp_values=['female', 'hermaphrodite', 'male', 'neuter', \
                    'not determined']
        obs=get_selected_column_values(controlled_vocab,col_name,table_name)

        self.assertEqual(obs,exp_values)
        
        
        
exp_select_box_str='''\
<option id="HOST####SEP####HOST_TAXID" value="HOST####SEP####HOST_TAXID####STUDIES####89" onclick="showResult(\'metadata_left_col\',this.id,this.value)">HOST_TAXID</option>\n\n\
<option id="SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG" value="SEQUENCE_PREP####SEP####PRIMER_READ_GROUP_TAG####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">PRIMER_READ_GROUP_TAG</option>\n\n\
<option id="SEQUENCE_PREP####SEP####POOL_MEMBER_NAME" value="SEQUENCE_PREP####SEP####POOL_MEMBER_NAME####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">POOL_MEMBER_NAME</option>\n\n\
<option id="EXTRA_SAMPLE_89####SEP####HOST" value="EXTRA_SAMPLE_89####SEP####HOST####STUDIES####89" onclick="showResult(\'metadata_left_col\',this.id,this.value)">HOST</option>\n\n\
<option id="SEQUENCE_PREP####SEP####RUN_DATE" value="SEQUENCE_PREP####SEP####RUN_DATE####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">RUN_DATE</option>\n\n\
<option id="EXTRA_SAMPLE_89####SEP####DONOR" value="EXTRA_SAMPLE_89####SEP####DONOR####STUDIES####89" onclick="showResult(\'metadata_left_col\',this.id,this.value)">DONOR</option>\n\n\
<option id="SAMPLE####SEP####ELEVATION" value="SAMPLE####SEP####ELEVATION####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">ELEVATION</option>\n\n\
<option id="STUDY####SEP####STUDY_ALIAS" value="STUDY####SEP####STUDY_ALIAS####STUDIES####89S77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">STUDY_ALIAS</option>\n\n\
<option id="SEQUENCE_PREP####SEP####KEY_SEQ" value="SEQUENCE_PREP####SEP####KEY_SEQ####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">KEY_SEQ</option>\n\n\
<option id="HOST_ASSOC_VERTIBRATE####SEP####DIET" value="HOST_ASSOC_VERTIBRATE####SEP####DIET####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">DIET</option>\n\n\
<option id="SEQUENCE_PREP####SEP####RUN_CENTER" value="SEQUENCE_PREP####SEP####RUN_CENTER####STUDIES####89" onclick="showResult(\'metadata_left_col\',this.id,this.value)">RUN_CENTER</option>\n\n\
<option id="SEQUENCE_PREP####SEP####EXPERIMENT_TITLE" value="SEQUENCE_PREP####SEP####EXPERIMENT_TITLE####STUDIES####77" onclick="showResult(\'metadata_left_col\',this.id,this.value)">EXPERIMENT_TITLE</option>\n\
'''

exp_info_table1='''\
<tr>\
<td><em>Column Name:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
</tr>\
<tr>\
<td><em>Table Name:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr>\
<td><em>Data Type:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr>\
<td><em>Description or Value:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
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
<td><em>Table Name:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr>\
<td colspan=2 style="color:black;text-decoration:none">This is a study-specific column defined by the user, field-specific information is not available.</td>\
</tr>\
'''

exp_info_table3='''\
<tr>\
<td><em>Column Name:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
<td rowspan=5><b>Select Values</b><br>\
<select onchange="window.location.href=this.options[this.selectedIndex].value;reset_select(this);">\
<option value="javascript:"><option value="javascript:select_all_col_values(\'TEST####SEP####TEST_COL####STUDIES####100\');">All\
<option value="javascript:select_none_col_values(\'TEST####SEP####TEST_COL####STUDIES####100\');">None\
<option value="Javascript:select_invert_col_values(\'TEST####SEP####TEST_COL####STUDIES####100\');">Invert\
</select>\
<select id="TEST####SEP####TEST_COL####STUDIES####100" multiple style="width:300px;" onchange="saveSelection(this.id)">\
<option id="y" value="y">y</option>\
<option id="n" value="n">n</option>\
</select>\
</tr>\
<tr>\
<td><em>Table Name:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr><td><em>Data Type:</em></td>\
<td style="color:black;text-decoration:none">TEST</td>\
</tr>\
<tr>\
<td><em>Description or Value:</em></td>\
<td style="color:black;text-decoration:none">TEST_COL</td>\
</tr>\
<tr>\
<td><em>Definition:</em></td>\
<td style="color:black;text-decoration:none">This is a test</td>\
</tr>\
'''

if __name__ == "__main__":
    main()
    
    