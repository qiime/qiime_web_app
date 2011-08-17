#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.1-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename
from study_summary import print_study_info_and_values_table
from os.path import join
from data_access_connections import data_access_factory
from enums import ServerConfig

class studySummary(TestCase):
    
    def setUp(self):
        """setup the test values"""
        pass
        
        
    def tearDown(self):
        """remove all the files after completing tests """
        pass

    def test_print_study_info_and_values_table(self):
        """ test_print_study_info_and_values_table: This function write the 
            Study summary information below the select-box
        """
        data_access = data_access_factory(ServerConfig.data_access_type)
        analysis_data=[]
        results=data_access.getQiimeSffDbSummary(609)
        
        for row in results:
            analysis_data.append(row)
        
        self.assertEqual(print_study_info_and_values_table(analysis_data,data_access),exp_output)
       
exp_output="""\
<h3>jesse_test (<a href=\'./study_summary/export_metadata.psp\'  target="_blank">download metadata</a>)&nbsp;(<a href=\'./study_summary/export_sffs.psp\'  target="_blank">download sffs</a>)</h3>\
<table>\
<tr>\
<th><u>Study Information</u></th><td>\
</tr>\
<tr>\
<th>Study ID:</th>\
<td style="color:black;text-decoration:none">609</td>\
</tr>\
<tr>\
<th>Project Name:</th>\
<td style="color:black;text-decoration:none">jesse_test</td>\
</tr>\
<tr>\
<th>Study Title:</th>\
<td style="color:black;text-decoration:none">Fasting subset mice for testing purposes</td>\
</tr>\
<tr>\
<th>Study Abstract:</th>\
<td style="color:black;text-decoration:none">This is a test dataset using the Fasting subset of mice.</td>\
</tr>\
<tr>\
<th>Pubmed ID (pmid):</th>\
<td style="color:black;text-decoration:none"><a href=http://www.ncbi.nlm.nih.gov/pubmed?term=None[uid] target="_blank">None</a></td>\
</tr>\
</table>\
<br>\
<table>\
<tr>\
<th><u>SFF(s) Information</u></th>\
<td></td>\
</tr>\
<tr>\
<th>SFF Filename:</th>\
<td>Fasting_subset</td>\
</tr><tr>\
<th>Number of Reads:</th>\
<td>22</td></tr>\
<tr>\
<th>Number of Samples:</th>\
<td>8</td>\
</tr>\
<tr>\
<th>Split-Library Sequences:</th>\
<td>22</td>\
</tr>\
<tr>\
<th><a id=\'sym_0\' onclick="show_hide_samples(\'div_0\',this.id);" style="color:blue;">&#x25BA;</a>&nbsp;Samples</th>\
<td></td>\
</tr>\
</table>\
<div id="div_0" style="display:none;">\
<table border="1px" style="font-size:smaller;">\
<tr>\
<th>SampleID</th>\
<th>Sequences/Sample</th>\
</tr>\
<tr>\
<td>test.PCx634.281528</td>\
<td>13</td>\
</tr>\
<tr>\
<td>test.PCx593.281529</td>\
<td>2</td>\
</tr><tr>\
<td>test.PCx635.281531</td>\
<td>2</td>\
</tr>\
<tr>\
<td>test.PCx481.281527</td>\
<td>1</td>\
</tr>\
<tr>\
<td>test.PCx354.281526</td>\
<td>1</td>\
</tr>\
<tr>\
<td>test.PCx355.281524</td>\
<td>1</td>\
</tr>\
<tr>\
<td>test.PCx636.281530</td>\
<td>1</td>\
</tr>\
<tr>\
<td>test.PCx356.281525</td>\
<td>1</td>\
</tr>\
</table>\
</div>\
<br>\
<table>\
<tr>\
<th>Total Number of Reads:</th>\
<td>22</td>\
</tr>\
</table>\
"""

if __name__ == "__main__":
    main()