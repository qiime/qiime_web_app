/*
This query pulls list of studies which are entirely non-environmental,
have been processed, and contain at least 50 samples per study. For 
clarity, the list of environmental and non-environmental study types
are listed below. This query pulls studies that do not contain any reference
to any environmental study type.

NON-ENVIRONMENTAL (HOST) STUDY TYPES

host-associated
human-associated
human-skin
human-oral
human-gut
human-vaginal
human-amniotic-fluid
human-urine
human-blood
plant-associated


ENVIRONMENTAL STUDY TYPES

air
microbial mat/biofilm
miscellaneous natural or artificial environment
sediment
soil
wastewater/sludge
water
*/

select study_id, project_name
from study
where study_id in
(
    select sa.study_id
    from sample sa
    -- Make sure it's been processed
    where exists
    (
        select 1
        from sff.analysis a
        where sa.study_id = a.study_id
    )
    -- Make sure it's not environmental
    and not exists
    (
        select 1
        from study_packages sp
        where sp.study_id = sa.study_id
        and sp.env_package in (1, 2, 11, 12, 13, 14, 15, 16, 17)
    )
    group by sa.study_id
    -- 50 more more samples per study
    having count(sa.study_id) >= 50
)
-- No test studies
and project_name not like '%test%'
order by project_name;

/*
--QUERIES FOR REFERENCE

select * from controlled_vocab_values where controlled_vocab_id = 1;
*/
