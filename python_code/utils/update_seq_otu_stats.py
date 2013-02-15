from data_access_connections import data_access_factory
from enums import ServerConfig
from summarize_seqs_otu_hits import summarize_all_stats
import traceback

data_access = data_access_factory(ServerConfig.data_access_type)
query = 'select distinct sa.study_id from sample sa inner join sff.analysis a on sa.study_id = a.study_id order by study_id desc'
results = data_access.dynamicMetadataSelect(query)
debug = True

for result in results:
    study_id = result[0]

    try:
        print 'Updating study {0}'.format(study_id)

        # Get results for all processed_data_ folders in this study's directory
        processed_results = summarize_all_stats(study_id)
        
        # Iterate over each folder's data - can be many processed_data_ folders for a single study
        for directory in processed_results:
            print 'processed_data_ folder: "{0}"'.format(directory)

            # Unpack the values for each processed_data_ directory
            mapping, seq_header_lines, otu_header_lines = processed_results[directory]

            # Unpack and iterate over each mapping
            for sample_name, sequence_count, otu_count, percent_assignment in mapping:
                sequence_prep_id = sample_name.split('.')[-1]
            
                # Write values to database for this sequence_prep_id        
                print '    sequence_prep_id: {0}, seq_count: {1}, otu_count: {2}, percent_assignment: {3}'.format(sequence_prep_id, sequence_count, otu_count, percent_assignment)
                data_access.updateSeqOtuCounts(sequence_prep_id, sequence_count, otu_count, percent_assignment)
            
                if debug:
                    print 'added to database: prep: {0}, seq_count: {1}, otu_count: {2}'.format(\
                        str(sequence_prep_id), str(sequence_count), str(otu_count))

    except Exception, e:
        print 'Could not process study_id: {0}. The error was: "{1}"\n{2}'.format(study_id, str(e), traceback.print_exc())


