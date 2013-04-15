create or replace procedure ag_available_barcodes
(
    ag_login_id_ raw,
    results_ in out types.ref_cursor
)
as
begin

    open results_ for
        select  akb.barcode 
        from    ag_kit_barcodes akb 
                inner join ag_kit ak 
                on akb.ag_kit_id = ak.ag_kit_id 
        where   ak.ag_login_id = ag_login_id_
                and ak.kit_verified = 'y'
                and akb.sample_date is null;

end;
