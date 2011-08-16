#!/usr/bin/env python

from cogent.parse.fasta import MinimalFastaParser
from sys import argv
from hashlib import md5
from time import time

def get_duplicate_ids_from_seqs(seqs):
    """Returns {sequence_md5_hash:[ids]}"""
    dup_ids = {}
    nr_seqs = {}

    start = time()
    for idx, (id_, seq) in enumerate(MinimalFastaParser(seqs)):
        seq_hash = md5(seq).hexdigest()
        if seq_hash in dup_ids:
            dup_ids[seq_hash].append(id_)
        else:
            dup_ids[seq_hash] = [id_]
            nr_seqs[seq_hash] = seq
        if idx % 100000 == 0:
            print time() - start
            start = time()
    return dup_ids, nr_seqs

def main():
    input_fp = open(argv[1])
    dup_ids, nr_seqs = get_duplicate_ids_from_seqs(input_fp)

    print len(dup_ids)



if __name__ == '__main__':
    main()

