create or replace procedure ag_check_barcode_status 
(
    barcode_ in varchar2,
    barcode_status_ OUT types.ref_cursor
)
as
begin

    open barcode_status_ for
        select  site_sampled, sample_date, sample_time, participant_name, 
                environment_sampled, notes 
        from    ag_kit_barcodes
        where   barcode = barcode_
                and sample_date is not null
                and sample_time is not null;

end;

/* 
variable x REFCURSOR;
execute ag_check_barcode_status('', :user_data_);
print x;
*/
 
 