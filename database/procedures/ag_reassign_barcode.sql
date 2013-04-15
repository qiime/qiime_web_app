create or replace procedure ag_reassign_barcode
(
    ag_kit_id_ raw,
    barcode_ varchar2
)
as 
begin

    update  ag_kit_barcodes
    set     ag_kit_id = ag_kit_id_
    where   barcode = barcode_;
    
    commit;

end;
