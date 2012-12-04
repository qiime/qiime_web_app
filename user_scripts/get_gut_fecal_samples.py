from data_access_connections import data_access_factory
from enums import ServerConfig

statement="""select distinct 
"SAMPLE".sample_name||'.'||"SEQUENCE_PREP".sequence_prep_id as SampleID, 
"SAMPLE".sample_id,
"SEQUENCE_PREP".barcode, 
concat("SEQUENCE_PREP".linker, "SEQUENCE_PREP".primer) as LinkerPrimerSequence, 
"SAMPLE".study_id, 
"SEQUENCE_PREP".run_prefix as RUN_PREFIX, 
"STUDY"."STUDY_ALIAS", 
"SEQUENCE_PREP".experiment_title as Description 
 
        from "STUDY"  
    inner join "SAMPLE" 
    on "STUDY".study_id = "SAMPLE".study_id 
      inner join "SEQUENCE_PREP" 
    on "SAMPLE".sample_id = "SEQUENCE_PREP".sample_id 

  where ("STUDY".study_id = 460 or "STUDY".study_id = 451) 
  and ("SAMPLE"."ENV_MATTER"='ENVO:feces' or "SAMPLE"."ENV_MATTER"='ENVO:gut')"""

data_access = data_access_factory(ServerConfig.data_access_type)
con = data_access.getMetadataDatabaseConnection()
cur = con.cursor()

results = cur.execute(statement)
file_opened_here = False

output_fasta = open('/home/wwwuser/gut_fecaL_mouse_sample_seqs.fna', 'w')

for i in results:
    # Get our copy of data_access
    sample_id=i[1]
    study_id=i[4]
    seqs = data_access.getSequencesFromSample(study_id, sample_id)

    for seq in seqs:
      output_fasta.write('>%s\n%s\n' % (seq, seqs[seq]))
  

# Close the file if opened in this function
output_fasta.close()