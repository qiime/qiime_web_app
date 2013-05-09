create or replace procedure ag_get_next_barcode
(
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  cast(barcode as int) + 1 as next_barcode
        from    (
                    select  barcode
                    from    ag_kit_barcodes
                    where   length(barcode) = 9
                            and barcode not in ('000009999', '000008888')
                            and barcode not like '9%'
                    union
                    select  barcode
                    from    ag_handout_kits
                    where   length(barcode) = 9
                            and barcode not in ('000009999', '000008888')
                            and barcode not like '9%'
                    order by barcode desc
                )
        where   rownum = 1;

end;

/* 
variable user_data_ REFCURSOR;
execute ag_get_next_barcode(:user_data_);
print user_data_;
*/
 
 