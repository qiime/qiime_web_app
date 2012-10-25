drop materialized view emp_statistics;

create materialized view emp_statistics
refresh complete start with (sysdate) next  (sysdate+60/1440) with rowid
as
    select  *
    from    (
                select  count(distinct reference_id) as otu_count
                from    study s
                        inner join sff.analysis a
                        on s.study_id = a.study_id
                        inner join sff.otu_table o
                        on a.otu_run_set_id = o.otu_run_set_id
                where   s.portal_type = 'emp'
            ),
            (
                select  sum(num_sequences) as num_sequences
                from    study s
                        inner join sample sa
                        on s.study_id = sa.study_id
                        inner join sequence_prep sp
                        on sa.sample_id = sp.sample_id
                where   s.portal_type = 'emp'
            ),
            (
                select  count(*) as collaborators
                from
                (
                    select  distinct trim(principal_investigator) as collaborator
                    from    study
                    where   trim(principal_investigator) is not null
                            and project_name not like '%test%'
                            and portal_type = 'emp'
                    union
                    select  distinct trim(lab_person)
                    from    study
                    where   trim(lab_person) is not null
                            and project_name not like '%test%'
                            and portal_type = 'emp'
                    order by collaborator
                )
            ),
            (
                select  count (distinct env_biome) as biom_count
                from    study s
                        inner join sample sa
                        on s.study_id = sa.study_id
                        inner join sequence_prep sp
                        on sa.sample_id = sp.sample_id
                        inner join sff.analysis an
                        on s.study_id = an.study_id
                where   s.portal_type = 'emp'
                        and env_biome is not null
            ),
            (
                select  count(*) as sample_count
                from    sample sa
                        inner join study s
                        on sa.study_id = s.study_id
                where   exists
                        (
                            select  1
                            from    sequence_prep sp
                            where   sa.sample_id = sp.sample_id
                                    and sp.num_sequences is not null
                        )
                        and s.portal_type = 'emp'
            );
    
    
/*

select * from emp_statistics;

*/