create or replace
procedure get_metadata_by_study_list
(
  column_name in varchar,
  value_list in varchar,
  column_values in out types.ref_cursor
)
as
begin    
  open column_values for  
    'select distinct ' || column_name || ' from microbe_metadata where study_name in ( ' || value_list || ' )';

end;

/*

variable column_values REFCURSOR;
execute get_metadata_by_study_list( 'host_age', '''DOG'',''GUT''', :column_values );
print column_values;

*/
