#!/usr/bin/env python
# File created on 03 Aug 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME-webdev"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 

from optparse import make_option
from qiime.util import parse_command_line_parameters, get_options_lookup
from load_tab_file import input_set_generator
from cogent.parse.fasta import MinimalFastaParser
from os.path import split
import cx_Oracle
from data_access_connections import data_access_factory
from enums import DataAccessType
data_access = data_access_factory(DataAccessType.qiime_production)


options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
make_option('-i','--input_file',help='the input fasta file, where the sequence ids are the prokmsa_ids')
 # Example required option
 #make_option('-i','--input_dir',help='the input directory'),\
 #options_lookup['input_fasta']
]
script_info['optional_options'] = [\
    make_option('-t','--submit_to_test_db',action='store_true',help='By setting this parameter, the data will be submitted to the test database.',default=False),\

 # Example optional option
 #make_option('-o','--output_dir',help='the output directory [default: %default]'),\
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
        parse_command_line_parameters(**script_info)

    fasta_file = dict(MinimalFastaParser(open(opts.input_file,'U')))
    fname=split(opts.input_file)[-1].split('_')
    ref_dataset=fname[0]
    if ref_dataset=='gg':
        reference_dataset='GREENGENES_REFERENCE'
    threshold=fname[1]
    print threshold
    try:
        from data_access_connections import data_access_factory
        from enums import DataAccessType
        import cx_Oracle
        if opts.submit_to_test_db:
            data_access = data_access_factory(DataAccessType.qiime_test)
        else:
            data_access = data_access_factory(DataAccessType.qiime_production)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
        
    prokmsas=[]
    for prok_id in fasta_file:
        prokmsas.append('%s\t%s\t%s' % (str(prok_id),str(threshold),
                                            reference_dataset))
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()

    data_types=['s','i','s']
    for input_set in input_set_generator(prokmsas, cur,data_types):
        valid=data_access.loadSeqToSourceMap(True,input_set)
        if not valid:
            raise ValueError, 'Error: Unable to load Sequence to Source Map!'


    

if __name__ == "__main__":
    main()