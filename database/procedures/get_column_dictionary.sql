create or replace procedure get_column_dictionary
(
  dictionary_values in out types.ref_cursor
)
as
begin    
  open dictionary_values for  
    select  cd.column_name, cd.desc_or_value, cd.definition, cd.data_type, atc.data_length
    from    column_dictionary cd
            left join all_tab_columns atc
            on upper(cd.column_name) = upper(atc.column_name)
              and atc.owner = 'QIIME_TEST'
    order by  column_name;
end;

/*

variable dictionary_values REFCURSOR;
execute get_column_dictionary( :dictionary_values );
print dictionary_values;

select * from all_tab_columns where owner = 'QIIME_TEST'

*/