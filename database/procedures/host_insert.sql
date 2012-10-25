create or replace procedure host_insert
(
  stud_id in int,
  samp_name in varchar2,
  host_subj_id in varchar2
)
as
  h_id int;
  samp_id int;
begin

  merge into host
  using dual
  on (dual.dummy is not null and host.host_subject_id = host_subj_id)
  when not matched then insert (host_id, host_subject_id) values (seq_host.nextval, host_subj_id);
  
  select  host_id into h_id
  from    host h
  where   host_subject_id = host_subj_id;
  
  select  sample_id into samp_id
  from    study st
          inner join "SAMPLE" sa
          on st.study_id = sa.study_id
  where   st.study_id = stud_id
          and sa.sample_name = samp_name;
  
  merge into host_sample
  using dual
  on (dual.dummy is not null and host_sample.host_id = h_id and host_sample.sample_id = samp_id)
  when not matched then insert (host_id, sample_id) values (h_id, samp_id);
  
  commit;
  
end;

/*

execute host_insert(2, 'F2M.2', 'F2');
select * from study;
select * from host;
select * from host_sample;

*/
