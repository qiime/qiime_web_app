create or replace procedure get_barcode_statuses(
  statuses_ out types.ref_cursor
)as 
begin
  open statuses_ for 
  select status from barcode_status;

end get_barcode_statuses;



/*
variable results REFCURSOR;
execute get_barcode_statuses(:results);
print results;
*/