
create or replace procedure get_ontology_list
(
  ontology_list in out types.ref_cursor,
  sname varchar2
)
as
begin    
  open ontology_list for  
    select  ontology_id, fullname, definition
    from    ontology
    where   shortname = sname;
end;

/*

variable ontology_list REFCURSOR;
execute get_ontology_list( :ontology_list, 'FMA' );
print ontology_list;

*/
