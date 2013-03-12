alter table ag_kit_barcodes add site_sampled varchar2(200);
alter table ag_kit_barcodes add sample_date varchar2(20);
alter table ag_kit_barcodes add hour integer;
alter table ag_kit_barcodes add minute integer;
alter table ag_kit_barcodes add meridian varchar(5);