-- procedure to insert a question-answer pair into AG_SURVEY_ANSWER

create or replace procedure ag_insert_survey_answer
(
  ag_login_id_ raw,
  participant_name_ in varchar2,
  question_ in varchar2,
  answer_ in varchar2
)
as
begin

  insert into ag_survey_answer
  (ag_login_id, participant_name, question, answer)

  values
  (ag_login_id_, participant_name_, question_, answer_);
  
  commit;

end;
