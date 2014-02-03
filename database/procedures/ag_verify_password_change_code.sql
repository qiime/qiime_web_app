create or replace procedure ag_verify_password_change_code
(
   email_ in varchar,
   kitid_ in varchar,
   pass_code_ in varchar,
   results_  out types.ref_cursor
)
as

   
   current_time_ timestamp(6) := systimestamp;
   
   
begin
open results_ for
select
case
    when (current_time_ < k.PASS_RESET_TIME)
   --when(current_time_ between (k.PASS_RESET_TIME - interval '2' hour) and k.PASS_RESET_TIME)
    then 1
  else 0
end 
from ag_kit k inner join ag_login l on l.AG_LOGIN_ID = k.AG_LOGIN_ID
        where k.PASS_RESET_CODE = pass_code_ and l.EMAIL = email_  and k.SUPPLIED_KIT_ID = kitid_;


end ag_verify_password_change_code;
 
/*

variable isgood number;
execute ag_verify_password_change_code('test@microbio.me', 'test', '123456789', :isgood);
print isgood;
*/