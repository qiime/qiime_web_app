#!/usr/bin/env python
# File created on 10 May 2011
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
import os, sys, copy
from qiime.util import get_qiime_scripts_dir,make_option
from html_from_script import script_path_components,get_script_info,\
                             _format_help,generate_choice_input,\
                             generate_string_input,generate_float_input,\
                             generate_int_input,generate_True_input,\
                             generate_False_input,get_html_for_options,get_html
                             
from qiime.alpha_diversity import list_known_metrics
alpha_metrics=list_known_metrics();

from qiime.beta_diversity import list_known_metrics
beta_metrics=list_known_metrics();

class HTMLFromScriptTests(TestCase):
    
    def setUp(self):
        """ """
        
        self.headers=['head1','head2','head3']
        self.test_option_file=make_option('-i', '--coord_fname',
                help='Input principal coordinates filepath',
                type='existing_path')
        self.test_option_colorby=make_option('-b', '--colorby', dest='colorby',\
                help='Comma-separated list categories metadata categories' +\
                ' (column headers) [default=color by all]')
        self.test_option_custom_axes=make_option('-a', '--custom_axes',
                help='This is the category from the metadata mapping file' +\
                ' [default: %default]')
        self.test_option_choice=make_option('-k', '--background_color',
                help='Background color to use in the plots.[default: %default]',
                default='black',type='choice',choices=['black','white'])
        self.test_option_float=make_option('--ellipsoid_opacity',
                help='Used only when plotting ellipsoids for jackknifed' +\
                ' beta diversity (i.e. using a directory of coord files' +\
                ' [default=%default]',
                default=0.33,type=float)
        self.test_option_int=make_option('--n_taxa_keep',
                help='Used only when generating BiPlots. This is the number '+\
                ' to display. Use -1 to display all. [default: %default]',
                default=10,type=int)
        self.test_option_true=make_option('--suppress_html_output',
                dest='suppress_html_output',\
                default=False,action='store_true',
                help='Suppress HTML output. [default: %default]')
        self.test_option_false=make_option('--suppress_html_output',
                dest='suppress_html_output',\
                default=True,action='store_false',
                help='Suppress HTML output. [default: %default]')
        
        self.option_labels={'coord_fname':'Principal coordinates filepath',
                                     'colorby': 'Colorby category',
                                     'background_color': 'Background color',
                                     'ellipsoid_opacity':'Ellipsoid opacity',
                                     'n_taxa_keep': '# of taxa to keep',
                                     'custom_axes':'Custom Axis'}
            
        self.script_dir = get_qiime_scripts_dir()
        self.test_script_info=get_script_info(self.script_dir,
                                                    'make_qiime_rst_file')
    
    def tearDown(self):
        """ """
        pass
        
    def test_get_script_info(self):
        """get_script_info runs without error"""
        
        self.obs=get_script_info(self.script_dir,'make_qiime_rst_file')
        
        for i in self.obs:
            self.assertTrue(i in self.test_script_info)
            self.assertEqual(len(self.obs[i]),len(self.test_script_info[i]))
        
    def test_script_path_components(self):
        """script_path_components runs without error"""
        
        dirname, fname=script_path_components('/test/test_file.py')
        
        self.assertEqual(dirname,'/test')
        self.assertEqual(fname,'test_file.py')
    
    def test_script_path_components(self):
        """script_path_components runs without error"""
        
        dirname, fname=script_path_components('/test/test_file.py')
        
        self.assertEqual(dirname,'/test')
        self.assertEqual(fname,'test_file.py')
    
    def test__format_help(self):
        """_format_help runs without error"""
        
        help_string='Help me [default:]'
        obs=_format_help(help_string)
        
        self.assertEqual(obs,'Help me ')
    
    def test_generate_choice_input(self):
        """generate_choice_input runs without error"""
        

        label_to_use=str(self.test_option_choice).split('/')[-1].strip('--')
        obs=generate_choice_input('make_3d_plots','Test choice',
                                  'Test choice',self.test_option_choice,
                                  label_to_use)
                                  
        exp='<tr><th>Test choice&nbsp;Test choice</th>' +\
            '<td><select id="make_3d_plots:background_color">\n'+\
            '<option selected>black\n<option>white\n</select></td></tr>\n'
        
        self.assertEqual(obs,exp)
    
    def test_generate_string_input(self):
        """generate_string_input runs without error"""
        
        label_to_use=str(self.test_option_colorby).split('/')[-1].strip('--')
        obs1=generate_string_input('make_3d_plots','Test file',
                                             'Test file',
                                             self.test_option_colorby,
                                             self.headers,label_to_use)
                                   
        exp1='<tr><th>Test file&nbsp;Test file</th><td><select '+\
             'id="make_3d_plots:colorby" multiple>\n<option>head1\n'+\
             '<option>head2\n<option>head3\n</select></td></tr>\n'          
        
        self.assertEqual(obs1,exp1)
        
        label_to_use=str(self.test_option_file).split('/')[-1].strip('--')
        obs2=generate_string_input('make_3d_plots','Test file',
                                             'Test file',
                                             self.test_option_file,self.headers,
                                             label_to_use)
                                             
        exp2='<tr><th>Test file&nbsp;Test file</th><td>'+\
             '<input class="string" type="text" '+ \
             'id="make_3d_plots:coord_fname" \\></td></tr>\n'                       
        
        self.assertEqual(obs2,exp2)
        
        label_to_use=str(self.test_option_custom_axes).split('/')[-1].strip('--')
        obs3=generate_string_input('make_3d_plots','Test file',
                                             'Test file',
                                             self.test_option_custom_axes,
                                             self.headers,label_to_use)
                                             
        exp3='<tr><th>Test file&nbsp;Test file</th><td><select '+\
             'id="make_3d_plots:custom_axes">\n<option>\n<option>head1\n<'+\
             'option>head2\n<option>head3\n</select></td></tr>\n'
        
        self.assertEqual(obs3,exp3)
    
    def test_generate_float_input(self):
        """generate_float_input runs without error"""
        
        label_to_use=str(self.test_option_float).split('/')[-1].strip('--')
        
        obs=generate_float_input('make_3d_plots','Test float',
                                  'Test float',self.test_option_float,
                                  label_to_use)
        
        exp='<tr><th>Test float&nbsp;Test float</th><td><input '+\
            'class="float" type="text" id="make_3d_plots:ellipsoid_opacity" '+\
            'value="0.33" \\></td></tr>\n'
        
        self.assertEqual(obs,exp)
    
    def test_generate_int_input(self):
        """generate_int_input runs without error"""
        
        label_to_use=str(self.test_option_int).split('/')[-1].strip('--')
        
        obs=generate_int_input('make_3d_plots','Test int',
                                  'Test int',self.test_option_int,
                                  label_to_use)
        
        exp='<tr><th>Test int&nbsp;Test int</th><td><input '+\
            'class="int" type="text" id="make_3d_plots:n_taxa_keep" '+\
            'value="10" \\></td></tr>\n'
        
        self.assertEqual(obs,exp)
    
    def test_generate_True_input(self):
        """generate_True_input runs without error"""
        
        label_to_use=str(self.test_option_true).split('/')[-1].strip('--')
        
        obs=generate_True_input('make_distance_histograms','Test true',
                                  'Test true',self.test_option_true,
                                  label_to_use)
        
        exp='<tr><th>Test true&nbsp;Test true</th><td><input '+\
            'class="check" type="checkbox" '+\
            'id="make_distance_histograms:suppress_html_output" \\></td></tr>\n'
        
        self.assertEqual(obs,exp)
    
    
    def test_generate_False_input(self):
        """generate_False_input runs without error"""
        
        label_to_use=str(self.test_option_false).split('/')[-1].strip('--')
        
        obs=generate_False_input('make_distance_histograms','Test false',
                                  'Test false',self.test_option_false,
                                  label_to_use)
        
        exp='<tr><th>Test false&nbsp;Test false</th><td><input '+\
            'class="check" type="checkbox" '+\
            'id="make_distance_histograms:suppress_html_output" checked '+\
            '\\></td></tr>\n'
        
        self.assertEqual(obs,exp)
    
    def test_get_html_for_options(self):
        """get_html_for_options runs without error"""
        
        
        obs1=get_html_for_options('make_distance_histograms',script_info,
                                 'required_options',self.headers,'./test_img.png')
        
        
        obs2=get_html_for_options('make_distance_histograms',script_info,
                                  'optional_options',self.headers,
                                  './test_img.png')
        
        self.assertEqual(obs1,exp_get_html_for_options)
        self.assertEqual(obs2,'')
    
    def test_get_html(self):
        """get_html runs without error"""
        
        obs=get_html('make_qiime_rst_file',self.headers,'./test_img.png')
        
        self.assertEqual(obs,exp_get_html)

#
script_info={}
script_info['required_options']=[\
make_option('-i', '--coord_fname',
        help='Input principal coordinates filepath',
        type='existing_path'),\
make_option('-b', '--colorby', dest='colorby',\
        help='Comma-separated list categories metadata categories' +\
        ' (column headers) [default=color by all]'),\
make_option('-a', '--custom_axes',
        help='This is the category from the metadata mapping file' +\
        ' [default: %default]'),\
make_option('-k', '--background_color',
        help='Background color to use in the plots.[default: %default]',
        default='black',type='choice',choices=['black','white']),
make_option('--ellipsoid_opacity',
        help='Used only when plotting ellipsoids for jackknifed' +\
        ' beta diversity (i.e. using a directory of coord files' +\
        ' [default=%default]',
        default=0.33,type=float),\
make_option('--n_taxa_keep',
        help='Used only when generating BiPlots. This is the number '+\
        ' to display. Use -1 to display all. [default: %default]',
        default=10,type=int),\
make_option('--suppress_html_output',
        dest='suppress_html_output',\
        default=False,action='store_true',
        help='Suppress HTML output. [default: %default]'),\
make_option('--suppress_html_output',
        dest='suppress_html_output',
        default=True,action='store_false',
        help='Suppress HTML output. [default: %default]'),\
]
    
exp_get_html_for_options='''<tr><th>colorby&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">Comma-separated list categories metadata categories (column headers) </span></a></th><td><input class="string" type="text" id="make_distance_histograms:colorby" \\></td></tr>\n<tr><th>custom_axes&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">This is the category from the metadata mapping file </span></a></th><td><select id="make_distance_histograms:custom_axes">\n<option>\n<option>head1\n<option>head2\n<option>head3\n</select></td></tr>\n<tr><th>background_color&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">Background color to use in the plots.</span></a></th><td><select id="make_distance_histograms:background_color">\n<option selected>black\n<option>white\n</select></td></tr>\n<tr><th>ellipsoid_opacity&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">Used only when plotting ellipsoids for jackknifed beta diversity (i.e. using a directory of coord files </span></a></th><td><input class="float" type="text" id="make_distance_histograms:ellipsoid_opacity" value="0.33" \\></td></tr>\n<tr><th>n_taxa_keep&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">Used only when generating BiPlots. This is the number  to display. Use -1 to display all. </span></a></th><td><input class="int" type="text" id="make_distance_histograms:n_taxa_keep" value="10" \\></td></tr>\n<tr><th>suppress_html_output&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">Suppress HTML output. </span></a></th><td><input class="check" type="checkbox" id="make_distance_histograms:suppress_html_output" \\></td></tr>\n<tr><th>suppress_html_output&nbsp;<a class="tooltip" href="#"><img src="./test_img.png" \\><span class="custom help">Suppress HTML output. </span></a></th><td><input class="check" type="checkbox" id="make_distance_histograms:suppress_html_output" checked \\></td></tr>\n'''

exp_get_html=('<tr><th>input_script&nbsp;<a class="tooltip" href="#">'+\
              '<img src="./test_img.png" \\><span class="custom help">'+\
              'This is the input script for which to  make a .rst file</span>'+\
              '</a></th><td><input class="string" type="text" '+\
              'id="make_qiime_rst_file:input_script" \\></td></tr>\n', '')
        
if __name__ == "__main__":
    main()