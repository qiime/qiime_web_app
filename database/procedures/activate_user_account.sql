--------------------------------------------------------
--  DDL for Procedure ACTIVATE_USER_ACCOUNT
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."ACTIVATE_USER_ACCOUNT" 
(
  email_addy in varchar2
)
as
begin
  update web_app_user
  set verified='y'
  where email=email_addy;
  commit;
end activate_user_account;


/*

execute activate_user_account( 'jesse.stombaugh@colorado.edu');
select * from web_app_user where email = 'jesse.stombaugh@colorado.edu'

*/
