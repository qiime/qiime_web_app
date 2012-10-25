
create or replace procedure get_field_details
(
  field_name in varchar2,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  column_name, data_type, desc_or_value, definition 
    from    column_dictionary
    where   column_name = field_name;

end;

/*

variable results REFCURSOR;
execute get_field_details( 'sequencing_meth', :results );
print results;

*/