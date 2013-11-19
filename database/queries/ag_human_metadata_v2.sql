/*
sample time/date - see what I can do
unknown values: 
*/

select  akb.barcode as sample_name, 
        akb.barcode as ANONYMIZED_NAME, 
        akb.sample_date as collection_date, 
        'y' as "public",
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
            when lower(country) = 'norway' then 'GAZ:Norway'
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
-- Random Strangers
--'000007094', '000007125', '000007134', '000007101', '000007093', '000007126', '000007089', '000007088', '000007097', '000007635', '000007092', '000007100', '000007133', '000007132', '000007082', '000007135', '000007107', '000007099', '000007096', '000007098', '000007091', '000007095', '000007076', '000007090', '000007082', '000007108', '000007109', '000007110', '000007111', '000007112', '000007113', '000007114', '000007115', '000007116', '000007117', '000007118', '000007119', '000007120', '000007121', '000007122', '000007123', '000007124', '000007077', '000007078', '000007079', '000007080', '000007081', '000007102', '000007103', '000007104', '000007105', '000007106', '000007127', '000007128', '000007129', '000007130', '000007131', '000007083', '000007084', '000007085', '000007086', '000007087'

-- AGP round 1
--'000001002', '000001004', '000001008', '000001018', '000001031', '000001032', '000001038', '000001046', '000001047', '000001048', '000001049', '000001056', '000001058', '000001059', '000001060', '000001065', '000001067', '000001069', '000001077', '000001078', '000001086', '000001089', '000001097', '000001098', '000001099', '000001100', '000001109', '000001110', '000001115', '000001116', '000001118', '000001120', '000001121', '000001126', '000001128', '000001130', '000001135', '000001138', '000001140', '000001141', '000001142', '000001150', '000001151', '000001152', '000001154', '000001155', '000001170', '000001171', '000001173', '000001174', '000001180', '000001189', '000001192', '000001194', '000001196', '000001214', '000001216', '000001218', '000001221', '000001225', '000001228', '000001231', '000001248', '000001256', '000001265', '000001269', '000001270', '000001272', '000001275', '000001278', '000001284', '000001285', '000001288', '000001291', '000001294', '000001299', '000001301', '000001303', '000001305', '000001311', '000001312', '000001315', '000001317', '000001322', '000001333', '000001336', '000001344', '000001345', '000001350', '000001353', '000001354', '000001362', '000001363', '000001364', '000001367', '000001375', '000001377', '000001380', '000001386', '000001397', '000001398', '000001399', '000001404', '000001405', '000001411', '000001417', '000001419', '000001421', '000001422', '000001427', '000001432', '000001435', '000001436', '000001446', '000001451', '000001482', '000001487', '000001488', '000001504', '000001516', '000001521', '000001528', '000001530', '000001531', '000001538', '000001541', '000001543', '000001545', '000001547', '000001548', '000001551', '000001552', '000001555', '000001556', '000001559', '000001574', '000001575', '000001576', '000001583', '000001587', '000001589', '000001593', '000001595', '000001597', '000001611', '000001615', '000001621', '000001622', '000001630', '000001632', '000001645', '000001649', '000001650', '000001651', '000001652', '000001654', '000001658', '000001659', '000001660', '000001661', '000001662', '000001669', '000001678', '000001685', '000001694', '000001704', '000001705', '000001711', '000001713', '000001714', '000001726', '000001731', '000001735', '000001745', '000001747', '000001749', '000001751', '000001755', '000001756', '000001762', '000001763', '000001764', '000001769', '000001770', '000001772', '000001786', '000001793', '000001794', '000001795', '000001797', '000001801', '000001802', '000001808', '000001812', '000001826', '000001830', '000001832', '000001835', '000001837', '000001842', '000001852', '000001854', '000001856', '000001860', '000001866', '000001874', '000001878', '000001884', '000001886', '000001888', '000001916', '000001923', '000001947', '000001948', '000001955', '000001961', '000001962', '000001969', '000001978', '000001979', '000001980', '000001985', '000001988', '000002035', '000002041', '000002042', '000002056', '000002067', '000002068', '000002087', '000002109', '000002147', '000002148', '000002151', '000002165', '000002166', '000002173', '000002175', '000002176', '000002185', '000002186', '000002199', '000002200', '000002205', '000002211', '000002219', '000002220', '000002229', '000002230', '000002237', '000002243', '000002244', '000002261', '000002262', '000002273', '000002274', '000002295', '000002304', '000002309', '000002310', '000002315', '000002319', '000002329', '000002330', '000002331', '000002349', '000002350', '000002359', '000002371', '000002372', '000002387', '000002391', '000002396', '000002419', '000002443', '000002444', '000002446', '000002466', '000002471', '000002472', '000002481', '000002482', '000002494', '000002506', '000002545', '000002546', '000002563', '000002564', '000002575', '000002576', '000002597', '000002598', '000002605', '000002606', '000002607', '000002609', '000002616', '000002619', '000002625', '000002631', '000002632', '000002637', '000002638', '000002683', '000002687', '000002689', '000002690', '000002735', '000002736', '000002739', '000002773', '000002774', '000002777', '000002781', '000002782', '000002805', '000002806', '000002814', '000002819', '000002825', '000002826', '000002833', '000002834', '000002849', '000002850', '000002853', '000002859', '000002863', '000002865', '000002866', '000002871', '000002873', '000002883', '000002884', '000002885', '000002886', '000002893', '000002894', '000002897', '000002898', '000002939', '000002943', '000002944', '000002951', '000002952', '000003028', '000003032', '000003047', '000003048', '000003058', '000003059', '000003060', '000003091', '000003092', '000003093', '000003103', '000003120', '000003154', '000003155', '000003199', '000003200', '000003201', '000003214', '000003216', '000003225', '000003280', '000003281', '000003282', '000003287', '000003300', '000003331', '000003364', '000003365', '000003366', '000003423', '000003430', '000003432', '000003439', '000003458', '000003505', '000003506', '000003507', '000003508', '000003533', '000003534', '000003536', '000003640', '000003666', '000003703', '000003879', '000003880', '000003937', '000003951', '000003969', '000003970', '000003971', '000003972', '000003973', '000004009', '000004011', '000004039', '000004040', '000004071', '000004072', '000004075', '000004139', '000004141', '000004158', '000004159', '000004160', '000004185', '000004187', '000004188', '000004189', '000004190', '000004191', '000004207', '000004221', '000004222', '000004223', '000004224', '000004234', '000004265', '000004266', '000004267', '000004672', '000004680'

-- AGP round 2
--'000001026', '000001042', '000001072', '000001073', '000001084', '000001111', '000001125', '000001156', '000001193', '000001197', '000001203', '000001205', '000001209', '000001238', '000001244', '000001252', '000001253', '000001255', '000001263', '000001267', '000001281', '000001286', '000001328', '000001331', '000001332', '000001334', '000001347', '000001374', '000001384', '000001391', '000001400', '000001410', '000001423', '000001438', '000001459', '000001483', '000001492', '000001499', '000001500', '000001509', '000001520', '000001529', '000001558', '000001568', '000001570', '000001572', '000001579', '000001582', '000001590', '000001594', '000001616', '000001631', '000001635', '000001647', '000001676', '000001684', '000001725', '000001765', '000001779', '000001782', '000001815', '000001827', '000001851', '000001861', '000001879', '000001887', '000001892', '000001908', '000001911', '000001912', '000001919', '000001922', '000001934', '000001939', '000001940', '000001960', '000001966', '000002023', '000002036', '000002043', '000002044', '000002050', '000002064', '000002073', '000002114', '000002132', '000002177', '000002179', '000002180', '000002183', '000002208', '000002276', '000002282', '000002287', '000002288', '000002301', '000002302', '000002334', '000002337', '000002338', '000002345', '000002346', '000002347', '000002348', '000002384', '000002389', '000002403', '000002404', '000002414', '000002437', '000002465', '000002475', '000002503', '000002577', '000002578', '000002589', '000002590', '000002628', '000002651', '000002652', '000002655', '000002656', '000002709', '000002710', '000002713', '000002715', '000002716', '000002734', '000002751', '000002752', '000002765', '000002783', '000002784', '000002817', '000002818', '000002851', '000002905', '000002906', '000002911', '000002971', '000002972', '000002979', '000002980', '000002995', '000002996', '000003001', '000003002', '000003022', '000003023', '000003024', '000003026', '000003082', '000003086', '000003125', '000003126', '000003136', '000003148', '000003149', '000003150', '000003169', '000003170', '000003171', '000003193', '000003220', '000003221', '000003222', '000003240', '000003277', '000003279', '000003319', '000003337', '000003368', '000003369', '000003370', '000003387', '000003438', '000003442', '000003460', '000003473', '000003475', '000003476', '000003602', '000003603', '000003713', '000003757', '000003793', '000003794', '000003795', '000003796', '000003797', '000003798', '000003894', '000003895', '000003900', '000004144', '000004145', '000004163', '000004272', '000004273', '000004281', '000004611', '000004612', '000004616', '000004633', '000004636', '000004640', '000004641', '000004642', '000004652', '000004654', '000004656', '000004660', '000004662', '000004667', '000004670', '000004676', '000004677', '000004679', '000004686', '000004691', '000004694', '000004695', '000004696', '000004697', '000004699', '000004707', '000004709', '000004711', '000004714', '000004716', '000004726', '000004730', '000004731', '000004735', '000004736', '000004737', '000004738', '000004752', '000004753', '000004758', '000004759', '000004773', '000004774', '000004780', '000004781', '000004782', '000004783', '000004796', '000004797', '000004807', '000004811', '000004812', '000004818', '000004819', '000004822', '000004823', '000004830', '000004831', '000004833', '000004847', '000004858', '000004859', '000004860', '000004864', '000004872', '000004881', '000004890', '000004891', '000004894', '000004915', '000004916', '000004917', '000004926', '000004951', '000004952', '000004979', '000004980', '000005015', '000005016', '000005017', '000005031', '000005032', '000005033', '000005034', '000005035', '000005036', '000005037', '000005039', '000005040', '000005068', '000005073', '000005080', '000005085', '000005163', '000005168', '000005223', '000005238', '000005263', '000005293', '000005360', '000005433', '000005554', '000005571', '000005576', '000005648', '000005653', '000005655', '000005660', '000005755', '000005756', '000005776', '000005780', '000005784', '000005792', '000005799', '000005811', '000005824', '000005825', '000005834', '000005835', '000005840', '000005841', '000005849', '000005850', '000005884', '000005885', '000005902', '000005903', '000005910', '000005916', '000005938', '000005945', '000005954', '000002733', '000008949', '000008950', '000008951', '000008952', '000008953', '000008954', '000008956', '000008957', '000008958', '000008959'

-- AGP round 3
--'000001001', '000001161', '000001164', '000001232', '000001240', '000001243', '000001378', '000001534', '000001600', '000001671', '000001787', '000001833', '000001907', '000001933', '000001970', '000001986', '000002020', '000002027', '000002028', '000002030', '000002051', '000002052', '000002081', '000002082', '000002088', '000002141', '000002142', '000002160', '000002161', '000002162', '000002172', '000002178', '000002212', '000002296', '000002303', '000002316', '000002320', '000002341', '000002342', '000002369', '000002370', '000002383', '000002388', '000002390', '000002395', '000002413', '000002438', '000002476', '000002504', '000002505', '000002581', '000002587', '000002588', '000002608', '000002610', '000002626', '000002641', '000002642', '000002650', '000002684', '000002688', '000002778', '000002794', '000002820', '000002854', '000002872', '000002940', '000003025', '000003029', '000003030', '000003031', '000003079', '000003080', '000003085', '000003087', '000003104', '000003105', '000003118', '000003119', '000003166', '000003167', '000003176', '000003189', '000003223', '000003224', '000003298', '000003299', '000003316', '000003317', '000003320', '000003321', '000003332', '000003339', '000003367', '000003385', '000003421', '000003422', '000003441', '000003443', '000003535', '000003557', '000003601', '000003604', '000003638', '000003639', '000003652', '000003701', '000003702', '000003810', '000003811', '000003820', '000003950', '000004012', '000004061', '000004206', '000004236', '000004237', '000004238', '000004239', '000004391', '000004394', '000004395', '000004396', '000004397', '000004398', '000004401', '000004402', '000004403', '000004404', '000004405', '000004406', '000004407', '000004408', '000004409', '000004410', '000004411', '000004412', '000004414', '000004415', '000004416', '000004418', '000004420', '000004421', '000004422', '000004423', '000004424', '000004425', '000004426', '000004427', '000004428', '000004429', '000004430', '000004431', '000004432', '000004433', '000004434', '000004435', '000004436', '000004437', '000004438', '000004440', '000004441', '000004442', '000004443', '000004444', '000004445', '000004446', '000004447', '000004448', '000004449', '000004450', '000004452', '000004453', '000004454', '000004455', '000004456', '000004458', '000004459', '000004460', '000004462', '000004463', '000004464', '000004465', '000004466', '000004467', '000004468', '000004469', '000004470', '000004471', '000004472', '000004473', '000004474', '000004475', '000004477', '000004478', '000004480', '000004481', '000004483', '000004484', '000004485', '000004486', '000004487', '000004489', '000004490', '000004491', '000004495', '000004496', '000004497', '000004498', '000004499', '000004500', '000004503', '000004504', '000004506', '000004507', '000004509', '000004511', '000004512', '000004513', '000004514', '000004515', '000004603', '000004689', '000004846', '000004854', '000004855', '000004865', '000004873', '000004880', '000004924', '000004925', '000004953', '000004984', '000004986', '000005065', '000005066', '000005067', '000005069', '000005070', '000005071', '000005079', '000005081', '000005083', '000005084', '000005086', '000005088', '000005159', '000005160', '000005161', '000005162', '000005164', '000005165', '000005166', '000005167', '000005219', '000005220', '000005221', '000005222', '000005235', '000005236', '000005237', '000005260', '000005261', '000005262', '000005289', '000005290', '000005291', '000005292', '000005359', '000005361', '000005363', '000005419', '000005420', '000005421', '000005429', '000005430', '000005431', '000005432', '000005555', '000005556', '000005557', '000005558', '000005568', '000005569', '000005570', '000005572', '000005573', '000005574', '000005575', '000005578', '000005634', '000005635', '000005636', '000005637', '000005638', '000005644', '000005645', '000005646', '000005649', '000005650', '000005651', '000005652', '000005654', '000005656', '000005657', '000005658', '000005686', '000005807', '000005812', '000005813', '000005842', '000005889', '000005892', '000005901', '000005915', '000005928', '000005929', '000005931', '000005935', '000006009', '000006030', '000006034', '000006065', '000006113', '000006114', '000006641', '000006651', '000006657', '000006666', '000006673', '000006676', '000006684', '000006685', '000006726', '000006742', '000006743', '000006756', '000006757', '000006778', '000006789', '000006794', '000006795', '000006808', '000006809', '000006818', '000006819', '000006893', '000006894', '000006895', '000006970', '000009353'

--AGP round 4
--'000001062', '000001079', '000001127', '000001139', '000001182', '000001184', '000001208', '000001321', '000001325', '000001376', '000001379', '000001396', '000001450', '000001477', '000001505', '000001513', '000001533', '000001535', '000001546', '000001565', '000001618', '000001673', '000001697', '000001701', '000001732', '000001778', '000001789', '000001792', '000001799', '000001805', '000001811', '000001862', '000001895', '000001902', '000001965', '000002013', '000002014', '000002049', '000002063', '000002099', '000002100', '000002111', '000002112', '000002128', '000002157', '000002159', '000002181',  '000002184', '000002191', '000002198', '000002221', '000002222', '000002253', '000002259', '000002281', '000002360', '000002392', '000002417', '000002418', '000002445', '000002449', '000002450', '000002467', '000002468', '000002489', '000002490', '000002491', '000002492', '000002493', '000002498', '000002530', '000002568', '000002620', '000002627', '000002649', '000002665', '000002669', '000002670', '000002703', '000002704', '000002740', '000002793', '000002807', '000002809', '000002811', '000002813', '000002831', '000002841', '000002842', '000002860', '000002864', '000002878', '000002881', '000002882', '000002921', '000002922', '000002958', '000002965', '000003013', '000003014', '000003027', '000003033', '000003046', '000003063', '000003137', '000003168', '000003172', '000003173', '000003174', '000003175', '000003215', '000003227', '000003228', '000003266', '000003267', '000003334', '000003338', '000003349', '000003350', '000003351', '000003358', '000003359', '000003386', '000003409', '000003424', '000003425', '000003426', '000003431', '000003437', '000003440', '000003452', '000003453', '000003537', '000003538', '000003559', '000003607', '000003714', '000003715', '000003716', '000003809', '000003812', '000003817', '000003818', '000003819', '000003830', '000003891', '000003949', '000003952', '000003981', '000003982', '000003995', '000004010', '000004018', '000004062', '000004076', '000004161', '000004208', '000004220', '000004225', '000004226', '000004294', '000004502', '000004508', '000004596', '000004613', '000004618', '000004625', '000004631', '000004645', '000004650', '000004651', '000004657', '000004672', '000004692', '000004703', '000004721', '000004734', '000004747', '000004765', '000004775', '000004786', '000004787', '000004790', '000004792', '000004793', '000004806', '000004813', '000004814', '000004836', '000004837', '000004849', '000004878', '000004879', '000004903', '000004921', '000004922', '000004923', '000004927', '000004930', '000004931', '000004932', '000004971', '000004972', '000004973', '000004974', '000004985', '000005012', '000005019', '000005020', '000005038', '000005062', '000005063', '000005064', '000005072', '000005082', '000005087', '000005259', '000005362', '000005422', '000005423', '000005454', '000005552', '000005553', '000005567', '000005647', '000005685', '000005692', '000005702', '000005703', '000005713', '000005716', '000005725', '000005726', '000005727', '000005750', '000005753', '000005754', '000005782', '000005785', '000005789', '000005790', '000005791', '000005814', '000005839', '000005843', '000005844', '000005845', '000005846', '000005887', '000005891', '000005893', '000005900', '000005907', '000005911', '000005918', '000005920', '000005921', '000005924', '000005927', '000005930', '000005936', '000005937', '000005939', '000005946', '000005965', '000005966', '000005970', '000005971', '000005981', '000005983', '000005989', '000005990', '000005992', '000005997', '000005999', '000006001', '000006020', '000006021', '000006026', '000006037', '000006042', '000006049', '000006050', '000006053', '000006064', '000006071', '000006072', '000006078', '000006080', '000006098', '000006100', '000006106', '000006111', '000006134', '000006135', '000006619', '000006620', '000006625', '000006626', '000006634', '000006635', '000006636', '000006637', '000006645', '000006650', '000006659', '000006661', '000006662', '000006664', '000006665', '000006670', '000006678', '000006679', '000006688', '000006690', '000006691', '000006694', '000006695', '000006702', '000006703', '000006710', '000006711', '000006714', '000006715', '000006716', '000006717', '000006728', '000006729', '000006733', '000006736', '000006737', '000006740', '000006741', '000006752', '000006762', '000006766', '000006767', '000006776', '000006777', '000006788', '000006796', '000006797', '000006800', '000006801', '000006802', '000006803', '000006804', '000006848', '000006850', '000006852', '000006863', '000006864', '000006912', '000006925', '000006926', '000006927', '000006928', '000006932', '000006937', '000006938', '000006939', '000006941', '000006942', '000006943', '000006944', '000006949', '000006950', '000006971', '000006993', '000007005', '000007009', '000007010', '000007025', '000007037', '000007039', '000007040', '000007043', '000007068', '000007139', '000007174', '000007183', '000007184', '000007645', '000007666', '000007669', '000007675', '000007678', '000007684', '000007727', '000007728', '000007729', '000007732', '000007734', '000007746', '000008955', '000008962', '000008972', '000008982', '000008989', '000009009', '000009011', '000009013', '000009035', '000009085', '000009108', '000009109', '000009111', '000009117', '000009118', '000009134', '000009139', '000009149', '000009180', '000009195', '000009204', '000009238', '000009353', '000009372', '000009383', '000009413', '000009427', '000009430', '000009526', '000009528', '000009529', '000009530', '000009531', '000009532', '000009535', '000009624', '000009766', '000009767'

-- AGP round 5
'000001022', '000001069', '000001114', '000001120', '000001125', '000001156', '000001214', '000001232', '000001241', '000001265', '000001270', '000001303', '000001315', '000001345', '000001389', '000001390', '000001391', '000001401', '000001410', '000001444', '000001464', '000001484', '000001493', '000001544', '000001555', '000001580', '000001582', '000001590', '000001593', '000001600', '000001621', '000001630', '000001631', '000001640', '000001662', '000001699', '000001719', '000001748', '000001759', '000001787', '000001795', '000001837', '000001851', '000001888', '000001905', '000001906', '000001912', '000001916', '000001944', '000002005', '000002023', '000002029', '000002068', '000002078', '000002079', '000002080', '000002125', '000002126', '000002127', '000002146', '000002152', '000002160', '000002162', '000002171', '000002175', '000002176', '000002183', '000002201', '000002202', '000002260', '000002282', '000002288', '000002301', '000002302', '000002309', '000002350', '000002370', '000002435', '000002451', '000002452', '000002457', '000002458', '000002472', '000002497', '000002511', '000002512', '000002529', '000002533', '000002534', '000002567', '000002581', '000002616', '000002619', '000002645', '000002646', '000002666', '000002688', '000002735', '000002771', '000002772', '000002778', '000002801', '000002802', '000002808', '000002810', '000002812', '000002824', '000002874', '000002877', '000002897', '000002903', '000002904', '000002911', '000002944', '000002997', '000003003', '000003004', '000003015', '000003016', '000003017', '000003018', '000003031', '000003061', '000003062', '000003079', '000003081', '000003083', '000003088', '000003089', '000003090', '000003145', '000003146', '000003147', '000003154', '000003155', '000003177', '000003224', '000003226', '000003265', '000003336', '000003360', '000003368', '000003410', '000003411', '000003436', '000003441', '000003444', '000003451', '000003529', '000003530', '000003531', '000003532', '000003549', '000003550', '000003551', '000003557', '000003603', '000003606', '000003650', '000003651', '000003729', '000003730', '000003731', '000003732', '000003761', '000003799', '000003838', '000003893', '000003894', '000003896', '000003953', '000003954', '000003955', '000003956', '000003983', '000004025', '000004026', '000004142', '000004144', '000004147', '000004148', '000004162', '000004187', '000004278', '000004280', '000004602', '000004611', '000004617', '000004633', '000004662', '000004666', '000004679', '000004693', '000004695', '000004705', '000004711', '000004753', '000004780', '000004782', '000004848', '000004859', '000004891', '000004894', '000004896', '000004904', '000004905', '000004916', '000004918', '000004919', '000004920', '000004926', '000004928', '000004929', '000005007', '000005013', '000005014', '000005021', '000005023', '000005024', '000005025', '000005026', '000005041', '000005059', '000005060', '000005061', '000005224', '000005225', '000005226', '000005227', '000005228', '000005234', '000005410', '000005455', '000005456', '000005457', '000005458', '000005549', '000005550', '000005551', '000005557', '000005564', '000005565', '000005566', '000005568', '000005577', '000005594', '000005595', '000005596', '000005597', '000005598', '000005662', '000005697', '000005712', '000005717', '000005738', '000005755', '000005757', '000005758', '000005768', '000005770', '000005771', '000005786', '000005787', '000005788', '000005805', '000005806', '000005809', '000005810', '000005847', '000005856', '000005868', '000005870', '000005871', '000005879', '000005880', '000005890', '000005892', '000005935', '000005948', '000005957', '000005967', '000005980', '000005986', '000005987', '000006007', '000006035', '000006044', '000006047', '000006074', '000006084', '000006092', '000006097', '000006104', '000006110', '000006114', '000006120', '000006125', '000006628', '000006631', '000006647', '000006653', '000006654', '000006655', '000006668', '000006675', '000006689', '000006732', '000006760', '000006761', '000006763', '000006779', '000006805', '000006819', '000006837', '000006838', '000006839', '000006841', '000006849', '000006851', '000006853', '000006865', '000006879', '000006880', '000006909', '000006910', '000006911', '000006929', '000006930', '000006931', '000006940', '000006952', '000006972', '000006973', '000006974', '000006975', '000006976', '000007011', '000007012', '000007038', '000007041', '000007044', '000007052', '000007053', '000007054', '000007055', '000007056', '000007057', '000007058', '000007151', '000007152', '000007176', '000007177', '000007178', '000007180', '000007181', '000007182', '000007641', '000007643', '000007663', '000007664', '000007668', '000007670', '000007673', '000007674', '000007676', '000007677', '000007683', '000007688', '000007689', '000007693', '000007694', '000007695', '000007696', '000007698', '000007700', '000007719', '000007736', '000007740', '000007741', '000007745', '000007748', '000007749', '000007811', '000007865', '000008193', '000008194', '000008195', '000008196', '000008197', '000008198', '000008199', '000008200', '000008201', '000008202', '000008203', '000008204', '000008963', '000008980', '000008981', '000008982', '000008983', '000008990', '000008998', '000009003', '000009004', '000009015', '000009021', '000009022', '000009033', '000009034', '000009036', '000009041', '000009042', '000009051', '000009052', '000009058', '000009059', '000009060', '000009061', '000009079', '000009080', '000009081', '000009090', '000009092', '000009093', '000009094', '000009097', '000009098', '000009101', '000009102', '000009114', '000009126', '000009129', '000009131', '000009140', '000009141', '000009142', '000009144', '000009150', '000009157', '000009158', '000009174', '000009181', '000009182', '000009196', '000009198', '000009201', '000009202', '000009209', '000009210', '000009211', '000009213', '000009214', '000009215', '000009221', '000009222', '000009224', '000009225', '000009227', '000009228', '000009230', '000009231', '000009236', '000009239', '000009240', '000009355', '000009365', '000009368', '000009375', '000009385', '000009386', '000009392', '000009397', '000009402', '000009403', '000009410', '000009419', '000009433', '000009434', '000009444', '000009445', '000009449', '000009455', '000009457', '000009458', '000009463', '000009464', '000009483', '000009484', '000009494', '000009495', '000009496', '000009507', '000009527', '000009539', '000009540', '000009552', '000009555', '000009558', '000009560', '000009562', '000009566', '000009567', '000009571', '000009580', '000009583', '000009586', '000009594', '000009596', '000009601', '000009606', '000009607', '000009621', '000009623', '000009626', '000009627', '000009628', '000009640', '000009641', '000009644', '000009655', '000009674', '000009684', '000009685', '000009705', '000009711', '000009712', '000009713', '000009714', '000009715', '000009733', '000009734'
)
order by sample_name;


/*

select  b.*
from    ag_kit_barcodes b
        inner join ag_kit k
        on b.ag_kit_id = k.ag_kit_id
        inner join ag_login l
        on k.ag_login_id = l.ag_login_id
        left join ag_human_survey s
        on l.ag_login_id = s.ag_login_id
where   b.barcode in
(
'000007111',
'000007114'
);

*/
