#/bin/env python

from data_access_connections import data_access_factory
from enums import ServerConfig

study_id_list = [1034]

#925, 933, 1034, 1035, 1036, 1043, 1198

query_string = 
"""
select  distinct sp.rowid as rid, 
        substr(slrm.sample_name, 0, instr(slrm.sample_name, '.', -1) - 1) as sample_name,
        substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) as sequence_prep_id_orig,
        sp.sequence_prep_id as sequence_prep_id_current,
		sa.sample_id
from    split_library_read_map slrm
        inner join analysis a
        on slrm.split_library_run_id = a.split_library_run_id
        inner join qiime_metadata.sample sa
        on substr(slrm.sample_name, 0, instr(slrm.sample_name, '.', -1) - 1) = sa.sample_name
        inner join qiime_metadata.sequence_prep sp
        on sa.sample_id = sp.sample_id
where   a.study_id = {0}
        and sa.study_id = a.study_id;
"""

update_string = 
"""
update	sequence_prep
set		sequence_prep_id = {0}
where	sample_id = {1}
"""

con = None

try:

	data_access = data_access_factory(ServerConfig.data_access_type)
	con = data_access.getMetadataDatabaseConnection()

	for study_id in study_id_list:
		rowid, sample_name, sequence_prep_id_orig, sequence_prep_id_current, sample_id = \
			dynamicMetadataSelect(query_string.format(str(study_id))
	
		print update_string.format(sequence_prep_id_orig, sample_id)
		#con.cursor.execute(update_string.format(sequence_prep_id_orig, sample_id))
	
finally:
	if con:
		con.close()
