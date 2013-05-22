create or replace procedure ag_get_barcode_details
(
    barcode_ in varchar2,
    user_data_ out types.ref_cursor
)
as
begin

    open user_data_ for
        select  al.email, 
                cast(akb.ag_kit_barcode_id as varchar2(100)), 
                cast(akb.ag_kit_id as varchar2(100)), 
                akb.barcode, 
                akb.site_sampled, akb.environment_sampled, akb.sample_date, 
                akb.sample_time, akb.participant_name, akb.notes
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
                inner join ag_login al
                on ak.ag_login_id = al.ag_login_id
        where   akb.barcode = barcode_;

end;


/* 
variable user_data_ REFCURSOR;
execute ag_get_barcode_details('000001029', :user_data_);
print user_data_;
*/


 