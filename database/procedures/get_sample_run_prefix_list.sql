
--------------------------------------------------------
--  DDL for Procedure GET_SAMPLE_RUN_PREFIX_LIST
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_SAMPLE_RUN_PREFIX_LIST" 
(
  study_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select distinct s.sample_name,p.run_prefix
    from    "SAMPLE" s
    inner join SEQUENCE_PREP p on s.sample_id=p.sample_id
    inner join SFF.SFF_FILE sf on p.run_prefix=sf.sff_filename
    inner join SFF.SEQ_RUN_TO_SFF_FILE sr on sf.sff_file_id=sr.sff_file_id
    inner join SFF.ANALYSIS an on s.study_id=an.study_id and sr.seq_run_id=an.seq_run_id
    where   s.study_id = study_id_
    order by  sample_name;

end get_sample_run_prefix_list;


/* 
variable user_data REFCURSOR;
execute get_sample_run_prefix_list(289,:user_data);
print user_data
*/
