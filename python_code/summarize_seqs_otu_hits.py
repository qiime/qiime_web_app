from os import listdir, getcwd
from os.path import isdir, join, exists

def get_processed_data_dirs(study_dir):
    """ Returns a list of processed_data_ directories for a study_dir
    """
    processed_data_dirs = []
    prefix = 'processed_data_'

    #print 'study_dir: {0}'.format(study_dir)

    for name in listdir(study_dir):
        #print name
        if name.startswith(prefix):
            processed_data_dirs.append(name)

    return processed_data_dirs

def parse_log_file(log_path, read_start_line, target_token_count):
	"""
	"""
	summary_dict = {}
    header_lines = []
    start_read = False
	
	log = open(log_path, 'r')
	
    for l in log:
        l = l.strip()
        if not start_read:
            # Ignore all lines until sample listing but store and return them to client
            if l != read_start_line:
                header_lines.append(l)
                continue
            else:
                start_read = True

        # Exit read loop when we reach end of sample list
        #if l == read_end_line:
        if l == '':
            break

        # Start reading samples. Non-zero length items are, in order, sample_name, sequence_count, barcode
        items = l.split()
        if len(items) != target_token_count:
            continue

        if target_token_count == 3:
        	sample_name, sequence_count, barcode = l.split()
        	summary_dict[sample_name] = sequence_count
        elif target_token_count == 2:
        	sample_name, otu_count = l.split()
        	summary_dict[sample_name] = otu_count

    log.close()

    return header_lines, summary_dict 

def summarize_seqs(processed_dir):
    """ 
    """
    log_path = join(processed_dir, 'split_libraries/split_library_log.txt')
    read_start_line = 'Sample\tSequence Count\tBarcode'

    header_lines, seq_summary_dict = parse_log_file(log_path, read_start_line, read_end_line)
    return header_lines, seq_summary_dict

def summarize_otus(processed_dir):
    """
    """
    per_librar_stats_file = join(processed_dir, 'gg_97_otus/per_library_stats.txt')
    # Generate the per_library_stats_file if it doesn't already exist
    if not exists (per_librar_stats_file):
    	biom_file = join(processed_dir, 'gg_97_otus/exact_uclust_ref_otu_table.biom')
        # Generate the file
        f = open(per_librar_stats_file, 'w')

        

        print str(count_per_sample)
		#counts_per_sample_values = counts_per_sample.values()



        compute_seqs_per_library_stats(biom_file)
        


        f.close()

	read_start_line = 'Seqs/sample detail:'

    header_lines, seq_summary_dict = parse_log_file(log_path, read_start_line, read_end_line)
    return header_lines, seq_summary_dict

def summarize_all_stats(study_id):
    """
    """

    # Get the processed data directories
    study_dir = 'study_{0}'.format(study_id)
    study_dir = join('/home/wwwuser/user_data/studies/', study_dir)
    processed_data_dirs = get_processed_data_dirs(study_dir)

    #print str(processed_data_dirs)

    # For each processed data folder, get the seq and otu sumamries
    for processed_dir in processed_data_dirs:
        header_lines, seq_summary_dict = summarize_seqs(join(study_dir, processed_dir))
        
        print processed_dir
        print '\n\n'
        for line in header_lines:
            print '::{0}'.format(line)
        print '\n\n\n'
        for item in seq_summary_dict:
            print '{0}:{1}'.format(item, seq_summary_dict[item])

        #otu_summary = summarize_otus(join(study_dir, processed_dir))
    
    # Match up the lists by sample name and return percent OTU assignment


