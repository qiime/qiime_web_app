/*

drop table torque_job;
drop table torque_job_state;
drop table torque_job_type;
drop table gg_taxonomy;
drop table gg_tax_source;
drop table gg;
drop table seq;
drop table seq_source;

*/

------------------------------------------
-- TORQUE TABLES
------------------------------------------

CREATE TABLE "TORQUE_JOB_STATE" 
(	"JOB_STATE_ID" NUMBER(2,0), 
"JOB_STATE_NAME" VARCHAR2(500 BYTE)
);

CREATE TABLE "TORQUE_JOB_TYPE" 
(	"JOB_TYPE_ID" NUMBER(2,0), 
"JOB_TYPE_NAME" VARCHAR2(500 CHAR)
);

REM INSERTING into TORQUE_JOB_STATE
SET DEFINE OFF;
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (4,'COMPLETED_ERROR');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (3,'COMPLETED_OKAY');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (5,'COMPLETING');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (7,'ERROR_STARTING');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (6,'EXITING');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (2,'HALTED');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (-1,'NEW');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (-2,'QIIME_HOLD');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (0,'QUEUED');
Insert into TORQUE_JOB_STATE (JOB_STATE_ID,JOB_STATE_NAME) values (1,'RUNNING');
REM INSERTING into TORQUE_JOB_TYPE
SET DEFINE OFF;
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (14,'ExportToEBISRAHandler');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (6,'ExportToMGRASTHandler');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (12,'LoadAnalysisOTUTableHandler');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (15,'LoadSplitLibSeqsHandler');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (2,'PollerTestHandlerErr');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (1,'PollerTestHandlerOkay');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (3,'ProcessSFFHandler');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (17,'ToggleStudyStatusHandler');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (10,'alphaRarefaction');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (8,'betaDiversityThroughPlots');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (7,'generateMapOTUTableSubmitJobs');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (13,'generateMapSubmitJobs');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (4,'makeMappingAndOTUFiles');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (5,'makeMappingFileandPCoAPlots');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (9,'makeOTUHeatmap');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (0,'poller_test_1');
Insert into TORQUE_JOB_TYPE (JOB_TYPE_ID,JOB_TYPE_NAME) values (11,'summarizeTaxa');

CREATE UNIQUE INDEX "UNI_JOB_STATE_NAME" ON "TORQUE_JOB_STATE" ("JOB_STATE_NAME");
CREATE UNIQUE INDEX "TORQUE_STATE_TYPE_PK" ON "TORQUE_JOB_STATE" ("JOB_STATE_ID");
CREATE UNIQUE INDEX "UNI_JOB_TYPE_NAME" ON "TORQUE_JOB_TYPE" ("JOB_TYPE_NAME");
CREATE UNIQUE INDEX "TORQUE_JOB_TYPE_PK" ON "TORQUE_JOB_TYPE" ("JOB_TYPE_ID");

ALTER TABLE "TORQUE_JOB_STATE" ADD CONSTRAINT "PK_TORQUE_STATE_TYPE" PRIMARY KEY ("JOB_STATE_ID") ENABLE;
ALTER TABLE "TORQUE_JOB_STATE" MODIFY ("JOB_STATE_NAME" NOT NULL ENABLE);
ALTER TABLE "TORQUE_JOB_STATE" ADD CONSTRAINT "UNI_JOB_STATE_NAME" UNIQUE ("JOB_STATE_NAME") ENABLE;
ALTER TABLE "TORQUE_JOB_TYPE" MODIFY ("JOB_TYPE_NAME" NOT NULL ENABLE);
ALTER TABLE "TORQUE_JOB_TYPE" ADD CONSTRAINT "TORQUE_JOB_TYPE_PK" PRIMARY KEY ("JOB_TYPE_ID") ENABLE;
ALTER TABLE "TORQUE_JOB_TYPE" ADD CONSTRAINT "UNI_JOB_TYPE_NAME" UNIQUE ("JOB_TYPE_NAME") ENABLE;

CREATE TABLE "TORQUE_JOB" 
(	"JOB_ID" NUMBER(10,0), 
"JOB_TYPE_ID" NUMBER(2,0), 
"JOB_ARGUMENTS" VARCHAR2(2000 BYTE), 
"USER_ID" NUMBER(10,0), 
"JOB_STATE_ID" NUMBER(2,0) DEFAULT -1, 
"JOB_NOTES" VARCHAR2(4000 CHAR) DEFAULT '', 
"STUDY_ID" NUMBER(*,0)
);

CREATE UNIQUE INDEX "TORQUE_JOB_PK" ON "TORQUE_JOB" ("JOB_ID");
CREATE INDEX "IDX_TJ_JOB_TYPE_ID" ON "TORQUE_JOB" ("JOB_TYPE_ID");
CREATE INDEX "IDX_TJ_USER_ID" ON "TORQUE_JOB" ("USER_ID");
CREATE INDEX "IDX_TJ_JOB_STATE_ID" ON "TORQUE_JOB" ("JOB_STATE_ID");

ALTER TABLE "TORQUE_JOB" MODIFY ("JOB_TYPE_ID" NOT NULL ENABLE); 
ALTER TABLE "TORQUE_JOB" MODIFY ("JOB_STATE_ID" NOT NULL ENABLE);
ALTER TABLE "TORQUE_JOB" ADD CONSTRAINT "TORQUE_JOB_PK" PRIMARY KEY ("JOB_ID") ENABLE;

ALTER TABLE "TORQUE_JOB" ADD FOREIGN KEY ("JOB_STATE_ID")
  REFERENCES "TORQUE_JOB_STATE" ("JOB_STATE_ID") ENABLE;

ALTER TABLE "TORQUE_JOB" ADD CONSTRAINT "TORQUE_JOB_TYPE_FK" FOREIGN KEY ("JOB_TYPE_ID")
  REFERENCES "TORQUE_JOB_TYPE" ("JOB_TYPE_ID") ENABLE;

------------------------------------------
-- REFERENCE TABLES
------------------------------------------

create table seq_source
(
    seq_source_id int not null,
    sequence_source varchar2(500) not null,
    description varchar2(2000) not null,
    
    constraint pk_seq_source primary key (seq_source_id)
) organization index;

insert into seq_source (seq_source_id, sequence_source, description)
values (1, 'gg_5_13:97', 'Greengenes May, 2013 at 97%');

create table seq
(
    seq_id int,
    seq_source_id int not null,
    sequence_string varchar2(4000),
    sequence_md5 char(32 char),
    
    constraint pk_seq 
        primary key (seq_id),
    constraint fk_seq_seq_source_id
        foreign key (seq_source_id)
        references seq_source (seq_source_id)
);

create index ix_seq_seq_source_id on seq (seq_source_id);

create table gg
(
    gg_id int not null,
    seq_id int not null,
    
    constraint pk_gg 
        primary key (gg_id),
    constraint fk_gg_seq_id
        foreign key (seq_id)
        references seq (seq_id)
) organization index;

create index ix_gg_seq_id on gg (seq_id);

create table gg_tax_source
(
    gg_tax_source_id int not null,
    tax_source varchar2(200) not null,
    
    constraint pk_gg_tax_source 
        primary key (gg_tax_source_id)
) organization index;

insert into gg_tax_source (gg_tax_source_id, tax_source)
values (1, 'gg_taxonomy');

create table gg_taxonomy
(
    gg_id int not null,
    gg_tax_source_id int not null,
    taxonomy_string varchar2(1000) not null,
    
    constraint pk_gg_taxonomy 
        primary key (gg_id, gg_tax_source_id),
    constraint fk_gg_taxonomy_tax_source_id
        foreign key (gg_tax_source_id)
        references gg_tax_source (gg_tax_source_id)
) organization index;

------------------------------------------
-- 
------------------------------------------



------------------------------------------
-- 
------------------------------------------

