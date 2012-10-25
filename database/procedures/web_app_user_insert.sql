
--------------------------------------------------------
--  DDL for Procedure WEB_APP_USER_INSERT
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."WEB_APP_USER_INSERT" 
(
  email_addy in varchar2,
  pwd in varchar2,
  act_code in varchar2
)
as
  next_web_app_user_id int;
begin

  select  max(web_app_user_id) + 1 into next_web_app_user_id
  from    web_app_user;

  merge into web_app_user
  using dual
  on (dual.dummy is not null and web_app_user.email = email_addy)
  when not matched then 
    insert (web_app_user_id, email, password, is_admin, is_locked, max_cpu_time, actual_cpu_time, 
      actual_num_login, last_login, ip_address, last_web_app_id, max_jobs, is_pending, pending_conf_id, activation_code, verified) 
    values (next_web_app_user_id, email_addy, pwd, 0, 0, 172800, 0, 
      0, '1-JAN-00 01.00.00.00 AM', '0.0.0.0', 1, 20, 0, 161912986, act_code, 'n')
  when matched then
    update
    set     password = pwd
    where   email = email_addy;
  commit;
  
end;

/*

execute web_app_user_insert('test_emp', 'test_emp','123456789');
select * from web_app_user where email = 'test_emp';

*/