
--------------------------------------------------------
--  DDL for Procedure VERIFY_USER_ACTIVATION_CODE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."VERIFY_USER_ACTIVATION_CODE" 
(
  username in VARCHAR2,
  act_code in VARCHAR2,
  user_data in out types.ref_cursor
)
as
begin

  open user_data for
    select  web_app_user_id, email, password, is_admin, is_locked, last_login,activation_code,verified
    from    web_app_user
    where   email = username
            and activation_code = act_code;

end verify_user_activation_code;

/*

variable user_data REFCURSOR;
execute verify_user_activation_code( 'jesse.stombaugh@colorado.edu', '123456789', :user_data );
print user_data;

*/