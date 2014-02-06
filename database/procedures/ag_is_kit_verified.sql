create or replace procedure ag_is_kit_verified 
(
  kit_id_ in varchar2 
, results_ out types.ref_cursor
) as 
begin
  open results_ for 
    select kit_verified from ag_kit where supplied_kit_id = kit_id_;

  
end ag_is_kit_verified;


/*variable user_data_ REFCURSOR;
execute ag_is_kit_verified('test', :user_data_);
print user_data_;
*/