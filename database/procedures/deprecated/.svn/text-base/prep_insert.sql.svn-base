create or replace procedure prep_insert
(
  stud_id in int,
  samp_name in varchar2
)
as
  samp_id int;
begin

  select  sample_id into samp_id
  from    "SAMPLE" sa
          inner join study st
          on sa.study_id = st.study_id
  where   sa.sample_name = samp_name
          and st.study_id = stud_id;

  merge into sequence_prep
  using dual
  on (dual.dummy is not null and sequence_prep.sample_id = samp_id)
  when not matched then insert (sequence_prep_id, sample_id) values (seq_prep.nextval, samp_id);
  
  commit;
  
end;

/*

execute prep_insert(2, 'F2M.2');
select * from sequence_prep;
select * from study;

*/
