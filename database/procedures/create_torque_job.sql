create or replace 
PROCEDURE "CREATE_TORQUE_JOB" 
(
  job_type_ IN varchar2,
  job_input_ IN varchar2,
  user_id_ IN integer,
  study_id_ in integer,
  job_state_id_ in integer,
  job_id_ in out integer
) 
AS
BEGIN
  -- job state id 0 means 'NEW'
  INSERT  INTO TORQUE_JOB (job_id, job_type_id, job_arguments, user_id, study_id,job_state_id)
  VALUES  (TORQUE_JOB_ID_SEQ.nextval,
          (SELECT job_type_id 
           FROM torque_job_type 
           WHERE job_type_name = job_type_),
          job_input_, 
          user_id_,
          study_id_,
          job_state_id_)
    returning job_id into job_id_;
          
  commit;
  
END CREATE_TORQUE_JOB;