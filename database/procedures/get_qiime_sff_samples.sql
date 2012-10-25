
--------------------------------------------------------
--  DDL for Procedure GET_QIIME_SFF_SAMPLES
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."GET_QIIME_SFF_SAMPLES" 
(
  study_id_ in integer,
  seq_run_id_ in integer,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  distinct slrm.sample_name
    from    split_library_read_map slrm
    inner join analysis an on slrm.split_library_run_id=an.split_library_run_id
    where   slrm.seq_run_id = seq_run_id_ and an.study_id=study_id_;
    
end get_qiime_sff_samples;

/*
variable results REFCURSOR;
execute get_qiime_sff_samples(380,578, :results);
print results;
*/
