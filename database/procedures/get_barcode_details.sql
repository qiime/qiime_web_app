create or replace procedure get_barcode_details 
(
  barcode_ in varchar2 
, results_ out types.ref_cursor
) as 
begin
  open results_ for
  select create_date_time, status, scan_date, sample_postmark_date, biomass_remaining, sequencing_status, obsolete
  from barcode
  where barcode = barcode_;
end get_barcode_details;


/* 
variable user_data_ REFCURSOR;
execute get_barcode_details('000001029', :user_data_);
print user_data_;
*/