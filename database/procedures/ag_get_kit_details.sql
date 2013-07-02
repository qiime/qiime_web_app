create or replace
procedure ag_get_kit_details
(
    supplied_kit_id_ IN varchar2,
    result_ OUT types.ref_cursor
)
as 
begin

    open result_ for
    select
        cast(ag_kit_id as varchar2(100)),
        supplied_kit_id,
        kit_password,
        swabs_per_kit,
        kit_verification_code,
        kit_verified,
        verification_email_sent
    from
        ag_kit
    where
        supplied_kit_id = supplied_kit_id_;

end;
