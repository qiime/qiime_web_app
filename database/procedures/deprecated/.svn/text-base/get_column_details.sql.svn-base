
create or replace procedure get_column_details
(
  column_details in out types.ref_cursor,
  col_name in varchar2
)
as
begin    
  open column_details for  
    select  data_type
    from    column_dictionary 
    where   column_name = col_name;
end;


/*

variable column_details REFCURSOR;
execute get_column_details( :column_details, 'drug_usage' );
print column_details;

*/
