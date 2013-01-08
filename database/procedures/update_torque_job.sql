create or replace 
PROCEDURE "UPDATE_TORQUE_JOB" 
  (jobid IN NUMBER,
   new_state in VARCHAR2,
   notes in VARCHAR2) as
BEGIN
  --  UPDATE TORQUE_JOB
  --  SET JOB_STATE_ID = (SELECT JOB_STATE_ID
  --                     FROM TORQUE_JOB_STATE
  --                     WHERE JOB_STATE_NAME=new_state)
  --  WHERE JOB_ID=jobid;

  UPDATE TORQUE_JOB
  SET JOB_STATE_ID=(SELECT JOB_STATE_ID
                    FROM TORQUE_JOB_STATE
                    WHERE JOB_STATE_NAME=new_state),
      JOB_NOTES=notes
  WHERE JOB_ID=jobid;
  
  commit;
  
END update_torque_job;