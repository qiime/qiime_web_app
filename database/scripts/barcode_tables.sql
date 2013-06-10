/*

drop table project_barcode;
drop table project;
drop table barcode;

*/

create table barcode
(
    barcode char(9) not null,
    create_date_time date default (sysdate),
    constraint pk_barcode primary key (barcode)
) organization index;

create table project
(
    project_id int not null,
    project varchar2(1000),
    
    constraint pk_project primary key (project_id)
) organization index;

insert  into project (project_id, project)
values   (1, 'American Gut Project');

insert  into project (project_id, project)
values   (2, 'ICU Microbiome');

insert  into project (project_id, project)
values   (3, 'Handout Kits');

commit;

create table project_barcode
(
    project_id int not null,
    barcode char(9) not null,
    
    constraint pk_project_barcode primary key (project_id, barcode),
    constraint fk_pb_to_project
        foreign key (project_id) 
        references project (project_id),
    constraint fk_pb_to_barcode
        foreign key (barcode) 
        references barcode (barcode)
) organization index;

-- Add all of the american gut barcodes to the barcodes table

insert  into barcode
        (barcode)
select  barcode
from    ag_kit_barcodes
where   length(barcode) = 9;

insert  into project_barcode
        (project_id, barcode)
select  1, barcode
from    ag_kit_barcodes
where   length(barcode) = 9;

insert  into barcode
        (barcode)
select  ahk.barcode
from    ag_handout_kits ahk
        left join ag_kit_barcodes akb
        on ahk.barcode = akb.barcode
where   akb.barcode is null;

insert  into project_barcode
        (project_id, barcode)
select  3, ahk.barcode
from    ag_handout_kits ahk
        left join ag_kit_barcodes akb
        on ahk.barcode = akb.barcode
where   akb.barcode is null;

commit;

/*

select * from barcode order by barcode;
select * from project_barcode order by barcode;

*/

