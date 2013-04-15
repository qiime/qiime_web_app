create or replace procedure ag_get_barcodes
(
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  barcode
        from    ag_kit_barcodes
        order by barcode;

end;

/* 
variable user_data_ REFCURSOR;
execute ag_get_barcodes(:user_data_);
print user_data_;
*/
 
 