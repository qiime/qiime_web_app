#!/usr/bin/env python
# File created on 07 Feb 2014
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
script_info['brief_description'] = """Take a plate map and creates db insert
statements for plate and plate_barcode table"""
script_info['script_description'] = """Input american gut plate map, 
sql output file"""
script_info['script_usage'] = [("Examples:","create db insert statment",
    "%prog -i ag_plate_map.txt -o ag_plate_inserts.sql")]
script_info['output_description']= "sql file"
script_info['required_options'] = [
 # Example required option
make_option('-i','--input_fp',type="existing_filepath",
    help='the input filepath'),
make_option('-o','--output_fp', type="new_filepath",
    help='the output filename')
]
script_info['optional_options'] = []
script_info['version'] = __version__


def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    platemapfile=opts.input_fp
    sqlfile=opts.output_fp
    verbose = opts.verbose
    sqloutfile=open(sqlfile, 'w')
    platemaplines = open(platemapfile,'r').readlines()
    platename=''
    print len(platemaplines)
    for line in platemaplines:
        line = line.split(',')
        if 'Plate' in line[0] and line[1] != '1':
            #new plate we only care about the first line
            platename=line[0]
            sqlstmt = "insert into plate (plate_id, plate) values"\
            " (seq_plate_id.nextval, '%s');\n" % platename
            sqloutfile.write(sqlstmt)
        elif line[0] != '':
            #this line contains barcodes
            if len(line[0]) == 1:
                for barcode in line[1:]:
                    try:
                        barcode = int(barcode)
                    except:
                        if verbose:
                            print 'barcode %s cannot be added' % barcode
                        continue
                #create an insert statment
                    sqlstmt = "insert into plate_barcode" \
                    " (plate_id, barcode) select plate_id, '%09d'"\
                    " from plate where plate = '%s';\n"\
                    % (barcode, platename)
                    sqloutfile.write(sqlstmt)
        else:
            #this is a separator between plates reset platename 
            platename = ''

    sqloutfile.close()


if __name__ == "__main__":
    main()