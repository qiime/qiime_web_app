from summarize_seqs_otu_hits import summarize_all_stats, submit_mapping_to_database
from optparse import OptionParser
from os import walk, remove
from os.path import join, exists

parser = OptionParser()
#parser.add_option("-i", "--input_dir", dest="input directory", help="Processed data directory to summarize and load into db")
parser.add_option("-s",  dest="study_id", help="The study_id to summarize seqs and otu stats for")
(options, args) = parser.parse_args()
study_id = options.study_id

base_dir = "/home/wwwuser/s/study_{0}/"
for dirname, dirnames, filenames in walk(base_dir.format(study_id)):
    for d in dirnames:
        if d.startswith('processed_data_'):
            processed_dir = join(base_dir.format(study_id), d)
            per_library_stats_file = join(processed_dir, 'gg_97_otus', 'per_library_stats.txt')
            if exists(per_library_stats_file):
                print 'Removing old per_library_stats.txt file: "{0}"'.format(per_library_stats_file)
                remove(per_library_stats_file)
            print 'Summarizing results for: "{0}"'.format(processed_dir)
            processed_results = summarize_all_stats(processed_dir)
            print 'Writing seqs and otu summary to database...'
            submit_mapping_to_database(processed_results)
            print 'Seq and OTU summary results successfully added to database.'
