create or replace procedure ag_insert_login
(
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

  insert    into ag_login
            (email, name, address, city, state, zip, country)
  values    (email_, name_, address_, city_, state_, zip_, country_);
  
  commit;

end;