create or replace procedure ag_set_pass_change_code 
(
  email_ in varchar2, 
  kit_id_ in varchar2,  
  pass_code_ in varchar2
) as 
 
begin
  update ag_kit set pass_reset_code = pass_code_, pass_reset_time = systimestamp + interval '2' hour where
     supplied_kit_id = kit_id_ and ag_login_id in (select ag_login_id from ag_login where email = email_);
  commit;
end ag_set_pass_change_code;


/*
execute ag_set_pass_change_code('test@microbio.me','test', '123456789');
*/