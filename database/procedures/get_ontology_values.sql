
create or replace procedure get_ontology_values
(
  results in out types.ref_cursor,
  ontology_name in ontology.shortname%type
)
as
begin
  open results for
    select  t."IDENTIFIER"
    from    ontology o
            inner join term t
            on o.ontology_id = t.ontology_id
    where   o.shortname = ontology_name;
end;

/*

variable results REFCURSOR;
execute get_ontology_values( :results, 'FMA' );
print results;

*/
