create or replace procedure ag_get_logins 
(
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  cast(ag_login_id as varchar2(100)) as ag_login_id, 
                lower(email), name
        from    ag_login
        order by lower(email);

end;

/* 
variable user_data_ REFCURSOR;
execute ag_get_logins(:user_data_);
print user_data_;
*/
 
 