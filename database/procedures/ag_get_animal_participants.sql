create or replace
procedure ag_get_animal_participants
(
    ag_login_id_ raw,
    results_ in out types.ref_cursor
)
as
begin

    open results_ for
        select  participant_name
        from    ag_animal_survey
        where   ag_login_id = ag_login_id_;

end;
