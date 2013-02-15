from data_access_connections import data_access_factory
from enums import ServerConfig
from summarize_seqs_otu_hits import summarize_all_stats

data_access = data_access_factory(ServerConfig.data_access_type)
query = 'select distinct sa.study_id from sample sa inner join sff.analysis a on sa.study_id = a.study_id order by study_id desc'
results = data_access.dynamicMetadataSelect(query)

for result in results:
    study_id = result[0]
    try:
        print 'Updating study {0}'.format(study_id)
        mapping, seq_header_lines, otu_header_lines = summarize_all_stats(study_id)

        for sample_name, sequence_count, otu_count, percent_assignment in mapping:
            sequence_prep_id = sample_name.split('.')[-1]

        print '    sequence_prep_id: {0}, seq_count: {1}, otu_count: {2}, percent_assignment: {3}'.format(sequence_prep_id, sequence_count, otu_count, percent_assignment)
        data_access.updateSeqOtuCounts(sequence_prep_id, sequence_count, otu_count, percent_assignment)

        if debug:
            print 'added to database: prep: {0}, seq_count: {1}, otu_count: {2}'.format(\
                str(sequence_prep_id), str(sequence_count), str(otu_count))

    except Exception, e:
        print 'Could not process study_id: {0}. The error was: "{1}"'.format(study_id, str(e))

