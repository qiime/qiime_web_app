#!/usr/bin/env python

"""
the definition of the input file from Jesse Zaneveld. Email ref:

    From: Jesse Zaneveld <zaneveld@gmail.com>
    Date: Tue, Aug 10, 2010 at 3:37 PM
    Subject: Fwd: 16S sequences screened against GreenGenes
    To: Jesse Stombaugh <jesse.stombaugh@colorado.edu>

Here are the raw sequences found by screening KEGG against the
GreenGenes Core 09 set from the FastUniFrac website
('16S_seqs_nuc_vs_GreenGenesCore_May_5.fasta')...
"""

from sys import argv
from hashlib import md5
from cogent.parse.fasta import MinimalFastaParser

output = []
for seqid, seq in MinimalFastaParser(open(argv[1])):
    output.append('\t'.join([seqid.split(' ')[0], seq, md5(seq).hexdigest()]))
f = open(argv[2],'w')
f.write('\n'.join(output))
f.close()

