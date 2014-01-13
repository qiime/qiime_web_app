select A.study_id from
(select study_id, count(*) as num_successful from torque_job where job_type_id = 3 and job_state_id = 3 group by study_id) A
join (select study_id, count(*) as num_expected from torque_job where job_type_id = 3 group by study_id) B on A.study_id = B.study_id and A.num_successful = B.num_expected;
