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
from write_mapping_file import write_mapping_file,write_full_mapping_file
from os.path import join,exists
from os import makedirs,listdir
from shutil import rmtree
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

class writeMappingFile(TestCase):
    
    def setUp(self):
        """setup the test values"""
        self.dirs_to_remove = []
        self.files_to_remove = []
        self.tmp_dir='/tmp/'
        
        #generate random fnames for OTU maps
        self.output_dir=get_tmp_filename(tmp_dir=self.tmp_dir,
         prefix='tmp_mapping_files',suffix='',result_constructor=str)
        
        if not exists(self.output_dir):
            makedirs(self.output_dir)
            # if test creates the temp dir, also remove it
            self.dirs_to_remove.append(self.output_dir)
        
    def tearDown(self):
        """remove all the files after completing tests """

        # remove directories last, so we don't get errors
        # trying to remove files which may be in the directories
        for d in self.dirs_to_remove:
            if exists(d):
                rmtree(d)

    def test_write_mapping_file(self):
        """ test_write_mapping_file: This function writes a QIIME-formatted 
            mapping file
        """
        
        # write minimal mapping file
        write_mapping_file(0,False,self.output_dir,True)
        open_fpath=open(join(self.output_dir,'study_0_run_Fasting_subset_mapping.txt')).read()
        
        # this will return just a mapping file with the header, since 
        # study 0 is not assigned in the USER_STUDY table
        self.assertEqual(open_fpath,exp_mapping)
        
        # write full mapping file  
        write_mapping_file(0,True,self.output_dir,True)
        open_fpath=open(join(self.output_dir,'study_0_run_Fasting_subset_mapping.txt')).read()
        
        # this will return just a mapping file with the header, since 
        # study 0 is not assigned in the USER_STUDY table
        self.assertEqual(open_fpath,exp_full_mapping)
    
    def test_write_full_mapping_file(self):
        """ test_write_mapping_file: This function writes a QIIME-formatted 
            mapping file
        """
        
        # write minimal mapping file
        write_full_mapping_file(0,False,self.output_dir,True)
        open_fpath=open(join(self.output_dir,'study_0_mapping.txt')).read()
        
        # this will return just a mapping file with the header, since 
        # study 0 is not assigned in the USER_STUDY table
        self.assertEqual(open_fpath,exp_mapping)

        # write full mapping file
        write_full_mapping_file(0,True,self.output_dir,True)
        open_fpath=open(join(self.output_dir,'study_0_mapping.txt')).read()
        
        # this will return just a mapping file with the header, since 
        # study 0 is not assigned in the USER_STUDY table
        self.assertEqual(open_fpath,exp_full_mapping)

exp_mapping="""\
#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tSTUDY_ID\tRUN_PREFIX\tDescription
"""

exp_full_mapping="""\
#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tSTUDY_ID\tRUN_PREFIX\tALTITUDE\tANONYMIZED_NAME\tASSIGNED_FROM_GEO\tBARCODE_READ_GROUP_TAG\tCOLLECTION_DATE\tCOMMON_NAME\tCOUNTRY\tDEPTH\tDescription_duplicate\tDOB\tELEVATION\tENV_BIOME\tENV_FEATURE\tENV_MATTER\tEXPERIMENT_ALIAS\tEXPERIMENT_CENTER\tEXPERIMENT_DESIGN_DESCRIPTION\tHOST_SUBJECT_ID\tINSTRUMENT_NAME\tKEY_SEQ\tLATITUDE\tLIBRARY_CONSTRUCTION_PROTOCOL\tLONGITUDE\tPH\tPLATFORM\tPOOL_MEMBER_ACCESSION\tPOOL_MEMBER_NAME\tPOOL_PROPORTION\tPRIMER_READ_GROUP_TAG\tREGION\tRUN_ALIAS\tRUN_CENTER\tRUN_DATE\tSAMPLE_CENTER\tSAMP_SIZE\tSEQUENCING_METH\tSTUDY_CENTER\tSTUDY_REF\tTARGET_GENE\tTAXON_ID\tTITLE\tTREATMENT\tDescription
"""

if __name__ == "__main__":
    main()