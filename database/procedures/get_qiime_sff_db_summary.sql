create or replace 
PROCEDURE "GET_QIIME_SFF_DB_SUMMARY" 
(
  study_id_ in integer,
  results in out types.ref_cursor
)
as
begin

  open results for
    select st.study_id, st.project_name,st.study_title, st.study_abstract,st.pmid
    from    qiime_metadata.study st
    where   st.study_id = study_id_;
end get_qiime_sff_db_summary;


/*
variable results REFCURSOR;
execute get_qiime_sff_db_summary(77, :results);
print results;
*/