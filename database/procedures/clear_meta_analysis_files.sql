
--------------------------------------------------------
--  DDL for Procedure CLEAR_META_ANALYSIS_FILES
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."CLEAR_META_ANALYSIS_FILES" 
(
  meta_id IN NUMBER,
  fpath IN VARCHAR2
)
as 
begin
  delete from META_ANALYSIS_FILES 
  where meta_analysis_id=meta_id 
  and file_path=fpath;
  commit;

end clear_meta_analysis_files;
