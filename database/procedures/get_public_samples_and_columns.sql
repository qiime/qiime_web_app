
--------------------------------------------------------
--  DDL for Procedure GET_PUBLIC_SAMPLES_AND_COLUMNS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_PUBLIC_SAMPLES_AND_COLUMNS" 
(
  tab_name IN VARCHAR2,
  col_name IN VARCHAR2,
  study_ids IN VARCHAR2,
  user_data OUT types.ref_cursor
)as 
begin
  open user_data for
    'select distinct t.' || col_name || ' from ' || tab_name || ' t inner join "SAMPLE" s on t.sample_id=s.sample_id where s.study_id in ( ' || study_ids || ' )';
end get_public_samples_and_columns;

/*
variable user_data REFCURSOR;
execute get_public_samples_and_columns('STUDY','"PUBLIC"','77,89',:user_data);
print user_data;
*/