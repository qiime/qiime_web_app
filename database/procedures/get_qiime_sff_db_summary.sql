
--------------------------------------------------------
--  DDL for Procedure GET_QIIME_SFF_DB_SUMMARY
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."GET_QIIME_SFF_DB_SUMMARY" 
(
  study_id_ in integer,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  *
    from    qiime_sff_db_summary qsds
    where   qsds.study_id = study_id_;
end get_qiime_sff_db_summary;


/*
variable results REFCURSOR;
execute get_qiime_sff_db_summary(77, :results);
print results;
*/