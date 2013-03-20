-- procedure to delete an entry to AG_SURVEY_ANSWER

create or replace procedure ag_delete_survey_answer
(
  ag_login_id_ raw,
  participant_name_ in varchar2
)
as
begin

  delete ag_survey_answer

  where ag_login_id = ag_login_id_ and participant_name = participant_name_;

  commit;
end;
