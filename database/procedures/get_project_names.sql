create or replace procedure get_project_names 
( proj_names_  in out types.ref_cursor
)as 
begin
  open proj_names_ for 
    select project from project;

end get_project_names;



/*variable proj_names_ REFCURSOR;
execute get_project_names(:proj_names_);
print proj_names_;
*/