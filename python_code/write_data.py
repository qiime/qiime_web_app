#!/usr/bin/env python
'''
__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2009, the Qiime Project"
__credits__ = ["Jesse Stombaugh"] #remember to add yourself
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Prototype"

Author: Jesse Stombaugh (jesse.stombaugh@colorado.edu)
Status: Prototype

'''


def write_fasta_from_db(out_path,resulting_seqs):
    f_out = open(out_path+'seqs.fna', 'w')
    for i in range(len(resulting_seqs)):
        f_out.write(">%s_%s\t%s\n" % (resulting_seqs[i][0],resulting_seqs[i][3], resulting_seqs[i][1]))
        f_out.write("%s\n" % resulting_seqs[i][2])
    
    f_out.close()

def write_metadata_from_db(out_path,headers,resulting_metadata):
    header_dict={}
    for j in range(len(headers)):
        header_dict[headers[j][1]]= str(headers[j][0]) 
    
    f_out = open(out_path+'mapping.txt', 'w')
    metadata_results=""
    f_out.write("#")
    for j in range(len(header_dict)):
        f_out.write("%s\t" % str(header_dict[j+1]))
    
    f_out.write('\n')
        
    for i in range(len(resulting_metadata)):
        for j in range(len(resulting_metadata[i])):
            f_out.write("%s\t" % str(resulting_metadata[i][j]))

        f_out.write('\n')

    f_out.close()
