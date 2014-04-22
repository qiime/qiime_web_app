-- Run the metadata pulldown for a single barcode
create or replace
procedure ag_get_barcode_metadata
(
    barcode_ IN varchar2,
    user_data_ OUT types.ref_cursor
)
as 
begin

open user_data_ for
select akb.barcode as sample_name,
        akb.barcode as ANONYMIZED_NAME, 
        akb.sample_date as collection_date, 
        'y' as "public",
        0 as depth,
        'American Gut Project ' || akb.site_sampled || ' sample' as DESCRIPTION,
        akb.sample_time, 
        0 as altitude, 
        'y' as assigned_from_geo,
        'American Gut Project' as TITLE,
        case akb.site_sampled
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as site_sampled,
        
        ora_hash(ora_hash(cast(ahs.ag_login_id as varchar2(100)) || ahs.participant_name)) as host_subject_id,         
        
        case akb.site_sampled
            when 'Stool' then '408170'
            when 'Mouth' then '447426'
            when 'Right hand' then '539655'
            when 'Left hand' then '539655'
            when 'Forehead' then '539655'
            when 'Nares' then '1115523'
            when 'Hair' then '646099'
            when 'Tears' then '646099'
            when 'Ear wax' then '646099'
            when 'Vaginal mucus' then '646099'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as TAXON_ID,
        '9606' host_taxid,
        case akb.site_sampled
            when 'Stool' then 'human gut metagenome'
            when 'Mouth' then 'human oral metagenome'
            when 'Right hand' then 'human skin metagenome'
            when 'Left hand' then 'human skin metagenome'
            when 'Forehead' then 'human skin metagenome'
            when 'Nares' then 'upper respiratory tract metagenome'
            when 'Hair' then 'human metagenome'
            when 'Tears' then 'human metagenome'
            when 'Ear wax' then 'human metagenome'
            when 'Vaginal mucus' then 'human metagenome'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as common_name,        
        'human' as host_common_name,
        case akb.site_sampled
            when 'Stool' then 'UBERON:feces'
            when 'Mouth' then 'UBERON:oral cavity'
            when 'Right hand' then 'UBERON:skin'
            when 'Left hand' then 'UBERON:skin'
            when 'Forehead' then 'UBERON:skin'
            when 'Nares' then 'UBERON:nose'
            when 'Hair' then 'UBERON:hair'
            when 'Tears' then 'UBERON:eye'
            when 'Ear wax' then 'UBERON:ear'
            when 'Vaginal mucus' then 'UBERON:vagina'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as body_habitat, 
        case akb.site_sampled
            when 'Stool' then 'UBERON:feces'
            when 'Mouth' then 'UBERON:tongue'
            when 'Right hand' then 'UBERON:hand'
            when 'Left hand' then 'UBERON:hand'
            when 'Forehead' then 'UBERON:skin'
            when 'Nares' then 'UBERON:nostril'
            when 'Hair' then 'UBERON:hair follicle'
            when 'Tears' then 'UBERON:secretion'
            when 'Ear wax' then 'UBERON:ear canal'
            when 'Vaginal mucus' then 'UBERON:mucosa of vagina'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as body_site, 
        case akb.site_sampled
            when 'Stool' then 'UBERON:feces'
            when 'Mouth' then 'UBERON:saliva'
            when 'Right hand' then 'UBERON:sebum'
            when 'Left hand' then 'UBERON:sebum'
            when 'Forehead' then 'UBERON:sebum'
            when 'Nares' then 'UBERON:mucus'
            when 'Hair' then 'UBERON:sebum'
            when 'Tears' then 'UBERON:tear'
            when 'Ear wax' then 'UBERON:cerumen'
            when 'Vaginal mucus' then 'UBERON:mucus'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as body_product, 
        case akb.site_sampled
            when 'Stool' then 'ENVO:urban biome'
            when 'Mouth' then 'ENVO:urban biome'
            when 'Right hand' then 'ENVO:urban biome'
            when 'Left hand' then 'ENVO:urban biome'
            when 'Forehead' then 'ENVO:urban biome'
            when 'Nares' then 'ENVO:urban biome'
            when 'Hair' then 'ENVO:urban biome'
            when 'Tears' then 'ENVO:urban biome'
            when 'Ear wax' then 'ENVO:urban biome'
            when 'Vaginal mucus' then 'ENVO:urban biome'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as env_biome, 
        case akb.site_sampled
            when 'Stool' then 'ENVO:human-associated habitat'
            when 'Mouth' then 'ENVO:human-associated habitat'
            when 'Right hand' then 'ENVO:human-associated habitat'
            when 'Left hand' then 'ENVO:human-associated habitat'
            when 'Forehead' then 'ENVO:human-associated habitat'
            when 'Nares' then 'ENVO:human-associated habitat'
            when 'Hair' then 'ENVO:human-associated habitat'
            when 'Tears' then 'ENVO:human-associated habitat'
            when 'Ear wax' then 'ENVO:human-associated habitat'
            when 'Vaginal mucus' then 'ENVO:human-associated habitat'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as env_feature, 
        case akb.site_sampled
            when 'Stool' then 'ENVO:feces'
            when 'Mouth' then 'ENVO:saliva'
            when 'Right hand' then 'ENVO:sebum'
            when 'Left hand' then 'ENVO:sebum'
            when 'Forehead' then 'ENVO:sebum'
            when 'Nares' then 'ENVO:mucus'
            when 'Hair' then 'ENVO:sebum'
            when 'Tears' then 'ENVO:tears'
            when 'Ear wax' then 'ENVO:cerumen'
            when 'Vaginal mucus' then 'ENVO:mucus'
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as env_matter,
        case
            when city is null then 'unknown'
            else lower(city)
        end as city, 
        case
            when state is null then 'unknown'
            else upper(state)
        end as state,
        case 
            when zip is null then 'unknown'
            when regexp_like(zip, '^\d*$') then lpad(zip, 5, 0)
            else zip
        end as zip,
        case 
            when lower(country) is null then 'unknown'
            when lower(country) = 'united states' then 'GAZ:United States of America'
            when lower(country) = 'united states of america' then 'GAZ:United States of America'
            when lower(country) = 'us' then 'GAZ:United States of America'
            when lower(country) = 'usa' then 'GAZ:United States of America'
            when lower(country) = 'u.s.a' then 'GAZ:United States of America'
            when lower(country) = 'u.s.' then 'GAZ:United States of America'
            when lower(country) = 'canada' then 'GAZ:Canada'
            when lower(country) = 'canadian' then 'GAZ:Canada'
            when lower(country) = 'ca' then 'GAZ:Canada'
            when lower(country) = 'australia' then 'GAZ:Australia'
            when lower(country) = 'au' then 'GAZ:Australia'
            when lower(country) = 'united kingdom' then 'GAZ:United Kingdom'
            when lower(country) = 'belgium' then 'GAZ:Belgium'
            when lower(country) = 'gb' then 'GAZ:Great Britain'
            when lower(country) = 'korea, republic of' then 'GAZ:South Korea'
            when lower(country) = 'nl' then 'GAZ:Netherlands'
            when lower(country) = 'netherlands' then 'GAZ:Netherlands'
            when lower(country) = 'spain' then 'GAZ:Spain'
            when lower(country) = 'es' then 'GAZ:Spain'
            when lower(country) = 'norway' then 'GAZ:Norway'
            when lower(country) = 'germany' then 'GAZ:Germany'
            when lower(country) = 'de' then 'GAZ:Germany'
            when lower(country) = 'china' then 'GAZ:China'
            when lower(country) = 'singapore' then 'GAZ:Singapore'
            when lower(country) = 'new zealand' then 'GAZ:New Zealand'
            when lower(country) = 'france' then 'GAZ:France'
            when lower(country) = 'fr' then 'GAZ:France'
            when lower(country) = 'ch' then 'GAZ:Switzerland'
            when lower(country) = 'switzerland' then 'GAZ:Switzerland'
            when lower(country) = 'denmark' then 'GAZ:Denmark'
            when lower(country) = 'scotland' then 'GAZ:Scotland'
            when lower(country) = 'united arab emirates' then 'GAZ:United Arab Emirates'
            when lower(country) = 'ireland' then 'GAZ:Ireland'
            when lower(country) = 'thailand' then 'GAZ:Thailand'
            else 'unknown'
        end as country,
        case
            when al.latitude is null then 'unknown'
            else cast(al.latitude as varchar2(100))
        end as latitude, 
        case
            when al.longitude is null then 'unknown'
            else cast(al.longitude as varchar2(100))
        end as longitude, 
        case
            when al.elevation is null then 'unknown'
            else cast(al.elevation as varchar2(100))
        end as elevation, 
        'years' as age_unit,
        case
            when ahs.birth_date is not null then
                case
                    when cast((current_date - to_date(ahs.birth_date, 'MM/DD/YYYY')) / 365.0 as int) between 0 and 120 then
                        cast(cast((current_date - to_date(ahs.birth_date, 'MM/DD/YYYY')) / 365.0 as int) as varchar2(100))
                    else
                        'unknown'
                end
            else 'unknown'
        end as age,
        case
            when ACNE_MEDICATION is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(ACNE_MEDICATION, CHR(10)), CHR(13)), CHR(9)))
        end as ACNE_MEDICATION,
        case
            when ACNE_MEDICATION_OTC is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(ACNE_MEDICATION_OTC, CHR(10)), CHR(13)), CHR(9)))
        end as ACNE_MEDICATION_OTC, 
        case
            when ALCOHOL_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(ALCOHOL_FREQUENCY, CHR(10)), CHR(13)), CHR(9))
        end as ALCOHOL_FREQUENCY, 


        case
            when FAT_PER is null or CARBOHYDRATE_PER is null or PROTEIN_PER is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
                 cast(REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
                 cast(REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) as int) between 90 and 110 then
                case
                    when cast(REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) as int) >= 0 then
                        cast(REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
                    else 'unknown'
                end
            else 'unknown'
        end as FAT_PER, 
        case
            when FAT_PER is null or CARBOHYDRATE_PER is null or PROTEIN_PER is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
                 cast(REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
                 cast(REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) as int) between 90 and 110 then
                case
                    when cast(REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) as int) >= 0 then
                        cast(REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
                    else 'unknown'
                end
            else 'unknown'
        end as CARBOHYDRATE_PER, 
        case
            when FAT_PER is null or CARBOHYDRATE_PER is null or PROTEIN_PER is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
                 cast(REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
                 cast(REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) as int) between 90 and 110 then
                case
                    when cast(REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) as int) >= 0 then
                        cast(REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
                    else 'unknown'
                end
            else 'unknown'
        end as PROTEIN_PER, 



        case
            when ANIMAL_PER is null or PLANT_PER is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(ANIMAL_PER, CHR(10)), CHR(13)), CHR(9)) as int) + cast(REPLACE(REPLACE(REPLACE(PLANT_PER, CHR(10)), CHR(13)), CHR(9)) as int) between 90 and 110 then
                case
                    when cast(REPLACE(REPLACE(REPLACE(ANIMAL_PER, CHR(10)), CHR(13)), CHR(9)) as int) >= 0
                        then cast(REPLACE(REPLACE(REPLACE(ANIMAL_PER, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
                    else 'unknown'
                end
            else 'unknown'
        end as ANIMAL_PER, 
        case
            when ANIMAL_PER is null or PLANT_PER is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(ANIMAL_PER, CHR(10)), CHR(13)), CHR(9)) as int) + cast(REPLACE(REPLACE(REPLACE(PLANT_PER, CHR(10)), CHR(13)), CHR(9)) as int) between 90 and 110 then
                case
                    when cast(REPLACE(REPLACE(REPLACE(PLANT_PER, CHR(10)), CHR(13)), CHR(9)) as int) >= 0
                        then cast(REPLACE(REPLACE(REPLACE(PLANT_PER, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
                    else 'unknown'
                end
            else 'unknown'
        end as PLANT_PER, 





        case 
            when ANTIBIOTIC_CONDITION is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(ANTIBIOTIC_CONDITION, CHR(10)), CHR(13)), CHR(9))
        end as ANTIBIOTIC_CONDITION, 
        case 
            when ANTIBIOTIC_SELECT is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(ANTIBIOTIC_SELECT, CHR(10)), CHR(13)), CHR(9))
        end as ANTIBIOTIC_SELECT, 
        case 
            when APPENDIX_REMOVED is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(APPENDIX_REMOVED, CHR(10)), CHR(13)), CHR(9)))
        end as APPENDIX_REMOVED, 
        case
            when ASTHMA is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(ASTHMA, CHR(10)), CHR(13)), CHR(9)))
        end as ASTHMA, 
        case 
            when BIRTH_DATE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(BIRTH_DATE, CHR(10)), CHR(13)), CHR(9))
        end as BIRTH_DATE, 
        case 
            when CAT is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(CAT, CHR(10)), CHR(13)), CHR(9)))
        end as CAT, 
        case
            when CHICKENPOX is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(CHICKENPOX, CHR(10)), CHR(13)), CHR(9)))
        end as CHICKENPOX, 
        
        case 
            when COMMUNAL_DINING is null then 'unknown'
            when REPLACE(REPLACE(REPLACE(COMMUNAL_DINING, CHR(10)), CHR(13)), CHR(9)) = 'on' then 'yes'
            else REPLACE(REPLACE(REPLACE(COMMUNAL_DINING, CHR(10)), CHR(13)), CHR(9))
        end as COMMUNAL_DINING, 
        case 
            when CONDITIONS_MEDICATION is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(CONDITIONS_MEDICATION, CHR(10)), CHR(13)), CHR(9)))
        end as CONDITIONS_MEDICATION, 
        
        case 
            when CONTRACEPTIVE is null then 'unknown'
            when REPLACE(REPLACE(REPLACE(CONTRACEPTIVE, CHR(10)), CHR(13)), CHR(9)) = 'I take the ' then 'I take the pill'
            else REPLACE(REPLACE(REPLACE(CONTRACEPTIVE, CHR(10)), CHR(13)), CHR(9))
        end as contraceptive, 
        case
            when COSMETICS_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(COSMETICS_FREQUENCY, CHR(10)), CHR(13)), CHR(9))
        end as COSMETICS_FREQUENCY, 
        case
            when 
            (
                select  term
                from    controlled_vocab_values
                where   vocab_value_id = ahs.COUNTRY_OF_BIRTH
            ) is null then 'unknown'
            else
            (
                select  term
                from    controlled_vocab_values
                where   vocab_value_id = ahs.COUNTRY_OF_BIRTH
            )
        end as COUNTRY_OF_BIRTH,
        case
            when CSECTION is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(CSECTION, CHR(10)), CHR(13)), CHR(9)) 
        end as CSECTION, 
        case
            when CURRENT_RESIDENCE_DURATION is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(CURRENT_RESIDENCE_DURATION, CHR(10)), CHR(13)), CHR(9)) 
        end as CURRENT_RESIDENCE_DURATION, 
        case
            when DECEASED_PARENT is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(DECEASED_PARENT, CHR(10)), CHR(13)), CHR(9)) 
        end as DECEASED_PARENT, 
        case
            when DEODERANT_USE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(DEODERANT_USE, CHR(10)), CHR(13)), CHR(9)) 
        end as DEODORANT_USE, 
        case
            when DIABETES is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(DIABETES, CHR(10)), CHR(13)), CHR(9)) 
        end as DIABETES, 
        case
            when DIABETES_DIAGNOSE_DATE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(DIABETES_DIAGNOSE_DATE, CHR(10)), CHR(13)), CHR(9)) 
        end as DIABETES_DIAGNOSE_DATE, 
        case
            when DIABETES_MEDICATION is null then 'unknown'
            when REPLACE(REPLACE(REPLACE(DIABETES_MEDICATION, CHR(10)), CHR(13)), CHR(9)) = 'on' then 'yes'
            else REPLACE(REPLACE(REPLACE(DIABETES_MEDICATION, CHR(10)), CHR(13)), CHR(9))
        end as DIABETES_MEDICATION, 
        case
            when DIET_TYPE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(DIET_TYPE, CHR(10)), CHR(13)), CHR(9)) 
        end as DIET_TYPE, 
        case 
            when DOG is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(DOG, CHR(10)), CHR(13)), CHR(9))) 
        end as DOG, 
        case
            when DRINKING_WATER_SOURCE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(DRINKING_WATER_SOURCE, CHR(10)), CHR(13)), CHR(9)) 
        end as DRINKING_WATER_SOURCE, 
        case
            when EXERCISE_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(EXERCISE_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) 
        end as EXERCISE_FREQUENCY, 
        case
            when EXERCISE_LOCATION is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(EXERCISE_LOCATION, CHR(10)), CHR(13)), CHR(9)) 
        end as EXERCISE_LOCATION,         
        case 
            when FIBER_GRAMS is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(FIBER_GRAMS, CHR(10)), CHR(13)), CHR(9)) as float) between 1 and 1000 then
                cast(REPLACE(REPLACE(REPLACE(FIBER_GRAMS, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
            else 'unknown'
        end as FIBER_GRAMS, 
        case
            when FLOSSING_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(FLOSSING_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) 
        end as FLOSSING_FREQUENCY, 
        case
            when FLU_VACCINE_DATE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(FLU_VACCINE_DATE, CHR(10)), CHR(13)), CHR(9)) 
        end as FLU_VACCINE_DATE, 
        case 
            when FOODALLERGIES_OTHER is null then 'unknown'
            when FOODALLERGIES_OTHER = 'on' then 'yes'
            else FOODALLERGIES_OTHER
        end as FOODALLERGIES_OTHER, 
        case
            when FOODALLERGIES_OTHER_TEXT is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(FOODALLERGIES_OTHER_TEXT, CHR(10)), CHR(13)), CHR(9)) 
        end as FOODALLERGIES_OTHER_TEXT, 
        case
            when FOODALLERGIES_PEANUTS is null then 'unknown'
            when FOODALLERGIES_PEANUTS = 'on' then 'yes'
            else FOODALLERGIES_PEANUTS
        end as FOODALLERGIES_PEANUTS,
        case
            when FOODALLERGIES_SHELLFISH is null then 'unknown'
            when FOODALLERGIES_SHELLFISH = 'on' then 'yes'
            else FOODALLERGIES_SHELLFISH
        end as FOODALLERGIES_SHELLFISH, 
        case
            when FOODALLERGIES_TREENUTS is null then 'unknown'
            when FOODALLERGIES_TREENUTS = 'on' then 'yes'
            else FOODALLERGIES_TREENUTS
        end as FOODALLERGIES_TREENUTS, 
        case
            when FRAT is null then 'unknown'
            when FRAT = 'on' then 'yes'
            else FRAT
        end as FRAT, 
        case
            when GENDER is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(GENDER, CHR(10)), CHR(13)), CHR(9)))
        end as sex,
        case
            when GLUTEN is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(GLUTEN, CHR(10)), CHR(13)), CHR(9)))
        end as GLUTEN, 
        case
            when HAND is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(HAND, CHR(10)), CHR(13)), CHR(9)) 
        end as dominant_hand,
        case
            when HEIGHT_IN is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(HEIGHT_IN, CHR(10)), CHR(13)), CHR(9)) as float) between 10 and 106 then
                cast(cast(REPLACE(REPLACE(REPLACE(HEIGHT_IN, CHR(10)), CHR(13)), CHR(9)) as float) as varchar2(100))
            else 'unknown'
        end as HEIGHT_IN,
        case
            when HEIGHT_CM is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(HEIGHT_CM, CHR(10)), CHR(13)), CHR(9)) as float) between 25 and 270 then
                cast(cast(REPLACE(REPLACE(REPLACE(HEIGHT_CM, CHR(10)), CHR(13)), CHR(9)) as float) as varchar2(100))
            else 'unknown'
        end as height_or_length,
        case
            when IBD is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(IBD, CHR(10)), CHR(13)), CHR(9)) 
        end as IBD, 
        case
            when LACTOSE is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(LACTOSE, CHR(10)), CHR(13)), CHR(9)))
        end as LACTOSE, 
        case
            when LAST_TRAVEL is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(LAST_TRAVEL, CHR(10)), CHR(13)), CHR(9)) 
        end as LAST_TRAVEL, 
        case
            when LIVINGWITH is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(LIVINGWITH, CHR(10)), CHR(13)), CHR(9)) 
        end as LIVINGWITH, 
        case
            when MAINFACTOR_OTHER_1 is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MAINFACTOR_OTHER_1, CHR(10)), CHR(13)), CHR(9)) 
        end as MAINFACTOR_OTHER_1, 
        case
            when MAINFACTOR_OTHER_2 is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MAINFACTOR_OTHER_2, CHR(10)), CHR(13)), CHR(9)) 
        end as MAINFACTOR_OTHER_2, 
        case
            when MAINFACTOR_OTHER_3 is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MAINFACTOR_OTHER_3, CHR(10)), CHR(13)), CHR(9)) 
        end as MAINFACTOR_OTHER_3, 
        case
            when MIGRAINE is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(MIGRAINE, CHR(10)), CHR(13)), CHR(9))) 
        end as MIGRAINE, 
        case
            when MIGRAINEMEDS is null then 'unknown'
            when MIGRAINEMEDS = 'on' then 'yes'
            else MIGRAINEMEDS
        end as MIGRAINEMEDS, 
        case
            when MIGRAINE_AGGRAVATION is null then 'unknown'
            when MIGRAINE_AGGRAVATION = 'on' then 'yes'
            else MIGRAINE_AGGRAVATION
        end as MIGRAINE_AGGRAVATION, 
        case 
            when MIGRAINE_AURA is null then 'unknown'
            when MIGRAINE_AURA = 'on' then 'yes'
            else MIGRAINE_AURA
        end as MIGRAINE_AURA, 
        case
            when MIGRAINE_FACTOR_1 is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MIGRAINE_FACTOR_1, CHR(10)), CHR(13)), CHR(9)) 
        end as MIGRAINE_FACTOR_1, 
        case
            when MIGRAINE_FACTOR_2 is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MIGRAINE_FACTOR_2, CHR(10)), CHR(13)), CHR(9)) 
        end as MIGRAINE_FACTOR_2, 
        case
            when MIGRAINE_FACTOR_3 is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MIGRAINE_FACTOR_3, CHR(10)), CHR(13)), CHR(9)) 
        end as MIGRAINE_FACTOR_3, 
        case
            when MIGRAINE_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(MIGRAINE_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) 
        end as MIGRAINE_FREQUENCY, 
        case
            when MIGRAINE_NAUSEA is null then 'unknown'
            when MIGRAINE_NAUSEA = 'on' then 'yes'
            else MIGRAINE_NAUSEA
        end as MIGRAINE_NAUSEA, 
        case 
            when MIGRAINE_PAIN is null then 'unknown'
            when MIGRAINE_PAIN = 'on' then 'yes'
            else MIGRAINE_PAIN
        end as MIGRAINE_PAIN, 
        case
            when MIGRAINE_PHONOPHOBIA is null then 'unknown'
            when MIGRAINE_PHONOPHOBIA = 'on' then 'yes'
            else MIGRAINE_PHONOPHOBIA
        end as MIGRAINE_PHONOPHOBIA, 
        case
            when MIGRAINE_PHOTOPHOBIA is null then 'unknown'
            when MIGRAINE_PHOTOPHOBIA = 'on' then 'yes'
            else MIGRAINE_PHOTOPHOBIA
        end as MIGRAINE_PHOTOPHOBIA, 
        case
            when MIGRAINE_RELATIVES is null then 'unknown'
            when MIGRAINE_RELATIVES = 'on' then 'yes'
            else MIGRAINE_RELATIVES
        end as MIGRAINE_RELATIVES, 
        case
            when MULTIVITAMIN is null then 'unknown'
            else lower(MULTIVITAMIN)
        end as MULTIVITAMIN, 
        case
            when NAILS is null then 'unknown'
            else lower(NAILS)
        end as NAILS, 
        case
            when NONFOODALLERGIES_BEESTINGS is null then 'unknown'
            when NONFOODALLERGIES_BEESTINGS = 'on' then 'yes'
            else NONFOODALLERGIES_BEESTINGS
        end as NONFOODALLERGIES_BEESTINGS, 
        case
            when NONFOODALLERGIES_DANDER is null then 'unknown'
            when NONFOODALLERGIES_DANDER = 'on' then 'yes'
            else NONFOODALLERGIES_DANDER
        end as NONFOODALLERGIES_DANDER, 
        case
            when NONFOODALLERGIES_DRUG is null then 'unknown'
            when NONFOODALLERGIES_DRUG = 'on' then 'yes'
            else NONFOODALLERGIES_DRUG
        end as NONFOODALLERGIES_DRUG, 
        case
            when NONFOODALLERGIES_NO is null then 'unknown'
            when NONFOODALLERGIES_NO = 'on' then 'yes'
            else NONFOODALLERGIES_NO
        end as NONFOODALLERGIES_NO, 
        case
            when NONFOODALLERGIES_POISONIVY is null then 'unknown'
            when NONFOODALLERGIES_POISONIVY = 'on' then 'yes'
            else NONFOODALLERGIES_POISONIVY
        end as NONFOODALLERGIES_POISONIVY, 
        case
            when NONFOODALLERGIES_SUN is null then 'unknown'
            when NONFOODALLERGIES_SUN = 'on' then 'yes'
            else NONFOODALLERGIES_SUN
        end as NONFOODALLERGIES_SUN, 
        case
            when PERCENTAGE_FROM_CARBS is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(PERCENTAGE_FROM_CARBS, CHR(10)), CHR(13)), CHR(9)) 
        end as PERCENTAGE_FROM_CARBS, 
        case
            when PKU is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(PKU, CHR(10)), CHR(13)), CHR(9))) 
        end as PKU, 
        case
            when POOL_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(POOL_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) 
        end POOL_FREQUENCY, 
        case
            when PREGNANT is null and PREGNANT_DUE_DATE is null then 'no'
            when PREGNANT = 'on' and PREGNANT_DUE_DATE is null then 'unknown'
            when PREGNANT = 'on' and PREGNANT_DUE_DATE is not null then 'yes'
            else lower(PREGNANT)
        end as PREGNANT, 
        case
            when PREGNANT_DUE_DATE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(PREGNANT_DUE_DATE, CHR(10)), CHR(13)), CHR(9)) 
        end as PREGNANT_DUE_DATE, 
        case
            when PRIMARY_CARB is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(PRIMARY_CARB, CHR(10)), CHR(13)), CHR(9)) 
        end as PRIMARY_CARB, 
        case
            when PRIMARY_VEGETABLE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(PRIMARY_VEGETABLE, CHR(10)), CHR(13)), CHR(9)) 
        end as PRIMARY_VEGETABLE, 
        case
            when RACE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(RACE, CHR(10)), CHR(13)), CHR(9)) 
        end as RACE, 
        case
            when RACE_OTHER is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(RACE_OTHER, CHR(10)), CHR(13)), CHR(9)) 
        end as RACE_OTHER, 
        case
            when ROOMMATES is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(ROOMMATES, CHR(10)), CHR(13)), CHR(9)) 
        end as ROOMMATES, 
        case
            when SEASONAL_ALLERGIES is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(SEASONAL_ALLERGIES, CHR(10)), CHR(13)), CHR(9))) 
        end as SEASONAL_ALLERGIES, 
        case
            when SHARED_HOUSING is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(SHARED_HOUSING, CHR(10)), CHR(13)), CHR(9))) 
        end as SHARED_HOUSING, 
        case
            when SKIN_CONDITION is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(SKIN_CONDITION, CHR(10)), CHR(13)), CHR(9)) 
        end as SKIN_CONDITION, 
        case 
            when SLEEP_DURATION is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(SLEEP_DURATION, CHR(10)), CHR(13)), CHR(9)) 
        end as SLEEP_DURATION, 
        case
            when SMOKING_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(SMOKING_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) 
        end as SMOKING_FREQUENCY, 
        case
            when SOFTENER is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(SOFTENER, CHR(10)), CHR(13)), CHR(9))) 
        end as SOFTENER, 
        case
            when SPECIAL_RESTRICTIONS is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(SPECIAL_RESTRICTIONS, CHR(10)), CHR(13)), CHR(9))) 
        end as SPECIAL_RESTRICTIONS, 
        case
            when SUPPLEMENTS is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(SUPPLEMENTS, CHR(10)), CHR(13)), CHR(9))) 
        end as SUPPLEMENTS, 
        case
            when TANNING_BEDS is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(TANNING_BEDS, CHR(10)), CHR(13)), CHR(9)) 
        end as TANNING_BEDS, 
        case
            when TANNING_SPRAYS is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(TANNING_SPRAYS, CHR(10)), CHR(13)), CHR(9)) 
        end as TANNING_SPRAYS, 
        case
            when TEETHBRUSHING_FREQUENCY is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(TEETHBRUSHING_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) 
        end as TEETHBRUSHING_FREQUENCY, 
        case
            when TONSILS_REMOVED is null then 'unknown'
            else lower(REPLACE(REPLACE(REPLACE(TONSILS_REMOVED, CHR(10)), CHR(13)), CHR(9))) 
        end as TONSILS_REMOVED, 
        case
            when TYPES_OF_PLANTS is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(TYPES_OF_PLANTS, CHR(10)), CHR(13)), CHR(9)) 
        end as TYPES_OF_PLANTS, 
        case
            when WEIGHT_CHANGE is null then 'unknown'
            else REPLACE(REPLACE(REPLACE(WEIGHT_CHANGE, CHR(10)), CHR(13)), CHR(9)) 
        end as WEIGHT_CHANGE, 
        case
            when WEIGHT_KG is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(WEIGHT_KG, CHR(10)), CHR(13)), CHR(9)) as float) between 1 and 227 then
                cast(REPLACE(REPLACE(REPLACE(WEIGHT_KG, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
            else 'unknown'
        end as tot_mass,
        case
            when WEIGHT_LBS is null then 'unknown'
            when cast(REPLACE(REPLACE(REPLACE(WEIGHT_LBS, CHR(10)), CHR(13)), CHR(9)) as float) between 1 and 500 then
                cast(REPLACE(REPLACE(REPLACE(WEIGHT_LBS, CHR(10)), CHR(13)), CHR(9)) as varchar2(100))
            else 'unknown'
        end as WEIGHT_LBS,
        case
            when weight_lbs > 0 and height_in > 0 then
            case 
                when (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 between 5 and 100 
                    then cast((cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 as varchar2(100))
                else 'unknown'
            end
            else 'unknown'
        end as BMI,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'antibiotic_med_%'
            ) is null then 'unknown'
            else 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'antibiotic_med_%'
            )
        end as antibiotic_meds,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'diabetes_medications_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'diabetes_medications_%'
            )
        end as diabetes_medications,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'dietrestrictions_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'dietrestrictions_%'
            )
        end as diet_restrictions,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'general_meds_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'general_meds_%'
            )
        end as general_meds,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'migraine_medication_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'migraine_medication_%'
            )
        end as migraine_medications,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'pet_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'pet_%'
            )
        end as pets,
        case
            when
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'pet_contact_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'pet_contact_%'
            )
        end as pet_contact,
        case
            when
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'pet_location_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'pet_location_%'
            )
        end as pet_locations,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'relation_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'relation_%'
            )
        end as relations,
        case
            when
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'supplements_fields_%'
            ) is null then 'unknown'
            else
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and item_name like 'supplements_fields_%'
            )
        end as supplements_fields,
        (
            cast(REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
            cast(REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) as int) +
            cast(REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) as int)
        ) as macronutrient_pct_total,
        
        
        
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and lower(item_name) like 'antibiotic_med_%'
                        and 
                        (
                            lower(item_value) like '%moxifloxacin%'
                            or lower(item_value) like '%avelox%'
                            or lower(item_value) like '%ciprofloxacin%'
                            or lower(item_value) like '%cipro%'
                        )
            ) is null then 'no'
            else 'yes'
        end as Quinoline,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and lower(item_name) like 'antibiotic_med_%'
                        and 
                        (
                            lower(item_value) like '%metronidazole%'
                            or lower(item_value) like '%flagyl%'
                            or lower(item_value) like '%secnidazole%'
                            or lower(item_value) like '%tinidazole%'
                            or lower(item_value) like '%tindamax%'
                        )
            ) is null then 'no'
            else 'yes'
        end as Nitromidazole,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and lower(item_name) like 'antibiotic_med_%'
                        and 
                        (
                            lower(item_value) like '%amoxicillin%'
                            or lower(item_value) like '%penicillin%'
                            or lower(item_value) like '%augmentin%'
                            or lower(item_value) like '%methicillin%'
                        )
            ) is null then 'no'
            else 'yes'
        end as Penicillin,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and lower(item_name) like 'antibiotic_med_%'
                        and 
                        (
                            lower(item_value) like '%sulfamethoxazole%'
                            or lower(item_value) like '%bactrim%'
                            or lower(item_value) like '%septra%'
                        )
            ) is null then 'no'
            else 'yes'
        end as Sulfa_Drug,
        case
            when 
            (
                select  listagg(item_value, ', ') within group(order by item_name)
                from    ag_survey_multiples
                where   ag_login_id = al.ag_login_id
                        and participant_name = akb.participant_name
                        and lower(item_name) like 'antibiotic_med_%'
                        and 
                        (
                            lower(item_value) like '%cefuroxime axetil%'
                            or lower(item_value) like '%ceftin%'
                            or lower(item_value) like '%cefalexin%'
                            or lower(item_value) like '%keflex%'
                            or lower(item_value) like '%ceftriaxone%'
                            or lower(item_value) like '%recophin%'
                            or lower(item_value) like '%levofloxacin%'
                            or lower(item_value) like '%levaquin%'
                            or lower(item_value) like '%cefdinir%'
                            or lower(item_value) like '%omnicef%'
                            or lower(item_value) like '%cefotaxime%'
                        )
            ) is null then 'no'
            else 'yes'
        end as Cephalosporin
        
        
        
        
        
        
        
        
        
from    ag_login al
        inner join ag_kit ak
        on al.ag_login_id = ak.ag_login_id
        inner join ag_kit_barcodes akb
        on ak.ag_kit_id = akb.ag_kit_id
        inner join ag_human_survey ahs
        on al.ag_login_id = ahs.ag_login_id
where   akb.participant_name = ahs.participant_name
        and akb.site_sampled is not null
        and akb.site_sampled != 'Please Select...'
        and akb.sample_date is not null
        and akb.barcode = barcode_;

end;

/*
variable results_cursor REFCURSOR;
exec ag_check_barcode_metadata('000001002', :results_cursor);
print results_cursor;
*/
