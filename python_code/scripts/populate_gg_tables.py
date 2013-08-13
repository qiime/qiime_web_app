#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from data_access_connections import data_access_factory
from enums import *
from sys import argv
from optparse import make_option
from qiime.util import parse_command_line_parameters
from cogent.parse.fasta import MinimalFastaParser
from hashlib import md5

# Define the loading functions
def load_gg_seqs(otu_seqs_file, data_access):
    """ Loads the sequences and GG identifiers into the database. Note that 
    sequence_source_id of 1 maps to GG 5_13 at 97 percent identity
    """
    seq_id = 1
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    seq_sql = """
    insert  into seq 
            (seq_id, seq_source_id, sequence_string, sequence_md5) 
    values  (:seq_id, 1, :sequence_string, :sequence_md5) 
    """
    gg_sql = """
    insert  into gg 
            (gg_id, seq_id) 
    values  (:gg_id, :seq_id)
    """

    seq_sql_values = []
    gg_sql_values = []

    # Iterate over the file. This method comes at the cost of high
    # memory usage but is much faster.
    seqs = MinimalFastaParser(open(otu_seqs_file, 'U')) 
    for gg_id, sequence_string in seqs:
        sequence_md5 = md5(sequence_string).hexdigest()
        seq_sql_values.append((seq_id, sequence_string, sequence_md5))
        gg_sql_values.append((gg_id, seq_id))
        seq_id += 1

    # Insert the sequence values
    cur.prepare(seq_sql)
    cur.executemany(None, seq_sql_values)
    con.commit()

    # Insert the GG values
    cur.prepare(gg_sql)
    cur.executemany(None, gg_sql_values)
    con.commit()

def load_gg_taxonomy():
    pass

script_info = {}
script_info['brief_description'] = "This scirpt loads Greengenes sequences into the database."
script_info['script_description'] = "Loads the specified version of Greengenes OTUs and sequences into the database."
script_info['script_usage'] = [("Example", "This is an example usage", "python populate_gg_tables.py -i path_to_")]
script_info['output_description']= "No files are produced. This script populates the database with GG seqs and OTUs."
script_info['required_options'] = [make_option('-i','--otu_seqs_file', help='The GG rep_set OTU file.')]
script_info['optional_options'] = [\
    make_option('-d','--debug', action='store_true', help='Specifies that verbose debug output should be displayed.',default=True)
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # Some needed variables
    otu_seqs_file = opts.otu_seqs_file
    debug = opts.debug
    data_access = data_access_factory(ServerConfig.data_access_type)

    # Load the GG sequences
    load_gg_seqs(otu_seqs_file, data_access)

    # Load the GG taxonomy

if __name__ == "__main__":
    main()


