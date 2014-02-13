
select * from ag_kit_barcodes;


alter table ag_kit_barcodes add (results_ready varchar(1));
alter table ag_kit_barcodes add (withdrawn varchar(1));
alter table ag_kit_barcodes add (refunded varchar(1));

alter table barcode add (biomass_remaining varchar(1));
alter table barcode add (sequencing_status varchar(20));
alter table barcode add (extracted varchar(1));
alter table barcode add (obsolete varchar(1));


select * from barcode where SAMPLE_POSTMARK_DATE is not null;
 CREATE TABLE "QIIME_METADATA"."PLATE" 
   (	"PLATE_ID" NUMBER(*,0) NOT NULL ENABLE, 
	"PLATE" VARCHAR2(50 BYTE), 
	 CONSTRAINT "PK_PLATE" PRIMARY KEY ("PLATE_ID") ENABLE
   ) ORGANIZATION INDEX NOCOMPRESS PCTFREE 10 INITRANS 2 MAXTRANS 255 LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "QIIME_METADATA" 
 PCTTHRESHOLD 50;
 
  CREATE TABLE "QIIME_METADATA"."PLATE_BARCODE" 
   (	"PLATE_ID" NUMBER(*,0) NOT NULL ENABLE, 
	"BARCODE" CHAR(9 BYTE) NOT NULL ENABLE,  
	 CONSTRAINT "FK_PlateB_TO_PLATE" FOREIGN KEY ("PLATE_ID")
	  REFERENCES "QIIME_METADATA"."PLATE" ("PLATE_ID") ENABLE, 
	 CONSTRAINT "FK_PlateB_TO_BARCODE" FOREIGN KEY ("BARCODE")
	  REFERENCES "QIIME_METADATA"."BARCODE" ("BARCODE") ENABLE
   );

update plate set sequence_date = '05/20/2013' where plate_id in (1,2,3,4,5,6);
update plate set sequence_date = '07/18/2013' where plate_id in (7,8,9,10,15);
update plate set sequence_date = '08/12/2013' where plate_id in (11,12,13,14);
update plate set sequence_date = '09/25/2013' where plate_id in (16,18,24,19,20);
update plate set sequence_date = '10/22/2013' where plate_id in (17,21,22,23,25,26,27);
update plate set sequence_date = '12/18/2013' where plate_id in (28,33);


update barcode set sequencing_status = 'WAITING' where  barcode in (select pb.barcode from plate_barcode pb inner join plate p on pb.plate_id = p.plate_id where p.sequence_date is null);



--update barcode set obsolete = 'Y' where barcode = '000014062';
--update barcode set obsolete = 'Y' where barcode = '000014057';
update barcode set obsolete = 'Y' where barcode = '000004608';
update barcode set obsolete = 'Y' where barcode = '000007153';
update barcode set obsolete = 'Y' where barcode = '000009731';
--update barcode set obsolete = 'Y' where barcode = '000014059';
update barcode set obsolete = 'Y' where barcode = '000004607';
update barcode set obsolete = 'Y' where barcode = '000012412';
update barcode set obsolete = 'Y' where barcode = '000013641';
update barcode set obsolete = 'Y' where barcode = '000006836';
--update barcode set obsolete = 'Y' where barcode = '000014061';
--update barcode set obsolete = 'Y' where barcode = '000014060';
--update barcode set obsolete = 'Y' where barcode = '000014056';
--update barcode set obsolete = 'Y' where barcode = '000014058';

update AG_KIT_BARCODES set refunded = 'Y' where barcode = '000013641';





commit;