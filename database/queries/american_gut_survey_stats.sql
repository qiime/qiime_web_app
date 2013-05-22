select  ' General stats - Total surveys: ', count(*)
from    ag_human_survey
union
select  ' General stats - Total Kits: ', count(*)
from    ag_kit
union
select  ' General stats: Total barcodes: ', count(*)
from    ag_kit_barcodes
union
select  ' General stats - average age: ', avg((current_date - to_date(birth_date, 'MM/DD/YYYY')) / 365.0) as avg_age
from    ag_human_survey
where   birth_date is not null
union
select  ' General stats: Avg. height: ', avg(cast(height_in as integer))
from    ag_human_survey
where   height_in is not null
        and height_in > 30
union
select  'Diet type - Vegetarians:', count(diet_type)
from    ag_human_survey
where   diet_type = 'Vegetarian'
union
select  'Diet type - Vegetarian but eat seafood: ', count(diet_type)
from    ag_human_survey
where   diet_type = 'Vegetarian but eat seafood'
union
select  'Diet type - Omnivore but no red meat: ', count(diet_type)
from    ag_human_survey
where   diet_type = 'Omnivore but no red meat'
union
select  'Diet type - Omnivore: ', count(diet_type)
from    ag_human_survey
where   diet_type = 'Omnivore'
union
select  'Diet type - Vegan: ', count(diet_type)
from    ag_human_survey
where   diet_type = 'Vegan'
union
select  'Diet type - Did not answer: ', count(diet_type)
from    ag_human_survey
where   diet_type is null
union
select  'Gender - Female: ', count(*)
from    ag_human_survey
where   gender = 'Female'
union
select  'Gender - Male: ', count(*)
from    ag_human_survey
where   gender = 'Male'
union
select  'BMI - Underweight: ', count(*)
from    ag_human_survey
where   weight_lbs is not null
        and weight_lbs > 50
        and height_in is not null
        and height_in > 30
        and (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 < 18.5
union
select  'BMI - Normal: ', count(*)
from    ag_human_survey
where   weight_lbs is not null
        and weight_lbs > 50
        and height_in is not null
        and height_in > 30
        and (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 between 18.5 and 24.9
union
select  'BMI - Overweight: ', count(*)
from    ag_human_survey
where   weight_lbs is not null
        and weight_lbs > 50
        and height_in is not null
        and height_in > 30
        and (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 between 25 and 29.9
union
select  'BMI - Obesity: ', count(*)
from    ag_human_survey
where   weight_lbs is not null
        and weight_lbs > 50
        and height_in is not null
        and height_in > 30
        and (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 > 30
union
select  'Antibiotic - Did not answer: ', count(*)
from    ag_human_survey
where   antibiotic_select is null

union
select  'Antibiotic - In the past week: ', count(*)
from    ag_human_survey
where   antibiotic_select = 'In the past week'
union
select  'Antibiotic - In the past year: ', count(*)
from    ag_human_survey
where   antibiotic_select = 'In the past year'
union
select  'Antibiotic - Not in the last year: ', count(*)
from    ag_human_survey
where   antibiotic_select = 'Not in the last year'
union
select  'Antibiotic - In the past month: ', count(*)
from    ag_human_survey
where   antibiotic_select = 'In the past month'
union
select  'Antibiotic - In the past 6 months: ', count(*)
from    ag_human_survey
where   antibiotic_select = 'In the past 6 months'

;


select distinct antibiotic_select from ag_human_survey;





