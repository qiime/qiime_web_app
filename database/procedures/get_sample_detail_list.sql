create or replace procedure get_sample_detail_list
(
  study_id_ in int,
  results in out types.ref_cursor
)
as
begin

  --delete from sample_name_plus_prep;

  --insert  into sample_name_plus_prep
  --        (sample_name, sample_name_plus_prep_id)
  --select  sa.sample_name, sa.sample_name || '.' || sp.sequence_prep_id
  --from    sample sa
  --        inner join sequence_prep sp
  --        on sa.sample_id = sp.sample_id
  --where   sa.study_id = sp.sample_id;

  open results for
    select  sa.sample_name || '.' || sp.sequence_prep_id as sample_plus_row_num, 
            sa.sample_id, sa."PUBLIC", sa.collection_date, sp.run_prefix, 
            sp.num_sequences, sp.num_otus, sp.otu_percent_hit
    from    sample sa
            left join sequence_prep sp
            on sa.sample_id = sp.sample_id
    where   sa.study_id = study_id_
    order by  sa.sample_name;

end;

/*

*/