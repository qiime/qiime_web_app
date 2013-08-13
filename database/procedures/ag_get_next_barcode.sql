create or replace procedure ag_get_next_barcode
(
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  next_barcode
        from    (
                    select  max(cast(barcode as int)) + 1 as next_barcode
                    from    barcode
                    where   length(barcode) = 9
                            and barcode not like '9%'
                    union
                    select  min(cast(be.barcode as int)) as next_barcode
                    from    barcode_exceptions be
                            left join barcode b
                            on be.barcode = b.barcode
                    where   b.barcode is null
                )
        where   rownum = 1
        order by next_barcode;

end;

/* 
variable user_data_ REFCURSOR;
execute ag_get_next_barcode(:user_data_);
print user_data_;
*/
 
 