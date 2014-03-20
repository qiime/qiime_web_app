#!/usr/bin/env python


__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

"""Dump the observed funding amounts and counts

assumes addresses have been fixed
"""

from sys import argv

lines = [l.strip().split('\t') for l in open(argv[1])]
header = lines[0][:]
amount_idx = map(lambda x: x.lower(), header).index('amount')

counts = {}
for l in lines[1:]:
    amt = float(l[amount_idx])
    if amt in counts:
        counts[amt] += 1
    else:
        counts[amt] = 1

for k,v in sorted(counts.items()):
    print k, "\t", v


