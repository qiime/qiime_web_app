create or replace procedure ag_get_barcodes_by_login
(
    ag_login_id_ in raw,
    user_data_ out types.ref_cursor
)
as
begin

    open user_data_ for
        select  al.email, akb.ag_kit_barcode_id, akb.ag_kit_id, akb.barcode, 
                akb.site_sampled, akb.environment_sampled, akb.sample_date, 
                akb.sample_time, akb.participant_name, akb.notes
        from    ag_kit_barcodes akb
                inner join ag_kit ak
                on akb.ag_kit_id = ak.ag_kit_id
                inner join ag_login al
                on ak.ag_login_id = al.ag_login_id
        where   ak.ag_login_id = ag_login_id_;

end;


/* 
variable user_data_ REFCURSOR;
execute ag_get_barcodes_by_login('DB35DFE3F86250E6E0408A800C5D7309', :user_data_);
print user_data_;
*/


 