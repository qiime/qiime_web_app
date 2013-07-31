create or replace procedure update_akb
(
    barcode_ varchar2,
    moldy_ char,
    overloaded_ char,
    other_ char,
    other_text_ varchar2,
    date_ varchar2
)
as
begin

    update  ag_kit_barcodes
    set     moldy = moldy_,
            overloaded = overloaded_,
            other = other_,
            other_text = other_text_,
            date_of_last_email = date_
    where   barcode = barcode_;
    commit;
end;
