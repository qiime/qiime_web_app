create or replace procedure update_barcode_status
(
    status_ varchar2,
    postmark_ varchar2,
    scan_date_ varchar2,
    barcode_ varchar2
)
as
begin

    update  barcode
    set     status = status_,
            sample_postmark_date = postmark_,
            scan_date = scan_date_
    where   barcode = barcode_;
    
    commit;

end;

/*

*/
