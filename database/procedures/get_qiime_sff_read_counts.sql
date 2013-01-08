create or replace 
PROCEDURE "GET_QIIME_SFF_READ_COUNTS" 
(
  seq_run_id_id_ in integer,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  count(1)
    from    read_454 r4
    where   r4.seq_run_id = seq_run_id_id_;
end get_qiime_sff_read_counts;

/*
variable results REFCURSOR;
execute get_qiime_sff_read_counts(578, :results);
print results;
*/