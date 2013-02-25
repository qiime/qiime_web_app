#!/usr/bin/env python
# File created on 10 Feb 2013
from __future__ import division

__author__ = "Antonio Gonzalez Pena"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Antonio Gonzalez Pena"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Antonio Gonzalez Pena"
__email__ = "antgonza@gmail.com"
__status__ = "Development"


from qiime.util import parse_command_line_parameters, make_option
from cogent.parse.fasta import MinimalFastaParser

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 make_option('-i','--input_fp',type="existing_filepath",help='the input filepath'),\
 make_option('-o','--output_fp',type="new_filepath",help='the outpu filepath '),\
]
script_info['optional_options'] = [\
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    out_fp = open(opts.output_fp,'w')

    for label,seq in MinimalFastaParser(open(opts.input_fp,'U')):
        if len(seq)>90:
            seq=seq[:90]
        out_fp.write('>%s\n%s\n' % (label, seq))
    out_fp.close()

if __name__ == "__main__":
    main()
