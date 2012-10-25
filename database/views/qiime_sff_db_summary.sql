
--------------------------------------------------------
--  DDL for View QIIME_SFF_DB_SUMMARY
--------------------------------------------------------

  CREATE OR REPLACE FORCE VIEW "SFF"."QIIME_SFF_DB_SUMMARY" ("STUDY_ID", "PROJECT_NAME", "STUDY_TITLE", "STUDY_ABSTRACT", "PMID", "SFF_FILENAME", "SEQ_RUN_ID", "NUMBER_OF_READS") AS 
  select mst.study_id, mst.project_name,mst.study_title, mst.study_abstract,mst.pmid,sf.sff_filename,an.seq_run_id,sf.number_of_reads
from  QIIME_METADATA.STUDY mst
left join analysis an on mst.study_id=an.study_id
left join seq_run_to_sff_file srsf on an.seq_run_id=srsf.seq_run_id
left join sff_file sf on srsf.sff_file_id=sf.sff_file_id;