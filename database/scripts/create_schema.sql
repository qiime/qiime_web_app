/*

This will (indirectly) REMOVE all objects from the database. You have been warned...
select 'drop '|| object_type || ' "' || object_name || '"' || DECODE(OBJECT_TYPE,'TABLE',' CASCADE CONSTRAINTS;',';')
from user_objects

*/

-- Create the sequence for use in all controlled_vocab_values entries
create sequence seq_study
  minvalue 1
  start with 1
  increment by 1;

create sequence seq_sample
  minvalue 1
  start with 1
  increment by 1;

create sequence seq_prep
  minvalue 1
  start with 1
  increment by 1;

create sequence seq_host
  minvalue 1
  start with 1
  increment by 1;
  
create sequence seq_job
  minvalue 1
  start with 1
  increment by 1;  

-- Temporary tables
CREATE GLOBAL TEMPORARY TABLE tmp_id_table 
(
  ident int
) ON COMMIT DELETE ROWS;

create global temporary table sample_ids 
(
  sample_id int
) on commit delete rows;

create global temporary table host_ids 
(
  host_id int
) on commit delete rows;
  

CREATE TABLE air
    ( 
     sample_id INTEGER  NOT NULL , 
     barometric_press BINARY_DOUBLE , 
     carb_dioxide BINARY_DOUBLE , 
     carb_monoxide BINARY_DOUBLE , 
     humidity BINARY_DOUBLE , 
     pollutants VARCHAR2 (500 CHAR) , 
     resp_part_matter VARCHAR2 (200 CHAR) , 
     solar_irradiance BINARY_DOUBLE , 
     ventilation_rate BINARY_DOUBLE , 
     ventilation_type VARCHAR2 (500 CHAR) , 
     volatile_org_comp VARCHAR2 (500 CHAR) , 
     wind_direction INTEGER , 
     wind_speed BINARY_DOUBLE 
    ) 
;


CREATE INDEX idx_air_air_sample_id ON air 
    ( 
     sample_id ASC 
    ) 
;
CREATE INDEX idx_air_air_card_dir ON air 
    ( 
     wind_direction ASC 
    ) 
;

ALTER TABLE air 
    ADD CONSTRAINT pk_air PRIMARY KEY ( sample_id ) ;


CREATE TABLE column_dictionary 
    ( 
     column_name VARCHAR2 (200 CHAR)  NOT NULL , 
     data_type varchar2(100) not null,
     desc_or_value VARCHAR2 (1000 CHAR) , 
     definition VARCHAR2 (4000 CHAR)
    ) 
;



ALTER TABLE column_dictionary 
    ADD CONSTRAINT column_dictionary_PK PRIMARY KEY ( column_name ) ;



CREATE TABLE common_fields 
    ( 
     sample_id INTEGER  NOT NULL , 
     alkalinity BINARY_DOUBLE , 
     alkyl_diethers BINARY_DOUBLE , 
     aminopept_act BINARY_DOUBLE , 
     ammonium BINARY_DOUBLE , 
     bacteria_carb_prod BINARY_DOUBLE , 
     biomass VARCHAR2 (400 CHAR) , 
     bishomohopanol BINARY_DOUBLE , 
     bromide BINARY_DOUBLE , 
     calcium BINARY_DOUBLE , 
     carb_nitro_ratio BINARY_DOUBLE , 
     chloride BINARY_DOUBLE , 
     chlorophyll BINARY_DOUBLE , 
     "CURRENT" BINARY_DOUBLE , 
     density BINARY_DOUBLE , 
     diether_lipids VARCHAR2 (400 CHAR) , 
     diss_carb_dioxide BINARY_DOUBLE , 
     diss_hydrogen BINARY_DOUBLE , 
     diss_org_carbon BINARY_DOUBLE , 
     diss_oxygen BINARY_DOUBLE , 
     glucosidase_act BINARY_DOUBLE , 
     magnesium BINARY_DOUBLE , 
     mean_frict_vel BINARY_DOUBLE , 
     mean_peak_frict_vel BINARY_DOUBLE , 
     methane BINARY_DOUBLE , 
     misc_param VARCHAR2 (4000 CHAR) , 
     n_alkanes BINARY_DOUBLE , 
     nitrate BINARY_DOUBLE , 
     nitrite BINARY_DOUBLE , 
     nitro BINARY_DOUBLE , 
     org_carb BINARY_DOUBLE , 
     org_matter BINARY_DOUBLE , 
     org_nitro BINARY_DOUBLE , 
     organism_count VARCHAR2 (500 CHAR) , 
     oxygen BINARY_DOUBLE , 
     part_org_carb BINARY_DOUBLE , 
     petroleum_hydrocarb BINARY_DOUBLE , 
     ph BINARY_DOUBLE , 
     phaeopigments VARCHAR2 (500 CHAR) , 
     phosphate BINARY_DOUBLE , 
     phosplipid_fatt_acid VARCHAR2 (500 CHAR) , 
     potassium BINARY_DOUBLE , 
     press BINARY_DOUBLE , 
     redox_potential BINARY_DOUBLE , 
     salinity BINARY_DOUBLE , 
     silicate BINARY_DOUBLE , 
     sulfate BINARY_DOUBLE , 
     sulfide BINARY_DOUBLE , 
     tot_carb BINARY_DOUBLE , 
     tot_nitro BINARY_DOUBLE , 
     tot_org_carb BINARY_DOUBLE , 
     turbidity BINARY_DOUBLE , 
     water_content BINARY_DOUBLE 
    ) 
;



ALTER TABLE common_fields 
    ADD CONSTRAINT pk_common_fields PRIMARY KEY ( sample_id ) ;


CREATE TABLE controlled_vocab_values 
    ( 
     vocab_value_id INTEGER  NOT NULL , 
     controlled_vocab_id INTEGER  NOT NULL , 
     term VARCHAR2 (500 CHAR)  NOT NULL , 
     order_by INTEGER ,
     default_item char(1)
    ) 
;

CREATE INDEX idx_cvv_vocab_value_id ON controlled_vocab_values 
    ( 
     vocab_value_id ASC 
    ) 
;

ALTER TABLE controlled_vocab_values 
    ADD CONSTRAINT pk_controlled_vocab_values PRIMARY KEY ( vocab_value_id ) ;


CREATE TABLE controlled_vocabs 
    ( 
     controlled_vocab_id INTEGER  NOT NULL , 
     vocab_name VARCHAR2 (500 CHAR) 
    ) 
;



ALTER TABLE controlled_vocabs 
    ADD CONSTRAINT pk_controlled_vocabs PRIMARY KEY ( controlled_vocab_id ) ;


CREATE TABLE diet_componenets 
    ( 
     exp_diet_id INTEGER  NOT NULL , 
     perent_carbo FLOAT , 
     percent_fat FLOAT , 
     percent_protein FLOAT , 
     percent_starch FLOAT 
    ) 
;




CREATE TABLE "GROUP"
    ( 
     group_id INTEGER  NOT NULL , 
     group_name VARCHAR2 (500 CHAR) 
     study_id int not null,
    ) 
;

ALTER TABLE "GROUP" 
    ADD CONSTRAINT group_PK PRIMARY KEY ( group_id ) ;
    
alter table "GROUP"
  add constraint fk_group_study_id foreign key (study_id)
  references study (study_id);


CREATE TABLE group_timeline 
    ( 
     timeline_id INTEGER  NOT NULL , 
     group_id INTEGER  NOT NULL 
    ) 
;



ALTER TABLE group_timeline 
    ADD CONSTRAINT group_timeline_PK PRIMARY KEY ( timeline_id, group_id ) ;


CREATE TABLE host 
    ( 
     host_id INTEGER  NOT NULL , 
     host_subject_id varchar2(200 char) ,
     age BINARY_DOUBLE ,
     age_unit integer ,
     host_common_name VARCHAR2 (200 CHAR) , 
     disease_stat varchar(2000 CHAR),
     dry_mass BINARY_DOUBLE , 
     genotype VARCHAR2 (200 CHAR) , 
     height_or_length BINARY_DOUBLE , 
     infra_specific_name VARCHAR2 (200 CHAR) , 
     infra_specific_rank VARCHAR2 (100 CHAR) , 
     life_stage VARCHAR2 (200 CHAR) , 
     phenotype VARCHAR2 (200 CHAR) , 
     host_taxid INTEGER , 
     total_mass BINARY_DOUBLE , 
     host_color VARCHAR2 (100 CHAR) , 
     host_shape VARCHAR2 (100 CHAR) 
    ) 
;


CREATE INDEX idx_host_pheno ON host 
    ( 
     phenotype ASC 
    ) 
;

ALTER TABLE host 
    ADD CONSTRAINT pk_host PRIMARY KEY ( host_id ) ;


CREATE TABLE host_assoc_vertibrate 
    ( 
     host_id INTEGER  NOT NULL , 
     body_habitat VARCHAR2 (200 CHAR)  , 
     body_site VARCHAR2 (200 CHAR)  , 
     body_product VARCHAR2 (200 CHAR)  , 
     blood_press_diast BINARY_DOUBLE , 
     blood_press_syst BINARY_DOUBLE , 
     host_body_temp BINARY_DOUBLE , 
     diet VARCHAR2 (100 CHAR) , 
     family_relationship VARCHAR2 (200 CHAR) , 
     medications VARCHAR2 (500 CHAR) , 
     gravidity CHAR (1 CHAR) , 
     gravidity_due_date VARCHAR2 (200 CHAR) , 
     host_growth_cond VARCHAR2 (500 CHAR) , 
     last_meal VARCHAR2 (500 CHAR) , 
     scientific_name VARCHAR2 (500 CHAR) , 
     sex INTEGER , 
     substrate VARCHAR2 (200 CHAR) , 
     time_since_last_medication BINARY_DOUBLE , 
     date_of_birth DATE 
    ) 
;


CREATE INDEX idx_hav_body_habitat ON host_assoc_vertibrate 
    ( 
     body_habitat ASC 
    ) 
;
CREATE INDEX idx_hav_body_product ON host_assoc_vertibrate 
    ( 
     body_product ASC 
    ) 
;
CREATE INDEX idx_hav_body_site ON host_assoc_vertibrate 
    ( 
     body_site ASC 
    ) 
;
CREATE INDEX idx_hav_host_id ON host_assoc_vertibrate 
    ( 
     host_id ASC 
    ) 
;
CREATE INDEX idx_hav_sex ON host_assoc_vertibrate 
    ( 
     sex ASC 
    ) 
;

ALTER TABLE host_assoc_vertibrate 
    ADD CONSTRAINT pk_host_assoc_vert PRIMARY KEY ( host_id ) ;


CREATE TABLE host_associated_plant 
    ( 
     host_id INTEGER  NOT NULL , 
     air_temp_regm VARCHAR2 (200 CHAR) , 
     antibiotic_regm VARCHAR2 (500 CHAR) , 
     chem_mutagen VARCHAR2 (500 CHAR) , 
     climate_environment VARCHAR2 (300 CHAR) , 
     fertilizer_regm VARCHAR2 (500 CHAR) , 
     fungicide_regm VARCHAR2 (500 CHAR) , 
     gaseous_environment VARCHAR2 (500 CHAR) , 
     gravity VARCHAR2 (500 CHAR) , 
     growth_hormone_regm VARCHAR2 (500 CHAR) , 
     growth_med VARCHAR2 (300 CHAR) , 
     herbicide_regm VARCHAR2 (500 CHAR) , 
     humidity_regm VARCHAR2 (500 CHAR) , 
     infra_specific_name VARCHAR2 (200 CHAR) , 
     infra_specific_rank VARCHAR2 (200 CHAR) , 
     life_stage VARCHAR2 (200 CHAR) , 
     mechanical_damage VARCHAR2 (500 CHAR) , 
     mineral_nutr_regm VARCHAR2 (500 CHAR) , 
     non_mineral_nutr_regm VARCHAR2 (500 CHAR) , 
     pesticide_regm VARCHAR2 (500 CHAR) , 
     ph_regm VARCHAR2 (500 CHAR) , 
     plant_body_site VARCHAR2 (200 CHAR) , 
     plant_product VARCHAR2 (200 CHAR) , 
     radiation_regm VARCHAR2 (500 CHAR) , 
     rainfall_regm VARCHAR2 (500 CHAR) , 
     salt_regm VARCHAR2 (500 CHAR) , 
     season_environment VARCHAR2 (300 CHAR) , 
     standing_water_regm VARCHAR2 (500 CHAR) , 
     tiss_cult_growth_med VARCHAR2 (200 CHAR) , 
     water_temp_regm VARCHAR2 (500 CHAR) , 
     watering_regm VARCHAR2 (500 CHAR) , 
     wet_mass BINARY_DOUBLE 
    );



ALTER TABLE host_associated_plant 
    ADD CONSTRAINT pk_host_associated_plant PRIMARY KEY ( host_id ) ;



CREATE TABLE host_group 
    ( 
     group_id INTEGER  NOT NULL , 
     host_id INTEGER  NOT NULL 
    ) 
;



ALTER TABLE host_group 
    ADD CONSTRAINT host_group_PK PRIMARY KEY ( group_id, host_id ) ;


CREATE TABLE host_relationship 
    ( 
     host_id_1 INTEGER  NOT NULL , 
     host_id_2 INTEGER  NOT NULL , 
     relationship_type_id INTEGER  NOT NULL 
    ) 
;



ALTER TABLE host_relationship 
    ADD CONSTRAINT pk_host_relationship PRIMARY KEY ( host_id_1, host_id_2 ) ;


CREATE TABLE host_sample 
    ( 
     sample_id INTEGER  NOT NULL , 
     host_id INTEGER  NOT NULL 
    ) 
;


CREATE INDEX idx_host_samp_host_id ON host_sample 
    ( 
     host_id ASC 
    ) 
;
CREATE INDEX idx_host_samp_sample_id ON host_sample 
    ( 
     sample_id ASC 
    ) 
;

ALTER TABLE host_sample 
    ADD CONSTRAINT pk_host_sample PRIMARY KEY ( sample_id, host_id ) ;


CREATE TABLE host_timeline 
    ( 
     timeline_id INTEGER  NOT NULL , 
     host_id INTEGER  NOT NULL 
    ) 
;



ALTER TABLE host_timeline 
    ADD CONSTRAINT host_timeline_PK PRIMARY KEY ( timeline_id, host_id ) ;



CREATE TABLE human_associated 
    ( 
     host_id INTEGER  NOT NULL , 
     body_mass_index BINARY_DOUBLE , 
     drug_usage VARCHAR2 (500 CHAR) , 
     hiv_stat CHAR (1) , 
     ihmc_ethnicity INTEGER  , 
     ihmc_occupation INTEGER  , 
     last_meal VARCHAR2 (500 CHAR) , 
     diet_last_six_month VARCHAR2 (200) , 
     medic_hist_perform CHAR (1) , 
     pet_farm_animal VARCHAR2 (300 CHAR) , 
     pulse BINARY_DOUBLE , 
     smoker CHAR (1) , 
     travel_out_six_month VARCHAR2 (300 CHAR) , 
     twin_sibling CHAR (1) , 
     weight_loss_3_month BINARY_DOUBLE , 
     nose_throat_disord VARCHAR2 (500 CHAR)  , 
     pulmonary_disord VARCHAR2 (500 CHAR) , 
     study_complt_stat INTEGER  ,
     amniotic_fluid_color VARCHAR2 (100 CHAR) , 
     gestation_state VARCHAR2 (200 CHAR) , 
     foetal_health_stat VARCHAR2 (200 CHAR) , 
     maternal_health_stat VARCHAR2 (200 CHAR) ,
     blood_disord VARCHAR2 (200 CHAR) ,
     gastrointest_disord VARCHAR2 (200 CHAR) , 
     liver_disord VARCHAR2 (200 CHAR) , 
     special_diet VARCHAR2 (400 CHAR) ,
     nose_mouth_teeth_throat_disord VARCHAR2 (400 CHAR) , 
     time_last_toothbrush BINARY_DOUBLE ,
     dermatology_disord VARCHAR2 (500 CHAR) , 
     dominant_hand VARCHAR2 (100 CHAR) , 
     time_since_last_wash BINARY_DOUBLE ,
     kidney_disord VARCHAR2 (200 CHAR) , 
     urine_collect_meth INTEGER  , 
     urogenit_tract_disor VARCHAR2 (200 CHAR) ,
     birth_control VARCHAR2 (100 CHAR) , 
     douche DATE , 
     gynecologic_disord VARCHAR2 (200 CHAR) , 
     menarche DATE , 
     hrt DATE , 
     hysterectomy CHAR (1) , 
     menopause DATE , 
     pregnancy DATE , 
     sexual_act VARCHAR2 (200 CHAR) , 
     urogenit_disord VARCHAR2 (200 CHAR) 
    ) 
;


CREATE INDEX idx_ha_study_comp_status ON human_associated 
    ( 
     study_complt_stat ASC 
    ) 
;
CREATE INDEX idx_ha_ihmc_occupation ON human_associated 
    ( 
     ihmc_occupation ASC 
    ) 
;

CREATE INDEX idx_ha_ihmc_ethnicity ON human_associated 
    ( 
     ihmc_ethnicity ASC 
    ) 
;
CREATE INDEX idx_ha_cvv_nose_throad ON human_associated 
    ( 
     nose_throat_disord ASC 
    ) 
;

CREATE INDEX idx_hum_urn_urn_col_meth ON human_associated 
    ( 
     urine_collect_meth ASC 
    ) 
;

ALTER TABLE human_associated
    ADD CONSTRAINT fk_human_ass_host primary key (host_id);
    
ALTER TABLE human_associated
    ADD CONSTRAINT pk_human_associated foreign key (host_id) 
    REFERENCES host (host_id);


CREATE TABLE microbial_mat_biofilm 
    ( 
     sample_id INTEGER  NOT NULL 
    ) 
;


ALTER TABLE microbial_mat_biofilm 
    ADD CONSTRAINT "pk_microbial_mat)biofilm" PRIMARY KEY ( sample_id ) ;


CREATE TABLE other_environment 
    ( 
     sample_id INTEGER  NOT NULL 
    ) 
;

ALTER TABLE other_environment 
    ADD CONSTRAINT pk_other_environment PRIMARY KEY ( sample_id ) ;

CREATE TABLE "SAMPLE" 
( 
  sample_id INTEGER  NOT NULL , 
  study_id INTEGER  NOT NULL , 
  sample_name VARCHAR2 (300 CHAR) , 
  "PUBLIC" CHAR (1 CHAR) , 
  assigned_from_geo char(1),
  altitude FLOAT , 
  biological_specimen varchar(1000 char),
  chem_administration varchar(2000 CHAR),
  collection_date varchar2(200 char) , 
  country VARCHAR2 (200 CHAR), 
  depth varchar2(50 CHAR) , 
  elevation FLOAT , 
  env_biome VARCHAR2 (200 CHAR), 
  env_feature VARCHAR2 (200 CHAR), 
  env_matter VARCHAR2 (200 CHAR), 
  organism_count BINARY_DOUBLE , 
  oxy_stat_samp INTEGER, 
  perturbation VARCHAR2 (1000 CHAR) , 
  ph BINARY_DOUBLE , 
  latitude FLOAT , 
  longitude FLOAT , 
  samp_collect_device VARCHAR2 (500 CHAR) , 
  samp_mat_process VARCHAR2 (500 CHAR) , 
  samp_salinity BINARY_DOUBLE , 
  samp_size varchar2 (300 char),
  samp_store_dur varchar(200) , 
  samp_store_loc VARCHAR2 (200 CHAR) , 
  samp_store_temp BINARY_DOUBLE , 
  temp BINARY_DOUBLE,     
  TITLE varchar2(500),
  TAXON_ID integer,
  COMMON_NAME varchar2(500),
  ANONYMIZED_NAME varchar2(500),
  DESCRIPTION varchar2(2000)
);

CREATE INDEX idx_samp_env_feat ON "SAMPLE" 
    ( 
     env_feature ASC 
    ) 
;
CREATE INDEX idx_samp_country ON "SAMPLE" 
    ( 
     country ASC 
    ) 
;
CREATE INDEX idx_samp_env_matter ON "SAMPLE" 
    ( 
     env_matter ASC 
    ) 
;
CREATE INDEX idx_samp_study_id ON "SAMPLE" 
    ( 
     study_id ASC 
    ) 
;
CREATE INDEX idx_samp_env_biome ON "SAMPLE" 
    ( 
     env_biome ASC 
    ) 
;

ALTER TABLE "SAMPLE" 
    ADD CONSTRAINT pk_sample PRIMARY KEY ( sample_id ) ;



create table sequence_prep
(
  sequence_prep_id integer not null,
  sample_id int not null,
  nucl_acid_ext varchar2 (4000),
  nucl_acid_amp varchar2 (4000),
  lib_size integer,
  lib_reads_seqd integer,
  lib_vector varchar2 (1000),
  libr_screen varchar2 (1000),
  target_gene varchar2 (500),
  target_subfragment varchar2 (500),
  pcr_primers varchar2(2000),
  multiplex_ident varchar2(500),
  pcr_cond varchar2(2000),
  sequencing_meth varchar2(200), -- controlled vocab, need values
  seq_quality_check integer, -- controlled vocab, need values
  chimera_check integer, -- controlled vocab, need values
  sop varchar2 (1000),
  url varchar2 (1000),
  -- SRA Experiment Fields
  EXPERIMENT_ALIAS varchar2(500),
  EXPERIMENT_CENTER varchar2(500),
  EXPERIMENT_TITLE varchar2(500),
  EXPERIMENT_ACCESSION varchar2(500),
  STUDY_ACCESSION varchar2(500),
  STUDY_REF varchar2(500),
  STUDY_CENTER varchar2(500),
  EXPERIMENT_DESIGN_DESCRIPTION varchar2(4000),
  LIBRARY_CONSTRUCTION_PROTOCOL varchar2(4000),
  SAMPLE_ACCESSION varchar2(500),
  SAMPLE_ALIAS varchar2(500),
  SAMPLE_CENTER varchar2(500),
  POOL_MEMBER_ACCESSION varchar2(500),
  POOL_MEMBER_NAME varchar2(500),
  POOL_PROPORTION varchar2(500),
  BARCODE_READ_GROUP_TAG varchar2(500),
  BARCODE varchar2(500),
  LINKER varchar2(500),
  KEY_SEQ varchar2(500),
  PRIMER_READ_GROUP_TAG varchar2(500),
  PRIMER varchar2(500),
  RUN_PREFIX varchar2(500),
  REGION varchar2(500),
  PLATFORM varchar2(500),
  RUN_ACCESSION varchar2(500),
  RUN_ALIAS varchar2(500),
  RUN_CENTER varchar2(500),
  RUN_DATE varchar2(500),
  INSTRUMENT_NAME varchar2(500),
  LIBRARY_STRATEGY varchar2(500),
  LIBRARY_SOURCE varchar2(500),
  LIBRARY_SELECTION varchar2(500)
  
);

ALTER TABLE sequence_prep 
    ADD CONSTRAINT pk_sequence_prep PRIMARY KEY ( sequence_prep_id ) ;

create index idx_sp_seq_meth on sequence_prep (sequencing_meth asc);
create index idx_sp_seq_qual_chk on sequence_prep (seq_quality_check asc);
create index idx_sp_chimera_check on sequence_prep (chimera_check asc);


create table sample_sequence_prep
(
  sample_id integer not null,
  sequence_prep_id integer not null
);

alter table sample_sequence_prep
  add constraint pk_sample_sequence_prep primary key (sample_id, sequence_prep_id);
  
alter table sample_sequence_prep
  add constraint fk_ssp_sample foreign key (sample_id)
    references sample (sample_id);
    
alter table sample_sequence_prep
  add constraint fk_ssp_seq_prep foreign key (sequence_prep_id)
    references sequence_prep (sequence_prep_id);


create index idx_ssp_sample_id on sample_sequence_prep (sample_id);
create index idx_ssp_seq_prep_id on sample_sequence_prep (sequence_prep_id);


CREATE TABLE sample_timeline 
    ( 
     timeline_id INTEGER  NOT NULL , 
     sample_id INTEGER  NOT NULL 
    ) 
;



ALTER TABLE sample_timeline 
    ADD CONSTRAINT sample_timeline_PK PRIMARY KEY ( timeline_id, sample_id ) ;


CREATE TABLE sampling_event 
    ( 
     study_id INTEGER  NOT NULL , 
     sample_id INTEGER  NOT NULL , 
     event_description VARCHAR2 (500 CHAR) , 
     event_date DATE 
    ) 
;



ALTER TABLE sampling_event 
    ADD CONSTRAINT pk_sampling_event PRIMARY KEY ( study_id, sample_id ) ;


CREATE TABLE sediment 
    ( 
     sample_id INTEGER  NOT NULL , 
     particle_class VARCHAR2 (500 CHAR) , 
     porosity BINARY_DOUBLE , 
     sediment_type VARCHAR2 (500 CHAR) 
    ) 
;



ALTER TABLE sediment 
    ADD CONSTRAINT Sediment_PK PRIMARY KEY ( sample_id ) ;

CREATE TABLE soil 
( 
  sample_id INTEGER  NOT NULL , 
  cur_land_use integer,
  cur_vegetation varchar2(200 CHAR),
  cur_vegetation_meth varchar2(200 CHAR),
  previous_land_use varchar2(500 CHAR),
  previous_land_use_meth varchar2(500 CHAR),
  crop_rotation varchar2(200 CHAR),
  agrochem_addition varchar2(500 CHAR),
  tillage varchar2(200 CHAR),
  fire varchar2(500 CHAR),
  flooding varchar2(500 CHAR),
  extreme_event varchar2(500 CHAR),
  other varchar2(1000 CHAR),
  horizon varchar2(100 CHAR),
  horizon_meth varchar2(200 CHAR),
  sieving varchar2(200 CHAR),
  water_content_soil BINARY_DOUBLE , 
  water_content_soil_meth varchar2(200 CHAR),
  samp_weight_dna_ext BINARY_DOUBLE , 
  pool_dna_extracts smallint,
  store_cond varchar2(400 CHAR),
  link_climate_info varchar2(500 CHAR),
  annual_season_temp BINARY_DOUBLE , 
  annual_season_precpt BINARY_DOUBLE , 
  link_class_info varchar2(500 CHAR),
  fao_class varchar2(200 CHAR),
  local_class varchar2(200 CHAR),
  local_class_meth varchar2(200 CHAR),
  soil_type varchar2(200 CHAR),
  soil_type_meth varchar2(200 CHAR),
  slope_gradient BINARY_DOUBLE , 
  slope_aspect varchar2(200 CHAR),
  profile_position varchar2(200 CHAR),
  drainage_class varchar2(200 CHAR),
  texture varchar2(300 CHAR),
  texture_meth varchar2(200 CHAR),
  ph_meth varchar2(200 CHAR),
  tot_org_c_meth varchar2(200 CHAR),
  tot_n_meth varchar2(200 CHAR),
  microbial_biomass varchar2(200 CHAR),
  microbial_biomass_meth varchar2(200 CHAR),
  link_addit_analys varchar2(500 CHAR),
  extreme_salinity BINARY_DOUBLE , 
  salinity_meth varchar2(200 CHAR),
  heavy_metals varchar2(200 CHAR),
  heavy_metals_meth varchar2(200 CHAR),
  al_sat BINARY_DOUBLE , 
  al_sat_meth varchar2(200 CHAR),
  misc_param varchar2(1000 CHAR)
);

CREATE INDEX idx_soil_sample_id ON soil 
    ( 
     sample_id ASC 
    ) 
;
CREATE INDEX idx_soil_cur_land_use ON soil 
    ( 
     cur_land_use ASC 
    ) 
;

ALTER TABLE soil 
    ADD CONSTRAINT pk_soil PRIMARY KEY ( sample_id ) ;


CREATE TABLE study 
( 
  study_id INTEGER  NOT NULL , 
  submit_to_insdc CHAR (1) , 
  miens_compliant char(1) default 'y',
  investigation_type INTEGER  NOT NULL , 
  project_name VARCHAR2 (200 CHAR) , 
  experimental_factor VARCHAR2 (1000 CHAR) , 
  -- Fields to track uploaded data
  metadata_complete char(1) default 'n',
  -- SRA Study Fields
  STUDY_ALIAS varchar2(500),
  STUDY_TITLE varchar2(500),
  STUDY_TYPE integer,
  STUDY_ABSTRACT varchar2(4000),
  STUDY_DESCRIPTION varchar2(500),
  CENTER_NAME varchar2(500),
  CENTER_PROJECT_NAME varchar2(500),
  PROJECT_ID varchar2(500),
  PMID varchar2(500)
);



CREATE INDEX idx_study_invest_type ON study 
    ( 
     investigation_type ASC 
    ) 
;

ALTER TABLE study 
    ADD CONSTRAINT pk_study PRIMARY KEY ( study_id ) ;

create table study_sffs
(
  study_id integer not null,
  sff_path varchar2(1000) not null,
  
  constraint pk_study_sffs primary key (study_id, sff_path),
  constraint fk_study_sffs_study_id foreign key (study_id) references study (study_id)
);

create index idx_study_sffs_study_id on study_sffs (study_id);

create table study_mapping_files
(
  study_id integer not null,
  mapping_file_path varchar2(1000) not null,
  
  constraint pk_study_mapping_files primary key (study_id, mapping_file_path),
  constraint fk_smf_study_id foreign key (study_id) references study (study_id)
);

create index idx_smf_study_id on study_mapping_files (study_id);

create table study_actual_columns
(
  study_id int not null,
  column_name not null,
  table_name not null,
  
  constraint pk_study_columns primary key (study_id, column_name),
  constraint fk_study_col_study foreign key (study_id) references study (study_id)
);

create index idx_sac_study_id on study_actual_columns(study_id);
create index idx_sac_column_name on study_actual_columns(column_name);

create table study_packages
(
  study_id integer not null,
  env_package integer not null,
  
  constraint pk_study_packages primary key (study_id, env_package),
  constraint fk_stud_pack_study foreign key (study_id) references study (study_id),
  constraint fk_stud_pack_cvv foreign key (env_package) references controlled_vocab_values (vocab_value_id)
);

create index idx_study_packages_study_id on study_packages(study_id);
create index idx_study_packages_env_pkg on study_packages(env_package);


CREATE TABLE study_columns 
    ( 
     package_type_id INTEGER  NOT NULL , 
     column_name VARCHAR2 (200 CHAR)  NOT NULL , 
     required CHAR (1 CHAR) 
    ) 
;



ALTER TABLE study_columns 
    ADD CONSTRAINT study_columns_PK PRIMARY KEY ( package_type_id, column_name ) ;


CREATE TABLE timeline 
    ( 
     timeline_id INTEGER  NOT NULL , 
     study_id INTEGER  NOT NULL , 
     entry_date DATE , 
     entry_text VARCHAR2 (1000 CHAR) 
    ) 
;


CREATE INDEX idx_tline_study_id ON timeline 
    ( 
     study_id ASC 
    ) 
;

ALTER TABLE timeline 
    ADD CONSTRAINT timeline_PK PRIMARY KEY ( timeline_id ) ;


CREATE TABLE wastewater_sludge 
    ( 
     sample_id INTEGER  NOT NULL , 
     biochem_oxygen_dem BINARY_DOUBLE , 
     chem_oxygen_dem BINARY_DOUBLE , 
     efficiency_percent BINARY_DOUBLE , 
     emulsions VARCHAR2 (200 CHAR) , 
     gaseous_substances VARCHAR2 (200 CHAR) , 
     indust_eff_percent BINARY_DOUBLE , 
     inorg_particles VARCHAR2 (500 CHAR) , 
     org_particles VARCHAR2 (500 CHAR) , 
     pre_treatment VARCHAR2 (300 CHAR) , 
     primary_treatment VARCHAR2 (300 CHAR) , 
     reactor_type VARCHAR2 (200 CHAR) , 
     secondary_treatment VARCHAR2 (300 CHAR) , 
     sewage_type VARCHAR2 (200 CHAR) , 
     sludge_retent_time BINARY_DOUBLE , 
     soluble_inorg_mat BINARY_DOUBLE , 
     soluble_org_mat BINARY_DOUBLE , 
     suspend_solids VARCHAR2 (400 CHAR) , 
     tertiary_treatment VARCHAR2 (300 CHAR) , 
     tot_phosphate BINARY_DOUBLE , 
     wastewater_type VARCHAR2 (200 CHAR) 
    ) 
;



ALTER TABLE wastewater_sludge 
    ADD CONSTRAINT WastewaterSludge_PK PRIMARY KEY ( sample_id ) ;


CREATE TABLE water 
    ( 
     sample_id INTEGER  NOT NULL , 
     atmospheric_data VARCHAR2 (500 CHAR) , 
     diss_inorg_nitro BINARY_DOUBLE , 
     diss_inorg_phosp BINARY_DOUBLE , 
     light_intensity BINARY_DOUBLE , 
     photon_flux BINARY_DOUBLE , 
     primary_prod BINARY_DOUBLE , 
     soluble_react_phosp BINARY_DOUBLE , 
     suspend_part_matter BINARY_DOUBLE , 
     tot_depth_water_col BINARY_DOUBLE , 
     tot_inorg_nitro BINARY_DOUBLE , 
     tot_part_carb BINARY_DOUBLE , 
     tot_phosp BINARY_DOUBLE 
    ) 
;



ALTER TABLE water 
    ADD CONSTRAINT pk_water PRIMARY KEY ( sample_id ) ;


create table column_controlled_vocab
(
  column_name varchar2(200)  not null,
  controlled_vocab_id integer not null,
  constraint pk_column_cont_vocab 
    primary key (column_name, controlled_vocab_id),
  constraint fk_col_cont_vocab_cont_vocab 
    foreign key (controlled_vocab_id) 
    references controlled_vocabs (controlled_vocab_id),
  constraint fk_col_cont_vocab_col_name 
    foreign key (column_name) 
    references column_dictionary (column_name)
);

create table column_ontology
(
  column_name varchar2(200) not null,
  ontology_short_name varchar2(50) not null,
  constraint pk_column_ontology
    primary key (column_name, ontology_short_name),
  constraint fk_col_ont_col_name 
    foreign key (column_name) 
    references column_dictionary (column_name)
);


create table user_study
(
  web_app_user_id int not null,
  study_id int not null,
  constraint pk_user_study
    primary key (web_app_user_id, study_id),
  constraint fk_study_id 
    foreign key (study_id)
    references study (study_id)
);


ALTER TABLE air 
    ADD CONSTRAINT fk_air_cont_vocabs FOREIGN KEY 
    ( 
     wind_direction
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE air 
    ADD CONSTRAINT fk_air_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE common_fields 
    ADD CONSTRAINT fk_common_fields_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE controlled_vocab_values 
    ADD CONSTRAINT fk_cont_vcb_values_cont_vcbs FOREIGN KEY 
    ( 
     controlled_vocab_id
    ) 
    REFERENCES controlled_vocabs 
    ( 
     controlled_vocab_id
    ) 
;


ALTER TABLE diet_componenets 
    ADD CONSTRAINT fk_diet_comp_cont_vocabs FOREIGN KEY 
    ( 
     exp_diet_id
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE human_associated 
    ADD CONSTRAINT fk_ha_cvv_study_comp FOREIGN KEY 
    ( 
     study_complt_stat
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE host_associated_plant 
    ADD CONSTRAINT fk_hap_host FOREIGN KEY 
    ( 
     host_id
    ) 
    REFERENCES host 
    ( 
     host_id
    ) 
;


ALTER TABLE host_relationship 
    ADD CONSTRAINT fk_hav_cvv_rel_type_id FOREIGN KEY 
    ( 
     relationship_type_id
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE host_assoc_vertibrate 
    ADD CONSTRAINT fk_hav_host FOREIGN KEY 
    ( 
     host_id
    ) 
    REFERENCES host 
    ( 
     host_id
    ) 
;


ALTER TABLE host_assoc_vertibrate 
    ADD CONSTRAINT fk_hav_ont_sex FOREIGN KEY 
    (
     sex
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;




ALTER TABLE host_group 
    ADD CONSTRAINT fk_host_group_group FOREIGN KEY 
    ( 
     group_id
    ) 
    REFERENCES "GROUP" 
    ( 
     group_id
    ) 
;


ALTER TABLE host_group 
    ADD CONSTRAINT fk_host_group_host FOREIGN KEY 
    ( 
     host_id
    ) 
    REFERENCES host 
    ( 
     host_id
    ) 
;


ALTER TABLE host_relationship 
    ADD CONSTRAINT fk_host_relationship_hav_1 FOREIGN KEY 
    ( 
     host_id_1
    ) 
    REFERENCES host_assoc_vertibrate 
    ( 
     host_id
    ) 
;


ALTER TABLE host_relationship 
    ADD CONSTRAINT fk_host_relationship_hav_2 FOREIGN KEY 
    ( 
     host_id_2
    ) 
    REFERENCES host_assoc_vertibrate 
    ( 
     host_id
    ) 
;


ALTER TABLE host_sample 
    ADD CONSTRAINT fk_host_sample_host FOREIGN KEY 
    ( 
     host_id
    ) 
    REFERENCES host 
    ( 
     host_id
    ) 
;


ALTER TABLE host_sample 
    ADD CONSTRAINT fk_host_sample_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE host_timeline 
    ADD CONSTRAINT fk_host_timeline_host FOREIGN KEY 
    ( 
     host_id
    ) 
    REFERENCES host 
    ( 
     host_id
    ) 
;


ALTER TABLE host_timeline 
    ADD CONSTRAINT fk_host_timeline_timeline FOREIGN KEY 
    ( 
     timeline_id
    ) 
    REFERENCES timeline 
    ( 
     timeline_id
    ) 
;


ALTER TABLE microbial_mat_biofilm 
    ADD CONSTRAINT fk_micro_mat_biofilm_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE other_environment 
    ADD CONSTRAINT fk_other_environment_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE "SAMPLE" 
    ADD CONSTRAINT fk_sample_cvv_oxy_stat FOREIGN KEY 
    ( 
     oxy_stat_samp
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE "SAMPLE"
    ADD CONSTRAINT fk_sample_study FOREIGN KEY 
    ( 
     study_id
    ) 
    REFERENCES study 
    ( 
     study_id
    ) 
;


ALTER TABLE sample_timeline 
    ADD CONSTRAINT fk_sample_timeline_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE sample_timeline 
    ADD CONSTRAINT fk_sample_timeline_timeline FOREIGN KEY 
    ( 
     timeline_id
    ) 
    REFERENCES timeline 
    ( 
     timeline_id
    ) 
;


ALTER TABLE sampling_event 
    ADD CONSTRAINT fk_sampling_event_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE sampling_event 
    ADD CONSTRAINT fk_sampling_event_study FOREIGN KEY 
    ( 
     study_id
    ) 
    REFERENCES study 
    ( 
     study_id
    ) 
;


ALTER TABLE sediment 
    ADD CONSTRAINT fk_sediment_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE soil 
    ADD CONSTRAINT fk_soil_cv_cur_land_use FOREIGN KEY 
    ( 
     cur_land_use
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE soil 
    ADD CONSTRAINT fk_soil_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE study_columns 
    ADD CONSTRAINT fk_study_col_cvv_pack_type_id FOREIGN KEY 
    ( 
     package_type_id
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE study_columns 
    ADD CONSTRAINT fk_study_columns_column_dict FOREIGN KEY 
    ( 
     column_name
    ) 
    REFERENCES column_dictionary 
    ( 
     column_name
    ) 
;


ALTER TABLE study 
    ADD CONSTRAINT fk_study_cvv_invest_type FOREIGN KEY 
    ( 
     investigation_type
    ) 
    REFERENCES controlled_vocab_values 
    ( 
     vocab_value_id
    ) 
;


ALTER TABLE group_timeline 
    ADD CONSTRAINT fk_timeline_group_group FOREIGN KEY 
    ( 
     group_id
    ) 
    REFERENCES "GROUP" 
    ( 
     group_id
    ) 
;


ALTER TABLE group_timeline 
    ADD CONSTRAINT fk_timeline_group_timeline FOREIGN KEY 
    ( 
     timeline_id
    ) 
    REFERENCES timeline 
    ( 
     timeline_id
    ) 
;


ALTER TABLE timeline 
    ADD CONSTRAINT fk_timeline_study FOREIGN KEY 
    ( 
     study_id
    ) 
    REFERENCES study 
    ( 
     study_id
    ) 
;


ALTER TABLE wastewater_sludge 
    ADD CONSTRAINT fk_wastewater_sludge_sample FOREIGN KEY 
    ( 
     sample_id
    ) 
    REFERENCES "SAMPLE"
    ( 
     sample_id
    ) 
;


ALTER TABLE water 
    ADD CONSTRAINT fk_water_sample foreign key (sample_id) 
    REFERENCES "SAMPLE" (sample_id) 
;

create table qiime_queue
(
  job_id integer not null, 
  study_id integer not null,
  user_id integer not null,
  submission_date date default sysdate not null,
  status varchar2(100 char) default 'new' not null,
  mapping_file varchar2(1000) default '' not null,
  sff_file varchar2(1000) default '' not null,
  
  constraint pk_qiime_queue primary key (job_id),
  constraint fk_qiime_queue_study_id foreign key (study_id) references study (study_id)
);

--------------------------------------------------------
-- END SCHEMA
--------------------------------------------------------

--------------------------------------------------------
-- DATA
--------------------------------------------------------    

-- Allows special characters in text strings
set define ~

-- Controlled Vocabularies 
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (1, 'Package Type');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (2, 'Investigation Type');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (3, 'Urine Collection Method');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (4, 'Nose/Throad Disorders');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (5, 'Study Completion Status');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (6, 'Current Land Use');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (7, 'Cardinal Direction');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (8, 'Sex');
--insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (9, 'Sequencing Method');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (10, 'Sequence Quality Check');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (11, 'Horizon');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (17, 'Oxygenation Status of Sample');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (18, 'Experimental Diet Types');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (19, 'Special Diets');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (20, 'Age Units');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (21, 'IHMC Medication Codes');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (22, 'IHMC Ethnicities');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (23, 'IHMC Occupations');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (24, 'Dominant Hand');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (25, 'Tillage');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (26, 'Profile Position');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (27, 'Drainage class');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (28, 'INSDC Country List');
insert into controlled_vocabs (controlled_vocab_id, vocab_name) values (29, 'Soil Types');
commit;

-- Package Type
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-7, 1, 'sra-study-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-6, 1, 'sra-sample-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-5, 1, 'sra-experiment-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-4, 1, 'sra-submission-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-3, 1, 'study-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-2, 1, 'sample-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (-1, 1, 'prep-level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (1, 1, 'air', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (2, 1, 'host-associated', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (3, 1, 'human-associated', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (4, 1, 'human-skin', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (5, 1, 'human-oral', 5, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (6, 1, 'human-gut', 6, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (7, 1, 'human-vaginal', 7, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (8, 1, 'human-amniotic-fluid', 8, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (9, 1, 'human-urine', 9, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (10, 1, 'human-blood', 10, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (11, 1, 'microbial mat/biofilm', 11, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (12, 1, 'miscellaneous natural or artificial environment', 10, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (13, 1, 'plant-associated', 12, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (14, 1, 'sediment', 13, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (15, 1, 'soil', 14, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (16, 1, 'wastewater/sludge', 15, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (17, 1, 'water', 16, 'N');
commit;


-- Create the sequence for use in all controlled_vocab_values entries
create sequence seq_vocab_values
  minvalue 18
  start with 18
  increment by 1;


-- Investigation Type
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'eukaryote', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'bacteria_archaea', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'plasmid', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'virus', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'organelle', 5, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'metagenome', 6, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'miens-survey', 7, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 2, 'miens-culture', 8, 'N');
commit;

-- Urine Collection Method
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 3, 'clean catch', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 3, 'catheter', 1, 'N');
commit;

-- Nose/Throad Disorders
-- insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 4, '', 1, 'N');
-- commit;

-- Study Completion Status
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 5, '(0) complete', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 5, '(1) adverse event', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 5, '(2) non-compliance', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 5, '(3) lost to follow up', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 5, '(4) other', 5, 'N');
commit;

-- Current Land Use
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 6, 'urban (artificial cover)', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 6, 'barren land', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 6, 'crop cover', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 6, 'grass/herbaceous cover', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 6, 'shrub cover', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 6, 'tree cover', 1, 'N');
commit;

-- Cardinal Directions
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'N', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'S', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'E', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'W', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'NW', 5, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'NE', 6, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'SW', 7, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 7, 'SE', 8, 'N');
commit;

-- Sex
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 8, 'male', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 8, 'female', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 8, 'neuter', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 8, 'hermaphrodite', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 8, 'not determined', 5, 'N');
commit;

-- Sequencing Method
--insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 9, 'Sanger', 1, 'N');
--insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 9, '454', 1, 'N');
--insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 9, 'Illumina', 1, 'N');
--commit;

-- Sequence Quality Check
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 10, 'Manual', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 10, 'None', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 10, 'Software', 1, 'N');
commit;

-- Horizon Method
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'O horizon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'A horizon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'E horizon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'B horizon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'C horizon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'R layer', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 11, 'Permafrost', 1, 'N');
commit;

-- Oxygenation Status of Sample
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'aerobe', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'anaerobe', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'facultative', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'microaerophilic', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'microanaerobe', 5, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'obligate aerobe', 6, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 17, 'obligate anaerobe', 7, 'N');
commit;

-- Experimental Diet Type
-- insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 18, '', 1, 'N');
-- commit;

-- Special Diets
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 19, 'low carb', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 19, 'reduced calorie', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 19, 'vegetarian', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 19, 'other-specify', 1, 'N');
commit;

-- Age Units
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 20, 'seconds', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 20, 'minutes', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 20, 'days', 3, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 20, 'weeks', 4, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 20, 'months', 5, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 20, 'years', 6, 'N');
commit;

-- IHMC Medication Codes
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '01=1=Analgesics/NSAIDS', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '02=2=Anesthetics', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '03=3=Antacids/H2  antagonists', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '04=4=Anti-acne', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '05=5=Anti-asthma/bronchodilators', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '06=6=Anti-cholesterol/Anti-hyperlipidemic', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '07=7=Anti-coagulants', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '08=8=Antibiotics/(anti)-infectives, parasitics, microbials', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '09=9=Antidepressants/mood-altering drugs', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '10=10=Antihistamines/ Decongestants', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '11=11=Antihypertensives', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '12=12=Cardiovascular, other than hyperlipidemic/HTN', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '13=13=Contraceptives (oral, implant, injectable)', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '14=14=Emergency/support medications', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '15=15=Endocrine/Metabolic agents', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '16=16=GI meds (anti-diarrheal, emetic, spasmodics)', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '17=17=Herbal/homeopathic products', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '18=18=Hormones/steroids', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '19=19=OTC cold & flu', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '20=20=Vaccine prophylaxis', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '21=21=Vitamins, minerals, food supplements', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 21, '99=99=Other', 1, 'N');
commit;

-- IHMC Ethnicities
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 22, '01=Hispanic or Latino or Spanish', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 22, '02=Non-Hispanic or Non-Latino or Non- Spanish', 1, 'N');
commit;

-- IHMC Occupations
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '01=01 Accounting/Finance', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '02=02 Advertising/Public Relations', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '03=03 Arts/Entertainment/Publishing', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '04=04 Automotive', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '05=05 Banking/ Mortgage', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '06=06 Biotech', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '07=07 Broadcast/Journalism', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '08=08 Business  Development', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '09=09 Clerical/Administrative', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '10=10 Construction/Trades', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '11=11 Consultant', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '12=12 Customer Services', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '13=13 Design', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '14=14 Education', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '15=15 Engineering', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '16=16 Entry Level', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '17=17 Executive', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '18=18 Food Service', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '19=19 Government', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '20=20 Grocery', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '21=21 Healthcare', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '22=22 Hospitality', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '23=23 Human Resources', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '24=24 Information  Technology', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '25=25 Insurance', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '26=26 Law/Legal', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '27=27 Management', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '28=28 Manufacturing', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '29=29 Marketing', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '30=30 Pharmaceutical', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '31=31 Professional Services', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '32=32 Purchasing', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '33=33 Quality Assurance (QA)', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '34=34 Research', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '35=35 Restaurant', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '36=36 Retail', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '37=37 Sales', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '38=38 Science', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '39=39 Security/Law Enforcement', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '40=40 Shipping/Distribution', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '41=41 Strategy', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '42=42 Student', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '43=43 Telecommunications', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '44=44 Training', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '45=45 Transportation', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '46=46 Warehouse', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '47=47 Other', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 23, '99=99 Unknown/Refused', 1, 'N');
commit;

-- Dominant Hand
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 24, 'left', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 24, 'right', 2, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 24, 'ambidextrous', 3, 'N');
commit;

-- Tillage
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 25, 'conservation tillage or zero tillage', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 25, 'reduced tillage', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 25, 'conventional tillage', 1, 'N');
commit;

-- Profile Position
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 26, 'summit', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 26, 'shoulder', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 26, 'backslope', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 26, 'footslope', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 26, 'toeslope', 1, 'N');
commit;

-- Drainage Class
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 27, 'very poorly', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 27, 'poorly', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 27, 'somewhat poorly', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 27, 'moderately well', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 27, 'well', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 27, 'excessively drained', 1, 'N');
commit;

-- INSDC Country List
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Afghanistan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Albania', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Algeria', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'American Samoa', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Andorra', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Angola', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Anguilla', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Antarctica', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Antigua and Barbuda', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Argentina', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Armenia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Arctic Ocean', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Aruba', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Ashmore and Cartier Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Atlantic Ocean', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Australia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Austria', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Azerbaijan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bahamas', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bahrain', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Baker Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bangladesh', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Barbados', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bassas da India', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Belarus', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Belgium', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Belize', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Benin', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bermuda', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bhutan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bolivia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bosnia and Herzegovina', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Botswana', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bouvet Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Brazil', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'British Virgin Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Brunei', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Bulgaria', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Burkina Faso', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Burundi', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cambodia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cameroon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Canada', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cape Verde', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cayman Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Central African Republic', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Chad', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Chile', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'China', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Christmas Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Clipperton Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cocos Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Colombia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Comoros', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cook Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Coral Sea Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Costa Rica', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cote d''Ivoire', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Croatia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cuba', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Cyprus', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Czech Republic', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Denmark', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Democratic Republic of the Congo', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Djibouti', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Dominica', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Dominican Republic', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'East Timor', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Ecuador', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Egypt', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'El Salvador', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Equatorial Guinea', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Eritrea', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Estonia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Ethiopia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Europa Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Falkland Islands (Islas Malvinas)', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Faroe Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Fiji', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Finland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'France', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'French Guiana', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'French Polynesia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'French Southern and Antarctic Lands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Gabon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Gambia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Gaza Strip', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Georgia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Germany', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Ghana', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Gibraltar', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Glorioso Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Greece', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Greenland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Grenada', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guadeloupe', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guam', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guatemala', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guernsey', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guinea', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guinea-Bissau', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Guyana', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Haiti', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Heard Island and McDonald Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Honduras', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Hong Kong', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Howland Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Hungary', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Iceland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'India', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Indian Ocean', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Indonesia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Iran', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Iraq', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Ireland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Isle of Man', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Israel', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Italy', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Jamaica', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Jan Mayen', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Japan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Jarvis Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Jersey', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Johnston Atoll', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Jordan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Juan de Nova Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kazakhstan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kenya', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kingman Reef', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kiribati', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kerguelen Archipelago', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kuwait', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Kyrgyzstan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Laos', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Latvia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Lebanon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Lesotho', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Liberia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Libya', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Liechtenstein', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Lithuania', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Luxembourg', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Macau', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Macedonia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Madagascar', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Malawi', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Malaysia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Maldives', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mali', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Malta', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Marshall Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Martinique', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mauritania', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mauritius', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mayotte', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mexico', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Micronesia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Midway Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Moldova', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Monaco', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mongolia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Montenegro', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Montserrat', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Morocco', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Mozambique', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Myanmar', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Namibia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Nauru', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Navassa Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Nepal', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Netherlands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Netherlands Antilles', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'New Caledonia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'New Zealand', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Nicaragua', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Niger', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Nigeria', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Niue', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Norfolk Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'North Korea', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Northern Mariana Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Norway', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Oman', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Pacific Ocean', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Pakistan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Palau', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Palmyra Atoll', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Panama', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Papua New Guinea', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Paracel Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Paraguay', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Peru', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Philippines', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Pitcairn Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Poland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Portugal', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Puerto Rico', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Qatar', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Reunion', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Republic of the Congo', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Romania', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Russia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Rwanda', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Saint Helena', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Saint Kitts and Nevis', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Saint Lucia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Saint Pierre and Miquelon', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Saint Vincent and the Grenadines', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Samoa', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'San Marino', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Sao Tome and Principe', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Saudi Arabia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Senegal', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Serbia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Seychelles', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Sierra Leone', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Singapore', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Slovakia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Slovenia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Solomon Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Somalia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'South Africa', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'South Georgia and the South Sandwich Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'South Korea', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Spain', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Spratly Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Sri Lanka', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Sudan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Suriname', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Svalbard', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Swaziland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Sweden', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Switzerland', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Syria', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Taiwan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tajikistan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tanzania', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Thailand', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Togo', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tokelau', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tonga', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Trinidad and Tobago', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tromelin Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tunisia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Turkey', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Turkmenistan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Turks and Caicos Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Tuvalu', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Uganda', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Ukraine', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'United Arab Emirates', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'United Kingdom', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'USA', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Uruguay', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Uzbekistan', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Vanuatu', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Venezuela', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Viet Nam', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Virgin Islands', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Wake Island', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Wallis and Futuna', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'West Bank', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Western Sahara', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Yemen', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Yugoslavia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Zambia', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 28, 'Zimbabwe', 1, 'N');

-- Soil Types
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Acrisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Albeluvisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Alisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Andosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Anthrosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Arenosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Calcisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Cambisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Chernozem', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Cryosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Durisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Ferralsol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Fluvisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Gleysol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Gypsisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Histosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Kastanozem', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Leptosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Lixisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Luvisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Nitisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Phaeozem', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Planosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Plinthosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Podzol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Regosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Solonchak', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Solonetz', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Stagnosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Technosol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Umbrisol', 1, 'N');
insert into controlled_vocab_values ( vocab_value_id, controlled_vocab_id, term, order_by, default_item ) values (seq_vocab_values.nextval, 29, 'Vertisol', 1, 'N');
commit;

-------------------------------------------
-- Column/Database Dictionary
-------------------------------------------

-- Study
set define ~
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('yn', 'submit_to_insdc', '[y/n]', 'Depending on the study (large-scale e.g. done with next generation sequencing technology, or small-scale) sequences have to be submitted to SRA (Short Read Archives), ENA (European Nucleotide Archive), DRA (DDBJ Read Archive) or via the classical Webin/Sequin systems to Genbank, EMBL and DDBJ');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'investigation_type',	'[eukaryote, bacteria_archaea, plasmid, virus, organelle, metagenome, miens-survey or miens-culture]',	'Nucleic Acid Sequence Report is the root element of all MIGS/MIMS compliant reports as standardized by Genomic Standards Consortium. This field is either eukaryote,bacteria,virus,plasmid,organelle, metagenome, miens-survey or miens-culture)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'project_name', 'text', 'Name of the project within which the sequencing was organized');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'experimental_factor', '(the experimental design of the study) [EFO and/or OBI]', 'A factor is a variable which is deliberately varied between trials, in order to study its influence on the outcome. There are two main types of variables to consider: treatment factors, when you are especially interested in studying how the outcome varies as a function of these factors; and confounders, other factors or covariates, such as temperature, pH, humidity, drift over time, etc... that may influence the outcome. In the biological or health sciences, age, sex and other characteristics of an individual may be confounders. This field accepts ontology terms from EFO and/or OBI. For a browser of EFO terms, please see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=EFO; for a browser of OBI terms please see http://bioportal.bioontology.org/visualize/40832');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'env_package', '[air,host-associated,human-associated,human-skin,human-oral,human-gut,human-vaginal,microbial mat/biofilm,miscellaneous natural or artificial environment,plant-associated,sediment,soil,wastewater/sludge,water]', 'MIMS/MIENS extension for reporting of parameters obtained from one or more of the environments listed. All the environments listed here have separate subtables of fields. After indicating which environmental package(s) was used, a selection of fields can be made from the subtables and can be reported within the MIENS report');
commit;

-- Sample
set define ~
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('yn', 'public', '[y/n]', 'Whether the sample will be public or private');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sample_name', 'text', 'A unique identifier for the sample.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('yn', 'assigned_from_geo', 'y/n', 'Was this sample''s geolocated data assigned from a standard source? If not or data is of a highly imprecise nature, choose ''n''');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'biological_specimen', '[text]', 'A unique name for this biological specimen. This should be a reference to who or what the sample was taken from.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'collection_date',	'date or date/time values', 'The time of sampling, single point in time. In case no exact time is available, the time can be truncated. This is a 24-hour time format. Valid examples: "11/30/2003 10:12:24", "2/29/2003 20:14:56", "5/22/2003". Date ranges may also be specified. In the instance where deidentified data is necessary, truncate the date to the appropriate level of detail.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'latitude', '[float]', 'The geographical origin of the sample as defined by latitude and longitude. The values should be reported in decimal degrees and in WGS84 system');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'longitude', '[float]', 'The geographical origin of the sample as defined by latitude and longitude. The values should be reported in decimal degrees and in WGS84 system');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('range', 'depth', '[float] or [range], examples: 5, 3.4, 0-5', 'The geographical origin of the sample as defined by depth. Depth is defined as the distance from surface, e.g. for sediment samples depth is measured from sediment surface. Depth can be reported as an interval for subsurface samples');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'altitude', '([float])', 'The altitude of the sample is the distance between surface and the sampled position.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'elevation', '(elevation of site [float]; altitude of sample [float])', 'The geographical origin of the sample as defined by altitude and/or elevation. The elevation of the site is measured from the sea level.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'country', '[country:INSDC or GAZ;region:GAZ]', 'The geographical origin of the sample as defined by the country. Country names should be chosen from the INSDC list (http://www.insdc.org/country.html), or the GAZ ontology (http://bioportal.bioontology.org/visualize/40651)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'env_biome', '(biome [EnvO])', 'Description of the environment type where the sample was originally obtained from with EnvO terms. EnvO terms can be used on three different levels. Biomes are defined based on factors such as plant structures, leaf types, plant spacing, and other factors like climate. Examples include: desert, taiga, deciduous woodland, coral reef. For a browser of EnvO terms, please see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=ENVO');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'env_feature', '(feature [EnvO])', 'Description of the environment type where the sample was originally obtained from with EnvO terms. EnvO terms can be used on three different levels. Environmental feature level includes geographic environmental features. Examples include: harbour, cliff, lake. For a browser of EnvO terms, please see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=ENVO');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'env_matter', '(matter [EnvO])', 'Description of the environment type where the sample was originally obtained from with EnvO terms. EnvO terms can be used on three different levels. The environmental matter level refers to the matter that was displaced by the sample, prior to the sampling event. Environmental matter terms are generally mass nouns. Examples include: air, soil, water. For a browser of EnvO terms, please see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=ENVO');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'organism_count', '[text=numeric value],multiple', 'total count of any organism per gram or volume of sample,should include name of organism followed by count; can include multiple organism counts');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'oxy_stat_samp', '[aerobe/anaerobe/facultative/microaerophilic/microanaerobe/obligate aerobe/obligate anaerobe]', 'oxygenation status of sample');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'perturbation', '[text; start_timestamp;end_timestamp], multiple', 'type of perturbation, e.g. chemical administration, physical disturbance, etc., coupled with time that perturbation occurred; can include multiple perturbation types');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'ph', '[numeric value]', 'pH measurement');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'samp_collect_device', '(e.g. biopsy, niskin bottle, push core)', 'The method or deviced employed for collecting the sample');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'samp_mat_process', '(e.g. filtering of seawater, storing samples in ethanol) [OBI]', 'Any processing applied to the sample during or after retrieving the sample from environment. This field accepts OBI (Ontology for Biomedical Investigations), for a browser of OBI terms please see http://bioportal.bioontology.org/visualize/40547');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'samp_salinity', '[numeric value]', 'salinity of sample, i.e. measure of total salt concentration');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'samp_store_dur', '[start_timestamp;end_timestamp]', 'duration for which sample was stored, e.g. 8/1/2003-7/24/2005""');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'samp_store_loc', '[text]', 'location at which sample was stored, usually name of a specific freezer/room');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'samp_store_temp', '[numeric value]', 'temperature at which sample was stored, e.g. -80');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'temp', '[numeric value]', 'temperature of the sample at time of sampling');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'samp_size', '[integer, unit]', 'Amount or size of sample (volume, mass or area) that was collected');
commit;

-- Prep/sequencing
set define ~
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'nucl_acid_ext', '(extraction method) [PMID, DOI or url]', 'Link to a literature reference, electronic resource or a standard operating procedure (SOP)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'nucl_acid_amp', '(amplification method; clean-up method) [PMID, DOI or url]', 'Link to a literature reference, electronic resource or a standard operating procedure (SOP)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'lib_size', '(library size) [integer]', 'Total number of clones in library prepared for the project');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'lib_reads_seqd', '(number of reads sequenced) [integer]', 'Total number of clones sequenced ');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'lib_vector', '(vector) [CV]', 'Cloning vector type(s) used in construction of libraries');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'libr_screen', '(e.g. enriched, screened, normalized) [CV]', 'Specific enrichment or screening methods applied before and/or after creating clone libraries');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'target_gene', '(e.g. 16S rRNA, 18S rRNA, nif, amoA, rpo, V6, ITS)', 'Targeted gene or locus name for marker gene studies');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'target_subfragment', '(e.g. V6, V9, ITS)', 'Name of subfragment of a gene or locus. Important to e.g. identify special regions on marker genes like V6 on 16S rRNA.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pcr_primers', '[FWD: forward primer sequence; REV:reverse primer sequence]', 'PCR primers, barcodes and adaptors that were used to amplify the sequence of the targeted gene or locus. This field should contain all the primers used for a single PCR reaction if multiple forward or reverse primers are present in a single PCR reaction. The primer sequence should be reported in uppercase letters, however in case of the presence of a barcode or adaptor sequence, the relevant strectches of nucleotides should be reported in lowercase letters.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'multiplex_ident', '[multiplex identifier sequence]', 'Molecular barcodes, called Multiplex Identifiers (MIDs), that are used to specifically tag unique samples in a sequencing run. Sequence should be reported in uppercase letters');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pcr_cond', '[initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; final elongation:degrees_minutes; total cycles]', 'Description of reaction conditions and components for PCR in the form of  ''initial denaturation:94degC_1.5min; annealing=...''');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sequencing_meth', '(e.g. dideoxysequencing, pyrosequencing, polony) [OBI]', 'Sequencing method used; e.g. Sanger, pyrosequencing, ABI-solid');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'seq_quality_check', '[none or manually edited]', 'Indicate if the sequence has been called by automatic systems (none) or undergone a manual editing procedure (e.g. by inspecting the raw data or chromatograms). Applied only for sequences that are not submitted to SRA,ENA or DRA');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'chimera_check', '[software]', 'A chimeric sequence, or chimera for short, is a sequence comprised of two or more phylogenetically distinct parent sequences. Chimeras are usually PCR artifacts thought to occur when a prematurely terminated amplicon reanneals to a foreign DNA strand and is copied to completion in the following PCR cycles. The point at which the chimeric sequence changes from one parent to the next is called the breakpoint or conversion point. ');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sop', '(SOPs)', 'A standard operating procedure is a set of instructions having the force of a directive, covering those features of operations that lend themselves to a definite or standardized procedure without loss of effectiveness');
commit;

-- Package specific
set define ~
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('yn', 'hiv_stat', '[y/n]', 'HIV status of subject, if yes HAART initiation status should also be indicated as [YES or NO]');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'hrt', '[timestamp]', 'whether subject had hormone replacement theraphy, and if yes start date');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'ihmc_ethnicity', '[IHMC code or free text]', 'ethnicity of the subject. IHMC ethnicity codes are; 01=Hispanic or Latino or Spanish, 02=Non-Hispanic or Non-Latino or Non- Spanish');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'ihmc_medication_code', '[IHMC code], multiple', 'can include multiple medication codes. 01=1=Analgesics/NSAIDS, 02=2=Anesthetics, 03=3=Antacids/H2  antagonists, 04=4=Anti-acne, 05=5=Anti-asthma/bronchodilators, 06=6=Anti-cholesterol/Anti-hyperlipidemic, 07=7=Anti-coagulants, 08=8=Antibiotics/(anti)-infectives, parasitics, microbials, 09=9=Antidepressants/mood-altering drugs, 10=10=Antihistamines/ Decongestants, 11=11=Antihypertensives, 12=12=Cardiovascular, other than hyperlipidemic/HTN, 13=13=Contraceptives (oral, implant, injectable), 14=14=Emergency/support medications, 15=15=Endocrine/Metabolic agents, 16=16=GI meds (anti-diarrheal, emetic, spasmodics), 17=17=Herbal/homeopathic products, 18=18=Hormones/steroids, 19=19=OTC cold & flu, 20=20=Vaccine prophylaxis, 21=21=Vitamins, minerals, food supplements, 99=99=Other');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'age', '[numeric value]', 'age of host at the time of sampling; relevant scale depends on species and study, e.g. could be seconds for amoebae or centuries for trees');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'age_unit', '[text]', 'units of the age field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'air_temp_regm', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving an exposure to varying temperatures; should include the temperature, treatment duration, interval and total experimental duration; can include different temperature regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'alkalinity', '[numeric value]', 'alkalinity measurement');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'alkyl_diethers', '[numeric value]', 'concentration of alkyl diethers');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'aminopept_act', '[numeric value]', 'measurement of aminopeptidase activity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'ammonium', '[numeric value]', 'concentration of ammonium');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'amniotic_fluid_color', '[text]', 'specification of the color of the amniotic fluid sample');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'foetal_health_stat', '[text]', 'specification of foetal health status, should also include abortion');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'gestation_state', '[text]', 'specification of the gestation state');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'maternal_health_stat', '[text]', 'specification of the maternal health status');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'antibiotic_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving antibiotic administration; should include the name of antibiotic, amount administered, treatment duration, interval and total experimental duration; can include multiple antibiotic regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'atmospheric_data', '[text=numeric value], multiple', 'measurement of atmospheric data; can include multiple data');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'bacteria_carb_prod', '[numeric value]', 'measurement of bacterial carbon production');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'barometric_press', '[numeric value]', 'force per unit area exerted against a surface by the weight of air above that surface');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'biochem_oxygen_dem', '[numeric value]', 'a measure of the relative oxygen-depletion effect of a waste contaminant');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'biomass', '[text=numeric value], multiple', 'amount of biomass; should include the name for the part of biomass measured, e.g. microbial, total. can include multiple measurements');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'birth_control', '[text]', 'specification of birth control medication used');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'bishomohopanol', '[numeric value]', 'concentration of bishomohopanol ');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'blood_press_diast', '[numeric value]', 'resting diastolic blood pressure, measured as mm mercury');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'blood_press_syst', '[numeric value]', 'resting systolic blood pressure, measured as mm mercury');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'blood_disord', '[text], multiple', 'history of blood disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'body_habitat', '[FMA]', 'original body habitat where the sample was obtained from.name of body site that the sample was obtained from. for FMA (Foundational Model of Anatomy) browser see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=FMA');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'body_product', '[FMA]', 'substance produced by the body, e.g. stool, mucus, where the sample was obtained from. for FMA (Foundational Model of Anatomy) browser see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=FMA');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'body_site', '[FMA]', 'name of body site that the sample was obtained from. for FMA (Foundational Model of Anatomy) browser see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=FMA');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'body-mass_index', '[numeric value]', 'body mass index, calculated as weight/(height)squared');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'bromide', '[numeric value]', 'concentration of bromide');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'calcium', '[numeric value]', 'concentration of calcium');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'carb_dioxide', '[numeric value]', 'carbon dioxide (gas) amount or concentration at the time of sampling');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'carb_monoxide', '[numeric value]', 'carbon monoxide (gas) amount or concentration at the time of sampling');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'carb_nitro_ratio', '[numeric value]', 'ratio of amount or concentrations of carbon to nitrogen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'chem_administration', '[CHEBI; timestamp], multiple', 'list of chemical compounds administered to the host or site where sampling occurred, and when (e.g. antibiotics, N fertilizer, air filter); can include multiple compounds. for CHEBI, see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=CHEBI');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'chem_mutagen', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'treatment involving use of mutagens; should include the name of mutagen, amount administered, treatment duration, interval and total experimental duration; can include multiple mutagen regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'chem_oxygen_dem', '[numeric value]', 'a measure of the relative oxygen-depletion effect of a waste contaminant');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'chloride', '[numeric value]', 'concentration of chloride ');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'chlorophyll', '[numeric value]', 'concentration of chlorophyll');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'climate_environment', '[text;treatment duration;interval;experimental duration], multiple', 'treatment involving an exposure to a particular climate; can include multiple climates');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sieving', '[name]', 'collection design of pooled samples and/or sieve size and amount of sample sieved');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'current', '[numeric value]', 'measurement of current');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'cur_land_use', '[enumeration]', 'present state of sample site. values are; urban (artificial cover):cities, farmstead, industrial areas, roads/railroads; barren land:rock, sand, gravel, mudflats, salt flats, badlands, permanent snow or ice, saline seeps, mines/quarries, oil waste areas; crop cover:small grains, row crops, vegetable crops, horticultural plants (e.g., tulips); grass/herbaceous cover: marshlands (grass, sedges, rushes), tundra (mosses, lichens), rangeland, pastureland (grasslands used for livestock grazing), hayland, meadows (grasses, alfalfa, fescue, bromegrass, timothy); shrub cover: shrub land (e.g., mesquite, sage-brush, creosote bush, shrub oak, eucalyptus), successional shrub land (tree saplings, hazels, sumacs, chokecherry, shrub dogwoods, blackberries), shrub crops (blueberries, nursery ornamentals, filberts), vine crops (grapes); tree cover:conifers (e.g., pine, spruce, fir, cypress), hardwoods (e.g., oak, hickory, elm, aspen), intermixed hardwood and conifers, tropical (e.g., mangrove, palms), rainforest (evergreen forest receiving >406 cm annual rainfall), swamp (permanent or semi-permanent water body dominated by woody plants), crop trees (nuts, fruit, christmas trees, nursery trees)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'cur_vegetation', '[enumeration]', 'vegetation classification from one or more standard classification systems, or agricultural crop');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'cur_vegetation_meth', '[PMID,DOI or link]', 'reference or method used in vegetation classification');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'density', '[numeric value]', 'density of sample');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'dermatology_disord', '[text], multiple', 'history of dermatology disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'diet', '[text],multiple', 'type of diet depending on the host, for animals omnivore, herbivore etc., for humans high-fat, meditteranean etc.; can include multiple diet types');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'diether_lipids', '[text=numeric value], multiple', 'concentration of diether lipids; can include multiple types of diether lipids');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'disease_stat', '[text or DO], multiple', 'list of diseases with which the host has been diagnosed; can include multiple diagnoses. the value of the field depends on host; for humans the terms should be chosen from DO (Disease Ontology), other hosts are free text. for disease ontology see; http://gemina.svn.sourceforge.net/viewvc/gemina/trunk/Gemina/ontologies/gemina_symptom.obo?view=log');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'diss_carb_dioxide', '[numeric value]', 'concentration of dissolved carbon dioxide');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'diss_hydrogen', '[numeric value]', 'concentration of dissolved hydrogen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'diss_inorg_nitro', '[numeric value]', 'concentration of dissolved inorganic nitrogen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'diss_inorg_phosp', '[numeric value]', 'concentration of dissolved inorganic phosphorus ');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'diss_org_carb', '[numeric value]', 'concentration of dissolved organic carbon');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'diss_oxygen', '[numeric value]', 'concentration of dissolved oxygen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'dominant_hand', '[left/right/ambidextrous]', 'dominant hand of the subject');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'douche', '[timestamp]', 'date of most recent douche');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'drainage_class', '[enumeration]', 'drainage classification from a standard system such as the USDA system. possible values are; very poorly, poorly, somewhat poorly, moderately well, well, excessively drained');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'drug_usage', '[text=frequency], multiple', 'any drug used by subject and the frequency of usage; can include multiple drugs used');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'dry_mass', '[numeric value]', 'measurement of dry mass');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'efficiency_percent', '[numeric value]', 'percentage of volatile solids removed from the anaerobic digestor');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'emulsions', '[text=numeric value], multiple', 'amount or concentration of substances such as paints, adhesives, mayonnaise, hair colorants, emulsified oils, etc.; can include multiple emulsion types');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'al_sat', '[numeric value]', 'aluminum saturation (esp. for tropical soils)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'al_sat_meth', '[PMID,DOI or link]', 'reference or method used in determining Al saturation');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'heavy_metals', '[numeric value]', 'heavy metals present and concentrations');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'heavy_metals_meth', '[PMID,DOI or link]', 'reference or method used in determining heavy metals');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'extreme_salinity', '[numeric value]', 'measured salinity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'salinity_meth', '[PMID,DOI or link]', 'reference or method used in determining salinity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'family_relationship', '[arbitrary id;relationship type], multiple', 'relationships to other hosts in the same study, e.g. child of host # 131; can include multiple relationships');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'fertilizer_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving the use of fertilizers; should include the name fertilizer, amount administered, treatment duration, interval and total experimental duration; can include multiple fertilizer regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'fungicide_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving use of fungicides; should include the name of fungicide, amount administered, treatment duration, interval and total experimental duration; can include multiple fungicide regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'gaseous_environment', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'use of conditions with differing gaseous environments; should include the name of gaseous compound, amount administered, treatment duration, interval and total experimental duration; can include multiple gaseous environment regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'gaseous_substances', '[text=numeric value], multiple', 'amount or concentration of substances such as hydrogen sulfide, carbon dioxide, methane, etc.; can include multiple substances');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'gastrointest_disord', '[text], multiple', 'history of gastrointestinal tract disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'genotype', '[text]', 'observed genotype');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'glucosidase_act', '[numeric value]', 'measurement of glucosidase activity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'gravidity', '[timestamp]', 'whether or not subject is gravid, and if yes date due or date post-conception, specifying which is used');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'gravity', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving use of gravity factor to study various types of responses in presence, absence or modified levels of gravity; can include multiple treatments');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'growth_hormone_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving use of growth hormones; should include the name of growth hormone, amount administered, treatment duration, interval and total experimental duration; can include multiple growth hormone regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'growth_med', '[soil/liquid]', 'information about growth media for growing the plants or tissue cultured samples');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'gynecologic_disord', '[text], multiple', 'history of gynecological disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'height_or_length', '[numeric value]', 'measurement of height or length');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'herbicide_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving use of herbicides; information about treatment involving use of growth hormones; should include the name of herbicide, amount administered, treatment duration, interval and total experimental duration; can include multiple regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'agrochem_addition', '[name]', 'addition of fertilizers, pesticides, etc. - amount and time of applications');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'crop_rotation', '[name]', 'whether or not crop is rotated, and if yes, rotation schedule');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'extreme_event', '[date]', 'unusual physical events that may have affected microbial populations');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'fire', '[date]', 'historical and/or physical evidence of fire');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'flooding', '[date]', 'historical and/or physical evidence of flooding');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'previous_land_use', '[name]', 'previous land use and dates');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'previous_land_use_meth', '[PMID,DOI or link]', 'reference or method used in determining previous land use and dates');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'tillage', '[enumeration]', 'note method(s) used for tilling. values are conservation tillage or zero tillage: drill or cutting disc; reduced tillage: ridge till, strip tillage, zonal tillage, chisel or tined; conventional tillage: mouldboard or disc plough');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'horizon', '[enumeration]', 'specific layer in the land area which measures parallel to the soil surface and possesses physical characteristics which differ from the layers above and beneath. values are; O horizon, A horizon, E horizon, B horizon, C horizon, R layer, Permafrost');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'horizon_meth', '[PMID,DOI or link]', 'reference or method used in determining the horizon');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'host_body_temp', '[numeric value]', 'core body temperature of the host when sample was collected');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'host_color', '[text]', 'the color of host');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'host_common_name', '[text]', 'common name of the host, e.g. human');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'host_growth_cond', '[PMID,DOI,url or free text]', 'literature reference giving growth conditions of the host');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'host_shape', '[text]', 'morphological shape of host');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'host_subject_id', '[unique identifier within each study]', 'a unique identifier by which each subject can be referred to, de-identified, e.g. #131');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'host_taxid', '[NCBI taxon id], example: 9606', 'NCBI taxon id of the host, e.g. 9606');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'humidity', '[numeric value]', 'amount of water vapour in the air, at the time of sampling');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'humidity_regm', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving an exposure to varying degree of humidity; information about treatment involving use of growth hormones; should include amount of humidity administered, treatment duration, interval and total experimental duration; can include multiple regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'hysterectomy', '[YES or NO]', 'specification of whether hysterectomy was performed');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'indust_eff_percent', '[numeric value]', 'percentage of industrial effluents received by wastewater treatment plant');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'infra_specific_name', '[text]', 'taxonomic information about the host below subspecies level');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'infra_specific_rank', '[text]', 'taxonomic rank information about the host below subspecies level, such as variety, form, rank etc...');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'inorg_particles', '[text=numeric value], multiple', 'concentration of particles such as sand, grit, metal particles, ceramics, etc.; can include multiple particles');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'last_meal', '[text; start_time; end_time], multiple', 'content of last meal and time since feeding; can include multiple values');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'life_stage', '[text]', 'description of life stage of host');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'light_intensity', '[numeric value]', 'measurement of light intensity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'link_class_info', '[text]', 'link to digitized soil maps or other soil classification information');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'link_climate_info', '[text]', 'link to climate resource');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'link_addit_analys', '[text]', 'link to additional analysis');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'liver_disord', '[text], multiple', 'history of liver disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'nose_throat_disord', '[text], multiple', 'history of nose-throat disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pulmonary_disord', '[text], multiple', 'history of pulmonary disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'magnesium', '[numeric value]', 'concentration of magnesium');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'diet_last_six_month', '[YES or NO]', 'specification of major diet changes in the last six months, if yes the change should be specified');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'annual_season_precpt', '[numeric value]', 'mean annual and seasonal precipitation (mm)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'annual_season_temp', '[numeric value]', 'mean annual and seasonal temperature (oC)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'mean_frict_vel', '[numeric value]', 'measurement of mean friction velocity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'mean_peak_frict_vel', '[numeric value]', 'measurement of mean peak friction velocity');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'mechanical_damage', '[text=body site], multiple', 'information about any mechanical damage exerted on the plant; can include multiple damages and sites');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'medic_hist_perform', '[true or false]', 'whether full medical history was collected');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'menarche', '[timestamp]', 'date of most recent menstruation');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'menopause', '[timestamp]', 'date of onset of menopause');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'methane', '[numeric value]', 'methane (gas) amount or concentration at the time of sampling');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'microbial_biomass', '[numeric value,DOI,PMID,link or text]', 'the part of the organic matter in the soil that constitutes living microorganisms smaller than 5-10 µm. IF you keep this, you would need to have correction factors used for conversion to the final units, which should be mg C (or N)/kg soil).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'microbial_biomass_meth', '[DOI,PMID or link]', 'reference or method used in determining microbial biomass');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'mineral_nutr_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving the use of mineral supplements; should include the name of mineral nutrient, amount administered, treatment duration, interval and total experimental duration; can include multiple mineral nutrient regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'misc_param', '[text=numeric value or text], multiple', 'any other measurement performed or parameter collected, that is not listed here.should be given in the form of measurement name/parameter name=value and unit; can include multiple measurements or parameters');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'n_alkanes', '[text=numeric value], multiple', 'concentration of n-alkanes; can include multiple n_alkanes');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'nitrate', '[numeric value]', 'concentration of nitrate');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'nitrite', '[numeric value]', 'concentration of nitrite');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'nitro', '[numeric value]', 'concentration of nitrogen (total)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'non_mineral_nutr_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving the exposure of plant to non-mineral nutrient such as oxygen, hydrogen or carbon; should include the name of non-mineral nutrient, amount administered, treatment duration, interval and total experimental duration; can include multiple non-mineral nutrient regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'nose_mouth_teeth_throat_disord', '[text], multiple', 'history of nose/mouth/teeth/throat disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'num_replicons', '(for eukaryotes and bacteria: chromosomes (haploid count); for viruses: segments) [integer]', 'Reports the number of replicons in a nuclear genome of eukaryotes, in the genome of a bacterium or archaea or the number of segments in a segmented virus. Always applied to the haploid chromosome count of a eukaryote');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'occupation', '[IHMC code]', 'most frequent job performed by subject. IHMC codes are; 01=01 Accounting/Finance, 02=02 Advertising/Public Relations, 03=03  Arts/Entertainment/Publishing, 04=04 Automotive, 05=05 Banking/ Mortgage, 06=06 Biotech, 07=07 Broadcast/Journalism, 08=08 Business  Development, 09=09 Clerical/Administrative, 10=10 Construction/Trades,  11=11 Consultant, 12=12 Customer Services, 13=13 Design, 14=14  Education, 15=15 Engineering, 16=16 Entry Level, 17=17 Executive,  18=18 Food Service, 19=19 Government, 20=20 Grocery, 21=21 Healthcare,  22=22 Hospitality, 23=23 Human Resources, 24=24 Information  Technology, 25=25 Insurance, 26=26 Law/Legal, 27=27 Management, 28=28  Manufacturing, 29=29 Marketing, 30=30 Pharmaceutical, 31=31  Professional Services, 32=32 Purchasing, 33=33 Quality Assurance (QA),  34=34 Research, 35=35 Restaurant, 36=36 Retail, 37=37 Sales, 38=38  Science, 39=39 Security/Law Enforcement, 40=40 Shipping/Distribution,  41=41 Strategy, 42=42 Student, 43=43 Telecommunications, 44=44  Training, 45=45 Transportation, 46=46 Warehouse, 47=47 Other, 99=99  Unknown/Refused');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'org_carb', '[numeric value]', 'concentration of organic carbon');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'org_matter', '[numeric value]', 'concentration of organic matter'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'org_nitro', '[numeric value]', 'concentration of organic nitrogen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'org_particles', '[text=numeric value], multiple', 'concentration of particles such as faeces, hairs, food, vomit, paper fibers, plant material, humus, etc…');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'other', '[text]', 'additional relevant information');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'oxygen', '[numeric value]', 'oxygen (gas) amount or concentration at the time of sampling');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'ph_meth', '[PMID,DOI or link]', 'reference or method used in determining pH');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'ph_regm', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving exposure of plants to varying levels of pH of the growth media; can include multiple regimen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'particle_class', '[text=numeric value], multiple', 'particles are classified, based on their size, into six general categories:clay, silt, sand, gravel, cobbles, and boulders; should include amount of particle preceded by the name of the particle type; can include multiple values');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'part_org_carb', '[numeric value]', 'concentration of particulate organic carbon');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'part_org_nitro', '[numeric value]', 'concentration of particulate organic nitrogen');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pesticide_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving use of insecticides; should include the name of pesticide, amount administered, treatment duration, interval and total experimental duration; can include multiple pesticide regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'petroleum_hydrocarb', '[numeric value]', 'concentration of petroleum hydrocarbon');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'phaeopigments', '[numeric value], multiple', 'concentration of phaeopigments; can include multiple phaeopigments');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'phenotype', '[PATO]', 'phenotype of host. for PATO, see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=PATO');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'phosphate', '[numeric value]', 'concentration of phosphate');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'phosplipid_fatt_acid', '[text=numeric value], multiple', 'concentration of phospholipid fatty acids; can include multiple values');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'photon_flux', '[numeric value]', 'measurement of photon flux');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'plant_body_site', '[PO]', 'name of body site that the sample was obtained from. for PO (Plant Ontology) browser see http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=PO');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'plant_product', '[text]', 'substance produced by the plant, where the sample was obtained from');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'ploidy', '(e.g. allopolyploid, polyploid) [PATO]', 'The ploidy level of the genome (e.g. allopolyploid, haploid, diploid, triploid, tetraploid). It has implications for the downstream study of duplicated gene and regions of the genomes (and perhaps for difficulties in assembly). For terms, please select terms listed under class ploidy (PATO:001374) of PATO, and for a browser of PATO please refer to http://www.ebi.ac.uk/ontology-lookup/browse.do?ontName=PATO');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pollutants', '[text=numeric value], multiple', 'pollutant types and, amount or concentrations measured at the time of sampling; can report multiple pollutants by entering numeric values preceded by name of pollutant');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'pool_dna_extracts', '[numeric value]', 'were multiple DNA extractions mixed? how many?');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'porosity', '[numeric value]', 'porosity of deposited sediment is volume of voids divided by the total volume of sample');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'potassium', '[numeric value]', 'concentration of potassium'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pre_treatment', '[text]', 'the process of pre-treatment removes materials that can be easily collected from the raw wastewater');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'pregnancy', '[timestamp]', 'date due of pregnancy');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'pet_farm_animal', '[text], multiple', 'specification of presence of pets or farm animals in the environment of subject, if yes the animals should be specified; can include multiple animals present');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'press', '[numeric value]', 'pressure to which the sample is subject, in atmospheres');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'primary_prod', '[numeric value]', 'measurement of primary production'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'primary_treatment', '[text]', 'the process to produce both a generally homogeneous liquid capable of being treated biologically and a sludge that can be separately treated or processed');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'profile_position', '[enumeration]', 'cross-sectional position in the hillslope where sample was collected.sample area position in relation to surrounding areas:  depression, % slope, ridge top, upland, stream terrace, alluvial plane, etc. values are; summit, shoulder, backslope, footslope, toeslope');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'pulse', '[numeric value]', 'resting pulse, measured as beats per minute');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'radiation_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving exposure of plant or a plant part to a particular radiation regimen; should include the radiation type, amount or intensity administered, treatment duration, interval and total experimental duration; can include multiple radiation regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'rainfall_regm', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving an exposure to a given amount of rainfall; can include multiple regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'reactor_type', '[text]', 'anaerobic digesters can be designed and engineered to operate using a number of different process configurations, as batch or continuous, mesophilic, high solid or low solid, and single stage or multistage');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'redox_potential', '[numeric value]', 'redox potential, measured relative to a hydrogen cell, indicating oxidation or reduction potential');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'url', '[url]', 'url');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'resp_part_matter', '[text=numeric value], multiple', 'concentration of substances that remain suspended in the air, and comprise mixtures of organic and inorganic substances (PM10 and PM2.5); can report multiple PM''s by entering numeric values preceded by name of PM');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'salinity', '[numeric value]', 'salinity measurement');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'salt_regm', '[text=numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving use of salts as supplement to liquid and soil growth media; should include the name of salt, amount administered, treatment duration, interval and total experimental duration; can include multiple salt regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'samp_weight_dna_ext', '[numeric value]', 'weight (g) of soil processed');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'season_environment', '[text;treatment duration;interval;experimental duration], multiple', 'treatment involving an exposure to a particular season (e.g. winter, summer, rabi, rainy etc…)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'secondary_treatment', '[text]', 'the process for substantially degrading the biological content of the sewage'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sediment_type', '[biogenous/cosmogenous/hydrogenous/lithogenous]', 'information about the sediment type based on major constituents');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sewage_type', '[text]', 'type of wastewater treatment plant as municipial or industrial');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'sex', '[male/female/neuter/hermaphrodite/not determined]', 'physical sex of the host');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'sexual_act', '[partner=male or female;frequency]', 'current sexual partner and frequency of sex');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'silicate', '[numeric value]', 'concentration of silicate');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'slope_aspect', '[numeric value]', 'the direction a slope faces. While looking down a slope use a compass to record the direction you are facing (direction or degrees); e.g., NW or 315°.  This measure provides an indication of sun and wind exposure that will influence soil temperature and evapotranspiration.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'slope_gradient', '[numeric value]', 'commonly called “slope.”  The angle between ground surface and a horizontal line (in percent).  This is the direction that overland water would flow.  This measure is usually taken with a hand level meter or clinometer.'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'sludge_retent_time', '[numeric value]', 'the time activated sludge remains in reactor');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'smoker', '[YES or NO]', 'specification of smoking status');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'soil_type', '[name]', 'soil series name or other lower-level classification');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'soil_type_meth', '[PMID,DOI or link]', 'reference or method used in determining soil series name or other lower-level classification');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'fao_class', '[enumeration]', 'soil classification from the FAO World Reference Database for Soil Resources http://www.fao.org/ag/agl/agll/wrb/doc/wrb2007_corr.pdf');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'local_class', '[enumeration]', 'soil classification based on local soil classification system');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'local_class_meth', '[PMID,DOI or link]', 'reference or method used in determining the local soil classification'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'solar_irradiance', '[numeric value]', 'the amount of solar energy that arrives at a specific area of a surface during a specific time interval');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'soluble_inorg_mat', '[text=numeric value], multiple', 'concentration of substances such as ammonia, road-salt, sea-salt, cyanide, hydrogen sulfide, thiocyanates, thiosulfates, etc…');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'soluble_org_mat', '[text=numeric value], multiple', 'concentration of substances such as urea, fruit sugars, soluble proteins, drugs, pharmaceuticals, etc…');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'soluble_react_phosp', '[numeric value]', 'concentration of soluble reactive phosphorus');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('ontology', 'source_mat_identifiers', '(cultures of microorganisms: identifiers [alphanumeric] for two culture collections [OBI]; specimens (e.g., organelles and Eukarya): voucher condition and location [CV])', 'The name of the culture collection, holder of the voucher or an institution. Could enumerate a list of common resources, just as the American Type Culture Collection (ATCC), German Collection of Microorganisms and Cell Cultures (DSMZ) etc. Can select not deposited. This field accepts OBI terms, for a browser of OBI terms please see http://bioportal.bioontology.org/visualize/40547');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'special_diet', '[low carb/reduced calorie/vegetarian/other-specify], multiple', 'specification of special diet; can include multiple special diets');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'standing_water_regm', '[text;treatment duration;interval;experimental duration], multiple', 'treatment involving an exposure to standing water during a plant''s life span, types can be flood water or standing water; can include multiple regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'store_cond', '[text]', 'explain how and for how long the soil sample was stored before DNA extraction.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'study_complt_stat', '[(0) complete, (1) adverse event, (2) non-compliance, (3) lost to follow up, (4) other]', 'specification of study completion status.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'substrate', '[text]', 'the growth substrate of the host'); 
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'sulfate', '[numeric value]', 'concentration of sulfate');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'sulfide', '[numeric value]', 'concentration of sulfide');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'suspend_part_matter', '[numeric value]', 'concentration of suspended particulate matter');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'suspend_solids', '[text=numeric value], multiple', 'concentration of substances including a wide variety of material, such as silt, decaying plant and animal matter, etc,; can include multiple substances');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'tertiary_treatment', '[text]', 'the process providing a final treatment stage to raise the effluent quality before it is discharged to the receiving environment');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'texture', '[numeric value]', 'the relative proportion of different grain sizes of mineral particles in a soil, as described using a standard system; express as % sand (50 um to 2 mm), silt (2 um to 50 um), and clay (<2 um) with textural name (e.g., silty clay loam) optional.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'texture_meth', '[PMID,DOI or link]', 'reference or method used in determining soil texture');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'time_last_toothbrush', '[timestamp]', 'specification of the time since last toothbrushing');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('date', 'time_since_last_wash', '[timestamp]', 'specification of the time since last wash');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'tiss_cult_growth_med', '[PMID,DOI,url or text]', 'description of plant tissue culture growth media used');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'tot_n_meth', '[PMID,DOI or link]', 'reference or method used in determining the total N');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_carb', '[numeric value]', 'total carbon content');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_depth_water_col', '[numeric value]', 'measurement of total depth of water column');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_inorg_nitro', '[numeric value]', 'total inorganic nitrogen content');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_mass', '[numeric value]', 'total mass of the host at collection, the unit depends on host');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_nitro', '[numeric value]', 'total amount or concentration of nitrogenous substances');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_org_c_meth', '[PMID,DOI or link]', 'reference or method used in determining total organic C');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_org_carb', '[numeric value]', 'total organic carbon content');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_part_carb', '[numeric value]', 'total particulate carbon content');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_phosphate', '[numeric value]', 'total amount or concentration of phosphate');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'tot_phosp', '[numeric value]', 'total phosphorus content');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'travel_out_six_month', '[text], multiple', 'specification of the countries travelled in the last six months; can include multiple travels');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'turbidity', '[numeric value]', 'turbidity measurement');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'twin_sibling', '[YES or NO]', 'specification of twin sibling presence');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'urine_collect_meth', '[clean catch or catheter]', 'specification of urine collection method');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'kidney_disord', '[text], multiple', 'history of kidney disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'urogenit_tract_disor', '[text], multiple', 'history of urogenitaltract disorders; can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'urogenit_disord', '[text], multiple', 'history of urogenital disorders, can include multiple disorders');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'ventilation_rate', '[numeric value]', 'ventilation rate of the system in the sampled premises');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'ventilation_type', '[text]', 'ventilation system used in the sampled premises');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'volatile_org_comp', '[text=numeric value], multiple', 'concentration of carbon-based chemicals that easily evaporate at room temperature; can report multiple volatile organic compounds by entering numeric values preceded by name of compound');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'wastewater_type', '[text]', 'the origin of wastewater such as human waste, rainfall, storm drains, etc…');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'water_content', '[numeric value]', 'water content measurement');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'water_content_soil', '[numeric value]', 'water content (g/g or cm3/cm3)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'water_content_soil_meth', '[PMID,DOI or link]', 'reference or method used in determining the water content of soil');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'water_temp_regm', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving an exposure to water with varying degree of temperature; can include multiple regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'watering_regm', '[numeric value;treatment duration;interval;experimental duration], multiple', 'information about treatment involving an exposure to watering frequencies; can include multiple regimens');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'weight_loss_3_month', '[YES or NO]', 'specification of weight loss in the last three months, if yes should be further specified to include amount of weight loss');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'wet_mass', '[numeric value]', 'measurement of wet mass');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'wind_direction', '[text]', 'wind direction is the direction from which a wind originates');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'wind_speed', '[numeric value]', 'speed of wind measured at the time of sampling');
commit;

-- SRA Study Fields
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_ALIAS', '[text]', 'One study per publication (i.e. the STUDY is supposed to be about the same amount of info as in a paper). This is something you define arbitrarily, and is used as an id to link files (so can contain only alphanumeric characters and underscores).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_TITLE', '[text]', 'Expected (or actual) title of the paper that will be published about the study. Free text.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('list', 'STUDY_TYPE', '[text]', 'Should be "metagenome" for 16S surveys (regrettably). Other choices relate to whole-genome studies. Controlled vocabulary.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_ABSTRACT', '[text]', 'Abstract, e.g. of the publication. Free text.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_DESCRIPTION', '[text]', 'Use "Targeted Gene Survey" for 16S or other target gene studies');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'CENTER_NAME', '[text], example: "CCME"', 'NCBI-approved name of the center coordinating the overall study, e.g. WUGSC. If you don''t have a center name, you need to get NCBI to define one and then use that - you can''t do this as free text. This will often be the same as other center names.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'CENTER_PROJECT_NAME', '[text]', 'Name of project as used by the center responsible for the study, NULL if none.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'PROJECT_ID', '[text]', 'Project ID, assigned by SRA, leave blank if not yet assigned.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'PMID', '[text]', 'PubMed ID of paper describing project, if supplied will write out STUDY_LINK block, can be multiple (comma-delimited), can be absent if no linked publication yet.');
commit;

-- SRA Sample Fields
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'TITLE', '[text], example: "human hand microbiome"', 'Arbitrary title for your sample that you make up.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'COMMON_NAME', '[text], example: "human skin metagenome"', 'Common name of what is being sequenced, should match taxon id''s name, e.g. human skin metagenome.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'ANONYMIZED_NAME', '[text], example: "subject 1"', 'Anonymized name of the subject, if applicable (e.g. deidentified subject IDs from dbGAP, deidentified subject ids from your study). Only applies to human studies, leave blank if not applicable.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'DESCRIPTION', '[text], example: "female right palm"', 'Free-text description of this specific sample.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'SAMPLE_ALIAS', '[text], example: "S1"', 'Unique (within the STUDY referenced) ID for each sample. You can use the same sample in multiple pools referenced in the same EXPERIMENT. If you mixed samples from more than one STUDY in the same EXPRIMENT, the components from each STUDY need to be a separate EXPERIMENT.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('numeric', 'TAXON_ID', '[integer], example: 539655', 'Taxon Id is what is getting sequenced: i.e txid 539655 = human skin metagenome, species, metagenomes');
commit;

-- SRA Experiment Fields
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'EXPERIMENT_ALIAS', '[text]', 'Unique id (within the submission) for the experiment. Should be the same for everything in a given pool.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'EXPERIMENT_CENTER', '[text]', 'Official abbreviation for the sequencing center associated with the experiment, i.e. who made the pool. Should be the same for every member of a given pool. This is your center name as assigned by NCBI and is often the same as the STUDY center.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'EXPERIMENT_TITLE', '[text]', 'Title  of the experiment: should be the same for every member of a given pool. Free text.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'EXPERIMENT_ACCESSION', '[text]', 'Accession number for the experiment. If you already created the Experiment accession in SRA, use it -- otherwise, leave blank.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_ACCESSION', '[text]', 'Accession number for study. You should already have created the study in SRA in the first stage submission and should reuse that id here.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_REF', '[text]', 'Official STUDY alias of the study, should be the same for every member of a given pool but can be different for different pools. If you put items from multiple STUDY records (e.g. clinical and mock) on the same run, create separate pools but have them reference the same RUN_PREFIX so they can pull sffs from the same files.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'STUDY_CENTER', '[text]', 'Name of the center associated with the overall STUDY, i.e. whoever is designated as having overall responsibility for the STUDY (this is a controlled vocabulary, assigned by NCBI). Should be the same for every member of a pool.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'EXPERIMENT_DESIGN_DESCRIPTION', '[text]', 'Description of the overall motivation for the experiment (i.e. pool) - why those samples were mixed together, what it was for, etc. Should be the same for every member of a pool. Free text.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'LIBRARY_CONSTRUCTION_PROTOCOL', '[text]', 'Free-text description of how the library was put together (e.g. from the methods section of a paper). Should be the same for everything in a given pool. Note that this is a required field.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'SAMPLE_ACCESSION', '[text]', 'Sample accession number, if available (leave blank if you don''t have e.g. an accession assigned by dbGAP).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'SAMPLE_CENTER', '[text]', 'Name of the center that provided the sample, can be separate for each sample.  If sample information is stored in dbGAP, the SAMPLE_CENTER should be set to "NCBI".');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'POOL_MEMBER_ACCESSION', '[text]', 'Accession number for pool member. This should be blank if not already assigned.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'POOL_MEMBER_NAME', '[text]', 'Unique (within the pool) id for each pool member. In the hand example, we only used V2 primers, so I am calling the pool members S1_V2 etc. If you mixed primers, a reasonable thing to do would be to use sample_primer codes; if you did replicates doing different barcodes you might want to use sample_primer_barcode or sample_primer_replicate,if you used different numbers of PCR cycles you might want to use sample_numcycle, etc. Because it''s difficult to predict what the most common use cases are, you must fill this field in manually (or leave it blank, in which case the SAMPLE_ALIAS will be used and assumed to be unique).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'POOL_PROPORTION', '[text]', 'Floating-point number representing the fraction of the pool that was intended to come from that library member.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'BARCODE_READ_GROUP_TAG', '[text]', 'Pool that a sample will be assigned to based on the barcode: this should usually be the POOL_MEMBER_NAME.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'BARCODE', '[text]', 'Barcode sequence used for each pool member. Need only be unique for each combination of barcode, primer and plate region.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'LINKER', '[text]', 'Linker sequence between the primer and the barcode (to reduce differences in hybridization based on the barcode), can be empty.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'KEY_SEQ', '[text]', 'This is a technical aspect of the 454 platform, is usually TCAG, can be obtained from the sff file using the sfftools.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'PRIMER_READ_GROUP_TAG', '[text]', 'Read group that samples will be assigned to based on the primer, e.g. V2 for the V2 primers. By default, multidimensional demultiplexing on the barcode and primer is performed.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'PRIMER', '[text]', 'Primer sequence that was used for this particular library member. If you used more than one primer for a given pool member (which is allowed) you need to duplicate the whole row with the additional primer information. This needs to be the actual sequence of the primer, not the name of the primer (i.e. not V2 or whatever).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'RUN_PREFIX', '[text]', 'The 454 instrument usually produces more than one sff file. This should be the prefix of the sff file name that was produced by a given run (usually these will have 01, 02, etc. sufixes). This allows you to designate a pool as per-library rather than per sff file (otherwise you would need to duplicate all the info per run for each sff file).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'REGION', '[text]', 'Region of the plate that was sequenced (in cases where there was a split run and the same primer/barcode means different things in different parts of the plate).');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'PLATFORM', '[text]', 'This is the sequencing platform, e.g. FLX or Titanium');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'RUN_ACCESSION', '[text]', 'Accession number for the run. Leave blank if not already assigned.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'RUN_ALIAS', '[text]', 'Alias for the run.  Presently, this should be different for every pool member, since each pool member gets a unique RUN element in the run XML.  In the future, we plan to change this behavior, and create only a single RUN element of multiple pool members share the same RUN_ALIAS. Needs to be a short identifier, alphanumeric and underscores only (no special characters)');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'RUN_CENTER', '[text]', 'Name of the institution that performed the run, assigned by NCBI. You can use the center name for your lab for this even if you had the sequencing done elsewhere according to SRA.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'RUN_DATE', '[text]', 'Date the run was performed: this can be obtained from the sff file.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'INSTRUMENT_NAME', '[text]', 'This field is if the specific machine used has a name or label (i.e. a label on that specific piece of equipment, not the type of instrument). Some sequencing centers assign names to specific instruments.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'LIBRARY_STRATEGY', '[text], example: AMPLICON', 'Sequencing technique intended for this library (optional field). This will usually be AMPLICON or METAGENOMIC.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'LIBRARY_SOURCE', '[text], example: GENOMIC', 'Type of source material that is being sequenced (optional field). This will usually be GENOMIC or METAGENOMIC.');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'LIBRARY_SELECTION', '[text], example: PCR', 'Whether any method was used to select and/or enrich the material being sequenced (optional field). This is used in cases where e.g. the cells were sorted, if PCR was used to make a specific amplicon, if fractionation for viruses was done, etc.');
commit;

-- SRA Submission Fields
/*
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'accession', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'submission_id', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'center_name', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'submission_comment', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'lab_name', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'submission_date', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'CONTACT', '[text]', 'SRA Submission Field');
insert into column_dictionary (data_type, column_name, desc_or_value, definition) values ('text', 'file', '[text]', 'SRA Submission Field');
commit;
*/

-------------------------------------------
-- Map columns to lists
-------------------------------------------

insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('env_package', 1); -- Package Type
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('investigation_type', 2); -- Investigation Type
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('STUDY_TYPE', 2); -- Investigation Type
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('urine_collect_meth', 3); -- Urine Collection Method'
--insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('nose_mouth_teeth_throat_disord', 4); -- Nose/Throad Disorders
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('study_complt_stat', 5); -- Study Completion Status
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('cur_land_use', 6); -- Current Land Use
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('wind_direction', 7); -- Cardinal Direction
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('sex', 8); -- Sex
--insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('sequencing_meth', 9); -- Sequencing Method
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('seq_quality_check', 10); -- Sequence Quality Check
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('horizon', 11); -- Horizon
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('oxy_stat_samp', 17); -- Oxygenation Status of Sample
--insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('', 18); -- Experimental Diet Types
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('special_diet', 19); -- Special Diets
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('age_unit', 20); -- Age Units
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('ihmc_medication_code', 21); -- IHMC Medication Codes
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('ihmc_ethnicity', 22); -- IHMC Ethnicities
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('occupation', 23); -- IHMC Occupations
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('dominant_hand', 24); -- Dominant Hand
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('tillage', 25); -- Tillage
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('profile_position', 26); -- Profile Position
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('drainage_class', 27); -- Drainage class
--insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('country', 28); -- INSDC Country List
insert into column_controlled_vocab (column_name, controlled_vocab_id) values ('fao_class', 29); -- Soil Types
commit;

-------------------------------------------
-- Map columns to ontologies
-------------------------------------------

insert into column_ontology(column_name, ontology_short_name) values ('body_habitat', 'FMA');
insert into column_ontology(column_name, ontology_short_name) values ('env_biome', 'ENVO');
insert into column_ontology(column_name, ontology_short_name) values ('env_feature', 'ENVO');
insert into column_ontology(column_name, ontology_short_name) values ('env_matter', 'ENVO');
insert into column_ontology(column_name, ontology_short_name) values ('source_mat_identifiers', 'OBI');
insert into column_ontology(column_name, ontology_short_name) values ('samp_mat_process', 'OBI');
insert into column_ontology(column_name, ontology_short_name) values ('body_product', 'FMA');
insert into column_ontology(column_name, ontology_short_name) values ('body_site', 'FMA');
--insert into column_ontology(column_name, ontology_short_name) values ('chem_administration', 'CHEBI');
--insert into column_ontology(column_name, ontology_short_name) values ('disease_stat', 'DO');
insert into column_ontology(column_name, ontology_short_name) values ('ploidy', 'PATO');
insert into column_ontology(column_name, ontology_short_name) values ('phenotype', 'PATO');
insert into column_ontology(column_name, ontology_short_name) values ('plant_body_site', 'PO');
insert into column_ontology(column_name, ontology_short_name) values ('experimental_factor', 'EFO');
insert into column_ontology(column_name, ontology_short_name) values ('experimental_factor', 'OBI');
commit;

-------------------------------------------
-- Map columns to package types
-------------------------------------------

-- FIELDS REQUIRED FOR SRA SUBMISSION

-- SRA Study Fields
insert into study_columns (package_type_id, column_name, required) values (-7, 'STUDY_ALIAS', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'STUDY_TITLE', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'STUDY_TYPE', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'STUDY_ABSTRACT', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'STUDY_DESCRIPTION', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'CENTER_NAME', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'CENTER_PROJECT_NAME', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'PROJECT_ID', 'M');
insert into study_columns (package_type_id, column_name, required) values (-7, 'PMID', 'M');
commit;

-- SRA Sample Fields
insert into study_columns (package_type_id, column_name, required) values (-6, 'TITLE', 'M');
insert into study_columns (package_type_id, column_name, required) values (-6, 'COMMON_NAME', 'M');
insert into study_columns (package_type_id, column_name, required) values (-6, 'ANONYMIZED_NAME', 'M');
insert into study_columns (package_type_id, column_name, required) values (-6, 'DESCRIPTION', 'M');
insert into study_columns (package_type_id, column_name, required) values (-6, 'TAXON_ID', 'M');
commit;

-- SRA Experiment Fields
insert into study_columns (package_type_id, column_name, required) values (-5, 'EXPERIMENT_ALIAS', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'EXPERIMENT_CENTER', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'EXPERIMENT_TITLE', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'EXPERIMENT_ACCESSION', 'X');
insert into study_columns (package_type_id, column_name, required) values (-5, 'STUDY_ACCESSION', 'X');
insert into study_columns (package_type_id, column_name, required) values (-5, 'STUDY_REF', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'STUDY_CENTER', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'EXPERIMENT_DESIGN_DESCRIPTION', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'LIBRARY_CONSTRUCTION_PROTOCOL', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'SAMPLE_ACCESSION', 'X');
insert into study_columns (package_type_id, column_name, required) values (-5, 'SAMPLE_CENTER', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'POOL_MEMBER_ACCESSION', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'POOL_MEMBER_NAME', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'POOL_PROPORTION', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'BARCODE_READ_GROUP_TAG', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'BARCODE', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'LINKER', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'KEY_SEQ', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'PRIMER_READ_GROUP_TAG', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'PRIMER', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'RUN_PREFIX', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'REGION', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'PLATFORM', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'RUN_ACCESSION', 'X');
insert into study_columns (package_type_id, column_name, required) values (-5, 'RUN_ALIAS', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'RUN_CENTER', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'RUN_DATE', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'INSTRUMENT_NAME', 'M');
insert into study_columns (package_type_id, column_name, required) values (-5, 'LIBRARY_STRATEGY', 'X');
insert into study_columns (package_type_id, column_name, required) values (-5, 'LIBRARY_SOURCE', 'X');
insert into study_columns (package_type_id, column_name, required) values (-5, 'LIBRARY_SELECTION', 'X');
commit;

-- SRA Submission Fields
/*
insert into study_columns (package_type_id, column_name, required) values (-4, 'accession', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'submission_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'center_name', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'submission_comment', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'lab_name', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'submission_date', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'CONTACT', 'M');
insert into study_columns (package_type_id, column_name, required) values (-4, 'file', 'M');
commit;
*/

-- STUDY

--insert into study_columns (package_type_id, column_name, required) values (-3, 'project_name', 'M');
--insert into study_columns (package_type_id, column_name, required) values (-3, 'public', 'M');
--insert into study_columns (package_type_id, column_name, required) values (-3, 'submit_to_insdc', 'M');
--insert into study_columns (package_type_id, column_name, required) values (-3, 'investigation_type', 'M');
insert into study_columns (package_type_id, column_name, required) values (-3, 'experimental_factor', 'C');
--insert into study_columns (package_type_id, column_name, required) values (-3, 'env_package', 'M');
commit;

-- SAMPLE

insert into study_columns (package_type_id, column_name, required) values (-2, 'project_name', 'H');
insert into study_columns (package_type_id, column_name, required) values (-2, 'sample_name', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'public', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'assigned_from_geo', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'collection_date', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'latitude', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'longitude', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'depth', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'altitude', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'elevation', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'country', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'env_biome', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'env_feature', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'env_matter', 'M');
insert into study_columns (package_type_id, column_name, required) values (-2, 'biological_specimen', 'X');
commit;

-- LIBRARY/PRIMER/SEQUENCE

insert into study_columns (package_type_id, column_name, required) values (-1, 'sample_name', 'H');
insert into study_columns (package_type_id, column_name, required) values (-1, 'nucl_acid_ext', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'target_subfragment', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'seq_quality_check', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'samp_collect_device', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'samp_mat_process', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'samp_size', 'M');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'nucl_acid_amp', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'lib_size', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'lib_reads_seqd', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'lib_vector', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'libr_screen', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'target_gene', 'M');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'pcr_primers', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'multiplex_ident', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'pcr_cond', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'sequencing_meth', 'M');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'chimera_check', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'sop', 'C');	
insert into study_columns (package_type_id, column_name, required) values (-1, 'url', 'C');
commit;

--AIR

insert into study_columns (package_type_id, column_name, required) values (1, 'barometric_press', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'carb_dioxide', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'carb_monoxide', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'humidity', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'methane', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'oxygen', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'pollutants', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'resp_part_matter', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'solar_irradiance', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'ventilation_rate', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'ventilation_type', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'volatile_org_comp', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'wind_direction', 'X');
insert into study_columns (package_type_id, column_name, required) values (1, 'wind_speed', 'X');
commit;

--HOST ASSOCIATED

insert into study_columns (package_type_id, column_name, required) values (2, 'host_common_name', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'host_taxid', 'M');
insert into study_columns (package_type_id, column_name, required) values (2, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (2, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'age_unit', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'life_stage', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'body_habitat', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'host_growth_cond', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'substrate', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'infra_specific_name', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'infra_specific_rank', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'dry_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'blood_press_diast', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'blood_press_syst', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'host_color', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'host_shape', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'gravidity', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (2, 'misc_param', 'X');
commit;

--HUMAN ASSOCIATED

insert into study_columns (package_type_id, column_name, required) values (3, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (3, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'smoker', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'hiv_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'drug_usage', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'diet_last_six_month', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'weight_loss_3_month', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'pet_farm_animal', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'travel_out_six_month', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'twin_sibling', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'study_complt_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'pulmonary_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'nose_throat_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'blood_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'gestation_state', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'maternal_health_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'foetal_health_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'amniotic_fluid_color', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'kidney_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'urogenit_tract_disor', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'urine_collect_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (3, 'misc_param', 'X');
commit;

--HUMAN GUT

insert into study_columns (package_type_id, column_name, required) values (6, 'gastrointest_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'liver_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'special_diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (6, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (6, 'misc_param', 'X');
commit;

--HUMAN-ORAL

insert into study_columns (package_type_id, column_name, required) values (5, 'nose_mouth_teeth_throat_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'time_last_toothbrush', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (5, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (5, 'misc_param', 'X');
commit;

--HUMAN-SKIN

insert into study_columns (package_type_id, column_name, required) values (4, 'dermatology_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'time_since_last_wash', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'dominant_hand', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (4, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (4, 'misc_param', 'X');
commit;

--HUMAN-VAGINAL

insert into study_columns (package_type_id, column_name, required) values (7, 'menarche', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'sexual_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'pregnancy', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'douche', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'birth_control', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'menopause', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'hrt', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'hysterectomy', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'gynecologic_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'urogenit_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (7, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (7, 'misc_param', 'X');
commit;

-- HUMAN AMNIOTIC FLUID

insert into study_columns (package_type_id, column_name, required) values (8, 'amniotic_fluid_color', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'gestation_state', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'foetal_health_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'maternal_health_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (8, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (8, 'misc_param', 'X');
commit;

-- HUMAN URINE

insert into study_columns (package_type_id, column_name, required) values (9, 'kidney_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'urine_collect_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'urogenit_tract_disor', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (9, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (9, 'misc_param', 'X');
commit;

-- HUMAN BLOOD

insert into study_columns (package_type_id, column_name, required) values (10, 'blood_disord', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'host_subject_id', 'M');
insert into study_columns (package_type_id, column_name, required) values (10, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'sex', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'ihmc_medication_code', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'diet', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'last_meal', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'family_relationship', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'host_body_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'body-mass_index', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'ihmc_ethnicity', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'occupation', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'medic_hist_perform', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'pulse', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (10, 'misc_param', 'X');
commit;

--MICROBIAL MAT/BIOFILM

insert into study_columns (package_type_id, column_name, required) values (11, 'alkalinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'alkyl_diethers', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'aminopept_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'ammonium', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'bacteria_carb_prod', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'biomass', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'bishomohopanol', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'bromide', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'calcium', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'carb_nitro_ratio', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'chloride', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'chlorophyll', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'diether_lipids', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'diss_carb_dioxide', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'diss_hydrogen', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'diss_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'diss_oxygen', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'glucosidase_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'magnesium', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'mean_frict_vel', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'mean_peak_frict_vel', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'methane', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'n_alkanes', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'nitrate', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'nitrite', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'org_matter', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'org_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'ph', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'part_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'petroleum_hydrocarb', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'phaeopigments', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'phosphate', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'phosplipid_fatt_acid', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'potassium', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'press', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'redox_potential', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'silicate', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'sulfate', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'sulfide', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'tot_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'tot_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'tot_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'turbidity', 'X');
insert into study_columns (package_type_id, column_name, required) values (11, 'water_content', 'X');
commit;

--MISCELLANEOUS NATURAL OR ARTIFICIAL ENVIRONNMENT

insert into study_columns (package_type_id, column_name, required) values (12, 'alkalinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'ammonium', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'biomass', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'bromide', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'calcium', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'chloride', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'chlorophyll', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'current', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'density', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'diether_lipids', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'diss_carb_dioxide', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'diss_hydrogen', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'diss_oxygen', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'nitrate', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'nitrite', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'org_matter', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'org_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'ph', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'phosphate', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'phosplipid_fatt_acid', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'potassium', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'press', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'silicate', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'sulfate', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'sulfide', 'X');
insert into study_columns (package_type_id, column_name, required) values (12, 'temp', 'X');
commit;

--PLANT-ASSOCIATED

insert into study_columns (package_type_id, column_name, required) values (13, 'age', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'air_temp_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'antibiotic_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'body_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'chem_mutagen', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'climate_environment', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'disease_stat', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'dry_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'fertilizer_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'fungicide_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'gaseous_environment', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'genotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'gravity', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'growth_hormone_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'growth_med', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'height_or_length', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'herbicide_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'host_common_name', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'host_taxid', 'M');
insert into study_columns (package_type_id, column_name, required) values (13, 'humidity_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'infra_specific_name', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'infra_specific_rank', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'life_stage', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'mechanical_damage', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'mineral_nutr_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'non_mineral_nutr_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'ph_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'pesticide_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'phenotype', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'plant_body_site', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'plant_product', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'radiation_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'rainfall_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'salt_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'season_environment', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'standing_water_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'tiss_cult_growth_med', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'tot_mass', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'water_temp_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'watering_regm', 'X');
insert into study_columns (package_type_id, column_name, required) values (13, 'wet_mass', 'X');
commit;

--SEDIMENT

insert into study_columns (package_type_id, column_name, required) values (14, 'alkalinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'alkyl_diethers', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'aminopept_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'ammonium', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'bacteria_carb_prod', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'biomass', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'bishomohopanol', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'bromide', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'calcium', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'carb_nitro_ratio', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'chloride', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'chlorophyll', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'density', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'diether_lipids', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'diss_carb_dioxide', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'diss_hydrogen', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'diss_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'diss_oxygen', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'glucosidase_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'magnesium', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'mean_frict_vel', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'mean_peak_frict_vel', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'methane', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'n_alkanes', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'nitrate', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'nitrite', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'org_matter', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'org_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'ph', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'particle_class', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'part_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'petroleum_hydrocarb', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'phaeopigments', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'phosphate', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'phosplipid_fatt_acid', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'porosity', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'potassium', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'press', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'redox_potential', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'sediment_type', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'silicate', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'sulfate', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'sulfide', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'tot_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'tot_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'tot_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'turbidity', 'X');
insert into study_columns (package_type_id, column_name, required) values (14, 'water_content', 'X');
commit;

--SOIL

insert into study_columns (package_type_id, column_name, required) values (15, 'cur_land_use', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'cur_vegetation', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'cur_vegetation_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'previous_land_use', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'previous_land_use_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'crop_rotation', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'agrochem_addition', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'tillage', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'fire', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'flooding', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'extreme_event', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'other', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'horizon_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'sieving', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'water_content_soil', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'water_content_soil_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'samp_weight_dna_ext', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'pool_dna_extracts', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'store_cond', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'link_climate_info', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'annual_season_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'annual_season_precpt', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'link_class_info', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'fao_class', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'local_class', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'local_class_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'soil_type', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'soil_type_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'slope_gradient', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'slope_aspect', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'profile_position', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'drainage_class', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'texture', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'texture_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'ph', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'ph_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'tot_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'tot_org_c_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'tot_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'tot_n_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'microbial_biomass', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'microbial_biomass_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'link_addit_analys', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'extreme_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'salinity_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'heavy_metals', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'heavy_metals_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'al_sat', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'al_sat_meth', 'X');
insert into study_columns (package_type_id, column_name, required) values (15, 'misc_param', 'X');
commit;

--WASTEWATER/SLUDGE

insert into study_columns (package_type_id, column_name, required) values (16, 'alkalinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'biochem_oxygen_dem', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'chem_oxygen_dem', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'efficiency_percent', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'emulsions', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'gaseous_substances', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'indust_eff_percent', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'inorg_particles', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'nitrate', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'org_particles', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'ph', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'phosphate', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'pre_treatment', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'primary_treatment', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'reactor_type', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'samp_salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'secondary_treatment', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'sewage_type', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'sludge_retent_time', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'soluble_inorg_mat', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'soluble_org_mat', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'suspend_solids', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'tertiary_treatment', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'tot_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'tot_phosphate', 'X');
insert into study_columns (package_type_id, column_name, required) values (16, 'wastewater_type', 'X');
commit;

--WATER

insert into study_columns (package_type_id, column_name, required) values (17, 'alkalinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'alkyl_diethers', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'aminopept_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'ammonium', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'atmospheric_data', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'bacteria_carb_prod', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'biomass', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'bishomohopanol', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'bromide', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'calcium', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'carb_nitro_ratio', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'chem_administration', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'chloride', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'chlorophyll', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'current', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'density', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diether_lipids', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diss_carb_dioxide', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diss_hydrogen', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diss_inorg_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diss_inorg_phosp', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diss_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'diss_oxygen', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'glucosidase_act', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'light_intensity', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'magnesium', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'mean_frict_vel', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'mean_peak_frict_vel', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'misc_param', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'n_alkanes', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'nitrate', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'nitrite', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'org_matter', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'org_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'organism_count', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'oxy_stat_samp', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'ph', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'part_org_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'part_org_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'perturbation', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'petroleum_hydrocarb', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'phaeopigments', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'phosphate', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'phosplipid_fatt_acid', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'photon_flux', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'potassium', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'press', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'primary_prod', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'redox_potential', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'salinity', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'samp_store_dur', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'samp_store_loc', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'samp_store_temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'silicate', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'soluble_react_phosp', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'sulfate', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'sulfide', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'suspend_part_matter', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'temp', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'tot_depth_water_col', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'tot_inorg_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'tot_nitro', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'tot_part_carb', 'X');
insert into study_columns (package_type_id, column_name, required) values (17, 'tot_phosp', 'X');
commit;

