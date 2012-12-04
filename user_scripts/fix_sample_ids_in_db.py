from data_access_connections import data_access_factory
from enums import ServerConfig
data_access = data_access_factory(ServerConfig.data_access_type)


fopen=open('ltsp_old_ids.txt','U').readlines()

old_sample_ids={}
for i in fopen:
	sample_name='.'.join(i.split('.')[:-1])
	old_id=i.split('.')[-1]
	if sample_name not in old_sample_ids:
		old_sample_ids[sample_name]=old_id
	else:
		print sample_name

study_id=1037
for sample_name in old_sample_ids:
    statement = "update sequence_prep set sequence_prep_id=%s where sequence_prep_id=(select sp.sequence_prep_id from sample s inner join sequence_prep sp on s.sample_id=sp.sample_id where s.sample_name=\'%s\' and study_id=%s)" % (str(old_sample_ids[sample_name]),sample_name,str(study_id))
    
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    #results = cur.execute(statement)
    #results = cur.execute('commit')
    print statement
    