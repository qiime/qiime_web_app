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
from handler_workflows import run_make_otu_heatmap_html
from qiime.workflow import call_commands_serially
from qiime.parse import parse_qiime_parameters
from qiime.util import load_qiime_config, create_dir
from os.path import join
from os import environ, remove
from shutil import rmtree

qiime_config = load_qiime_config()

class TopLevelTests(TestCase):
    """Tests of top-level functions"""

    def setUp(self):
        self._paths_to_clean_up = []
        self._folders_to_cleanup = []
        
        # create output dir
        self.output_dir = '/tmp/heatmap'
        create_dir(self.output_dir)
        self._folders_to_cleanup.append(self.output_dir)
        
        self.otu_table_fp=join(self.output_dir, 'otu_table.biom')
        self._paths_to_clean_up.append(self.otu_table_fp)
        self.mapping_fp=join(self.output_dir, 'mapping_file.txt')
        self._paths_to_clean_up.append(self.mapping_fp)
        
        # write otu table
        otu_table_file = open(self.otu_table_fp,'w')
        otu_table_file.write(biom_json_str)
        otu_table_file.close()
        
        # write mapping file
        mapping_file = open(self.mapping_fp,'w')
        mapping_file.write(mapping_file_str)
        mapping_file.close()
        
        self.tree_fp = \
            '%s/software/gg_otus_4feb2011/trees/gg_97_otus_4feb2011.tre' % \
            (environ['HOME'])
        
    def tearDown(self):
        '''This function removes the generated files'''
        
        map(remove,self._paths_to_clean_up)
        map(rmtree,self._folders_to_cleanup)
        
        
    def test_run_make_otu_heatmap_html(self):
        """ run_make_otu_heatmap_html: generate an OTU Table Heatmap"""
        
        
        valid=run_make_otu_heatmap_html(self.otu_table_fp, self.mapping_fp,     
                                        self.output_dir, {}, qiime_config,  
                                        call_commands_serially,self.tree_fp)
        
        # get the otu-table as js 
        heatmap_js_fpath = join(self.output_dir, 'js', 'otu_table.js')
        obs=open(heatmap_js_fpath,'U').read()
        
        self.assertEqual(obs,exp_heatmap_js_table)



biom_json_str="""\
{"rows": [{"id": "266771", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Lactobacillales", " f__Lactobacillaceae", " g__Lactobacillus", " s__"]}}, {"id": "385188", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "190047", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "275888", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "230541", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "228512", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "269169", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "260756", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "186526", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "272819", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "164638", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "400879", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "303491", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "260666", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "183384", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "169479", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "180097", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "212750", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "165986", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "232773", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "191199", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "174272", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "302407", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "169379", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "197240", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "569818", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "234635", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "309188", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "269815", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "255362", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "178596", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "259056", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "249661", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Porphyromonadaceae", " g__Parabacteroides", " s__"]}}, {"id": "233169", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__", " g__", " s__"]}}, {"id": "204547", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "331820", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__"]}}, {"id": "412648", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "346275", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "275869", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "567604", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Lactobacillales", " f__Lactobacillaceae", " g__Lactobacillus", " s__"]}}, {"id": "176858", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "299668", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Clostridiaceae", " g__Clostridium", " s__"]}}, {"id": "263876", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "264496", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "135493", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "170555", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "216933", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__", " s__"]}}, {"id": "191109", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "172705", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "192659", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "235071", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "191814", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "210178", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "241287", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "307595", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "233411", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "269003", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "227953", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "259451", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "232142", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "322112", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__", " g__", " s__"]}}, {"id": "263334", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "264035", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__"]}}, {"id": "422931", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Lactobacillales", " f__Lactobacillaceae", " g__Lactobacillus", " s__"]}}, {"id": "104780", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "176977", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "97294", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "204911", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "275913", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "270351", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "231997", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "173192", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "268947", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Eubacterium", " s__"]}}, {"id": "272454", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "173697", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "189531", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "318370", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "256899", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "267123", "metadata": {"taxonomy": ["k__Bacteria", " p__Actinobacteria", " c__Actinobacteria (class)", " o__Coriobacteriales", " f__Coriobacteriaceae", " g__Adlercreutzia", " s__"]}}, {"id": "240571", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "182621", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "265813", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "353820", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "271014", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Lactobacillales", " f__Lactobacillaceae", " g__Lactobacillus", " s__"]}}, {"id": "319219", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "131203", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "259965", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__Allobaculum", " s__Allobaculum sp ID4"]}}, {"id": "282677", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "232037", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "115098", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__Allobaculum", " s__Allobaculum sp ID4"]}}, {"id": "163240", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "400627", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "231904", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "321220", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "215193", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "208222", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "230364", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "342948", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "398943", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "268856", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "272270", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "269618", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "335952", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "231684", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "261177", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "175699", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__Allobaculum", " s__Allobaculum sp ID4"]}}, {"id": "95638", "metadata": {"taxonomy": ["k__Bacteria", " p__Deferribacteres", " c__Deferribacteres (class)", " o__Deferribacterales", " f__Deferribacteraceae", " g__Mucispirillum", " s__Mucispirillum schaedleri"]}}, {"id": "171239", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Oscillospira", " s__"]}}, {"id": "303652", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Lactobacillales", " f__Streptococcaceae", " g__Streptococcus", " s__"]}}, {"id": "273549", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "185403", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Peptococcaceae", " g__", " s__"]}}, {"id": "308269", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "212758", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Catabacteriaceae", " g__", " s__"]}}, {"id": "263106", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Oscillospira", " s__"]}}, {"id": "285281", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "227950", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Catabacteriaceae", " g__", " s__"]}}, {"id": "328391", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "178026", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "167204", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "133453", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "470494", "metadata": {"taxonomy": ["k__Bacteria", " p__Proteobacteria", " c__Epsilonproteobacteria", " o__Campylobacterales", " f__Helicobacteraceae", " g__Flexispira", " s__Helicobacter cinaedi"]}}, {"id": "259868", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Oscillospira", " s__"]}}, {"id": "229761", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Clostridiales Family XIII. Incertae Sedis", " g__", " s__"]}}, {"id": "209866", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "447694", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "170502", "metadata": {"taxonomy": ["k__Bacteria", " p__Proteobacteria", " c__Deltaproteobacteria", " o__Desulfovibrionales", " f__Desulfovibrionaceae", " g__Desulfovibrio", " s__"]}}, {"id": "461524", "metadata": {"taxonomy": ["k__Bacteria", " p__Actinobacteria", " c__Actinobacteria (class)", " o__Coriobacteriales", " f__Coriobacteriaceae", " g__", " s__"]}}, {"id": "261434", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "215086", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Catabacteriaceae", " g__", " s__"]}}, {"id": "393399", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "270015", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "288931", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "386087", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "209907", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "268581", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "195470", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "346400", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "413456", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__Coprobacillus", " s__"]}}, {"id": "319134", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "184585", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "278423", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Peptococcaceae", " g__", " s__"]}}, {"id": "441301", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "274084", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__Allobaculum", " s__Allobaculum sp ID4"]}}, {"id": "132165", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "269378", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Ruminococcus", " s__"]}}, {"id": "195445", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "328536", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "318106", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "185989", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "183428", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "578025", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "194822", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "271480", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "403497", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "175432", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "273626", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__", " g__", " s__"]}}, {"id": "258899", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "204144", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "194202", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "300748", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "169943", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "353711", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "187078", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "14035", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "263014", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "316842", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "269872", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "274578", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "15711", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__Clostridium", " s__Clostridium cocleatum"]}}, {"id": "271439", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "269645", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "2000", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__Bacteroides fragilis"]}}, {"id": "270244", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "232941", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "320141", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "230534", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Oscillospira", " s__"]}}, {"id": "199177", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "568692", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__", " g__", " s__"]}}, {"id": "264734", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "309361", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "266214", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "174476", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "269994", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "270840", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "270825", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "309206", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "270519", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "205987", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "261606", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "230573", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "262375", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__", " s__"]}}, {"id": "322991", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "274125", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "258202", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "331317", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "266639", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "190522", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Prevotellaceae", " g__Prevotella", " s__"]}}, {"id": "407754", "metadata": {"taxonomy": ["k__Bacteria", " p__Proteobacteria", " c__Deltaproteobacteria", " o__Desulfovibrionales", " f__Desulfovibrionaceae", " g__", " s__"]}}, {"id": "407007", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Ruminococcus", " s__"]}}, {"id": "333219", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "213896", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "332311", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__Bacteroides eggerthii"]}}, {"id": "166592", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "423411", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "366044", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Porphyromonadaceae", " g__", " s__"]}}, {"id": "321808", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "170335", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Porphyromonadaceae", " g__Odoribacter", " s__"]}}, {"id": "182470", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "267066", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "569158", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__", " s__"]}}, {"id": "170836", "metadata": {"taxonomy": ["k__Bacteria", " p__Proteobacteria", " c__Deltaproteobacteria", " o__Desulfovibrionales", " f__Desulfovibrionaceae", " g__", " s__"]}}, {"id": "175843", "metadata": {"taxonomy": ["k__Bacteria", " p__Actinobacteria", " c__Actinobacteria (class)", " o__Coriobacteriales", " f__Coriobacteriaceae", " g__Adlercreutzia", " s__"]}}, {"id": "269726", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "265730", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "260352", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "182033", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "170545", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Bacillales", " f__Staphylococcaceae", " g__Staphylococcus", " s__"]}}, {"id": "164612", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Bacilli", " o__Bacillales", " f__Staphylococcaceae", " g__Staphylococcus", " s__"]}}, {"id": "264373", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "367581", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Porphyromonadaceae", " g__Parabacteroides", " s__"]}}, {"id": "263592", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "163413", "metadata": {"taxonomy": ["k__Bacteria", " p__TM7", " c__TM7-3", " o__CW040", " f__", " g__", " s__"]}}, {"id": "343906", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "291090", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Porphyromonadaceae", " g__Parabacteroides", " s__Parabacteroides distasonis"]}}, {"id": "469832", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__Bacteroides uniformis"]}}, {"id": "335530", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Rikenellaceae", " g__Alistipes", " s__"]}}, {"id": "332547", "metadata": {"taxonomy": ["k__Bacteria", " p__Actinobacteria", " c__Actinobacteria (class)", " o__Coriobacteriales", " f__Coriobacteriaceae", " g__Adlercreutzia", " s__"]}}, {"id": "197301", "metadata": {"taxonomy": ["k__Bacteria", " p__Actinobacteria", " c__Actinobacteria (class)", " o__Coriobacteriales", " f__Coriobacteriaceae", " g__Adlercreutzia", " s__"]}}, {"id": "362383", "metadata": {"taxonomy": ["k__Bacteria", " p__Tenericutes", " c__Erysipelotrichi", " o__Erysipelotrichales", " f__Erysipelotrichaceae", " g__", " s__Clostridium innocuum"]}}, {"id": "267590", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "262247", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "188969", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "328453", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Coprococcus", " s__"]}}, {"id": "248140", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__Bacteroides caccae"]}}, {"id": "353985", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Porphyromonadaceae", " g__Parabacteroides", " s__Parabacteroides distasonis"]}}, {"id": "289177", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "313166", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__Bacteroidaceae", " g__Bacteroides", " s__"]}}, {"id": "269914", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "263443", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "131681", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "231169", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "273706", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "264889", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "180864", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__", " g__", " s__"]}}, {"id": "181443", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "196240", "metadata": {"taxonomy": ["k__Bacteria", " p__Bacteroidetes", " c__Bacteroidia", " o__Bacteroidales", " f__", " g__", " s__"]}}, {"id": "355178", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}, {"id": "322062", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__Clostridium", " s__"]}}, {"id": "191951", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__", " g__", " s__"]}}, {"id": "274021", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "325036", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "275847", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "251891", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "338887", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__Oscillospira", " s__"]}}, {"id": "355771", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "334098", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "339743", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "317740", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "178173", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Lachnospiraceae", " g__", " s__"]}}, {"id": "275543", "metadata": {"taxonomy": ["k__Bacteria", " p__Firmicutes", " c__Clostridia", " o__Clostridiales", " f__Ruminococcaceae", " g__", " s__"]}}], "format": "Biological Observation Matrix 1.0.0", "data": [[0, 0, 1], [0, 1, 1], [0, 3, 14], [0, 8, 14], [1, 0, 1], [1, 2, 1], [2, 0, 1], [2, 6, 1], [3, 0, 1], [4, 0, 2], [4, 3, 1], [4, 8, 1], [5, 0, 1], [5, 3, 29], [5, 8, 10], [6, 0, 19], [6, 4, 2], [6, 7, 3], [6, 8, 2], [7, 0, 1], [7, 8, 1], [8, 0, 1], [9, 0, 1], [10, 0, 4], [10, 3, 1], [11, 0, 1], [12, 0, 1], [12, 2, 1], [13, 0, 1], [14, 0, 1], [14, 8, 1], [15, 0, 1], [16, 0, 1], [16, 4, 1], [17, 0, 2], [17, 1, 1], [17, 4, 3], [17, 6, 1], [17, 7, 3], [18, 0, 1], [18, 4, 1], [19, 0, 2], [19, 8, 1], [20, 0, 1], [21, 0, 1], [21, 6, 1], [22, 0, 1], [23, 0, 3], [23, 1, 2], [23, 2, 8], [23, 3, 1], [23, 4, 1], [23, 5, 4], [23, 6, 5], [23, 7, 2], [23, 8, 1], [24, 0, 1], [24, 1, 1], [24, 4, 1], [24, 6, 3], [25, 0, 9], [25, 1, 1], [25, 3, 4], [25, 5, 2], [26, 0, 2], [26, 1, 2], [26, 5, 1], [27, 0, 2], [27, 1, 4], [27, 2, 5], [27, 5, 4], [27, 7, 1], [27, 8, 2], [28, 0, 1], [28, 1, 5], [28, 2, 1], [28, 3, 1], [29, 0, 4], [29, 1, 5], [29, 3, 1], [29, 8, 2], [30, 0, 4], [30, 3, 1], [30, 6, 1], [30, 8, 3], [31, 0, 1], [31, 1, 7], [31, 5, 2], [32, 0, 1], [32, 6, 2], [33, 0, 1], [33, 3, 1], [33, 8, 1], [34, 0, 1], [34, 4, 4], [34, 5, 1], [34, 7, 1], [35, 0, 18], [35, 1, 1], [35, 3, 2], [35, 5, 4], [35, 6, 4], [35, 7, 21], [36, 0, 1], [36, 3, 1], [36, 4, 8], [36, 5, 1], [36, 6, 1], [36, 8, 6], [37, 0, 1], [37, 3, 1], [38, 0, 1], [39, 0, 1], [39, 1, 1], [39, 3, 1], [39, 4, 3], [40, 0, 2], [41, 0, 1], [41, 7, 3], [42, 0, 4], [42, 2, 2], [42, 4, 1], [42, 5, 2], [42, 6, 1], [42, 8, 3], [43, 0, 2], [43, 1, 1], [43, 3, 2], [44, 0, 13], [44, 1, 13], [44, 3, 12], [44, 8, 5], [45, 1, 1], [46, 1, 9], [46, 7, 3], [47, 1, 2], [48, 1, 1], [49, 1, 1], [50, 1, 1], [51, 1, 1], [52, 1, 2], [53, 1, 1], [54, 1, 1], [55, 1, 1], [56, 1, 1], [57, 1, 1], [57, 5, 5], [57, 6, 2], [57, 7, 1], [58, 1, 1], [58, 5, 1], [59, 1, 2], [60, 1, 1], [60, 6, 1], [60, 7, 1], [60, 8, 1], [61, 1, 1], [62, 1, 1], [62, 5, 2], [62, 6, 19], [62, 7, 1], [63, 1, 1], [63, 4, 1], [64, 1, 2], [65, 1, 1], [65, 4, 4], [66, 1, 1], [67, 1, 6], [67, 5, 1], [68, 1, 2], [68, 5, 1], [69, 1, 2], [69, 3, 1], [70, 1, 1], [71, 1, 1], [72, 1, 1], [73, 1, 1], [74, 1, 2], [75, 1, 2], [75, 3, 1], [75, 4, 16], [75, 8, 4], [76, 1, 1], [77, 1, 1], [78, 1, 1], [79, 1, 1], [79, 2, 2], [80, 1, 1], [81, 1, 1], [81, 2, 1], [82, 1, 2], [83, 1, 1], [83, 3, 1], [84, 1, 1], [85, 1, 1], [86, 1, 3], [86, 2, 5], [86, 4, 9], [87, 1, 1], [87, 8, 1], [88, 1, 1], [88, 5, 1], [88, 8, 1], [89, 1, 2], [89, 2, 7], [89, 4, 8], [90, 1, 1], [91, 1, 1], [91, 5, 1], [92, 1, 1], [93, 1, 1], [94, 1, 1], [95, 2, 2], [96, 2, 5], [96, 5, 5], [96, 6, 3], [96, 7, 9], [97, 2, 1], [97, 3, 1], [98, 2, 5], [99, 2, 1], [100, 2, 1], [100, 4, 5], [100, 6, 3], [100, 8, 2], [101, 2, 1], [102, 2, 1], [103, 2, 1], [104, 2, 1], [104, 7, 1], [105, 2, 8], [106, 2, 3], [106, 5, 2], [106, 6, 6], [106, 7, 5], [107, 2, 1], [108, 2, 1], [109, 2, 1], [110, 2, 1], [111, 2, 6], [111, 5, 3], [112, 2, 1], [113, 2, 1], [114, 2, 1], [115, 2, 2], [116, 2, 1], [116, 5, 1], [116, 6, 1], [117, 2, 1], [118, 2, 6], [119, 2, 1], [120, 2, 2], [120, 4, 5], [121, 2, 1], [122, 2, 1], [122, 7, 1], [123, 2, 1], [124, 2, 1], [124, 4, 9], [125, 2, 1], [126, 2, 2], [127, 2, 2], [127, 5, 1], [128, 2, 1], [129, 2, 2], [129, 4, 2], [129, 5, 3], [129, 6, 1], [129, 7, 1], [130, 2, 1], [131, 2, 1], [132, 3, 1], [133, 3, 6], [133, 4, 2], [133, 8, 4], [134, 3, 1], [135, 3, 1], [136, 3, 1], [136, 8, 1], [137, 3, 1], [138, 3, 3], [138, 4, 3], [139, 3, 1], [139, 8, 1], [140, 3, 1], [140, 4, 1], [140, 5, 1], [141, 3, 2], [142, 3, 1], [143, 3, 1], [144, 3, 1], [144, 5, 2], [145, 3, 1], [146, 3, 14], [146, 4, 7], [147, 3, 1], [148, 3, 1], [148, 4, 2], [148, 8, 1], [149, 3, 1], [150, 3, 1], [151, 3, 1], [152, 3, 1], [153, 3, 1], [154, 3, 1], [155, 3, 1], [155, 4, 10], [156, 3, 1], [157, 4, 1], [157, 6, 2], [157, 7, 2], [157, 8, 3], [158, 4, 1], [159, 4, 2], [160, 4, 2], [160, 6, 3], [160, 7, 2], [161, 4, 1], [162, 4, 1], [163, 4, 2], [163, 5, 3], [164, 4, 1], [165, 4, 1], [166, 4, 1], [167, 4, 2], [167, 7, 1], [168, 4, 4], [168, 6, 2], [169, 4, 1], [170, 4, 1], [171, 4, 3], [172, 4, 2], [173, 5, 1], [174, 5, 1], [175, 5, 1], [175, 8, 1], [176, 5, 2], [176, 6, 1], [177, 5, 1], [178, 5, 1], [178, 8, 2], [179, 5, 1], [179, 8, 1], [180, 5, 1], [181, 5, 1], [182, 5, 1], [182, 6, 2], [182, 8, 2], [183, 5, 1], [184, 5, 1], [185, 5, 1], [186, 5, 1], [187, 5, 1], [187, 8, 1], [188, 5, 1], [189, 5, 1], [190, 5, 1], [191, 5, 1], [191, 6, 1], [192, 5, 1], [193, 5, 1], [193, 6, 1], [193, 8, 1], [194, 5, 1], [195, 5, 1], [196, 5, 1], [197, 5, 1], [198, 5, 1], [199, 5, 1], [200, 5, 2], [200, 6, 2], [201, 5, 1], [201, 7, 2], [202, 5, 1], [203, 5, 1], [204, 5, 3], [204, 7, 1], [205, 5, 1], [206, 5, 1], [206, 7, 3], [207, 6, 1], [208, 6, 1], [208, 7, 1], [209, 6, 1], [210, 6, 1], [210, 7, 2], [211, 6, 1], [212, 6, 1], [213, 6, 1], [214, 6, 1], [214, 7, 1], [215, 6, 1], [216, 6, 2], [217, 6, 1], [218, 6, 1], [219, 7, 2], [220, 7, 1], [221, 7, 2], [222, 7, 1], [223, 7, 1], [224, 7, 13], [225, 7, 5], [226, 7, 1], [227, 7, 1], [228, 7, 4], [229, 7, 1], [230, 7, 1], [231, 7, 1], [232, 7, 1], [233, 7, 1], [234, 7, 2], [235, 7, 1], [236, 7, 1], [237, 8, 2], [238, 8, 2], [239, 8, 1], [240, 8, 1], [241, 8, 1], [242, 8, 1], [243, 8, 1], [244, 8, 1], [245, 8, 1], [246, 8, 1], [247, 8, 1], [248, 8, 1], [249, 8, 1], [250, 8, 2], [251, 8, 1], [252, 8, 1], [253, 8, 1], [254, 8, 2], [255, 8, 1], [256, 8, 1], [257, 8, 1], [258, 8, 2], [259, 8, 1]], "columns": [{"id": "test.PCx355.283435", "metadata": null}, {"id": "test.PCx481.283438", "metadata": null}, {"id": "test.PCx607.283434", "metadata": null}, {"id": "test.PCx354.283437", "metadata": null}, {"id": "test.PCx593.283440", "metadata": null}, {"id": "test.PCx635.283442", "metadata": null}, {"id": "test.PCx636.283441", "metadata": null}, {"id": "test.PCx634.283439", "metadata": null}, {"id": "test.PCx356.283436", "metadata": null}], "generated_by": "QIIME-DB", "matrix_type": "sparse", "shape": [260, 9], "format_url": "http://biom-format.org", "date": "2012-09-04T19:42:44.412292", "type": "OTU table", "id": null, "matrix_element_type": "int"}"""

mapping_file_str="""\
#SampleID	BarcodeSequence	LinkerPrimerSequence	RUN_PREFIX	STUDY_ID	TREATMENT	COUNTRY	Description
test.PCx355.283435	AACTCGTCGATG	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Control	GAZ:United States of America	test_dataset
test.PCx481.283438	ACCAGCGACTAG	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Control	GAZ:United States of America	test_dataset
test.PCx607.283434	AACTGTGCGTAC	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Fast	GAZ:United States of America	test_dataset
test.PCx354.283437	AGCACGAGCCTA	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Control	GAZ:United States of America	test_dataset
test.PCx593.283440	AGCAGCACTTGT	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Control	GAZ:United States of America	test_dataset
test.PCx635.283442	ACCGCAGAGTCA	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Fast	GAZ:United States of America	test_dataset
test.PCx636.283441	ACGGTGAGTGTC	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Fast	GAZ:United States of America	test_dataset
test.PCx634.283439	ACAGAGTCGGCT	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Fast	GAZ:United States of America	test_dataset
test.PCx356.283436	ACAGACCACTCA	CATGCTGCCTCCCGTAGGAGT	Fasting_subset	0	Control	GAZ:United States of America	test_dataset"""

exp_heatmap_js_table="""\
var otu_num_cutoff=5;    var OTU_table=new Array();
    var i=0;
    for (i==0;i<11;i++) {
    OTU_table[i]=new Array();}
OTU_table[0][0]='#OTU ID';
OTU_table[0][1]='95638';
OTU_table[0][2]='15711';
OTU_table[0][3]='175699';
OTU_table[0][4]='259965';
OTU_table[0][5]='115098';
OTU_table[0][6]='470494';
OTU_table[0][7]='169379';
OTU_table[0][8]='393399';
OTU_table[0][9]='178596';
OTU_table[0][10]='412648';
OTU_table[0][11]='189531';
OTU_table[0][12]='272270';
OTU_table[0][13]='204547';
OTU_table[0][14]='264496';
OTU_table[0][15]='398943';
OTU_table[0][16]='212750';
OTU_table[0][17]='204144';
OTU_table[0][18]='447694';
OTU_table[0][19]='469832';
OTU_table[0][20]='331820';
OTU_table[0][21]='264035';
OTU_table[0][22]='309188';
OTU_table[0][23]='230364';
OTU_table[0][24]='227953';
OTU_table[0][25]='335530';
OTU_table[0][26]='273626';
OTU_table[0][27]='269994';
OTU_table[0][28]='169943';
OTU_table[0][29]='569818';
OTU_table[0][30]='319134';
OTU_table[0][31]='228512';
OTU_table[0][32]='234635';
OTU_table[0][33]='209907';
OTU_table[0][34]='269815';
OTU_table[0][35]='255362';
OTU_table[0][36]='167204';
OTU_table[0][37]='176977';
OTU_table[0][38]='135493';
OTU_table[0][39]='197240';
OTU_table[0][40]='164638';
OTU_table[0][41]='14035';
OTU_table[0][42]='259056';
OTU_table[0][43]='328536';
OTU_table[0][44]='269169';
OTU_table[0][45]='308269';
OTU_table[0][46]='204911';
OTU_table[0][47]='263876';
OTU_table[0][48]='216933';
OTU_table[0][49]='567604';
OTU_table[0][50]='266771';
OTU_table[1][0]='test.PCx355.283435';
OTU_table[1][1]=0.0000;
OTU_table[1][2]=0.0000;
OTU_table[1][3]=0.0000;
OTU_table[1][4]=0.0000;
OTU_table[1][5]=0.0000;
OTU_table[1][6]=0.0000;
OTU_table[1][7]=3.0000;
OTU_table[1][8]=0.0000;
OTU_table[1][9]=4.0000;
OTU_table[1][10]=1.0000;
OTU_table[1][11]=0.0000;
OTU_table[1][12]=0.0000;
OTU_table[1][13]=1.0000;
OTU_table[1][14]=2.0000;
OTU_table[1][15]=0.0000;
OTU_table[1][16]=2.0000;
OTU_table[1][17]=0.0000;
OTU_table[1][18]=0.0000;
OTU_table[1][19]=0.0000;
OTU_table[1][20]=18.0000;
OTU_table[1][21]=0.0000;
OTU_table[1][22]=2.0000;
OTU_table[1][23]=0.0000;
OTU_table[1][24]=0.0000;
OTU_table[1][25]=0.0000;
OTU_table[1][26]=0.0000;
OTU_table[1][27]=0.0000;
OTU_table[1][28]=0.0000;
OTU_table[1][29]=9.0000;
OTU_table[1][30]=0.0000;
OTU_table[1][31]=1.0000;
OTU_table[1][32]=2.0000;
OTU_table[1][33]=0.0000;
OTU_table[1][34]=1.0000;
OTU_table[1][35]=4.0000;
OTU_table[1][36]=0.0000;
OTU_table[1][37]=0.0000;
OTU_table[1][38]=13.0000;
OTU_table[1][39]=1.0000;
OTU_table[1][40]=4.0000;
OTU_table[1][41]=0.0000;
OTU_table[1][42]=1.0000;
OTU_table[1][43]=0.0000;
OTU_table[1][44]=19.0000;
OTU_table[1][45]=0.0000;
OTU_table[1][46]=0.0000;
OTU_table[1][47]=4.0000;
OTU_table[1][48]=0.0000;
OTU_table[1][49]=1.0000;
OTU_table[1][50]=1.0000;
OTU_table[2][0]='test.PCx481.283438';
OTU_table[2][1]=0.0000;
OTU_table[2][2]=0.0000;
OTU_table[2][3]=0.0000;
OTU_table[2][4]=3.0000;
OTU_table[2][5]=2.0000;
OTU_table[2][6]=0.0000;
OTU_table[2][7]=2.0000;
OTU_table[2][8]=0.0000;
OTU_table[2][9]=0.0000;
OTU_table[2][10]=0.0000;
OTU_table[2][11]=2.0000;
OTU_table[2][12]=0.0000;
OTU_table[2][13]=0.0000;
OTU_table[2][14]=1.0000;
OTU_table[2][15]=0.0000;
OTU_table[2][16]=1.0000;
OTU_table[2][17]=0.0000;
OTU_table[2][18]=0.0000;
OTU_table[2][19]=0.0000;
OTU_table[2][20]=1.0000;
OTU_table[2][21]=1.0000;
OTU_table[2][22]=4.0000;
OTU_table[2][23]=0.0000;
OTU_table[2][24]=1.0000;
OTU_table[2][25]=0.0000;
OTU_table[2][26]=0.0000;
OTU_table[2][27]=0.0000;
OTU_table[2][28]=0.0000;
OTU_table[2][29]=1.0000;
OTU_table[2][30]=0.0000;
OTU_table[2][31]=0.0000;
OTU_table[2][32]=2.0000;
OTU_table[2][33]=0.0000;
OTU_table[2][34]=5.0000;
OTU_table[2][35]=5.0000;
OTU_table[2][36]=0.0000;
OTU_table[2][37]=1.0000;
OTU_table[2][38]=13.0000;
OTU_table[2][39]=1.0000;
OTU_table[2][40]=0.0000;
OTU_table[2][41]=0.0000;
OTU_table[2][42]=7.0000;
OTU_table[2][43]=0.0000;
OTU_table[2][44]=0.0000;
OTU_table[2][45]=0.0000;
OTU_table[2][46]=6.0000;
OTU_table[2][47]=0.0000;
OTU_table[2][48]=9.0000;
OTU_table[2][49]=1.0000;
OTU_table[2][50]=1.0000;
OTU_table[3][0]='test.PCx607.283434';
OTU_table[3][1]=3.0000;
OTU_table[3][2]=0.0000;
OTU_table[3][3]=8.0000;
OTU_table[3][4]=5.0000;
OTU_table[3][5]=7.0000;
OTU_table[3][6]=2.0000;
OTU_table[3][7]=8.0000;
OTU_table[3][8]=2.0000;
OTU_table[3][9]=0.0000;
OTU_table[3][10]=0.0000;
OTU_table[3][11]=0.0000;
OTU_table[3][12]=1.0000;
OTU_table[3][13]=0.0000;
OTU_table[3][14]=0.0000;
OTU_table[3][15]=5.0000;
OTU_table[3][16]=0.0000;
OTU_table[3][17]=0.0000;
OTU_table[3][18]=1.0000;
OTU_table[3][19]=0.0000;
OTU_table[3][20]=0.0000;
OTU_table[3][21]=0.0000;
OTU_table[3][22]=5.0000;
OTU_table[3][23]=5.0000;
OTU_table[3][24]=0.0000;
OTU_table[3][25]=0.0000;
OTU_table[3][26]=0.0000;
OTU_table[3][27]=0.0000;
OTU_table[3][28]=0.0000;
OTU_table[3][29]=0.0000;
OTU_table[3][30]=0.0000;
OTU_table[3][31]=0.0000;
OTU_table[3][32]=0.0000;
OTU_table[3][33]=0.0000;
OTU_table[3][34]=1.0000;
OTU_table[3][35]=0.0000;
OTU_table[3][36]=6.0000;
OTU_table[3][37]=0.0000;
OTU_table[3][38]=0.0000;
OTU_table[3][39]=0.0000;
OTU_table[3][40]=0.0000;
OTU_table[3][41]=0.0000;
OTU_table[3][42]=0.0000;
OTU_table[3][43]=0.0000;
OTU_table[3][44]=0.0000;
OTU_table[3][45]=6.0000;
OTU_table[3][46]=0.0000;
OTU_table[3][47]=2.0000;
OTU_table[3][48]=0.0000;
OTU_table[3][49]=0.0000;
OTU_table[3][50]=0.0000;
OTU_table[4][0]='test.PCx354.283437';
OTU_table[4][1]=0.0000;
OTU_table[4][2]=0.0000;
OTU_table[4][3]=0.0000;
OTU_table[4][4]=0.0000;
OTU_table[4][5]=0.0000;
OTU_table[4][6]=0.0000;
OTU_table[4][7]=1.0000;
OTU_table[4][8]=0.0000;
OTU_table[4][9]=1.0000;
OTU_table[4][10]=1.0000;
OTU_table[4][11]=1.0000;
OTU_table[4][12]=0.0000;
OTU_table[4][13]=0.0000;
OTU_table[4][14]=2.0000;
OTU_table[4][15]=0.0000;
OTU_table[4][16]=0.0000;
OTU_table[4][17]=0.0000;
OTU_table[4][18]=0.0000;
OTU_table[4][19]=0.0000;
OTU_table[4][20]=2.0000;
OTU_table[4][21]=0.0000;
OTU_table[4][22]=0.0000;
OTU_table[4][23]=0.0000;
OTU_table[4][24]=0.0000;
OTU_table[4][25]=0.0000;
OTU_table[4][26]=1.0000;
OTU_table[4][27]=0.0000;
OTU_table[4][28]=0.0000;
OTU_table[4][29]=4.0000;
OTU_table[4][30]=3.0000;
OTU_table[4][31]=29.0000;
OTU_table[4][32]=0.0000;
OTU_table[4][33]=6.0000;
OTU_table[4][34]=1.0000;
OTU_table[4][35]=1.0000;
OTU_table[4][36]=0.0000;
OTU_table[4][37]=0.0000;
OTU_table[4][38]=12.0000;
OTU_table[4][39]=0.0000;
OTU_table[4][40]=1.0000;
OTU_table[4][41]=0.0000;
OTU_table[4][42]=0.0000;
OTU_table[4][43]=14.0000;
OTU_table[4][44]=0.0000;
OTU_table[4][45]=0.0000;
OTU_table[4][46]=0.0000;
OTU_table[4][47]=0.0000;
OTU_table[4][48]=0.0000;
OTU_table[4][49]=1.0000;
OTU_table[4][50]=14.0000;
OTU_table[5][0]='test.PCx593.283440';
OTU_table[5][1]=0.0000;
OTU_table[5][2]=4.0000;
OTU_table[5][3]=0.0000;
OTU_table[5][4]=9.0000;
OTU_table[5][5]=8.0000;
OTU_table[5][6]=5.0000;
OTU_table[5][7]=1.0000;
OTU_table[5][8]=2.0000;
OTU_table[5][9]=0.0000;
OTU_table[5][10]=8.0000;
OTU_table[5][11]=16.0000;
OTU_table[5][12]=5.0000;
OTU_table[5][13]=4.0000;
OTU_table[5][14]=0.0000;
OTU_table[5][15]=0.0000;
OTU_table[5][16]=3.0000;
OTU_table[5][17]=1.0000;
OTU_table[5][18]=9.0000;
OTU_table[5][19]=0.0000;
OTU_table[5][20]=0.0000;
OTU_table[5][21]=0.0000;
OTU_table[5][22]=0.0000;
OTU_table[5][23]=0.0000;
OTU_table[5][24]=0.0000;
OTU_table[5][25]=0.0000;
OTU_table[5][26]=10.0000;
OTU_table[5][27]=0.0000;
OTU_table[5][28]=2.0000;
OTU_table[5][29]=0.0000;
OTU_table[5][30]=3.0000;
OTU_table[5][31]=0.0000;
OTU_table[5][32]=0.0000;
OTU_table[5][33]=2.0000;
OTU_table[5][34]=0.0000;
OTU_table[5][35]=0.0000;
OTU_table[5][36]=0.0000;
OTU_table[5][37]=4.0000;
OTU_table[5][38]=0.0000;
OTU_table[5][39]=1.0000;
OTU_table[5][40]=0.0000;
OTU_table[5][41]=2.0000;
OTU_table[5][42]=0.0000;
OTU_table[5][43]=7.0000;
OTU_table[5][44]=2.0000;
OTU_table[5][45]=0.0000;
OTU_table[5][46]=0.0000;
OTU_table[5][47]=1.0000;
OTU_table[5][48]=0.0000;
OTU_table[5][49]=3.0000;
OTU_table[5][50]=0.0000;
OTU_table[6][0]='test.PCx635.283442';
OTU_table[6][1]=2.0000;
OTU_table[6][2]=0.0000;
OTU_table[6][3]=0.0000;
OTU_table[6][4]=0.0000;
OTU_table[6][5]=0.0000;
OTU_table[6][6]=0.0000;
OTU_table[6][7]=4.0000;
OTU_table[6][8]=3.0000;
OTU_table[6][9]=0.0000;
OTU_table[6][10]=1.0000;
OTU_table[6][11]=0.0000;
OTU_table[6][12]=0.0000;
OTU_table[6][13]=1.0000;
OTU_table[6][14]=0.0000;
OTU_table[6][15]=0.0000;
OTU_table[6][16]=0.0000;
OTU_table[6][17]=0.0000;
OTU_table[6][18]=0.0000;
OTU_table[6][19]=0.0000;
OTU_table[6][20]=4.0000;
OTU_table[6][21]=2.0000;
OTU_table[6][22]=4.0000;
OTU_table[6][23]=5.0000;
OTU_table[6][24]=5.0000;
OTU_table[6][25]=0.0000;
OTU_table[6][26]=0.0000;
OTU_table[6][27]=1.0000;
OTU_table[6][28]=0.0000;
OTU_table[6][29]=2.0000;
OTU_table[6][30]=0.0000;
OTU_table[6][31]=0.0000;
OTU_table[6][32]=1.0000;
OTU_table[6][33]=0.0000;
OTU_table[6][34]=0.0000;
OTU_table[6][35]=0.0000;
OTU_table[6][36]=0.0000;
OTU_table[6][37]=0.0000;
OTU_table[6][38]=0.0000;
OTU_table[6][39]=0.0000;
OTU_table[6][40]=0.0000;
OTU_table[6][41]=3.0000;
OTU_table[6][42]=2.0000;
OTU_table[6][43]=0.0000;
OTU_table[6][44]=0.0000;
OTU_table[6][45]=3.0000;
OTU_table[6][46]=1.0000;
OTU_table[6][47]=2.0000;
OTU_table[6][48]=0.0000;
OTU_table[6][49]=0.0000;
OTU_table[6][50]=0.0000;
OTU_table[7][0]='test.PCx636.283441';
OTU_table[7][1]=6.0000;
OTU_table[7][2]=2.0000;
OTU_table[7][3]=0.0000;
OTU_table[7][4]=0.0000;
OTU_table[7][5]=0.0000;
OTU_table[7][6]=0.0000;
OTU_table[7][7]=5.0000;
OTU_table[7][8]=1.0000;
OTU_table[7][9]=1.0000;
OTU_table[7][10]=1.0000;
OTU_table[7][11]=0.0000;
OTU_table[7][12]=3.0000;
OTU_table[7][13]=0.0000;
OTU_table[7][14]=0.0000;
OTU_table[7][15]=0.0000;
OTU_table[7][16]=1.0000;
OTU_table[7][17]=2.0000;
OTU_table[7][18]=0.0000;
OTU_table[7][19]=0.0000;
OTU_table[7][20]=4.0000;
OTU_table[7][21]=19.0000;
OTU_table[7][22]=0.0000;
OTU_table[7][23]=3.0000;
OTU_table[7][24]=2.0000;
OTU_table[7][25]=0.0000;
OTU_table[7][26]=0.0000;
OTU_table[7][27]=2.0000;
OTU_table[7][28]=3.0000;
OTU_table[7][29]=0.0000;
OTU_table[7][30]=0.0000;
OTU_table[7][31]=0.0000;
OTU_table[7][32]=0.0000;
OTU_table[7][33]=0.0000;
OTU_table[7][34]=0.0000;
OTU_table[7][35]=0.0000;
OTU_table[7][36]=0.0000;
OTU_table[7][37]=0.0000;
OTU_table[7][38]=0.0000;
OTU_table[7][39]=3.0000;
OTU_table[7][40]=0.0000;
OTU_table[7][41]=0.0000;
OTU_table[7][42]=0.0000;
OTU_table[7][43]=0.0000;
OTU_table[7][44]=0.0000;
OTU_table[7][45]=0.0000;
OTU_table[7][46]=0.0000;
OTU_table[7][47]=1.0000;
OTU_table[7][48]=0.0000;
OTU_table[7][49]=0.0000;
OTU_table[7][50]=0.0000;
OTU_table[8][0]='test.PCx634.283439';
OTU_table[8][1]=5.0000;
OTU_table[8][2]=0.0000;
OTU_table[8][3]=0.0000;
OTU_table[8][4]=0.0000;
OTU_table[8][5]=0.0000;
OTU_table[8][6]=0.0000;
OTU_table[8][7]=2.0000;
OTU_table[8][8]=1.0000;
OTU_table[8][9]=0.0000;
OTU_table[8][10]=0.0000;
OTU_table[8][11]=0.0000;
OTU_table[8][12]=0.0000;
OTU_table[8][13]=1.0000;
OTU_table[8][14]=0.0000;
OTU_table[8][15]=0.0000;
OTU_table[8][16]=3.0000;
OTU_table[8][17]=2.0000;
OTU_table[8][18]=0.0000;
OTU_table[8][19]=13.0000;
OTU_table[8][20]=21.0000;
OTU_table[8][21]=1.0000;
OTU_table[8][22]=1.0000;
OTU_table[8][23]=9.0000;
OTU_table[8][24]=1.0000;
OTU_table[8][25]=5.0000;
OTU_table[8][26]=0.0000;
OTU_table[8][27]=0.0000;
OTU_table[8][28]=2.0000;
OTU_table[8][29]=0.0000;
OTU_table[8][30]=0.0000;
OTU_table[8][31]=0.0000;
OTU_table[8][32]=0.0000;
OTU_table[8][33]=0.0000;
OTU_table[8][34]=0.0000;
OTU_table[8][35]=0.0000;
OTU_table[8][36]=0.0000;
OTU_table[8][37]=0.0000;
OTU_table[8][38]=0.0000;
OTU_table[8][39]=0.0000;
OTU_table[8][40]=0.0000;
OTU_table[8][41]=0.0000;
OTU_table[8][42]=0.0000;
OTU_table[8][43]=0.0000;
OTU_table[8][44]=3.0000;
OTU_table[8][45]=0.0000;
OTU_table[8][46]=0.0000;
OTU_table[8][47]=0.0000;
OTU_table[8][48]=3.0000;
OTU_table[8][49]=0.0000;
OTU_table[8][50]=0.0000;
OTU_table[9][0]='test.PCx356.283436';
OTU_table[9][1]=0.0000;
OTU_table[9][2]=0.0000;
OTU_table[9][3]=0.0000;
OTU_table[9][4]=0.0000;
OTU_table[9][5]=0.0000;
OTU_table[9][6]=0.0000;
OTU_table[9][7]=1.0000;
OTU_table[9][8]=0.0000;
OTU_table[9][9]=3.0000;
OTU_table[9][10]=6.0000;
OTU_table[9][11]=4.0000;
OTU_table[9][12]=2.0000;
OTU_table[9][13]=0.0000;
OTU_table[9][14]=0.0000;
OTU_table[9][15]=0.0000;
OTU_table[9][16]=0.0000;
OTU_table[9][17]=3.0000;
OTU_table[9][18]=0.0000;
OTU_table[9][19]=0.0000;
OTU_table[9][20]=0.0000;
OTU_table[9][21]=0.0000;
OTU_table[9][22]=2.0000;
OTU_table[9][23]=0.0000;
OTU_table[9][24]=0.0000;
OTU_table[9][25]=0.0000;
OTU_table[9][26]=0.0000;
OTU_table[9][27]=2.0000;
OTU_table[9][28]=0.0000;
OTU_table[9][29]=0.0000;
OTU_table[9][30]=0.0000;
OTU_table[9][31]=10.0000;
OTU_table[9][32]=0.0000;
OTU_table[9][33]=4.0000;
OTU_table[9][34]=0.0000;
OTU_table[9][35]=2.0000;
OTU_table[9][36]=0.0000;
OTU_table[9][37]=0.0000;
OTU_table[9][38]=5.0000;
OTU_table[9][39]=0.0000;
OTU_table[9][40]=0.0000;
OTU_table[9][41]=0.0000;
OTU_table[9][42]=0.0000;
OTU_table[9][43]=0.0000;
OTU_table[9][44]=2.0000;
OTU_table[9][45]=0.0000;
OTU_table[9][46]=0.0000;
OTU_table[9][47]=3.0000;
OTU_table[9][48]=0.0000;
OTU_table[9][49]=0.0000;
OTU_table[9][50]=14.0000;
OTU_table[10][0]='Consensus Lineage';
OTU_table[10][1]='k__Bacteria; p__Deferribacteres; c__Deferribacteres (class); o__Deferribacterales; f__Deferribacteraceae; g__Mucispirillum; s__Mucispirillum schaedleri';
OTU_table[10][2]='k__Bacteria; p__Tenericutes; c__Erysipelotrichi; o__Erysipelotrichales; f__Erysipelotrichaceae; g__Clostridium; s__Clostridium cocleatum';
OTU_table[10][3]='k__Bacteria; p__Tenericutes; c__Erysipelotrichi; o__Erysipelotrichales; f__Erysipelotrichaceae; g__Allobaculum; s__Allobaculum sp ID4';
OTU_table[10][4]='k__Bacteria; p__Tenericutes; c__Erysipelotrichi; o__Erysipelotrichales; f__Erysipelotrichaceae; g__Allobaculum; s__Allobaculum sp ID4';
OTU_table[10][5]='k__Bacteria; p__Tenericutes; c__Erysipelotrichi; o__Erysipelotrichales; f__Erysipelotrichaceae; g__Allobaculum; s__Allobaculum sp ID4';
OTU_table[10][6]='k__Bacteria; p__Proteobacteria; c__Epsilonproteobacteria; o__Campylobacterales; f__Helicobacteraceae; g__Flexispira; s__Helicobacter cinaedi';
OTU_table[10][7]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][8]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][9]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][10]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][11]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][12]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][13]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][14]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][15]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][16]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][17]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][18]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__; g__; s__';
OTU_table[10][19]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Bacteroidaceae; g__Bacteroides; s__Bacteroides uniformis';
OTU_table[10][20]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Bacteroidaceae; g__Bacteroides; s__';
OTU_table[10][21]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Bacteroidaceae; g__Bacteroides; s__';
OTU_table[10][22]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Rikenellaceae; g__Alistipes; s__';
OTU_table[10][23]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Rikenellaceae; g__Alistipes; s__';
OTU_table[10][24]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Rikenellaceae; g__Alistipes; s__';
OTU_table[10][25]='k__Bacteria; p__Bacteroidetes; c__Bacteroidia; o__Bacteroidales; f__Rikenellaceae; g__Alistipes; s__';
OTU_table[10][26]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__; g__; s__';
OTU_table[10][27]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Ruminococcaceae; g__; s__';
OTU_table[10][28]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Ruminococcaceae; g__; s__';
OTU_table[10][29]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][30]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][31]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][32]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][33]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][34]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][35]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][36]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][37]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][38]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][39]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Clostridium; s__';
OTU_table[10][40]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Clostridium; s__';
OTU_table[10][41]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Clostridium; s__';
OTU_table[10][42]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Clostridium; s__';
OTU_table[10][43]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Clostridium; s__';
OTU_table[10][44]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__Clostridium; s__';
OTU_table[10][45]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][46]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][47]='k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Lachnospiraceae; g__; s__';
OTU_table[10][48]='k__Bacteria; p__Firmicutes; c__Bacilli; o__Erysipelotrichales; f__Erysipelotrichaceae; g__; s__';
OTU_table[10][49]='k__Bacteria; p__Firmicutes; c__Bacilli; o__Lactobacillales; f__Lactobacillaceae; g__Lactobacillus; s__';
OTU_table[10][50]='k__Bacteria; p__Firmicutes; c__Bacilli; o__Lactobacillales; f__Lactobacillaceae; g__Lactobacillus; s__';
"""

if __name__ == "__main__":
    main()