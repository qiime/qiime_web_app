#!/usr/bin/env python


__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

"""Take dollar amounts and determine the number of samples

Assumes column zero is "Amount"
"""

from sys import argv

lines = [l.strip().split('\t') for l in open(argv[1],'U')]

header = lines[0][:]
header[0] = "swabs_per_kit"
#currency_idx = header.index('Currency')
country_idx = header.index('Country')

output_assigned = open(argv[1].split('.')[0] + '_numswabs.txt','w')
output_unassigned = open(argv[1].split('.')[0] + '_noswabs.txt','w')
output_assigned.write('\t'.join(header))
output_assigned.write('\n')
output_unassigned.write('\t'.join(lines[0]))
output_unassigned.write('\n')

amount_map = [(0.0, 0.1, 1), # assert currency.startswith('KNIGHT_')
              (98.9, 129.1, 1),
              (179.9, 230.1, 2),
              (259.9, 260.1, 3),
              (319.9, 320.1, 4),
              (499.9, 500.1, 7)]

us_amount_map = {1:99.0,
                 2:180.0,
                 3:260.0,
                 4:320.0,
                 7:500.0}

def write_unassigned(l):
    print '\t'.join(l)
    output_unassigned.write('\t'.join(l))
    output_unassigned.write('\n')

def write_assigned(l):
    l[0] = str(num_swabs)
    output_assigned.write('\t'.join(l))
    output_assigned.write('\n')

import string
amount_idx = map(string.lower, lines[0]).index('amount')
for l in lines[1:]:
    amount = float(l[amount_idx].replace(",",""))
    
    num_swabs = None
    for low,high,swabs in amount_map:
        if low <= amount <= high:
            num_swabs = swabs
            break
    
    if num_swabs is None:
        #print l
        #print "None"
        write_unassigned(l)
    elif l[country_idx] != 'US' \
         and num_swabs in us_amount_map \
         and amount == us_amount_map[num_swabs]:
        #print l
        print "bad ammount"
        write_unassigned(l)
    elif num_swabs == 1 \
            and amount < 98.9:
         #and not l[currency_idx].startswith('KNIGHT_'):
        write_unassigned(l)
    else:
        write_assigned(l)

output_unassigned.close()
output_assigned.close()
