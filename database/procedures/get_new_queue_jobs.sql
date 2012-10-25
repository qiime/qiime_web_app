create or replace procedure get_new_queue_jobs
(
  results in out types.ref_cursor
)
as
begin

  open results for
    select  job_id, user_id, submission_date
    from    qiime_queue
    where   status = 'new';

end;

/*

exec get_new_queue_jobs

*/