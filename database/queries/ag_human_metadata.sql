/*
sample time/date - see what I can do
unknown values: 
*/

select  akb.barcode as sample_name, 
        akb.barcode as ANONYMIZED_NAME, 
        akb.sample_date as collection_date, 
        'n' as "public",
        0 as depth,
        'unknown' as elevation,
        'American Gut Project ' || akb.site_sampled || ' sample' as DESCRIPTION,
        akb.sample_time, 
        0 as altitude, 
        'n' as assigned_from_geo,
        'American Gut Project' as TITLE,
        case akb.site_sampled
            when 'Please select...' then 'unknown'
            else akb.site_sampled
        end as site_sampled,
        ora_hash(al.email) as host_subject_id, 
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
            else zip
        end as zip,
        case 
            when lower(country) is null then 'unknown'
            when lower(country) = 'united states' then 'GAZ:United States of America'
            when lower(country) = 'united states of america' then 'GAZ:United States of America'
            when lower(country) = 'us' then 'GAZ:United States of America'
            when lower(country) = 'usa' then 'GAZ:United States of America'
            when lower(country) = 'canada' then 'GAZ:Canada'
            when lower(country) = 'spain' then 'GAZ:Spain'
            else lower(country)
        end as country,
        case
            when al.latitude is null then 'unknown'
            else cast(al.latitude as varchar2(100))
        end as latitude, 
        case
            when al.longitude is null then 'unknown'
            else cast(al.longitude as varchar2(100))
        end as longitude, 
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
            when PREGNANT is null then 'unknown'
            when PREGNANT = 'on' then 'yes'
            else PREGNANT
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
        /*
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'related_participant_%'
        ) as related_participants,
        */
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
        ) as macronutrient_pct_total
        /*,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'travel_duration_%'
        ) as travel_durations,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'travel_location_%'
        ) as travel_locations*/
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
        and akb.barcode in
(
-- AGP round 1
--'000001002', '000001004', '000001008', '000001018', '000001031', '000001032', '000001038', '000001046', '000001047', '000001048', '000001049', '000001056', '000001058', '000001059', '000001060', '000001065', '000001067', '000001069', '000001077', '000001078', '000001086', '000001089', '000001097', '000001098', '000001099', '000001100', '000001109', '000001110', '000001115', '000001116', '000001118', '000001120', '000001121', '000001126', '000001128', '000001130', '000001135', '000001138', '000001140', '000001141', '000001142', '000001150', '000001151', '000001152', '000001154', '000001155', '000001170', '000001171', '000001173', '000001174', '000001180', '000001189', '000001192', '000001194', '000001196', '000001214', '000001216', '000001218', '000001221', '000001225', '000001228', '000001231', '000001248', '000001256', '000001265', '000001269', '000001270', '000001272', '000001275', '000001278', '000001284', '000001285', '000001288', '000001291', '000001294', '000001299', '000001301', '000001303', '000001305', '000001311', '000001312', '000001315', '000001317', '000001322', '000001333', '000001336', '000001344', '000001345', '000001350', '000001353', '000001354', '000001362', '000001363', '000001364', '000001367', '000001375', '000001377', '000001380', '000001386', '000001397', '000001398', '000001399', '000001404', '000001405', '000001411', '000001417', '000001419', '000001421', '000001422', '000001427', '000001432', '000001435', '000001436', '000001446', '000001451', '000001482', '000001487', '000001488', '000001504', '000001516', '000001521', '000001528', '000001530', '000001531', '000001538', '000001541', '000001543', '000001545', '000001547', '000001548', '000001551', '000001552', '000001555', '000001556', '000001559', '000001574', '000001575', '000001576', '000001583', '000001587', '000001589', '000001593', '000001595', '000001597', '000001611', '000001615', '000001621', '000001622', '000001630', '000001632', '000001645', '000001649', '000001650', '000001651', '000001652', '000001654', '000001658', '000001659', '000001660', '000001661', '000001662', '000001669', '000001678', '000001685', '000001694', '000001704', '000001705', '000001711', '000001713', '000001714', '000001726', '000001731', '000001735', '000001745', '000001747', '000001749', '000001751', '000001755', '000001756', '000001762', '000001763', '000001764', '000001769', '000001770', '000001772', '000001786', '000001793', '000001794', '000001795', '000001797', '000001801', '000001802', '000001808', '000001812', '000001826', '000001830', '000001832', '000001835', '000001837', '000001842', '000001852', '000001854', '000001856', '000001860', '000001866', '000001874', '000001878', '000001884', '000001886', '000001888', '000001916', '000001923', '000001947', '000001948', '000001955', '000001961', '000001962', '000001969', '000001978', '000001979', '000001980', '000001985', '000001988', '000002035', '000002041', '000002042', '000002056', '000002067', '000002068', '000002087', '000002109', '000002147', '000002148', '000002151', '000002165', '000002166', '000002173', '000002175', '000002176', '000002185', '000002186', '000002199', '000002200', '000002205', '000002211', '000002219', '000002220', '000002229', '000002230', '000002237', '000002243', '000002244', '000002261', '000002262', '000002273', '000002274', '000002295', '000002304', '000002309', '000002310', '000002315', '000002319', '000002329', '000002330', '000002331', '000002349', '000002350', '000002359', '000002371', '000002372', '000002387', '000002391', '000002396', '000002419', '000002443', '000002444', '000002446', '000002466', '000002471', '000002472', '000002481', '000002482', '000002494', '000002506', '000002545', '000002546', '000002563', '000002564', '000002575', '000002576', '000002597', '000002598', '000002605', '000002606', '000002607', '000002609', '000002616', '000002619', '000002625', '000002631', '000002632', '000002637', '000002638', '000002683', '000002687', '000002689', '000002690', '000002735', '000002736', '000002739', '000002773', '000002774', '000002777', '000002781', '000002782', '000002805', '000002806', '000002814', '000002819', '000002825', '000002826', '000002833', '000002834', '000002849', '000002850', '000002853', '000002859', '000002863', '000002865', '000002866', '000002871', '000002873', '000002883', '000002884', '000002885', '000002886', '000002893', '000002894', '000002897', '000002898', '000002939', '000002943', '000002944', '000002951', '000002952', '000003028', '000003032', '000003047', '000003048', '000003058', '000003059', '000003060', '000003091', '000003092', '000003093', '000003103', '000003120', '000003154', '000003155', '000003199', '000003200', '000003201', '000003214', '000003216', '000003225', '000003280', '000003281', '000003282', '000003287', '000003300', '000003331', '000003364', '000003365', '000003366', '000003423', '000003430', '000003432', '000003439', '000003458', '000003505', '000003506', '000003507', '000003508', '000003533', '000003534', '000003536', '000003640', '000003666', '000003703', '000003879', '000003880', '000003937', '000003951', '000003969', '000003970', '000003971', '000003972', '000003973', '000004009', '000004011', '000004039', '000004040', '000004071', '000004072', '000004075', '000004139', '000004141', '000004158', '000004159', '000004160', '000004185', '000004187', '000004188', '000004189', '000004190', '000004191', '000004207', '000004221', '000004222', '000004223', '000004224', '000004234', '000004265', '000004266', '000004267', '000004672', '000004680'

-- AGP round 2
'000001026', '000001042', '000001072', '000001073', '000001084', '000001111', '000001125', '000001156', '000001193', '000001197', '000001203', '000001205', '000001209', '000001238', '000001244', '000001252', '000001253', '000001255', '000001263', '000001267', '000001281', '000001286', '000001328', '000001331', '000001332', '000001334', '000001347', '000001374', '000001384', '000001391', '000001400', '000001410', '000001423', '000001438', '000001459', '000001483', '000001492', '000001499', '000001500', '000001509', '000001520', '000001529', '000001558', '000001568', '000001570', '000001572', '000001579', '000001582', '000001590', '000001594', '000001616', '000001631', '000001635', '000001647', '000001676', '000001684', '000001725', '000001765', '000001779', '000001782', '000001815', '000001827', '000001851', '000001861', '000001879', '000001887', '000001892', '000001908', '000001911', '000001912', '000001919', '000001922', '000001934', '000001939', '000001940', '000001960', '000001966', '000002023', '000002036', '000002043', '000002044', '000002050', '000002064', '000002073', '000002114', '000002132', '000002177', '000002179', '000002180', '000002183', '000002208', '000002276', '000002282', '000002287', '000002288', '000002301', '000002302', '000002334', '000002337', '000002338', '000002345', '000002346', '000002347', '000002348', '000002384', '000002389', '000002403', '000002404', '000002414', '000002437', '000002465', '000002475', '000002503', '000002577', '000002578', '000002589', '000002590', '000002628', '000002651', '000002652', '000002655', '000002656', '000002709', '000002710', '000002713', '000002715', '000002716', '000002734', '000002751', '000002752', '000002765', '000002783', '000002784', '000002817', '000002818', '000002851', '000002905', '000002906', '000002911', '000002971', '000002972', '000002979', '000002980', '000002995', '000002996', '000003001', '000003002', '000003022', '000003023', '000003024', '000003026', '000003082', '000003086', '000003125', '000003126', '000003136', '000003148', '000003149', '000003150', '000003169', '000003170', '000003171', '000003193', '000003220', '000003221', '000003222', '000003240', '000003277', '000003279', '000003319', '000003337', '000003368', '000003369', '000003370', '000003387', '000003438', '000003442', '000003460', '000003473', '000003475', '000003476', '000003602', '000003603', '000003713', '000003757', '000003793', '000003794', '000003795', '000003796', '000003797', '000003798', '000003894', '000003895', '000003900', '000004144', '000004145', '000004163', '000004272', '000004273', '000004281', '000004611', '000004612', '000004616', '000004633', '000004636', '000004640', '000004641', '000004642', '000004652', '000004654', '000004656', '000004660', '000004662', '000004667', '000004670', '000004676', '000004677', '000004679', '000004686', '000004691', '000004694', '000004695', '000004696', '000004697', '000004699', '000004707', '000004709', '000004711', '000004714', '000004716', '000004726', '000004730', '000004731', '000004735', '000004736', '000004737', '000004738', '000004752', '000004753', '000004758', '000004759', '000004773', '000004774', '000004780', '000004781', '000004782', '000004783', '000004796', '000004797', '000004807', '000004811', '000004812', '000004818', '000004819', '000004822', '000004823', '000004830', '000004831', '000004833', '000004847', '000004858', '000004859', '000004860', '000004864', '000004872', '000004881', '000004890', '000004891', '000004894', '000004915', '000004916', '000004917', '000004926', '000004951', '000004952', '000004979', '000004980', '000005015', '000005016', '000005017', '000005031', '000005032', '000005033', '000005034', '000005035', '000005036', '000005037', '000005039', '000005040', '000005068', '000005073', '000005080', '000005085', '000005163', '000005168', '000005223', '000005238', '000005263', '000005293', '000005360', '000005433', '000005554', '000005571', '000005576', '000005648', '000005653', '000005655', '000005660', '000005755', '000005756', '000005776', '000005780', '000005784', '000005792', '000005799', '000005811', '000005824', '000005825', '000005834', '000005835', '000005840', '000005841', '000005849', '000005850', '000005884', '000005885', '000005902', '000005903', '000005910', '000005916', '000005938', '000005945', '000005954', '000002733', '000008949', '000008950', '000008951', '000008952', '000008953', '000008954', '000008956', '000008957', '000008958', '000008959'
)
order by sample_name;

