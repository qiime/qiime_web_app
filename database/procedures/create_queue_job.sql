create or replace
procedure create_queue_job
(
  user_id in qiime_queue.user_id%type, 
  job_id in out qiime_queue.job_id%type
)
as
begin

  insert into QIIME_QUEUE (JOB_ID, USER_ID, SUBMISSION_DATE, STATUS) 
  values (queue_sequence.nextval, user_id, sysdate, 'Submitted')
  returning JOB_ID into job_id;
  commit;

end;

/*

variable job_id NUMBER;
execute create_queue_job(1, :job_id );
print job_id; 

select * from qiime_queue;
delete from qiime_queue where job_id = job_id;

*/