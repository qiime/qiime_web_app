create table ag_human_survey
(
    ag_login_id raw(16) not null, 
    participant_name varchar2(200),
    consent varchar2(20),
    is_7_to_13 varchar2(20),
    parent_1_name varchar2(200),
    parent_2_name varchar2(200),
    deceased_parent varchar2(20),
    
    country_of_birth varchar2(100),
    birth_date varchar2(100),
    gender varchar2(100),
    height_in varchar2(100),
    height_cm varchar2(100),
    weight_lbs varchar2(100),
    weight_kg  varchar2(100),
    phone_num varchar2(100),
    zip_code varchar2(100),
    
    diet_type varchar2(100),
    multivitamin varchar2(100),
    supplements varchar2(100),
    lactose varchar2(100),
    gluten varchar2(100),
    foodallergies_peanuts varchar2(100),
    foodallergies_treenuts varchar2(100),
    foodallergies_shellfish varchar2(100),
    foodallergies_other varchar2(100),
    foodallergies_other_text varchar(400),
    special_restrictions varchar2(100),
    drinking_water_source varchar2(100),
    
    race varchar2(100),
    race_other varchar2(100),
    current_residence_duration varchar2(100),
    last_travel varchar2(100),
    livingwith varchar2(100),
    dog varchar2(100),
    cat varchar2(100),
    hand varchar2(100),
    shared_housing varchar2(100),

    tanning_beds varchar2(100),
    tanning_sprays varchar2(100),
    exercise_frequency varchar2(100),
    exercise_location varchar2(100),
    nails varchar2(100),
    pool_frequency varchar2(100),
    smoking_frequency varchar2(100),
    alcohol_frequency varchar2(100),
    teethbrushing_frequency varchar2(100),
    flossing_frequency varchar2(100),
    cosmetics_frequency varchar2(100),
    deoderant_use varchar2(100),
    sleep_duration varchar2(100),
    softener varchar2(100),
    
    antibiotic_select varchar2(100),
    antibiotic_condition varchar2(100),
    flu_vaccine_date varchar2(100),
    weight_change varchar2(100),
    tonsils_removed varchar2(100),
    appendix_removed varchar2(100),
    chickenpox varchar2(100),
    acne_medication varchar2(100),
    acne_medication_otc varchar2(100),
    conditions_medication varchar2(100),
    csection varchar2(100),
    pku varchar2(100),
    asthma varchar2(100),
    seasonal_allergies varchar2(100),
    nonfoodallergies_drug varchar2(100),
    nonfoodallergies_dander varchar2(100),
    nonfoodallergies_beestings varchar2(100),
    nonfoodallergies_poisonivy varchar2(100),
    nonfoodallergies_sun varchar2(100),
    nonfoodallergies_no varchar2(100),
    ibd varchar2(100),
    skin_condition varchar2(100),
    diabetes varchar2(100),
    migraine varchar2(100),
    
    protein_per varchar2(100),
    fat_per varchar2(100),
    carbohydrate_per varchar2(100),
    plant_per varchar2(100),
    animal_per varchar2(100),
    fiber_grams varchar2(100),
    types_of_plants varchar2(100),
    percentage_from_carbs varchar2(100),
    primary_vegetable varchar2(100),
    primary_carb varchar2(100),
    
    diabetes_diagnose_date varchar2(100),
    diabetes_medication varchar2(100),
    
    contraceptive varchar2(100),
    pregnant varchar2(100),
    pregnant_due_date varchar2(100),
    
    frat varchar2(100),
    communal_dining varchar2(100),
    roommates varchar2(100),
    
    migraine_frequency varchar2(100),
    migraine_factor_1 varchar2(100),
    mainfactor_other_1 varchar2(100),
    migraine_factor_2 varchar2(100),
    mainfactor_other_2 varchar2(100),
    migraine_factor_3 varchar2(100),
    mainfactor_other_3 varchar2(100),
    migraine_pain varchar2(100),
    migraine_photophobia varchar2(100),
    migraine_phonophobia varchar2(100),
    migraine_nausea varchar2(100),
    migraine_aggravation varchar2(100),
    migraine_aura varchar2(100),
    migraine_relatives varchar2(100),
    migrainemeds varchar2(100),
    
    about_yourself_text varchar2(2000),
    
    constraint pk_ag_human_survey
        primary key (ag_login_id, participant_name),
    
    constraint fk_ag_hum_surv_to_ag_login
        foreign key (ag_login_id)
        references ag_login(ag_login_id)
);

create table ag_survey_multiples
(
    ag_login_id raw(16) not null,
    participant_name varchar2(200),
    item_name varchar2(50) not null,
    item_value varchar2(1000),
    
    constraint pk_ag_survey_multiples
        primary key (ag_login_id, participant_name, item_name),
    
    constraint fk_ag_mul_to_ag_login
        foreign key (ag_login_id)
        references ag_login (ag_login_id)
);

create table ag_survey_answer
(
    ag_survery_answer_id raw(16) default sys_guid(),
    ag_login_id raw(16) not null,
    participant_name varchar2(200),
    question varchar2(100) not null,
    answer varchar2(4000),
    
    constraint pk_ag_survey_answer
        primary key (ag_login_id, participant_name, question),

    constraint fk_sur_an_to_ag_login
        foreign key (ag_login_id)
        references ag_login(ag_login_id)
);


/*
drop table ag_survey_answer;
drop table ag_survey_multiples;
drop table ag_human_survey;
*/
