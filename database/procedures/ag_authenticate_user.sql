create or replace procedure ag_authenticate_user
(
  ag_kit_id_ in varchar2,
  kit_password_ in varchar2,
  user_data in out types.ref_cursor
)
as
begin

  open user_data for
    select  cast(agl.ag_login_id as varchar2(100)) as ag_login_id, 
            agl.email, agl.name, agl.address, agl.city,
            agl.state, agl.zip, agl.country
    from    ag_login agl
            inner join ag_kit agk
            on agl.ag_login_id = agk.ag_login_id
    where   agk.supplied_kit_id = ag_kit_id_
            and agk.kit_password = kit_password_;

end;

/*

variable user_data REFCURSOR;
execute ag_authenticate_user('DctkP', 'z077$Wcz', :user_data);
print user_data;


select * from ag_kit;

*/