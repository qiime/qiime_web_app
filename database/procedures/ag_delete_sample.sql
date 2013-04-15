create or replace procedure ag_delete_sample
(
    barcode_ varchar2,
    ag_login_id_ varchar2
)
as
begin

    -- Delete the associated samples
    update  ag_kit_barcodes
    set     participant_name = '',
            site_sampled = '',
            sample_time = '',
            sample_date = '',
            environment_sampled = ''
    where   barcode in
            (
                select  akb.barcode
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = ag_login_id_
                        and akb.barcode = barcode_
            );
                
    commit;

end;