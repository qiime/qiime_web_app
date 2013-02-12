#!/usr/bin/env python
# File created on 10 Feb 2013
from __future__ import division

__author__ = "Antonio Gonzalez Pena, Doug Wendel"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Antonio Gonzalez Pena, Doug Wendel"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"


from qiime.util import parse_command_line_parameters, make_option
from cogent.parse.fastq import MinimalFastqParser
from itertools import izip

script_info = {}
script_info['brief_description'] = "Trims a fastq file to the specified length."
script_info['script_description'] = "Takes an input fastq file, trims each read and qual score to the specified length, and writes the results to the output file path."
script_info['script_usage'] = [("","","")]
script_info['output_description']= "A new fastq file with trimmed reads/qual scores."
script_info['required_options'] = [\
    make_option('-i','--input_fp',type="existing_filepath",help='The input file path'),\
    make_option('-o','--output_fp',type="new_filepath",help='The output file path'),\
    make_option('-l','--trim_length',type="int",help='The length to trim sequences and qual scores to.'),\
]
script_info['optional_options'] = []
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    out_fp = open(opts.output_fp, 'w')
    trim_length = opts.trim_length

    for fastq_data in izip(MinimalFastqParser(open(opts.input_fp, 'U'), strict=False)):
        sequence = fastq_data[0][1][:trim_length]
        qual = fastq_data[0][2][:trim_length]
        header = fastq_data[0][0]

        # Write the new output file
        out_fp.write(header + '\n')
        out_fp.write(sequence + '\n')
        out_fp.write('+\n')
        out_fp.write(qual + '\n')

    out_fp.close()

if __name__ == "__main__":
    main()

