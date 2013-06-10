-- Insert the CU ICU Microbiome barcodes

-- Step 1: Import the barcode list into a new table "cuicu"
-- drop table cuicu;

update  cuicu
set     barcode = '00000' || barcode;
commit;

insert  into barcode
        (barcode)
select  barcode
from    cuicu;

insert  into project_barcode
        (project_id, barcode)
select  2, barcode
from    cuicu;

commit;

/*

select * from cuicu;
select * from barcode;
select * from project_barcode where project_id = 2;

*/