/*

insert into study_actual_columns(study_id, column_name, table_name) values (968, 'specific_body_site', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (968, 'hypertension', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (968, 'myocardinfarct', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (968, 'atherosclerosis', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (968, 'obesity', '"COMMON_EXTRA_SAMPLE"');

insert into study_actual_columns(study_id, column_name, table_name) values (969, 'specific_body_site', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (969, 'hypertension', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (969, 'myocardinfarct', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (969, 'atherosclerosis', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (969, 'obesity', '"COMMON_EXTRA_SAMPLE"');
insert into study_actual_columns(study_id, column_name, table_name) values (969, 'target_subfragment', '"SEQUENCE_PREP"');

commit;

select * from study_actual_columns where study_id  = 968 order by column_name;

select * from all_tab_columns where lower(column_name) = 'target_subfragment';
*/

merge into common_extra_sample c
using
(
   select   sa.sample_id,
            hav.body_site as body_site,
            'n' as hypertension,
            'n' as myocardinfarct,
            'n' as atherosclerosis,
            case 
                when body_mass_index is null then null
                when body_mass_index > 30 then 'y'
                else 'n'
            end as obesity
    from    sample sa
            inner join host_assoc_vertibrate hav
            on sa.sample_id = hav.sample_id
            inner join human_associated ha
            on sa.sample_id = ha.sample_id
    where   sa.study_id in (968, 969)
) x
on (c.sample_id = x.sample_id)
when matched then update
    set c.specific_body_site = x.body_site,
        c.hypertension = x.hypertension,
        c.myocardinfarct = x.myocardinfarct,
        c.atherosclerosis = x.atherosclerosis,
        c.obesity = x.obesity;

rollback;
commit;

/*

select  specific_body_site, hypertension, myocardinfarct,
        atherosclerosis, obesity
from    common_extra_sample c
        inner join sample s
        on c.sample_id = s.sample_id
where   s.study_id in (968, 969);

*/

--select count(*) from sample where study_id in (968, 969);




select distinct body_site from host_assoc_vertibrate
where sample_id in
        (
            select  sample_id
            from    sample
            where   study_id in 968
        ) order by body_site;



update  host_assoc_vertibrate
set     body_site = case                             
            when body_site in ('UBERON:buccal mucosa', 'UBERON:gingiva', 'UBERON:hard palate', 'UBERON:oral cavity', 'UBERON:saliva') then 'UBERON:mouth'
            when body_site = 'UBERON:mucosa of tongue' then 'UBERON:tongue'
            when body_site in ('UBERON:oropharynx', 'UBERON:palatine tonsil') then 'UBERON:oropharynx'
            else body_site
        end
where   sample_id in
        (
            select  sample_id
            from    sample
            where   study_id in 968
        );

commit;

update  host_assoc_vertibrate
set     body_site = case                             
            when body_site in ('UBERON:buccal mucosa', 'UBERON:gingiva', 'UBERON:gingival epithelium','UBERON:hard palate','UBERON:oral cavity') then 'UBERON:mouth'
            when body_site = 'UBERON:mucosa of tongue' then 'UBERON:tongue'
            when body_site in ('UBERON:palatine tonsil') then 'UBERON:oropharynx'
            else body_site
        end
where   sample_id in
        (
            select  sample_id
            from    sample
            where   study_id in 969
        );

rollback;
commit;


merge into sequence_prep sp
using
(
    select  sample_id
    from    sample
    where   study_id = 969
) x
on (sp.sample_id = x.sample_id)
when matched then update
    set target_subfragment = 'v35';


select  count(*) 
from    sample sa
        inner join sequence_prep sp
        on sa.sample_id = sp.sample_id
where   sa.study_id = 969;

rollback;
commit;


-- HMP v13: 968
-- HMP v35: 969

/*
v13
if body_site: = UBERON:buccal mucosa, UBERON:gingiva, UBERON:hard palate, UBERON:oral cavity, UBERON:saliva change to= UBERON:mouth (i.e. these body_sites should now =UBERON:mouth)
if UBERON:mucosa of tongue change to =UBERON:tongue
if UBERON:oropharynx, UBERON:palatine tonsil change to=UBERON:oropharynx

v35
if body_site: = UBERON:buccal mucosa, UBERON:gingiva, UBERON:gingival epithelium, UBERON:hard palate, UBERON:oral cavity change to = UBERON:mouth (i.e. these body_sites should now =UBERON:mouth)
if UBERON:mucosa of tongue change to =UBERON:tongue
if UBERON:oropharynx, UBERON:palatine tonsil change to =UBERON:oropharynx


ALL IN COMMON EXTRA SAMPLE
For all samples, new metadata columns:
hypertension=n; 
myocardinfarct=n; 
atherosclerosis=n;
obesity=y if body_mass_index is 30 or greater, =n if body_mass_index is 29.9 or less, =unknown if no body_mass_index
*/