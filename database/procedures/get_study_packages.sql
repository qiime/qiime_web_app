create or replace procedure get_study_packages
(
  stdy_id in int,
  results in out types.ref_cursor
)
as
begin
  
  open results for
    select  env_package
    from    study_packages
    where   study_id = stdy_id;

end;

/*

variable results REFCURSOR;
execute get_study_packages(17, :results);
print results;


select * from study_packages
*/