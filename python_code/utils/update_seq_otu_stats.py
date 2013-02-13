from data_access_connections import data_access_factory
from enums import ServerConfig
from summarize_seqs_otu_hits import summarize_all_stats

data_access = data_access_factory(ServerConfig.data_access_type)
query = 'select distinct sa.study_id from sample sa inner join sff.analysis a on sa.study_id = a.study_id order by study_id desc'
results = data_access.dynamicMetadataSelect(query)

for result in results:
	study_id = result[0]
	try:
		summarize_all_stats(study_id)
	except Exception, e:
		print 'Could not process study_id: {0}. The error was: "{1}"'.format(study_id, str(e))

