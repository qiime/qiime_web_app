
--------------------------------------------------------
--  DDL for Procedure GET_NEW_TORQUE_JOBS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."GET_NEW_TORQUE_JOBS" (
  jobs_cursor OUT types.ref_cursor)AS 
BEGIN
  open jobs_cursor for
    SELECT tj.job_id, tjt.job_type_name, tj.job_arguments
    FROM TORQUE_JOB tj
    INNER JOIN TORQUE_JOB_STATE tjs 
    on tj.job_state_id = tjs.job_state_id
    INNER JOIN TORQUE_JOB_TYPE tjt 
    on tj.job_type_id = tjt.job_type_id
    WHERE tjs.job_state_name='NEW';
END GET_NEW_TORQUE_JOBS;