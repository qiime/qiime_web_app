#!/usr/bin/env python


__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

"""Correct the weird added newline in the address field

Fundrazr dumps a weird structure that needs to be beaten into submission

The specific issue is that some of the address fields break lines:

something TAB foo TAB bar TAB my broken
address TAB other TAB stuff

whereas what we want is:

something TAB foo TAB bar TAB my broken address TAB other TAB stuff
"""

from sys import argv
from string import strip

lines = [l.strip().split('\t') for l in open(argv[1],'U')]

header = lines[0][:]
address_idx = header.index('Address')
email_idx = header.index('Contact email')
header[email_idx] = 'email'

output = [header]
exp_field_count = len(header)

min_stack = None
for line in lines[1:]:
    if min_stack:
        assert len(line) != exp_field_count
         
        combo_line = min_stack[:-1]
        combo_line.append(' '.join([min_stack[-1], line[0]]))
        combo_line.extend(line[1:])
        assert len(combo_line) == exp_field_count
        
        line = combo_line
        min_stack = None
    elif len(line) != exp_field_count:
        min_stack = line[:]
        continue

    line = map(lambda x: x.strip().strip('"'), line)

    output.append(line[:])

f = open(argv[2],'w')
f.write('\n'.join(['\t'.join(l) for l in output]))
f.write('\n')
f.close()

