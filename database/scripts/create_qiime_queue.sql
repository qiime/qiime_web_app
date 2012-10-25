
create table qiime_queue
(
  job_id integer not null, 
  user_id integer not null,
  submission_date date not null,
  status varchar2(2000) not null,
  constraint pk_Qiime_Queue primary key (job_id)
);

