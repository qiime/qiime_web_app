
create or replace procedure sample_insert
(
  stud_id in int,
  samp_name in varchar2
)
as
begin

  merge into "SAMPLE"
  using dual
  on (dual.dummy is not null and "SAMPLE".SAMPLE_NAME = samp_name)
  when not matched then insert (sample_id, study_id, sample_name) values (seq_sample.nextval, stud_id, samp_name);
  
  commit;

end;

/*

execute sample_insert(2, 'BF1.2');
select * from sample;
select * from study;

*/