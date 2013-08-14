/*

select * from host_sample;
select * from host_ids;
select * from sample_ids;

select count(*) from sample;
114943
select count(*) from sequence_prep;
118675

select  sample_id
from    sample
where   sample_name = 'N00235'
        and study_id = 1939;


select * from all_constraints
where constraint_name = 'FK_HOST_SAMPLE_HOST';


select  sa.*
from    sample sa
        inner join sequence_prep sp
        on sa.sample_id = sp.sample_id
where   sp.run_prefix in
        (
            'A0U2P.1.Solexa-95395', 
            'A1UEN.1.Solexa-133787', 
            'A2NWB.1.Solexa-136286', 
            'A4848.1.Solexa-162418', 
            'A29H0.1.Solexa-149432'
        );
*/

declare
    sample_name_ varchar2(100);
    study_id_ int;
begin
    sample_name_ := '845.1B';
    study_id_ := 1939;
    
    insert  into sample_ids (sample_id)
    select  sample_id
    from    sample
    where   sample_name = sample_name_
            and study_id = study_id_;
    
    insert  into host_ids (host_id)
    select  h.host_id
    from    host h
            inner join host_sample hs
            on h.host_id = hs.host_id
    where   hs.sample_id in
            (
                select  sample_id
                from    sample_ids
            );
    
    delete  from host_assoc_vertibrate
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
            
    delete  from host_sample hs
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
            
    delete  from host_sample hs
    where   host_id in
            (
                select  host_id
                from    host_ids
            );
    
    delete  from human_associated
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
            
    delete  from host
    where   host_id in
            (
                select  host_id
                from    host_ids
            );
            
    delete  from common_extra_sample
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
            
    delete  from common_extra_sample_2
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
    
    delete  from sequence_prep
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
    
    delete  from extra_sample_1998
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
    
    delete  from sample
    where   sample_id in 
            (
                select  sample_id
                from    sample_ids
            );
        
end;

--rollback;
--commit;