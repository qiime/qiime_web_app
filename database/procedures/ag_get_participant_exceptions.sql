create or replace
procedure ag_get_participant_exceptions
(
    ag_login_id_ raw,
    results_ in out types.ref_cursor
)
as
begin

    open results_ for
        select  participant_name
        from    ag_bruce_waynes
        where   ag_login_id = ag_login_id_;

end;

