

try:
    from data_access_connections import data_access_factory
    from enums import ServerConfig
    import cx_Oracle
    data_access = data_access_factory(ServerConfig.data_access_type)
except ImportError:
    print "NOT IMPORTING QIIMEDATAACCESS"
    pass


statement="""select distinct st.study_id,sp.sequence_prep_id,sp.run_prefix,st.study_alias,s.sample_name,sp.barcode from "SAMPLE" s
             inner join study st on s.study_id=st.study_id
             inner join sequence_prep sp on s.sample_id=sp.sample_id
             inner join SFF.analysis an on s.study_id=an.study_id"""

con = data_access.getMetadataDatabaseConnection()
cur = con.cursor()

results = cur.execute(statement)
sample_id={}
study_samples={}
for i in results:
    if not study_samples.has_key(i[3]+'\t'+i[2]+'\t'+i[5]):
        study_samples[i[3]+'\t'+i[2]+'\t'+i[5]]=[str(i[4])+'.'+str(i[1])]
    else:
        study_samples[i[3]+'\t'+i[2]+'\t'+i[5]].append(str(i[4])+'.'+str(i[1]))


fout=open('barcode_counts.txt','w')
for i in study_samples:
    for j in study_samples[i]:
        statement="select count(sample_name) from sff.split_library_read_map where sample_name='%s'" % str(j)
        con = data_access.getMetadataDatabaseConnection()
        cur = con.cursor()

        results = cur.execute(statement)
        for result in results:
            fout.write('%s\t%s\t%s\n' % (str(i),str(j),str(result[0])))

fout.close()
