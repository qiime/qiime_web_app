create or replace procedure get_column_ontologies
(
  col in varchar2,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  ontology_short_name
    from    column_ontology
    where   column_name = col;

end;

/*

variable results REFCURSOR;
execute get_column_ontologies('body_habitat', :results);
print results;

*/