create table ag_animal_survey
(
    ag_login_id raw(16) not null, 
    participant_name varchar2(200),

    "type" varchar2(100),
    origin varchar2(100),
    birth_date varchar2(100),
    gender varchar2(100),
    setting varchar2(100),
    weight varchar2(100),
    diet varchar2(100),
    food_source_store  varchar2(100),
    food_source_human  varchar2(100),
    food_source_wild  varchar2(100),
    food_type varchar2(100),
    organic_food varchar2(100),
    grain_free_food varchar2(100),
    living_status varchar2(100),
    outside_time varchar2(100),

    toilet varchar2(100),
    coprophage varchar2(100),

    comments varchar2(2000),

    constraint pk_ag_animal_survey
        primary key (ag_login_id, participant_name),

    constraint fk_ag_animal_surv_to_ag_login
        foreign key (ag_login_id)
        references ag_login(ag_login_id)
);

/*
drop table ag_animal_survey;
*/
