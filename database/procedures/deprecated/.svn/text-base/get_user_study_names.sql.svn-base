
create or replace procedure get_user_study_names
(
  user_id in int,
  study_names in out types.ref_cursor
)
as
begin    

  open study_names for  
    select  s.study_id, s.project_name
    from    study s
            inner join user_study us
            on s.study_id = us.study_id
    where   us.web_app_user_id = user_id
    order by project_name;
    
end;


/*

variable study_names REFCURSOR;
execute get_user_study_names( 10020, :study_names );
print study_names;

*/
