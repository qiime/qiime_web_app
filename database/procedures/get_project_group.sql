create or replace procedure get_project_group 
(
  project_name in varchar2 ,
  group_name_ out types.ref_cursor
) as 
begin
open group_name_ for
select g.group_name from project_groups g inner join project p on g.group_id = p.group_id 
where p.project = project_name;
end get_project_group;


/*variable x REFCURSOR;
execute get_project_group('Handout Kits', :x);
print x;
*/