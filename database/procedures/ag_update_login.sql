create or replace procedure ag_update_login
(
    ag_login_id_ raw,
    email_ varchar2, 
    name_ varchar2, 
    address_ varchar2, 
    city_ varchar2, 
    state_ varchar2, 
    zip_ varchar2, 
    country_ varchar2
)
as
begin

    update  ag_login
    set     email = email_,
            name = name_,
            address = address_,
            city = city_,
            state = state_,
            zip = zip_,
            country = country_
    where   ag_login_id = ag_login_id_;
  
    commit;

end;