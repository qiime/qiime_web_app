create or replace procedure ag_get_next_barcode
(
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  cast(barcode as int) + 1 as next_barcode
        from    barcode
        where   length(barcode) = 9
                and barcode not like '9%'
                and rownum = 1
        order by barcode desc;

end;

/* 
variable user_data_ REFCURSOR;
execute ag_get_next_barcode(:user_data_);
print user_data_;
*/
 
 