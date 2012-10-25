
--------------------------------------------------------
--  DDL for Procedure ADD_META_ANALYSIS_FILES
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."ADD_META_ANALYSIS_FILES" 
(
  meta_ana_id IN NUMBER,
  fpath IN VARCHAR2,
  meta_type IN VARCHAR2,
  run_date IN VARCHAR2,
  ftype IN VARCHAR2
)
is
 meta_type_id NUMBER;
l_run_date TIMESTAMP;
 
begin
    l_run_date:=TO_TIMESTAMP(run_date, 'DD/MM/YYYY/HH24/MI/SS');
    select meta_analysis_type_id into meta_type_id from meta_analysis_type
    where meta_analysis_type=meta_type;
    
    INSERT INTO META_ANALYSIS_FILES(meta_analysis_id,file_path,meta_analysis_type_id,processing_date,file_type)
    VALUES(meta_ana_id,fpath,meta_type_id,l_run_date,ftype);
    commit;

end add_meta_analysis_files;