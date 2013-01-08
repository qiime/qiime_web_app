create or replace 
PROCEDURE "CLEAR_TORQUE_JOB" 
(
  job_id_ in int
)
as
begin

  delete  torque_job
  where   job_id = job_id_;
  
  commit;

end;

/*

execute clear_torque_job(52);
select * from torque_job where study_id = 269

*/