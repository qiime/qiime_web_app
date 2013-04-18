create or replace procedure ag_insert_bruce_wayne
(
    ag_login_id_ raw,
    participant_name_ varchar2
)
as
begin

  insert    into ag_bruce_waynes
            (ag_login_id, participant_name)
  values    (ag_login_id_, participant_name_);
  
  commit;

end;
