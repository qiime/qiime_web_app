
create or replace procedure get_ontology_list
(
  ontology_list in out types.ref_cursor,
  coL_name in varchar2
)
as
begin    
  open ontology_list for  
    select  oo.ontology_short_name
    from    column_ontology oo
    where   oo.column_name = col_name;
end;


/*

variable ontology_list REFCURSOR;
execute get_ontology_list( :ontology_list, 'body_habitat' );
print ontology_list;

*/
