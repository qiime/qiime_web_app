create or replace procedure ag_check_barcode_status 
(
    barcode_ in varchar2,
    barcode_status_ OUT types.ref_cursor
)
as
begin

    open barcode_status_ for
        select  akb.site_sampled, akb.sample_date, akb.sample_time, akb.participant_name, 
                akb.environment_sampled, akb.notes, ak.kit_verified
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
        where   akb.barcode = barcode_;

end;

/* 

variable x REFCURSOR;
execute ag_check_barcode_status('000001056', :x);
print x;


select distinct kit_verified from ag_kit;
*/
 
 