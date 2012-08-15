#/bin/env python

from data_access_connections import data_access_factory
from enums import ServerConfig

#study_id_list = [925, 933, 1034, 1035, 1036, 1043, 1198, 1222, 1242, 1289, 1453, 1526, 1235, 550, 722, 940]
#study_id_list = [1036, 1043, 1198, 1222, 1242, 1289, 1453, 1526, 1235, 550, 722, 940]
study_id_list = [808, 1031, 1033, 1453]
query_string = \
"""
select  distinct sp.rowid as rid, 
        substr(slrm.sample_name, 0, instr(slrm.sample_name, '.', -1) - 1) as sample_name,
        substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) as sequence_prep_id_orig,
        sp.sequence_prep_id as sequence_prep_id_current,
		sa.sample_id
from    sff.split_library_read_map slrm
        inner join sff.analysis a
        on slrm.split_library_run_id = a.split_library_run_id
        inner join qiime_metadata.sample sa
        on substr(slrm.sample_name, 0, instr(slrm.sample_name, '.', -1) - 1) = sa.sample_name
        inner join qiime_metadata.sequence_prep sp
        on sa.sample_id = sp.sample_id
where   a.study_id = {0}
        and sa.study_id = a.study_id
"""

update_string = \
"""
update	sequence_prep
set		sequence_prep_id = {0}
where	sample_id = {1}
"""

data_access = data_access_factory(ServerConfig.data_access_type)
con = data_access.getMetadataDatabaseConnection()

for study_id in study_id_list:
    print '======================================================================================='
    print query_string.format(str(study_id))

    results = data_access.dynamicMetadataSelect(query_string.format(str(study_id)))
    count = 0

    for rowid, sample_name, sequence_prep_id_orig, sequence_prep_id_current, sample_id in results:
        print rowid, sample_name, sequence_prep_id_orig, sequence_prep_id_current, sample_id
        print update_string.format(sequence_prep_id_orig, sample_id)
        try:
            con.cursor().execute(update_string.format(sequence_prep_id_orig, sample_id))
            count += 1
        except Exception, e:
            print str(e)

    print 'Total successful row count: {0}'.format(str(count))

    con.cursor().execute('commit');

con.close()

# end

