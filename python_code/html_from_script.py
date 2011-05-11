from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev Project"
__credits__ = ["Jesse Stombaugh","Gavin Huttley"]
__license__ = "GPL"
__version__ = "0.9.dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

import os, sys, copy
from optparse import make_option
from qiime.util import get_qiime_scripts_dir
from qiime.alpha_diversity import list_known_metrics
alpha_metrics=list_known_metrics();

from qiime.beta_diversity import list_known_metrics
beta_metrics=list_known_metrics();


def script_path_components(script_path):
    """returns the parent directory and file name"""
    dirname = os.path.dirname(script_path)
    fname = os.path.basename(script_path)
    return dirname, fname

def get_script_info(dirname, fname):
    """returns the module after checking both a script_info dict and a
    callable main function exist"""
    if not '.' in sys.path:
        sys.path.append('.')
    
    # get filepath information
    cwd = os.getcwd()
    os.chdir(dirname)
    if fname.endswith('.py'):
        fname = fname[:-3]
    
    if fname in sys.modules:
        del(sys.modules[fname])
    
    #import file information
    try:
        mod = __import__(fname)
        os.chdir(cwd)
    except ImportError, msg:
        os.chdir(cwd)
        return None
    
    # a script_info dict needs to be present
    try:
        script_info = mod.script_info
        assert type(script_info) == dict
        main = mod.main
        assert callable(main)
    except (AttributeError, AssertionError):
        return None # not a valid script
    
    script_info = copy.deepcopy(script_info)
    del(mod)
    return script_info

def _format_help(help_string):
    """removes default component from help_string"""

    index = help_string.find('[default')
    if index > -1:
        help_string = help_string[:index]

    return help_string

def generate_choice_input(script_name,label_to_use,option_help,option,
                          option_name):
    '''generate a select box, where defaults are set'''

    #get default values
    default_values=option.default
    
    #create the select box
    html_out='<tr><th>%s&nbsp;%s</th><td><select id="%s">\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
    
    #append the choices as options
    for i in option.choices:
        if i in default_values:
            html_out+='<option selected>%s\n' % (i)
        else:
            html_out+='<option>%s\n' % (i)
    
    #close the select box
    html_out+='</select></td></tr>\n'

    return html_out
#
def generate_string_input(script_name,label_to_use,option_help,option,headers,
                          option_name):
    '''generate input boxes, where defaults are set. Note: this is very
       specific to the QIIME scripts.'''
    
    html_out=''
    if script_name=='plot_taxa_summary' and option_name=='chart_type':
        #create a multi-select box specifically the chart_type in 
        #plot_taxa_summary
        html_out+='<tr><th>%s&nbsp;%s</th><td><select id="%s" multiple>\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
        html_out+='<option selected>bar\n<option selected>area\n<option>pie\n'
        html_out+='</select></td></tr>\n'
    elif script_name=='summarize_taxa' and option_name=='level':
        #create a multi-select box specifically the levels in 
        #summarize_taxa
        levels=['1','2','3','4','5','6','7']
        default_levels=option.default.split(',')
        html_out+='<tr><th>%s&nbsp;%s</th><td><select id="%s" multiple>\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
        for i in levels:
            if i in default_levels:
                html_out+='<option selected>%s\n' % (i)
            else:
                html_out+='<option>%s\n' % (i)
        html_out+='</select></td></tr>\n'
    elif script_name=='plot_taxa_summary' and option_name=='labels':
        #create a multi-select box specifically the labels in 
        #plot_taxa_summary
        labels=['Kingdom','Phylum','Class','Order','Family','Genus','Species']
        default_labels=['Phylum','Class','Order','Family','Genus']
        html_out+='<tr><th>%s&nbsp;%s</th><td><select id="%s" multiple>\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
        for i in labels:
            if i in default_labels:
                html_out+='<option selected>%s\n' % (i)
            else:
                html_out+='<option>%s\n' % (i)
        html_out+='</select></td></tr>\n'
    elif script_name=='alpha_diversity' and option_name=='metrics':
        #create a multi-select box specifically the metrics in 
        #alpha_diversity
        default_metrics=option.default.split(',')
        html_out+='<tr><th>%s&nbsp;%s</th><td><select id="%s" multiple>\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
        for i in alpha_metrics:
            if i in default_metrics:
                html_out+='<option selected>%s\n' % (i)
            else:
                html_out+='<option>%s\n' % (i)
        html_out+='</select></td></tr>\n'
    elif script_name=='beta_diversity' and option_name=='metrics':
        #create a multi-select box specifically the metrics in 
        #beta_diversity
        default_metrics=option.default.split(',')
        html_out+='<tr><th>%s&nbsp;%s</th><td><select id="%s" multiple>\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
            
        for i in beta_metrics:
            if i in default_metrics:
                html_out+='<option selected>%s\n' % (i)
            else:
                html_out+='<option>%s\n' % (i)
        html_out+='</select></td></tr>\n'
    elif option_name in ['colorby','mapping_category','fields']:
        #create a multi-select box which uses the column headers passed in
        html_out='<tr><th>%s&nbsp;%s</th><td><select id="%s" multiple>\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
        for i in headers:
            html_out+='<option>%s\n' % (i)
            
        html_out+='</select></td></tr>\n'
    elif option_name in ['custom_axes']:
        #create a single-select box which uses the column headers passed in
        html_out='<tr><th>%s&nbsp;%s</th><td><select id="%s">\n' % \
                        (label_to_use,option_help,script_name+":"+option_name)
        html_out+='<option>\n'
        for i in headers:
            html_out+='<option>%s\n' % (i)
            
        html_out+='</select></td></tr>\n'
    else:
        #otherwise create an input text-box
        if option.default and isinstance(option.default,str):
            html_out+='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
            html_out+='<td><input class="string" type="text" '
            html_out+='id="%s" value="%s" \></td></tr>\n' % \
                                (script_name+":"+option_name,option.default)
        else:
            html_out+='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
            html_out+='<td><input class="string" type="text" '
            html_out+='id="%s" \></td></tr>\n' % (script_name+":"+option_name)

    return html_out
#
def generate_float_input(script_name,label_to_use,option_help,option,
                         option_name):
    '''generate a text input box where the class is of type float, which
       allows for easier validation'''
    
    if option.default and isinstance(option.default,float):
        html_out='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
        html_out+='<td><input class="float" type="text" '
        html_out+='id="%s" value="%s" \></td></tr>\n' % \
                                  (script_name+":"+option_name,option.default)
    else:
        html_out='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
        html_out+='<td><input class="float" type="text" '
        html_out+='id="%s" \></td></tr>\n' % (script_name+":"+option_name)
    
    return html_out
#
def generate_int_input(script_name,label_to_use,option_help,option,option_name):
    '''generate a text input box where the class is of type int, which
       allows for easier validation'''
       
    if option.default and isinstance(option.default,int):
        html_out='<tr><th>%s&nbsp;%s</th>'  % (label_to_use,option_help)
        html_out+='<td><input class="int" type="text" '
        html_out+='id="%s" value="%s" \></td></tr>\n' % \
                                  (script_name+":"+option_name,option.default)
    else:
        html_out='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
        html_out+='<td><input class="int" type="text" '
        html_out+='id="%s" \></td></tr>\n' % (script_name+":"+option_name)
        
    return html_out

#
def generate_True_input(script_name,label_to_use,option_help,option,option_name):
    '''generate a checkbox where the class is of type check and the
       checkbox is unchecked'''
       
    html_out=''
    if option_name != 'show_metrics':
        html_out='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
        html_out+='<td><input class="check" type="checkbox" '
        html_out+='id="%s" \></td></tr>\n' % (script_name+":"+option_name)

    return html_out
#
def generate_False_input(script_name,label_to_use,option_help,option,option_name):
    '''generate a checkbox where the class is of type check and the
       checkbox is checked'''
       
    html_out='<tr><th>%s&nbsp;%s</th>' % (label_to_use,option_help)
    html_out+='<td><input class="check" type="checkbox" '
    html_out+='id="%s" checked \></td></tr>\n' % (script_name+":"+option_name)

    return html_out
    
def get_html_for_options(script_name,script_info,option_type,column_headers,
                         help_img):
    '''determine the option type and produce an html input instance'''
       
    option_html=''
    options_list=script_info.get(option_type)
    # get either required or optional options
    if options_list:
        for option in options_list:
        
            #see if an option_label exists for each argument, otherwise default
            #to the argument name
            option_name=str(option).split('/')[-1].strip('--')
            try:
                label_to_use=script_info['option_label'][option_name]
            except KeyError:
                label_to_use=option_name
        
            #see if there is a corresponding help message, if so, strip off the 
            #default tag associated
            if option.help is None:
                option_help_msg = ''
            else:
                option_help_msg = _format_help(option.help)
        
            #check if the option is deprecated based on the start of the help
            #message containing the word DEPRECATED
            if not option_help_msg.startswith('DEPRECATED'):
                #if option is valid, then generate the tooltip mouseover for the 
                #option
                option_help='<a class="tooltip" href="#">'
                option_help+='<img src="%s" \>' % (help_img)
                option_help+='<span class="custom help">%s</span></a>' % \
                                                              (option_help_msg)
        
                #determine option type and generate html syntax accordingly
                if option.type=='choice':
                    option_html+=generate_choice_input(script_name,label_to_use,
                                                       option_help,option,
                                                       option_name)
                elif option.type=='string' and option.action=='store':
                    option_html+=generate_string_input(script_name,label_to_use,
                                                       option_help,option,
                                                       column_headers,
                                                       option_name)   
                elif option.type=='float':
                    option_html+=generate_float_input(script_name,label_to_use,
                                                      option_help,option,
                                                      option_name) 
                elif option.type=='int':
                    option_html+=generate_int_input(script_name,label_to_use,
                                                    option_help,option,
                                                    option_name)
                # for the following we must use the action, since the type is None
                elif option.action=='store_true':
                    option_html+=generate_True_input(script_name,label_to_use,
                                                     option_help,option,
                                                     option_name)
                elif option.action=='store_false':
                    option_html+=generate_False_input(script_name,label_to_use,
                                                      option_help,option,
                                                      option_name)
        
    return option_html

def get_html(script_name,column_headers,help_img):
    '''generate the html table rows for a given QIIME script'''
    
    script_dir = get_qiime_scripts_dir()
    dirname,fname=script_path_components(os.path.join(script_dir,script_name))
    script_info_dict=get_script_info(dirname,fname)
    fname,fname_ext=os.path.splitext(script_name)
    
    #get all the required options
    required_html=get_html_for_options(fname,script_info_dict,
                                      'required_options',column_headers,
                                      help_img)
    #get all the optional options
    optional_html=get_html_for_options(fname,script_info_dict,
                                       'optional_options',column_headers,
                                       help_img)

    return required_html,optional_html
