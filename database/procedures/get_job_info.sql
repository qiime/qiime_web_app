
--------------------------------------------------------
--  DDL for Procedure GET_JOB_INFO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."GET_JOB_INFO" 
(
  study_id_ in integer,
  job_type_id_ in integer,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  tj.job_id, jt.job_type_name, tj.job_arguments, tj.user_id, 
            js.job_state_name, tj.job_notes,tj.job_type_id
    from    torque_job tj
            inner join torque_job_state js
            on tj.job_state_id = js.job_state_id
            inner join torque_job_type jt
            on tj.job_type_id = jt.job_type_id
    where   tj.study_id = study_id_ and tj.job_type_id=job_type_id_;

end;

/*

variable results REFCURSOR;
execute get_job_info(269, :results);
print results;

select * from torque_job

*/