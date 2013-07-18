create or replace
procedure ag_get_survey_details
(
    ag_login_id_ raw,
    participant_name_ varchar2,
    user_data_ OUT types.ref_cursor
)
as 
begin

    open user_data_ for
        select  cast(ag_login_id as varchar2(100)) as ag_login_id,
                participant_name, question, answer
        from    ag_survey_answer
        where   ag_login_id = ag_login_id_ and participant_name = participant_name_;

end;
