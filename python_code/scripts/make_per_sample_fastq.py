#!/usr/bin/env python
# File created on 02 May 2012
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.util import (parse_command_line_parameters, make_option,\
                       get_options_lookup,create_dir)
from cogent.parse.fasta import MinimalFastaParser
from qiime.parse import parse_mapping_file
from os.path import join, split, splitext


options_lookup=get_options_lookup()

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 # Example required option
 options_lookup['fasta_as_primary_input'],
 make_option('-q','--input_qual_fp',type="existing_filepath",
  help='path to the input quality file'),
 options_lookup['mapping_fp'],
 options_lookup['output_dir'],
]
script_info['optional_options'] = [\
 # Example optional option
 # options_lookup['output_dir'],
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    fasta_fp=opts.input_fasta_fp
    qual_fp=opts.input_qual_fp
    output_dir=opts.output_dir
    mapping_file=opts.mapping_fp
    
    create_dir(output_dir)
    
    map_data, map_header, map_comments = parse_mapping_file(open(mapping_file,'U'))
    
    # get a list of all possible sample_ids
    sample_ids=zip(*map_data)[0]
    output_fps={}
    # iterate over the sample_ids and generate a fasta file for each sample
    for s_id in sample_ids:
        output_fps[str(s_id)]=open(join(output_dir,'%s.fastq' % (str(s_id))),'w')
    
    # open sequence files
    sequences=MinimalFastaParser(open(fasta_fp,'U'))
    qual_sequences=MinimalFastaParser(open(qual_fp,'U'))

    for seq_name,seq in sequences:
        #print seq_name
        qual_seq_name,qual_seq=qual_sequences.next()
        #print qual_seq_name
        
        if seq_name==qual_seq_name:
            samp_id='_'.join(seq_name.split()[0].split('_')[:-1])
            output_fps[str(samp_id)].write('@%s\n%s\n+\n%s\n' % (seq_name,seq,qual_seq))
        else:
            print seq_name
        
    for s_id in sample_ids:
        output_fps[str(s_id)].close()
    
    

if __name__ == "__main__":
    main()