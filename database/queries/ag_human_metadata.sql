/*

Forehead = UBERON:skin; UBERON:skin of head; UBERON:sebum; ENVO:human-associated habitat;ÊENVO:human-associated habitat; ENVO:sebum;
Left hand= UBERON skin; UBERON:skin of hand: UBERON:sebum; ENVO:human-associated habitat;ÊENVO:human-associated habitat; ENVO:sebum;
Right hand= UBERON skin; UBERON:skin of hand: UBERON:sebum; ENVO:human-associated habitat;ÊENVO:human-associated habitat; ENVO:sebum;
UBERON:oral cavity; UBERON:mouth; UBERON:saliva; ENVO:human-associated habitat;ÊENVO:human-associated habitat; ENVO:saliva;
Stool= UBERON:feces;UBERON:feces:UBERON:feces; ENVO:human-associated habitat;ÊENVO:human-associated habitat; ENVO:feces:
Animal habitat=ÊUBERON:feces;UBERON:feces:UBERON:feces;ÊENVO:animalia-associated habitat, ENVO:animalia-associated habitat, ENVO:feces/sebum;
Biofilm = ENVO:terrestrial biome; ENVO:surface; ENVO:biofilm;
Fermented food= ENVO:terrestrial biome; ENVO:anthropogenic habitat; ENVO:fermented food;
Food= ENVO:terrestrial biome; ENVO:anthropogenic habitat; ENVO:food;
Indoor surface = Biome from area or ENVO:terrestrial biome; ENVO:anthropogenic feature; ENVO:surface

- Is there any way that the entries in the fields that come from the download can be lower case for most of the participant entered data?

(not from this query - only MIGRAINEMEDS exists)  There are 2 identical columns generated MIGRAINE_MEDS and MIGRAINEMEDS - seems like duplication.
(done) Can you generate BMI before download from height, weight?
(done) GENDER to sex




*/


select  akb.barcode as sample_name, akb.barcode as ANONYMIZED_NAME, akb.sample_date, 
        akb.sample_time, akb.site_sampled,
        case akb.site_sampled
            when 'Stool' then 'UBERON:feces'
            else akb.site_sampled
        end as env_matter, 
        lower(city) as city, upper(state) as state, 
        zip, country, al.latitude, al.longitude, 'years' as age_unit,
        case
            when ahs.birth_date is not null then
                cast((current_date - to_date(ahs.birth_date, 'MM/DD/YYYY')) / 365.0 as int)
            else null
        end as age,
        REPLACE(REPLACE(REPLACE(ACNE_MEDICATION, CHR(10)), CHR(13)), CHR(9)) ACNE_MEDICATION,
        REPLACE(REPLACE(REPLACE(ACNE_MEDICATION_OTC, CHR(10)), CHR(13)), CHR(9)) ACNE_MEDICATION_OTC, 
        REPLACE(REPLACE(REPLACE(ALCOHOL_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) ALCOHOL_FREQUENCY, 
        REPLACE(REPLACE(REPLACE(ANIMAL_PER, CHR(10)), CHR(13)), CHR(9)) ANIMAL_PER, 
        REPLACE(REPLACE(REPLACE(ANTIBIOTIC_CONDITION, CHR(10)), CHR(13)), CHR(9)) ANTIBIOTIC_CONDITION, 
        REPLACE(REPLACE(REPLACE(ANTIBIOTIC_SELECT, CHR(10)), CHR(13)), CHR(9)) ANTIBIOTIC_SELECT, 
        REPLACE(REPLACE(REPLACE(APPENDIX_REMOVED, CHR(10)), CHR(13)), CHR(9)) APPENDIX_REMOVED, 
        REPLACE(REPLACE(REPLACE(ASTHMA, CHR(10)), CHR(13)), CHR(9)) ASTHMA, 
        REPLACE(REPLACE(REPLACE(BIRTH_DATE, CHR(10)), CHR(13)), CHR(9)) BIRTH_DATE, 
        REPLACE(REPLACE(REPLACE(CARBOHYDRATE_PER, CHR(10)), CHR(13)), CHR(9)) CARBOHYDRATE_PER, 
        REPLACE(REPLACE(REPLACE(CAT, CHR(10)), CHR(13)), CHR(9)) CAT, 
        REPLACE(REPLACE(REPLACE(CHICKENPOX, CHR(10)), CHR(13)), CHR(9)) CHICKENPOX, 
        REPLACE(REPLACE(REPLACE(COMMUNAL_DINING, CHR(10)), CHR(13)), CHR(9)) COMMUNAL_DINING, 
        REPLACE(REPLACE(REPLACE(CONDITIONS_MEDICATION, CHR(10)), CHR(13)), CHR(9)) CONDITIONS_MEDICATION, 
        REPLACE(REPLACE(REPLACE(CONTRACEPTIVE, CHR(10)), CHR(13)), CHR(9)) CONTRACEPTIVE, 
        REPLACE(REPLACE(REPLACE(COSMETICS_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) COSMETICS_FREQUENCY, 
        (
            select  term
            from    controlled_vocab_values
            where   vocab_value_id = ahs.COUNTRY_OF_BIRTH
        ) as COUNTRY_OF_BIRTH,
        REPLACE(REPLACE(REPLACE(CSECTION, CHR(10)), CHR(13)), CHR(9)) CSECTION, 
        REPLACE(REPLACE(REPLACE(CURRENT_RESIDENCE_DURATION, CHR(10)), CHR(13)), CHR(9)) CURRENT_RESIDENCE_DURATION, 
        REPLACE(REPLACE(REPLACE(DECEASED_PARENT, CHR(10)), CHR(13)), CHR(9)) DECEASED_PARENT, 
        REPLACE(REPLACE(REPLACE(DEODERANT_USE, CHR(10)), CHR(13)), CHR(9)) DEODERANT_USE, 
        REPLACE(REPLACE(REPLACE(DIABETES, CHR(10)), CHR(13)), CHR(9)) DIABETES, 
        REPLACE(REPLACE(REPLACE(DIABETES_DIAGNOSE_DATE, CHR(10)), CHR(13)), CHR(9)) DIABETES_DIAGNOSE_DATE, 
        REPLACE(REPLACE(REPLACE(DIABETES_MEDICATION, CHR(10)), CHR(13)), CHR(9)) DIABETES_MEDICATION, 
        REPLACE(REPLACE(REPLACE(DIET_TYPE, CHR(10)), CHR(13)), CHR(9)) DIET_TYPE, 
        REPLACE(REPLACE(REPLACE(DOG, CHR(10)), CHR(13)), CHR(9)) DOG, 
        REPLACE(REPLACE(REPLACE(DRINKING_WATER_SOURCE, CHR(10)), CHR(13)), CHR(9)) DRINKING_WATER_SOURCE, 
        REPLACE(REPLACE(REPLACE(EXERCISE_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) EXERCISE_FREQUENCY, 
        REPLACE(REPLACE(REPLACE(EXERCISE_LOCATION, CHR(10)), CHR(13)), CHR(9)) EXERCISE_LOCATION, 
        REPLACE(REPLACE(REPLACE(FAT_PER, CHR(10)), CHR(13)), CHR(9)) FAT_PER, 
        REPLACE(REPLACE(REPLACE(FIBER_GRAMS, CHR(10)), CHR(13)), CHR(9)) FIBER_GRAMS, 
        REPLACE(REPLACE(REPLACE(FLOSSING_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) FLOSSING_FREQUENCY, 
        REPLACE(REPLACE(REPLACE(FLU_VACCINE_DATE, CHR(10)), CHR(13)), CHR(9)) FLU_VACCINE_DATE, 
        case 
            when FOODALLERGIES_OTHER = 'on' then 'yes'
            else FOODALLERGIES_OTHER
        end as FOODALLERGIES_OTHER, 
        REPLACE(REPLACE(REPLACE(FOODALLERGIES_OTHER_TEXT, CHR(10)), CHR(13)), CHR(9)) FOODALLERGIES_OTHER_TEXT, 
        case
            when FOODALLERGIES_PEANUTS = 'on' then 'yes'
            else FOODALLERGIES_PEANUTS
        end as FOODALLERGIES_PEANUTS,
        case
            when FOODALLERGIES_SHELLFISH = 'on' then 'yes'
            else FOODALLERGIES_SHELLFISH
        end as FOODALLERGIES_SHELLFISH, 
        case
            when FOODALLERGIES_TREENUTS = 'on' then 'yes'
            else FOODALLERGIES_TREENUTS
        end as FOODALLERGIES_TREENUTS, 
        case
            when FRAT = 'on' then 'yes'
            else FRAT
        end as FRAT, 
        REPLACE(REPLACE(REPLACE(GENDER, CHR(10)), CHR(13)), CHR(9)) SEX, 
        REPLACE(REPLACE(REPLACE(GLUTEN, CHR(10)), CHR(13)), CHR(9)) GLUTEN, 
        REPLACE(REPLACE(REPLACE(HAND, CHR(10)), CHR(13)), CHR(9)) HAND, 
        REPLACE(REPLACE(REPLACE(HEIGHT_CM, CHR(10)), CHR(13)), CHR(9)) HEIGHT_CM, 
        REPLACE(REPLACE(REPLACE(HEIGHT_IN, CHR(10)), CHR(13)), CHR(9)) HEIGHT_IN, 
        REPLACE(REPLACE(REPLACE(IBD, CHR(10)), CHR(13)), CHR(9)) IBD, 
        REPLACE(REPLACE(REPLACE(LACTOSE, CHR(10)), CHR(13)), CHR(9)) LACTOSE, 
        REPLACE(REPLACE(REPLACE(LAST_TRAVEL, CHR(10)), CHR(13)), CHR(9)) LAST_TRAVEL, 
        REPLACE(REPLACE(REPLACE(LIVINGWITH, CHR(10)), CHR(13)), CHR(9)) LIVINGWITH, 
        REPLACE(REPLACE(REPLACE(MAINFACTOR_OTHER_1, CHR(10)), CHR(13)), CHR(9)) MAINFACTOR_OTHER_1, 
        REPLACE(REPLACE(REPLACE(MAINFACTOR_OTHER_2, CHR(10)), CHR(13)), CHR(9)) MAINFACTOR_OTHER_2, 
        REPLACE(REPLACE(REPLACE(MAINFACTOR_OTHER_3, CHR(10)), CHR(13)), CHR(9)) MAINFACTOR_OTHER_3, 
        REPLACE(REPLACE(REPLACE(MIGRAINE, CHR(10)), CHR(13)), CHR(9)) MIGRAINE, 
        case
            when MIGRAINEMEDS = 'on' then 'yes'
            else MIGRAINEMEDS
        end as MIGRAINEMEDS, 
        case
            when MIGRAINE_AGGRAVATION = 'on' then 'yes'
            else MIGRAINE_AGGRAVATION
        end as MIGRAINE_AGGRAVATION, 
        case 
            when MIGRAINE_AURA = 'on' then 'yes'
            else MIGRAINE_AURA
        end as MIGRAINE_AURA, 
        REPLACE(REPLACE(REPLACE(MIGRAINE_FACTOR_1, CHR(10)), CHR(13)), CHR(9)) MIGRAINE_FACTOR_1, 
        REPLACE(REPLACE(REPLACE(MIGRAINE_FACTOR_2, CHR(10)), CHR(13)), CHR(9)) MIGRAINE_FACTOR_2, 
        REPLACE(REPLACE(REPLACE(MIGRAINE_FACTOR_3, CHR(10)), CHR(13)), CHR(9)) MIGRAINE_FACTOR_3, 
        REPLACE(REPLACE(REPLACE(MIGRAINE_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) MIGRAINE_FREQUENCY, 
        case
            when MIGRAINE_NAUSEA = 'on' then 'yes'
            else MIGRAINE_NAUSEA
        end as MIGRAINE_NAUSEA, 
        case 
            when MIGRAINE_PAIN = 'on' then 'yes'
            else MIGRAINE_PAIN
        end as MIGRAINE_PAIN, 
        case
            when MIGRAINE_PHONOPHOBIA = 'on' then 'yes'
            else MIGRAINE_PHONOPHOBIA
        end as MIGRAINE_PHONOPHOBIA, 
        case
            when MIGRAINE_PHOTOPHOBIA = 'on' then 'yes'
            else MIGRAINE_PHOTOPHOBIA
        end as MIGRAINE_PHOTOPHOBIA, 
        case
            when MIGRAINE_RELATIVES = 'on' then 'yes'
            else MIGRAINE_RELATIVES
        end as MIGRAINE_RELATIVES, 
        MULTIVITAMIN, 
        NAILS, 
        case
            when NONFOODALLERGIES_BEESTINGS = 'on' then 'yes'
            else NONFOODALLERGIES_BEESTINGS
        end as NONFOODALLERGIES_BEESTINGS, 
        case
            when NONFOODALLERGIES_DANDER = 'on' then 'yes'
            else NONFOODALLERGIES_DANDER
        end as NONFOODALLERGIES_DANDER, 
        case
            when NONFOODALLERGIES_DRUG = 'on' then 'yes'
            else NONFOODALLERGIES_DRUG
        end as NONFOODALLERGIES_DRUG, 
        case
            when NONFOODALLERGIES_NO = 'on' then 'yes'
            else NONFOODALLERGIES_NO
        end as NONFOODALLERGIES_NO, 
        case
            when NONFOODALLERGIES_POISONIVY = 'on' then 'yes'
            else NONFOODALLERGIES_POISONIVY
        end as NONFOODALLERGIES_POISONIVY, 
        case
            when NONFOODALLERGIES_SUN = 'on' then 'yes'
            else NONFOODALLERGIES_SUN
        end as NONFOODALLERGIES_SUN, 
        REPLACE(REPLACE(REPLACE(PERCENTAGE_FROM_CARBS, CHR(10)), CHR(13)), CHR(9)) PERCENTAGE_FROM_CARBS, 
        REPLACE(REPLACE(REPLACE(PKU, CHR(10)), CHR(13)), CHR(9)) PKU, 
        REPLACE(REPLACE(REPLACE(PLANT_PER, CHR(10)), CHR(13)), CHR(9)) PLANT_PER, 
        REPLACE(REPLACE(REPLACE(POOL_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) POOL_FREQUENCY, 
        case
            when PREGNANT = 'on' then 'yes'
            else PREGNANT
        end as PREGNANT, 
        REPLACE(REPLACE(REPLACE(PREGNANT_DUE_DATE, CHR(10)), CHR(13)), CHR(9)) PREGNANT_DUE_DATE, 
        REPLACE(REPLACE(REPLACE(PRIMARY_CARB, CHR(10)), CHR(13)), CHR(9)) PRIMARY_CARB, 
        REPLACE(REPLACE(REPLACE(PRIMARY_VEGETABLE, CHR(10)), CHR(13)), CHR(9)) PRIMARY_VEGETABLE, 
        REPLACE(REPLACE(REPLACE(PROTEIN_PER, CHR(10)), CHR(13)), CHR(9)) PROTEIN_PER, 
        REPLACE(REPLACE(REPLACE(RACE, CHR(10)), CHR(13)), CHR(9)) RACE, 
        REPLACE(REPLACE(REPLACE(RACE_OTHER, CHR(10)), CHR(13)), CHR(9)) RACE_OTHER, 
        REPLACE(REPLACE(REPLACE(ROOMMATES, CHR(10)), CHR(13)), CHR(9)) ROOMMATES, 
        REPLACE(REPLACE(REPLACE(SEASONAL_ALLERGIES, CHR(10)), CHR(13)), CHR(9)) SEASONAL_ALLERGIES, 
        REPLACE(REPLACE(REPLACE(SHARED_HOUSING, CHR(10)), CHR(13)), CHR(9)) SHARED_HOUSING, 
        REPLACE(REPLACE(REPLACE(SKIN_CONDITION, CHR(10)), CHR(13)), CHR(9)) SKIN_CONDITION, 
        REPLACE(REPLACE(REPLACE(SLEEP_DURATION, CHR(10)), CHR(13)), CHR(9)) SLEEP_DURATION, 
        REPLACE(REPLACE(REPLACE(SMOKING_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) SMOKING_FREQUENCY, 
        REPLACE(REPLACE(REPLACE(SOFTENER, CHR(10)), CHR(13)), CHR(9)) SOFTENER, 
        REPLACE(REPLACE(REPLACE(SPECIAL_RESTRICTIONS, CHR(10)), CHR(13)), CHR(9)) SPECIAL_RESTRICTIONS, 
        REPLACE(REPLACE(REPLACE(SUPPLEMENTS, CHR(10)), CHR(13)), CHR(9)) SUPPLEMENTS, 
        REPLACE(REPLACE(REPLACE(TANNING_BEDS, CHR(10)), CHR(13)), CHR(9)) TANNING_BEDS, 
        REPLACE(REPLACE(REPLACE(TANNING_SPRAYS, CHR(10)), CHR(13)), CHR(9)) TANNING_SPRAYS, 
        REPLACE(REPLACE(REPLACE(TEETHBRUSHING_FREQUENCY, CHR(10)), CHR(13)), CHR(9)) TEETHBRUSHING_FREQUENCY, 
        REPLACE(REPLACE(REPLACE(TONSILS_REMOVED, CHR(10)), CHR(13)), CHR(9)) TONSILS_REMOVED, 
        REPLACE(REPLACE(REPLACE(TYPES_OF_PLANTS, CHR(10)), CHR(13)), CHR(9)) TYPES_OF_PLANTS, 
        REPLACE(REPLACE(REPLACE(WEIGHT_CHANGE, CHR(10)), CHR(13)), CHR(9)) WEIGHT_CHANGE, 
        REPLACE(REPLACE(REPLACE(WEIGHT_KG, CHR(10)), CHR(13)), CHR(9)) WEIGHT_KG, 
        REPLACE(REPLACE(REPLACE(WEIGHT_LBS, CHR(10)), CHR(13)), CHR(9)) WEIGHT_LBS,
        case
            when weight_lbs > 0 and height_in > 0 then
            case 
                when (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703 between 5 and 100 
                    then (cast(weight_lbs as number) / ((cast(height_in as number) * cast(height_in as number)))) * 703
                else null
            end
            else null
        end as BMI,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'antibiotic_med_%'
        ) as antibiotic_meds,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'diabetes_medications_%'
        ) as diabetes_medications,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'dietrestrictions_%'
        ) as diet_restrictions,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'general_meds_%'
        ) as general_meds,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'migraine_medication_%'
        ) as migraine_medications,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'pet_%'
        ) as pets,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'pet_contact_%'
        ) as pet_contact,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'pet_location_%'
        ) as pet_locations,
        /*
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'related_participant_%'
        ) as related_participants,
        */
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'relation_%'
        ) as relations,
        (
            select  listagg(item_value, ', ') within group(order by item_name)
            from    ag_survey_multiples
            where   ag_login_id = al.ag_login_id
                    and participant_name = akb.participant_name
                    and item_name like 'supplements_fields_%'
        ) as supplements_fields,
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
        ) as travel_locations
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
        
        and case
            when ahs.birth_date is not null then
                cast((current_date - to_date(ahs.birth_date, 'MM/DD/YYYY')) / 365.0 as int)
            else null
        end between 0 and 120
        
        and akb.barcode in
(
'000001002', 
'000001004', 
'000001008', 
'000001018', 
'000001031', 
'000001032', 
'000001038', 
'000001046', 
'000001047', 
'000001048', 
'000001049', 
'000001056', 
'000001058', 
'000001059', 
'000001060', 
'000001065', 
'000001067', 
'000001069', 
'000001077', 
'000001078', 
'000001086', 
'000001089', 
'000001097', 
'000001098', 
'000001099', 
'000001100', 
'000001109', 
'000001110', 
'000001115', 
'000001116', 
'000001118', 
'000001120', 
'000001121', 
'000001126', 
'000001128', 
'000001130', 
'000001135', 
'000001138', 
'000001140', 
'000001141', 
'000001142', 
'000001150', 
'000001151', 
'000001152', 
'000001154', 
'000001155', 
'000001170', 
'000001171', 
'000001173', 
'000001174', 
'000001180', 
'000001189', 
'000001192', 
'000001194', 
'000001196', 
'000001214', 
'000001216', 
'000001218', 
'000001221', 
'000001225', 
'000001228', 
'000001231', 
'000001248', 
'000001256', 
'000001265', 
'000001269', 
'000001270', 
'000001272', 
'000001275', 
'000001278', 
'000001284', 
'000001285', 
'000001288', 
'000001291', 
'000001294', 
'000001299', 
'000001301', 
'000001303', 
'000001305', 
'000001311', 
'000001312', 
'000001315', 
'000001317', 
'000001322', 
'000001333', 
'000001336', 
'000001344', 
'000001345', 
'000001350', 
'000001353', 
'000001354', 
'000001362', 
'000001363', 
'000001364', 
'000001367', 
'000001375', 
'000001377', 
'000001380', 
'000001386', 
'000001397', 
'000001398', 
'000001399', 
'000001404', 
'000001405', 
'000001411', 
'000001417', 
'000001419', 
'000001421', 
'000001422', 
'000001427', 
'000001432', 
'000001435', 
'000001436', 
'000001446', 
'000001451', 
'000001482', 
'000001487', 
'000001488', 
'000001504', 
'000001516', 
'000001521', 
'000001528', 
'000001530', 
'000001531', 
'000001538', 
'000001541', 
'000001543', 
'000001545', 
'000001547', 
'000001548', 
'000001551', 
'000001552', 
'000001555', 
'000001556', 
'000001559', 
'000001574', 
'000001575', 
'000001576', 
'000001583', 
'000001587', 
'000001589', 
'000001593', 
'000001595', 
'000001597', 
'000001611', 
'000001615', 
'000001621', 
'000001622', 
'000001630', 
'000001632', 
'000001645', 
'000001649', 
'000001650', 
'000001651', 
'000001652', 
'000001654', 
'000001658', 
'000001659', 
'000001660', 
'000001661', 
'000001662', 
'000001669', 
'000001678', 
'000001685', 
'000001694', 
'000001704', 
'000001705', 
'000001711', 
'000001713', 
'000001714', 
'000001726', 
'000001731', 
'000001735', 
'000001745', 
'000001747', 
'000001749', 
'000001751', 
'000001755', 
'000001756', 
'000001762', 
'000001763', 
'000001764', 
'000001769', 
'000001770', 
'000001772', 
'000001786', 
'000001793', 
'000001794', 
'000001795', 
'000001797', 
'000001801', 
'000001802', 
'000001808', 
'000001812', 
'000001826', 
'000001830', 
'000001832', 
'000001835', 
'000001837', 
'000001842', 
'000001852', 
'000001854', 
'000001856', 
'000001860', 
'000001866', 
'000001874', 
'000001878', 
'000001884', 
'000001886', 
'000001888', 
'000001916', 
'000001923', 
'000001947', 
'000001948', 
'000001955', 
'000001961', 
'000001962', 
'000001969', 
'000001978', 
'000001979', 
'000001980', 
'000001985', 
'000001988', 
'000002035', 
'000002041', 
'000002042', 
'000002056', 
'000002067', 
'000002068', 
'000002087', 
'000002109', 
'000002147', 
'000002148', 
'000002151', 
'000002165', 
'000002166', 
'000002173', 
'000002175', 
'000002176', 
'000002185', 
'000002186', 
'000002199', 
'000002200', 
'000002205', 
'000002211', 
'000002219', 
'000002220', 
'000002229', 
'000002230', 
'000002237', 
'000002243', 
'000002244', 
'000002261', 
'000002262', 
'000002273', 
'000002274', 
'000002295', 
'000002304', 
'000002309', 
'000002310', 
'000002315', 
'000002319', 
'000002329', 
'000002330', 
'000002331', 
'000002349', 
'000002350', 
'000002359', 
'000002371', 
'000002372', 
'000002387', 
'000002391', 
'000002396', 
'000002419', 
'000002443', 
'000002444', 
'000002446', 
'000002466', 
'000002471', 
'000002472', 
'000002481', 
'000002482', 
'000002494', 
'000002506', 
'000002545', 
'000002546', 
'000002563', 
'000002564', 
'000002575', 
'000002576', 
'000002597', 
'000002598', 
'000002605', 
'000002606', 
'000002607', 
'000002609', 
'000002616', 
'000002619', 
'000002625', 
'000002631', 
'000002632', 
'000002637', 
'000002638', 
'000002683', 
'000002687', 
'000002689', 
'000002690', 
'000002735', 
'000002736', 
'000002739', 
'000002773', 
'000002774', 
'000002777', 
'000002781', 
'000002782', 
'000002805', 
'000002806', 
'000002814', 
'000002819', 
'000002825', 
'000002826', 
'000002833', 
'000002834', 
'000002849', 
'000002850', 
'000002853', 
'000002859', 
'000002863', 
'000002865', 
'000002866', 
'000002871', 
'000002873', 
'000002883', 
'000002884', 
'000002885', 
'000002886', 
'000002893', 
'000002894', 
'000002897', 
'000002898', 
'000002939', 
'000002943', 
'000002944', 
'000002951', 
'000002952', 
'000003028', 
'000003032', 
'000003047', 
'000003048', 
'000003058', 
'000003059', 
'000003060', 
'000003091', 
'000003092', 
'000003093', 
'000003103', 
'000003120', 
'000003154', 
'000003155', 
'000003199', 
'000003200', 
'000003201', 
'000003214', 
'000003216', 
'000003225', 
'000003280', 
'000003281', 
'000003282', 
'000003287', 
'000003300', 
'000003331', 
'000003364', 
'000003365', 
'000003366', 
'000003423', 
'000003430', 
'000003432', 
'000003439', 
'000003458', 
'000003505', 
'000003506', 
'000003507', 
'000003508', 
'000003533', 
'000003534', 
'000003536', 
'000003640', 
'000003666', 
'000003703', 
'000003879', 
'000003880', 
'000003937', 
'000003951', 
'000003969', 
'000003970', 
'000003971', 
'000003972', 
'000003973', 
'000004009', 
'000004011', 
'000004039', 
'000004040', 
'000004071', 
'000004072', 
'000004075', 
'000004139', 
'000004141', 
'000004158', 
'000004159', 
'000004160', 
'000004185', 
'000004187', 
'000004188', 
'000004189', 
'000004190', 
'000004191', 
'000004207', 
'000004221', 
'000004222', 
'000004223', 
'000004224', 
'000004234', 
'000004265', 
'000004266', 
'000004267', 
'000004672', 
'000004680'
);

