__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from cogent.parse.fasta import *
from data_access_connections import data_access_factory
from enums import ServerConfig
from hashlib import md5
from os.path import join

def process_items(md5_list, md5_sequence_map, md5_seq_id_map, otu_map, data_access, leftovers_fasta_file):
    # Get our list of found items
    results = data_access.getFoundOTUArray(md5_list)
    
    if results == None:
        return
    
    found_otus = results[1]
    found_otus_seq_md5 = results[2]
    
    # If found in DB, add to our OTU map. If not, write to our new FASTA file.
    i = 0
    while i < len(found_otus):
        
        otu_id = found_otus[i]
        md5 = found_otus_seq_md5[i]    
        i += 1
        
        if otu_id == None:
            continue
        
        seq_id = md5_seq_id_map[md5]    
        
        if otu_id in otu_map:
            otu_map[otu_id].append(seq_id)
        else:
            otu_map[otu_id] = [seq_id]
        
        # Subtract from our md5_sequence_map. We'll iterate over the remainder
        # next and write these entries to a new FASTA file
        del md5_sequence_map[md5]
        

    # Write the leftovers to a new FASTA file
    for md5 in md5_sequence_map:
        seq_id = md5_seq_id_map[md5]
        sequence = md5_sequence_map[md5]
        line = '>{id}\n{sequence}\n'.format(id = seq_id, sequence = sequence)
        leftovers_fasta_file.write(line)

def find_otus(input_fasta, leftover_fasta, otu_map):
    input_fasta_file = open(input_fasta, 'r')
    leftovers_fasta_file = open(leftover_fasta, 'w')
    otu_map_file = open(otu_map, 'w')

    # OTU map will be a dict of lists: otu_id, [list of sequence names]
    otu_map = {}

    # Dict of md5:sequnece values
    md5_sequence_map = {}
    md5_seq_id_map = {}
    md5_list = []

    # Collection count for database submission. This is the size of the array we will
    # pass to oracle for bulk lookups of existing sequences
    items_to_submit_to_db = 100
    i = 0

    data_access = data_access_factory(ServerConfig.data_access_type)
    parser = FastaParser(input_fasta_file)

    for rec in parser:
        # Increment the batch counter
        i += 1
    
        # Collect the values we'll be needing
        
        # First value is the arbitrary otu_id assigned by exact match filter
        #seq_id = rec[0].split()[0]
        seq_id = str(rec[0])
        #print str(seq_id)
        sequence = str(rec[1])
        m = md5(sequence).hexdigest()
        md5_list.append(m)
        md5_sequence_map[m] = sequence
        md5_seq_id_map[m] = seq_id
    
        # Determine if it's time to submit check existence in DB:
        if i == items_to_submit_to_db:
            process_items(md5_list, md5_sequence_map, md5_seq_id_map, otu_map, data_access, leftovers_fasta_file)
            i = 0

            # Clear containers for next round
            md5_list = []
            md5_sequence_map.clear()

    # If there are leftovers, process the last batch
    if i > 1:
        process_items(md5_list, md5_sequence_map, md5_seq_id_map, otu_map, data_access, leftovers_fasta_file)

    # Write out the otu_map if there are entries in the dict
    for otu_id in otu_map:
        seq_id_list = '\t'.join(otu_map[otu_id])
        line = '{otu_id}\t{seq_id_list}\n'.format(otu_id = otu_id, seq_id_list = seq_id_list)
        otu_map_file.write(line)
    
    # Close our files
    input_fasta_file.close()
    leftovers_fasta_file.close()
    otu_map_file.close()

