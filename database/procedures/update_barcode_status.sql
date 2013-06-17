create or replace procedure update_barcode_status
(
    status_ varchar2,
    barcode_ varchar2
)
as
begin

    update  barcode
    set     status = status_
    where   barcode = barcode_;

end;