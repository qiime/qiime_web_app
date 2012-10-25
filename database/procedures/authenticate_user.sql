
create or replace procedure authenticate_user
(
  username in VARCHAR2,
  pwd in VARCHAR2,
  user_data in out types.ref_cursor
)
as
begin

  open user_data for
    select  web_app_user_id, email, password, is_admin, is_locked, last_login
    from    web_app_users
    where   email = username
            and password = pwd;

end;


/*

variable user_data REFCURSOR;
execute authenticate_user( 'test', 'test', :user_data );
print user_data;

*/