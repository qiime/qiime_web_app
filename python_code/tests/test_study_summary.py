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
<table><tr><th><u>Study Information</u></th><td></tr><tr><th>Study ID:</th>\
<td style="color:black;text-decoration:none">609</td></tr>\
<tr><th>Project Name:</th><td style="color:black;text-decoration:none">\
jesse_test_fasta</td></tr><tr><th>Study Title:</th>\
<td style="color:black;text-decoration:none">Fasting subset mice for testing purposes</td>\
</tr><tr><th>Study Abstract:</th><td style="color:black;text-decoration:none">\
This is a test dataset using the Fasting subset of mice.</td></tr><tr>\
<th>Pubmed ID (pmid):</th><td style="color:black;text-decoration:none">\
<a href=http://www.ncbi.nlm.nih.gov/pubmed?term=None[uid] target="_blank">\
None</a></td></tr></table><br><table><th>Download Sequence Data:</th>\
<td style="color:red;">This dataset is not available. Feel free to contact \
Jesse Stombaugh for the status of this dataset (<a href=\
'mailto:jesse.stombaugh@colorado.edu?subject=Status of QIIME-DB Study: 609\'>\
email</a>)</td></table>\
"""

if __name__ == "__main__":
    main()
