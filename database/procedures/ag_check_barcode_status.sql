create or replace procedure ag_check_barcode_status 
(
    barcode_ in varchar2,
    barcode_status_ OUT types.ref_cursor
)
as
begin

    open barcode_status_ for
        select  akb.site_sampled, akb.sample_date, akb.sample_time, akb.participant_name,
                akb.environment_sampled, akb.notes, ak.kit_verified, al.email, akb.moldy,
                akb.overloaded, akb.other, akb.other_text, akb.date_of_last_email,
                barcode.status, barcode.scan_date, barcode.sample_postmark_date, ahs.participant_email,
                al.name, ahs.consent
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
                inner join ag_login al
                on ak.ag_login_id = al.ag_login_id
                inner join barcode
                on akb.barcode = barcode.barcode
                left join ag_human_survey ahs
                on ak.ag_login_id = ahs.ag_login_id
        where   akb.barcode = barcode_;

end;

/* 

variable x REFCURSOR;
execute ag_check_barcode_status('000001056', :x);
print x;


select distinct kit_verified from ag_kit;
*/
 
 
