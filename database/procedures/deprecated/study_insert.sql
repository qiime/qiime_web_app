create or replace procedure study_insert
(
  user_id in int,
  study_name in varchar2,
  investigation_type in int,
  study_completion_status in int,
  submit in varchar2,
  stdy_id in out int
)
as
begin
  
  insert into study (study_id, project_name, investigation_type, study_complt_stat, submit_to_insdc)
  values (seq_study.nextval, study_name, investigation_type, study_completion_status, submit)
  returning study_id into stdy_id;
  
  insert into user_study (web_app_user_id, study_id)
  values (user_id, stdy_id);
  
  commit;

end;

/*

variable stdy_id NUMBER;
execute study_insert(1, 'test_study_2', 'eukaryote', 'human-gut', 'complete', 'y', 'n', :stdy_id);
print std_id;

select * from user_study;
select * from study;

delete from user_study;
delete from study;
commit;
*/