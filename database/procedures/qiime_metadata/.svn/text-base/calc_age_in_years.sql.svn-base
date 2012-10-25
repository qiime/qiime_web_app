
create or replace procedure calc_age_in_years
(
    study_id_ in int
)
as
    age_in_years_exists_ int;
begin

    -- Add the value to study_actual_columns if column exists
    select  count(*) into age_in_years_exists_
    from    host_sample hs
            inner join sample sa
            on hs.sample_id = sa.sample_id
    where   sa.study_id = study_id_
            and hs.age_in_years is not null;
    
    if age_in_years_exists_ > 0 then
        update
        (
            select  cvv.term, hs.age, hs.age_in_years
            from    host_sample hs
                    right join sample s
                    on hs.sample_id = s.sample_id
                    inner join controlled_vocab_values cvv
                    on hs.age_unit = cvv.vocab_value_id
                        and cvv.controlled_vocab_id = 20
            where   s.study_id = study_id_
        ) x
        set x.age_in_years = 
        case x.term
            when 'seconds' then x.age / 31536000
            when 'minutes' then x.age / 525600
            when 'hours' then x.age / 8760
            when 'days' then x.age / 365
            when 'weeks' then x.age / 52
            when 'months' then x.age / 12
            when 'years' then x.age
            else null
        end;
        
        -- Add the value to study_actual_columns if column exists 
        insert into study_actual_columns (study_id, column_name, table_name) 
        values (study_id_, 'age_in_years', '"HOST_SAMPLE"'); 
        
        commit;
    end if;
    
end;

/*

execute calc_age_in_years (377);

select  hs.age, hs.age_unit, cvv.term, hs.age_in_years
from    host_sample hs
        inner join sample s
        on hs.sample_id = s.sample_id
        inner join controlled_vocab_values cvv
        on hs.age_unit = cvv.vocab_value_id
where   s.study_id = 377;


*/