create or replace procedure ag_get_barcodes_by_kit 
(
  supplied_kit_id_ in varchar2 
, results_  out types.ref_cursor
) as 
begin
  open results_ for 
    select b.barcode from ag_kit_barcodes b inner join ag_kit k on k.ag_kit_id =b.ag_kit_id 
      where k.supplied_kit_id = supplied_kit_id_;

end ag_get_barcodes_by_kit;

/*
variable barcodes REFCURSOR;
execute ag_get_barcodes_by_kit('test', :barcodes);
print barcodes;
*/