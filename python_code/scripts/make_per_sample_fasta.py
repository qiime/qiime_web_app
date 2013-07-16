#!/usr/bin/env python

from sys import argv
from optparse import OptionParser, make_option
from qiime.util import create_dir
from qiime.filter import filter_fasta
from qiime.parse import parse_mapping_file
from os.path import join
from cogent.parse.fasta import MinimalFastaParser

__author__ = "Doug Wendel"
__copyright__ = "2013, QIIME web application"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

options = [make_option('-m','--map_file',help='The input mapping file'),
    make_option('-i','--fna_file',help='The multiplexed input FASTA formatted file'),
    make_option('-o','--output_dir',help='The output directory')]

def get_seqs_to_keep_lookup_from_prefix(fasta_f,prefix):
    seqs_to_keep = [seq_id
                    for seq_id, seq in MinimalFastaParser(fasta_f)
                    if seq_id.startswith(prefix)]
    return {}.fromkeys(seqs_to_keep)

def filter_fasta_fp(input_seqs_fp, output_seqs_fp, seqs_to_keep, negate = False):
    """Filter a fasta file to include only sequences listed in seqs_to_keep """
    input_seqs = MinimalFastaParser(open(input_seqs_fp, 'U'))
    output_f = open(output_seqs_fp, 'w')
    filter_fasta(input_seqs, output_f, seqs_to_keep, negate)

def make_per_sample_fasta(input_seqs_fp, mapping_file, output_dir):
    """ Creates per-sample fasta files from a multiplexed fasta file and a mapping file """
    mapping_data, header, comments = parse_mapping_file(mapping_file, suppress_stripping=False)

    for item in mapping_data:
        negate = False
        create_dir(output_dir)
        seqs_to_keep = item[0]
        output_file = join(output_dir, seqs_to_keep + '.fna')
        seqs_to_keep_lookup = get_seqs_to_keep_lookup_from_prefix(open(input_seqs_fp), seqs_to_keep)
        filter_fasta_fp(input_seqs_fp, output_file, seqs_to_keep_lookup, negate)

def main(args_in = argv):
    parser = OptionParser(option_list = options)
    opts, args = parser.parse_args(args = args_in)
    map_file = opts.map_file
    fna_file = opts.fna_file
    output_dir = opts.output_dir

    make_per_sample_fasta(fna_file, map_file, output_dir)
    
if __name__ == '__main__':
    main()
