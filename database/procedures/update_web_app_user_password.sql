
--------------------------------------------------------
--  DDL for Procedure UPDATE_WEB_APP_USER_PASSWORD
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."UPDATE_WEB_APP_USER_PASSWORD" (
  email_addy in varchar2,
  pwd in varchar2
)
as
begin
  update web_app_user
  set password=pwd,verified='y',activation_code=''
  where email=email_addy;
  commit;
end update_web_app_user_password;

/*

execute update_web_app_user_password( 'test@colorado.edu','testing2');

*/
