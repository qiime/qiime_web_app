
create or replace procedure get_distinct_column_values
(
  column_name in varchar,
  column_values in out types.ref_cursor
)
as
begin
    
  open column_values for
    'select distinct ' || column_name || ' from microbe_metadata order by ' || column_name;

end;

/*

variable column_values REFCURSOR;
execute get_distinct_column_values( 'study_name', :column_values );
print column_values;

variable column_values REFCURSOR;
execute get_distinct_column_values( 'host_age', :column_values );
print column_values;

*/