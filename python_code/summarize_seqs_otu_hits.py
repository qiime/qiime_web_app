from os import listdir, getcwd
from os.path import isdir, join, exists
from qiime.util import get_qiime_scripts_dir, load_qiime_config
from subprocess import Popen, PIPE, STDOUT

def get_processed_data_dirs(study_dir):
    """ Returns a list of processed_data_ directories for a study_dir
    """
    processed_data_dirs = []
    prefix = 'processed_data_'
    
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
                continue

        # Exit read loop when we reach end of sample list
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
            sample_name = sample_name[:-1]
            summary_dict[sample_name] = otu_count

    log.close()

    return header_lines, summary_dict 

def summarize_seqs(processed_dir):
    """ 
    """
    log_path = join(processed_dir, 'split_libraries/split_library_log.txt')
    read_start_line = 'Sample\tSequence Count\tBarcode'
    header_lines, seq_summary_dict = parse_log_file(log_path, read_start_line, 3)
    return header_lines, seq_summary_dict

def summarize_otus(processed_dir):
    """
    """
    per_library_stats_file = join(processed_dir, 'gg_97_otus/per_library_stats.txt')

    # Generate the per_library_stats_file if it doesn't already exist
    if not exists (per_library_stats_file):
        qiime_config = load_qiime_config()
        biom_file = join(processed_dir, 'gg_97_otus/exact_uclust_ref_otu_table.biom')
        python_exe_fp = qiime_config['python_exe_fp']
        script_dir = get_qiime_scripts_dir()
        per_library_stats_script = join(script_dir, 'per_library_stats.py')
        command = '{0} {1} -i {2}'.format(python_exe_fp, per_library_stats_script, biom_file)

        # Run the script and produce the per_library_stats.txt
        proc = Popen(command, shell = True, universal_newlines = True, stdout = PIPE, stderr = STDOUT)
        return_value = proc.wait()
        f = open(per_library_stats_file, 'w')
        f.write(proc.stdout.read())
        f.close()

    # File exists, parse out details
    read_start_line = 'Seqs/sample detail:'
    header_lines, seq_summary_dict = parse_log_file(per_library_stats_file, read_start_line, 2)
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
        seq_header_lines, seq_summary_dict = summarize_seqs(join(study_dir, processed_dir))
        otu_header_lines, otu_summary_dict = summarize_otus(join(study_dir, processed_dir))

        # Create the tuples
        mapping = []
        for sample_name in seq_summary_dict:
            sequence_count = seq_summary_dict[sample_name]
            otu_count = None
            percent_assignment = None

            if sample_name in otu_summary_dict:
                otu_count = otu_summary_dict[sample_name]
                percent_assignment = (float(otu_count) / float(sequence_count)) * 100.0

            mapping.append((sample_name, sequence_count, otu_count, percent_assignment))

        return mapping, seq_header_lines, otu_header_lines


