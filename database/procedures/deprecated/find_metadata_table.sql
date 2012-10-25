
create or replace procedure find_metadata_table
(
  col_name in varchar2,
  tab_name in out types.ref_cursor
)
as
begin

  open tab_name for
    select  table_name
    from    all_tab_columns
    where   column_name = upper(col_name)
            and owner = 'QIIME_TEST';

end;

/*

variable tab_name REFCURSOR;
execute find_metadata_table('COUNTRY', :tab_name);
print tab_name;

select column_name from all_tab_columns

*/
