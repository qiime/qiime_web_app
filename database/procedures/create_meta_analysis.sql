
--------------------------------------------------------
--  DDL for Procedure CREATE_META_ANALYSIS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."CREATE_META_ANALYSIS" 
(
  user_id IN NUMBER,
  meta_ana_name IN VARCHAR2,
  meta_ana_id OUT NUMBER
)
as 
begin
  meta_ana_id:=seq_meta_analysis_id.nextval;
  INSERT INTO META_ANALYSIS(web_app_user_id,meta_analysis_id,meta_analysis_name)
  VALUES(user_id,meta_ana_id,meta_ana_name);
  COMMIT;
end create_meta_analysis;

/*
variable inv_id NUMBER:=0;
execute create_investigation(11272,'TEST',inv_id);
print inv_id;
*/