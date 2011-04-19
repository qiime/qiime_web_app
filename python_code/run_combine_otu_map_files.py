__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from os.path import *

def combine_otu_files(otu_map_files, output_otu_map):
    """
    Combines two 'like' otu files
    
    Unlike merge_otu_maps.py, this funciton simply takes two 'like' otu maps and
    puts them into a single file.
    """
    
    # Make sure output directory exists:
    if not exists(split(output_otu_map)[0]):
        mkdir(split(output_otu_map)[0])
    
    combined_output = open(output_otu_map, 'w')
    otu_map = {}

    # Merge all files
    otu_map_files = otu_map_files.split(',')
    for f in otu_map_files:
        current_file = open(f, 'r')
        for line in current_file:
            items = line.strip('\n').split('\t')
            key = items[0]
            #print str(otu_map)
            if key not in otu_map:
                otu_map[key] = []
    
            i = 1
            while i < len(items):
                names = otu_map[key]
                current_item = items[i]
                if current_item not in names:
                    names.append(current_item)
                i += 1    
        current_file.close()

    # Write out the combined file
    for otu_id in otu_map:
        seq_id_list = '\t'.join(otu_map[otu_id])
        line = '{otu_id}\t{seq_id_list}\n'.format(otu_id = otu_id, seq_id_list = seq_id_list)
        combined_output.write(line)    
        
    combined_output.close()
