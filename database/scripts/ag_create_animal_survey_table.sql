create table ag_animal_survey
(
    ag_login_id raw(16) not null, 
    participant_name varchar2(200),

    pet_type varchar2(100),
    origin varchar2(100),
    birth_date varchar2(100),
    gender varchar2(100),
    setting varchar2(100),
    weight_category varchar2(100),
    diet_type varchar2(100),
    food_source  varchar2(100),
    food_type varchar2(100),
    food_special_attributes varchar2(100),
    hours_spent_outdoors varchar2(100),

    toilet_water_access varchar2(100),
    coprophage varchar2(100),

    about_yourself_text varchar2(2000),

    constraint pk_ag_animal_survey
        primary key (ag_login_id, participant_name),

    constraint fk_ag_animal_surv_to_ag_login
        foreign key (ag_login_id)
        references ag_login(ag_login_id)
);

/*
drop table ag_animal_survey;
*/
