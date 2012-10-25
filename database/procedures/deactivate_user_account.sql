
--------------------------------------------------------
--  DDL for Procedure DEACTIVATE_USER_ACCOUNT
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."DEACTIVATE_USER_ACCOUNT" 
(
  email_addy in varchar2,
  act_code in varchar2
)
as
begin
  update web_app_user
  set verified='n',activation_code=act_code
  where email=email_addy;
  commit;
end deactivate_user_account;


/*

execute deactivate_user_account( 'test@colorado.edu','testing2');
select * from web_app_user where email = 'test@colorado.edu'

*/