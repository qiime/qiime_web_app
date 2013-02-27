/*
NOTE: The insert statements in this script work ONLY in the case
where there is one barcode per kit. 


drop table ag_kit_barcodes;
drop table ag_kit;
drop table ag_login;

select * from ag_login;
select * from ag_kit;
select * from ag_kit_barcodes;

*/

create table ag_login
(
    ag_login_id raw(16) default sys_guid() primary key,
    barcode varchar2(50),
    swabs_per_kit integer,
    email varchar2(100),
    name varchar2(200),
    address varchar2(500),
    city varchar2(100),
    state varchar2(100),
    zip varchar2(10),
    country varchar2(100),
    sample_barcode_file varchar2(500),
    sample_barcode_file_md5 varchar2(50),
    kit_id varchar2(50) not null,
    kit_password varchar2(50) not null,
    kit_verification_code varchar2(50)
);

create table ag_kit
(
    ag_kit_id raw(16) default sys_guid() primary key,
    ag_login_id raw(16) not null,
    kit_password varchar2(50) not null,
    swabs_per_kit int not null,
    kit_verification_code varchar2(50),
    
    constraint fk_ag_kit_to_login_id
        foreign key (ag_login_id)
        references ag_login (ag_login_id)
);

insert  into ag_kit
        (ag_login_id, kit_password, swabs_per_kit, kit_verification_code)
select  ag_login_id, kit_password, swabs_per_kit, kit_verification_code
from    ag_login;

create table ag_kit_barcodes
(
    ag_kit_id raw(16) default sys_guid() primary key,
    barcode varchar2(50) not null,
    sample_barcode_file varchar2(500),
    sample_barcode_file_md5 varchar2(50),
    
    constraint fk_ag_kit_bc_to_kit_id
        foreign key (ag_kit_id)
        references ag_kit (ag_kit_id)
);


insert  into ag_kit_barcodes
        (ag_kit_id, barcode, sample_barcode_file, sample_barcode_file_md5)
select  ag_kit_id, barcode, sample_barcode_file, sample_barcode_file_md5
from    ag_login al
        inner join ag_kit ak
        on al.ag_login_id = ak.ag_login_id;




