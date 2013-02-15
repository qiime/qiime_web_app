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
        submit_mapping_to_database(processed_results)

    except OSError, os:
        # Study dir doesn't exist on server - fine to just ignore
        pass
        
    except Exception, e:
        print 'Could not process study_id: {0}. The error was: "{1}"'.format(study_id, str(e))


