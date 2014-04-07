create or replace procedure get_sequencing_statuses(
seq_statuses_ out types.ref_cursor
)as 

begin
  open seq_statuses_ for 
  select sequencing_status from BARCODE_SEQUENCING_STATUS;

end get_sequencing_statuses;

/*variable sequencing_statuses_ REFCURSOR;
execute get_sequencing_statuses(:sequencing_statuses_);
print sequencing_statuses_;
*/