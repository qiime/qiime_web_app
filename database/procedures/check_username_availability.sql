
--------------------------------------------------------
--  DDL for Procedure CHECK_USERNAME_AVAILABILITY
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."CHECK_USERNAME_AVAILABILITY" 
(
  username in VARCHAR2,
  user_data in out types.ref_cursor
)
as
begin

  open user_data for
    select  web_app_user_id, email, password, is_admin, is_locked, last_login
    from    web_app_user
    where   email = username;

end;


/*

variable user_data REFCURSOR;
execute check_username_availability( 'test@colorado.edu', :user_data );
print user_data;

*/