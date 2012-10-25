
create or replace procedure get_package_columns
(
  pack_type_id in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  cd.column_name, sc.required, cd.data_type, cd.desc_or_value, cd.definition 
    from    column_dictionary cd
            inner join study_columns sc
            on cd.column_name = sc.column_name
    where   sc.package_type_id = pack_type_id;

end;

/*

variable results REFCURSOR;
execute get_package_columns( 1, :results );
print results;

*/