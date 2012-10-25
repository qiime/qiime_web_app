create or replace procedure study_packages_insert
(
  stud_id in int,
  env_pkg in int
)
as
begin
  
  insert into study_packages (study_id, env_package)
  values (stud_id, env_pkg);
  
  commit;

end;

/*

execute study_packages_insert(2, 4);

select * from study_packages;

delete from study_packages;
commit;

*/