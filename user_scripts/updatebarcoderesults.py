#!/usr/bin/env python
# File created on 11 Feb 2014
from __future__ import division

__author__ = "Emily TerAvest"
__copyright__ = "Copyright 2011, The QIIME Web App"
__credits__ = ["Emily TerAvest"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Emily TerAvest"
__email__ = "ejteravest@gmail.com"
__status__ = "Development"


from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = """Take a list of all the barcdoes we have
american gut results for and updates the database to reflect having results"""
script_info['script_description'] = """Takes a text file of the results of ls 
the american gut results directory and outputs an sql file to update the
 database"""
script_info['script_usage'] = [("Examples:","create database update statements",
    "%prog -i listoffiles.txt -o updateresults.sql")]
script_info['output_description']= "an sql file to update results "\
"read status of db"
script_info['required_options'] = [
 # Example required option
 make_option('-i','--input_fp',type="existing_filepath",
    help='the input filepath a list of all the files in the results directory'),
 make_option('-o','--output_fp',type="new_filepath",help='the output sqlfile')
]
script_info['optional_options'] = []
script_info['version'] = __version__


def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    input_fd=opts.input_fp
    filenamesfile = open(input_fd, 'r')
    sqlfile=opts.output_fp
    sqloutfile=open(sqlfile, 'w')
    barcodeline = filenamesfile.readline()
    while (barcodeline):
        barcode = barcodeline.split(' ')[-1].split('.')[0]
        sqlstmt = "update ag_kit_barcodes set results_ready = 'Y'"\
         " where barcode = '%s';\n" % barcode
        sqloutfile.write(sqlstmt)
        sqlstmt = "update barcode set sequencing_status = 'SUCCESS'"\
        " where barcode = '%s';\n" % barcode
        sqloutfile.write(sqlstmt)
        barcodeline = filenamesfile.readline()
    sqloutfile.close()
    filenamesfile.close()


if __name__ == "__main__":
    main()