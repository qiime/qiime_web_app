reate or replace procedure ag_get_print_results(
   kit_id_  in varchar2,
   results_ in out types.ref_cursor
)as 
begin
  open results_ for 
  select print_results from ag_handout_kits 
  where kit_id = kit_id_;
end ag_get_print_results;


/*
variable user_data_ REFCURSOR;
execute ag_get_print_results('test_kit', :user_data_);
print user_data_;
*/