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
from run_combine_otu_map_files import combine_otu_files
from os.path import join
from cogent.util.misc import remove_files
from cogent.app.util import get_tmp_filename

class combineOTUMapsTests(TestCase):
    
    def setUp(self):
        """setup the test values"""
        
        self.dirs_to_remove = []
        self.files_to_remove = []
        self.tmp_dir='/tmp/'
        
        #generate random fnames for OTU maps
        self.f1path=get_tmp_filename(tmp_dir=self.tmp_dir,
         prefix='otu_map1_',suffix='.txt',result_constructor=str)
        self.f2path=get_tmp_filename(tmp_dir=self.tmp_dir,
         prefix='otu_map2_',suffix='.txt',result_constructor=str)
        
        #write out two files for combining
        self.f1out=open(self.f1path,'w')
        self.f2out=open(self.f2path,'w')
        self.f1out.write(map1)
        self.f2out.write(map2)
        self.f1out.close()
        self.f2out.close()
        
        #append fpaths to an array
        self.otu_map_fpaths=[]
        self.otu_map_fpaths.append(self.f1path)
        self.otu_map_fpaths.append(self.f2path)
        
        #make sure files gets cleaned up
        self.files_to_remove.append(self.f1path)
        self.files_to_remove.append(self.f2path)
    
    def tearDown(self):
        """remove all the files after completing tests """
        
        remove_files(self.files_to_remove)

    def test_combine_otu_files(self):
        """test_combine_otu_files: combines two otu mapping files"""
        
        #write out the combined file results
        self.outpath=get_tmp_filename(tmp_dir=self.tmp_dir,
         prefix='otu_map_combined_',suffix='.txt',result_constructor=str)
        self.files_to_remove.append(self.outpath)
        #run the fxn
        combine_otu_files(','.join(self.otu_map_fpaths), self.outpath)
        
        #read output
        fin=open(self.outpath).read()
        self.assertEqual(fin,result_map)
        
        
map1="""\
362383	test.PCx634.281528_1
268947	test.PCx481.281527_4
230364	test.PCx634.281528_8
355771	test.PCx356.281525_17
469832	test.PCx634.281528_2	test.PCx634.281528_11
332311	test.PCx634.281528_7
343906	test.PCx634.281528_5
299668	test.PCx634.281528_18
331820	test.PCx634.281528_9	test.PCx634.281528_10
412648	test.PCx593.281529_22
"""

map2="""\
362383	test.PCx634.281528_10
230364	test.PCx634.281528_80
355771	test.PCx356.281525_170
469832	test.PCx634.281528_20	test.PCx634.281528_110
332311	test.PCx634.281528_70
343906	test.PCx634.281528_50
"""

result_map="""\
362383	test.PCx634.281528_1	test.PCx634.281528_10
268947	test.PCx481.281527_4
230364	test.PCx634.281528_8	test.PCx634.281528_80
355771	test.PCx356.281525_17	test.PCx356.281525_170
469832	test.PCx634.281528_2	test.PCx634.281528_11	test.PCx634.281528_20	test.PCx634.281528_110
332311	test.PCx634.281528_7	test.PCx634.281528_70
343906	test.PCx634.281528_5	test.PCx634.281528_50
299668	test.PCx634.281528_18
331820	test.PCx634.281528_9	test.PCx634.281528_10
412648	test.PCx593.281529_22
"""

if __name__ == "__main__":
    main()