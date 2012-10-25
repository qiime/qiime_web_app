
create or replace procedure get_ontology_terms
(
 ontology_value in varchar,
 query_string in varchar,
 column_values in out types.ref_cursor
)
as
  stmt varchar(5000);
begin

  -- Yeah, this is strange... but here's the deal: The results_temp temp
  -- table has the wonderful property of clearing itself on commit. However,
  -- if the commit is issued at the end of the statement, (logical!) no rows
  -- are returned to the caller. So I put the commit call here which essentially
  -- tells Oracle: "delete from results_temp". 
  commit;

  -- Exact matches in Term
  stmt := 
    'insert into results_temp (term_id, term_name, sort_order)
     select term_id, o.shortname || '':'' || term_name, term_sort_order.nextval
     from   term t
            inner join ontology o
            on t.ontology_id = o.ontology_id
     where  o.shortname in ('|| ontology_value ||')
            and trim(upper(term_name)) = '''|| query_string ||'''';
  execute immediate stmt;

  -- Exact matches in Synonym
  stmt := 
    'insert into results_temp (term_id, term_name, sort_order)
     select synonym_id, o.shortname || '':'' || synonym_value, term_sort_order.nextval
     from   term_synonym ts
            inner join term t
            on ts.term_id = t.term_id
            inner join ontology o
            on t.ontology_id = o.ontology_id
     where  o.shortname in ('|| ontology_value ||')
            and trim(upper(synonym_value)) = '''|| query_string ||'''';
  execute immediate stmt;
  
  -- Close term matches
  stmt := 
    'insert into results_temp (term_id, term_name, sort_order)
     select term_id, o.shortname || '':'' || term_name, term_sort_order.nextval
     from   term t
            inner join ontology o
            on t.ontology_id = o.ontology_id
     where  o.shortname in (' || ontology_value || ')
            and trim(upper(term_name)) like ''%' || query_string || '%''
            and rownum <= 20
            and t.term_id not in
            (
              select  term_id
              from    results_temp
            )';
  execute immediate stmt;
  
  -- Close synonym matches
  stmt := 
    'insert into results_temp (term_id, term_name, sort_order)
     select synonym_id, o.shortname || '':'' || synonym_value, term_sort_order.nextval
     from   term_synonym ts
            inner join term t
            on ts.term_id = t.term_id
            inner join ontology o
            on t.ontology_id = o.ontology_id
     where  o.shortname in ('|| ontology_value ||')
            and trim(upper(synonym_value)) like ''%' || query_string || '%''
            and rownum <= 20
            and ts.synonym_id not in
            (
              select  term_id
              from    results_temp
            )';
  execute immediate stmt;
  
  open column_values for
    select  term_id, term_name 
    from    results_temp
    where   rownum <= 50
    order by sort_order asc;

end get_ontology_terms;

/*

variable column_values REFCURSOR;
execute get_ontology_terms('''OBI''','COLCHI', :column_values);
print column_values;



select * from term_synonym where synonym_value like '%' || 'external return' || '%';
select * from term where term_id=210538359;

select * from term where ontology_id=761363151 and term_name like '%' || 'RNA' || '%';

*/