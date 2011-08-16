#!/usr/bin/env python

from cogent.parse.fasta import MinimalFastaParser
from sys import argv
from hashlib import md5

__author__ = "Daniel McDonald"
__copyright__ = "QIIME Web App"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "daniel.mcdonald@colorado.edu"
__status__ = "Development"

def get_duplicate_ids_from_seqs(seqs):
    """Returns {sequence_md5_hash:[ids]}"""
    dup_ids = {}
    nr_seqs = {}

    for id_, seq in MinimalFastaParser(seqs):
        seq_hash = md5(seq).hexdigest()
        if seq_hash in dup_ids:
            dup_ids[seq_hash].append(id_)
        else:
            dup_ids[seq_hash] = [id_]
            nr_seqs[seq_hash] = seq
    return dup_ids, nr_seqs

def main():
    input_fp = open(argv[1])
    dup_ids, nr_seqs = get_duplicate_ids_from_seqs(input_fp)

    ### 2) do something awesome 
    ### 3) profit


if __name__ == '__main__':
    main()

