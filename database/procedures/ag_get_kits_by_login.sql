create or replace procedure ag_get_kits_by_login
(
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  lower(al.email) as email, ak.supplied_kit_id, 
                cast(ak.ag_kit_id as varchar2(100)) as ag_kit_id
        from    ag_login al
                inner join ag_kit ak
                on al.ag_login_id = ak.ag_login_id
        order by lower(al.email), ak.supplied_kit_id;

end;

/* 
variable user_data_ REFCURSOR;
execute ag_get_kits_by_login(:user_data_);
print user_data_;
*/
 
 