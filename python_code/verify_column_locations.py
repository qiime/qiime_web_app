from data_access_connections import data_access_factory
from enums import *
data_access = data_access_factory(ServerConfig.data_access_type)

actual_tabs_cols = []
bad_tabs_cols = []

query = "select distinct upper(table_name), upper(column_name) from all_tab_columns where owner = 'QIIME_METADATA'"
results = data_access.dynamicMetadataSelect(query)
for table_name, column_name in results:
    table_name = '"{0}"'.format(table_name)
    column_name = '"{0}"'.format(column_name) 
    actual_tabs_cols.append((table_name, column_name))

query = "select distinct upper(column_name), upper(table_name) from study_actual_columns where study_id > 0 order by upper(column_name)"
results = data_access.dynamicMetadataSelect(query)
for column_name, table_name in results:
    upper_column_name = '"{0}"'.format(column_name)
    t = (table_name, upper_column_name)
    if t not in actual_tabs_cols:
        query = "select table_name from all_tab_columns where upper(column_name) = '{0}' and owner = 'QIIME_METADATA' and (table_name in \
        ('AIR', 'COMMON_EXTRA_PREP', 'COMMON_EXTRA_SAMPLE', 'COMMON_FIELDS', 'HOST', 'HOST_ASSOC_VERTIBRATE', 'HOST_ASSOCIATED_PLANT', \
            'HOST_SAMPLE', 'HUMAN_ASSOCIATED', 'MICROBIAL_MAT_BIOFILM', 'OTHER_ENVIRONMENT', 'SAMPLE', 'SAMPLE_SEQUENCE_PREP', 'SEDIMENT', \
            'SEQUENCE_PREP', 'SOIL', 'STUDY', 'WASTEWATER_SLUDGE', 'WATER') or table_name like 'EXTRA_SAMPLE_%' or table_name like \
            'EXTRA_PREP_%')".format(column_name.upper())
        results = data_access.dynamicMetadataSelect(query).fetchall()
        # More than one is a problemo.. handle manually
        if len(results) > 1:
            bad_tabs_cols.append(t)
            print 'Problem row - more than one table contains column. "{0}"'.format(str(t))
        else:
            correct_table_name = results[0][0]
            print correct_table_name 
            # Since there's only one possible correct table, fix it here.
            query = """update study_actual_columns set table_name = '"{0}"' where upper(column_name) = '{1}' and table_name = '{2}'""".format(correct_table_name, column_name, table_name)
            print query
            con = data_access.getMetadataDatabaseConnection()
            con.cursor().execute(query)
            con.cursor().execute('commit')
            print 'Updated'

# Done