from os import listdir, getcwd
from os.path import isdir, join, exists
from qiime.util import get_qiime_scripts_dir, load_qiime_config
from subprocess import Popen, PIPE, STDOUT
from enums import ServerConfig
from data_access_connections import data_access_factory
from enums import ServerConfig
from utils.psp_utils import tab_delim_lines_to_table

def parse_log_file(log_path, start_lines):
    """ Parses one of several log files produced in the qiime pipeline. Returns 
        aggregated counts of either seqs per sample or otus per sampe. A factory
        method derivitave.
    """

    summary_dict = {}
    header_lines = []
    start_read = False
    debug = True
    
    if debug:
    	print log_path

    log = open(log_path, 'U')
    
    for l in log:
        l = l.strip()
        header_lines.append(l)

        #if debug:
        #    print l

        if not start_read:            
            for start_line in start_lines:
                if l.startswith(start_line):
                    if debug:
                        print 'Start line found: {0}'.format(start_line)
                    start_read = True
            continue

        # Exit read loop when we reach end of sample list
        if l == '' or l == None:
            break

        # Start reading samples
        items = l.split()
        if len(items) < 2:
            continue

        sample_name = items[0]
        if sample_name.endswith(':'):
            sample_name = sample_name[:-1]
        count = items[1]
        summary_dict[sample_name] = count

    log.close()

    return header_lines, summary_dict 

def summarize_seqs(processed_dir):
    """ 
    """
    log_path = join(processed_dir, 'split_libraries/split_library_log.txt')
    start_lines = []
    start_lines.append('Median sequence length:')
    start_lines.append('Sample\tSequence Count\tBarcode')
    header_lines, seq_summary_dict = parse_log_file(log_path, start_lines)
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
    start_lines = ['Seqs/sample detail:']
    header_lines, otu_summary_dict = parse_log_file(per_library_stats_file, start_lines)
    return header_lines, otu_summary_dict

def summarize_all_stats(processed_dir):
    """
    """
    processed_results = {}

    try:
        seq_header_lines, seq_summary_dict = summarize_seqs(processed_dir)
        otu_header_lines, otu_summary_dict = summarize_otus(processed_dir)

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

        processed_results[processed_dir] = (mapping, seq_header_lines, otu_header_lines)
    except Exception, e:
        print str(e)


    # Return all of the results
    return processed_results

def histograms_as_html_table(processed_dir):
    """Generates an HTML table from the histograms.txt file

    Every "processed_data_*" directory witll contain a split_libraries
    directory, and in that directory is a text file, histograms.txt, that
    has read-length summaries from the split_libraries process. This
    function will grab that file (assuming the consistent location) and
    return an HTML-format table to display the information.

    input:
        processed_dir: The path to the processed directory

    output:
        HTML-format table containing the information in the histograms.txt
        file
    """
    histograms_fp = join(processed_dir, 'split_libraries', 'histograms.txt')
    return tab_delim_lines_to_table(open(histograms_fp, 'U').readlines())

def submit_mapping_to_database(processed_results, debug=True):
    data_access = data_access_factory(ServerConfig.data_access_type)
    
    # Iterate over each folder's data - can be many processed_data_ folders for a single study
    for directory in processed_results:
        # Unpack the values for each processed_data_ directory
        mapping, seq_header_lines, otu_header_lines = processed_results[directory]

        # Unpack and iterate over each mapping
        for sample_name, sequence_count, otu_count, percent_assignment in mapping:
            sequence_prep_id = sample_name.split('.')[-1]
        
            # Write values to database for this sequence_prep_id        
            data_access.updateSeqOtuCounts(sequence_prep_id, sequence_count, otu_count, percent_assignment)
        
            if debug:
                print 'added to database: prep: {0}, seq_count: {1}, otu_count: {2}'.format(\
                    str(sequence_prep_id), str(sequence_count), str(otu_count))




