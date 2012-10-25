
create or replace procedure validate_ontology_value
(
  ontology_name in ontology.shortname%type,
  identifier_value in term."IDENTIFIER"%type,
  results out int
)
as
begin

  select  x.return_id into results
  from    (
            select  t.term_id as return_id
            from    ontology o
                    left join term t
                    on o.ontology_id = t.ontology_id
            where   o.shortname = ontology_name
                    and lower(t.term_name) = lower(identifier_value)
            union
            select  ts.term_id as return_id
            from    ontology o
                    left join term t
                    on o.ontology_id = t.ontology_id
                    left join term_synonym ts
                    on t.term_id = ts.term_id
            where   o.shortname = ontology_name
                    and lower(ts.synonym_value) = lower(identifier_value)
          ) x
  where   rownum = 1;

exception
  when no_data_found then
    results := 0;
end;

/*

set serveroutput on;
declare
  results int;
begin
  validate_ontology_value( 'ENVO', 'shrubland', results );
  dbms_output.put_line(results);
end;

set serveroutput on;
declare
  results int;
begin
  validate_ontology_value( 'FMA', 'Stool', results );
  dbms_output.put_line(results);
end;

*/
