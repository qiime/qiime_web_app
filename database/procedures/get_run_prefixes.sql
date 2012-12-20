create or replace 
procedure "GET_RUN_PREFIXES"
(
   study_id_ in NUMBER,
   results_ out types.ref_cursor
)

as
begin
  open results_ for
    select    distinct j.run_prefix
    from      qiime_metadata.sequence_prep j
              inner join qiime_metadata.sample sa
                on j.sample_id = sa.sample_id
    where sa.study_id = study_id_;

end;

/*
variable column_details REFCURSOR;
execute GET_RUN_PREFIXES( 1701, :column_details );
print column_details;
*/
