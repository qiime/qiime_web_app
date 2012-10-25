--------------------------------------------------------
--  DDL for Procedure CHECK_IF_STUDY_ID_EXISTS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."CHECK_IF_STUDY_ID_EXISTS" 
(
  metadata_study_id IN NUMBER,
  study_id_cnt OUT NUMBER
)
as 
begin
    SELECT count(1) INTO study_id_cnt FROM ANALYSIS
    WHERE study_id=metadata_study_id;
  
end check_if_study_id_exists;


/*
variable study_id_cnt NUMBER;
execute check_if_study_id_exists(1,:study_id_cnt);
print study_id_cnt
*/
