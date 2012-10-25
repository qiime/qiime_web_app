#!/usr/bin/env python
# File created on 30 Dec 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.3.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 


from qiime.util import parse_command_line_parameters, make_option,create_dir
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType
from cogent.parse.fasta import MinimalFastaParser
from os.path import join,split


seq_sources=['454V2', '454V2']

script_info = {}
script_info['brief_description'] = "This script takes a representative set of sequences and otu map, then pulls the reference ids assigned to the OTU identifiers from the DB."
script_info['script_description'] = ""
script_info['script_usage'] = [("Example","Write a list of V2 Titanium reads that do not hit GGs.","python get_otu_failure_seqs.py -p TGCTGCCTCCCGTAGGAGT -s 'Titanium' -o test.fasta")]
script_info['output_description']= "Generates a fasta file containing unique sequences that do not hit GGs"
script_info['required_options'] = [\
 make_option('-f','--rep_set_fp',type="existing_filepath",
             help='Representative sequence fasta file'),\
 make_option('-s','--sequence_source',type="string",
             help='sequence source to get reference ids for (%s)' % ', '.join(seq_sources)),\
 make_option('-o','--output_dir',type="new_dirpath",
             help='output directory]'),\
]
script_info['optional_options'] = [\
 make_option('-i','--otu_map_fp',type="existing_filepath",
             help='OTU mapping file'),\
]
script_info['version'] = __version__


def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    # get command-line parameters
    rep_set_fp=opts.rep_set_fp
    otu_map_fp=opts.otu_map_fp
    sequence_source=opts.sequence_source
    output_dir = opts.output_dir
    
    # create output directory
    create_dir(output_dir)

    # get data access connection
    data_access = data_access_factory(ServerConfig.data_access_type)

    # write PL/SQL query statement
    statement="select rf.ssu_sequence_id,rf.reference_id from gg_plus_denovo_reference rf " +\
    "inner join sequence_source ss on rf.sequence_source_id=ss.sequence_source_id " +\
    "where ss.source_name='%s'" % (sequence_source)
    #print statement 
    
    # Run the statement
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    
    # create a lookup dictionary
    results = cur.execute(statement)
    #print results
    ssu_id_to_ref_id={}
    for i in results:
        ssu_id_to_ref_id[str(i[0])]=str(i[1])
    
    # write new fasta file with updated assignments
    new_fasta_fp=join(output_dir,'rep_set_reassigned_otu_ids.fasta')
    openfasta=open(new_fasta_fp,'w')
    
    # write a mapping file for topiary explorer
    new_map_fp=join(output_dir,'new_otu_id_mapping.txt')
    openmap=open(new_map_fp,'w')
    # parse and write new fasta file
    seqs=MinimalFastaParser(open(rep_set_fp,'U'))
    for seq_name,seq in seqs:
         seqs_name_split=seq_name.split()
         tmp_store=seqs_name_split[0]
         seqs_name_split[0]=seqs_name_split[1]
         seqs_name_split[1]=tmp_store
         openfasta.write('>%s\n%s\n' % (' '.join(seqs_name_split),seq))
         
         openmap.write('%s\t%s\n' % (seqs_name_split[0],sequence_source))
         
    openfasta.close()
    openmap.close()
         

if __name__ == "__main__":
    main()
