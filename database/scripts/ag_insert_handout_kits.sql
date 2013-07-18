
-------------------------------------------
-- LOADING
-------------------------------------------

-- Drop the table first
/*
drop table tmp_handout_kits;
select * from tmp_handout_kits;
*/

/*

Import spreadsheet as 'tmp_kits" from SQL Developer GUI

Helpful hints:
* Make sure to select entire spreadsheet and format all cells as "text"
* Make sure there is no password on spreadsheet. If necessary, remove it and save before importing.
* When importing, make sure to change the barcode varchar2 field length to 9

*/

-------------------------------------------
-- CLEANUP
-------------------------------------------

update  tmp_handout_kits
set     barcode = case
            -- Decimal barcode values
            when length(barcode) = 11 and instr(barcode, '.') > 0 then substr(barcode, 0, instr(barcode, '.') - 1)
            when length(barcode) = 10 and instr(barcode, '.') > 0 then '0' || substr(barcode, 0, instr(barcode, '.') - 1)
            when length(barcode) = 9 and instr(barcode, '.') > 0 then '00' || substr(barcode, 0, instr(barcode, '.') - 1)
            when length(barcode) = 8 and instr(barcode, '.') > 0 then '000' || substr(barcode, 0, instr(barcode, '.') - 1)
            when length(barcode) = 7 and instr(barcode, '.') > 0 then '0000' || substr(barcode, 0, instr(barcode, '.') - 1)
            when length(barcode) = 6 and instr(barcode, '.') > 0 then '00000' || substr(barcode, 0, instr(barcode, '.') - 1)
            -- Non-decimal barcode values
            when length(barcode) = 8 then '0' || barcode
            when length(barcode) = 7 then '00' || barcode
            when length(barcode) = 6 then '000' || barcode
            when length(barcode) = 5 then '0000' || barcode
            when length(barcode) = 4 then '00000' || barcode
            -- Everyting else
            else barcode
        end,
        kit_password = case
            when length(kit_password) = 7 then '0' || kit_password
            when length(kit_password) = 6 then '00' || kit_password
            when length(kit_password) = 5 then '000' || kit_password
            when length(kit_password) = 4 then '0000' || kit_password
            when length(kit_password) = 3 then '00000' || kit_password
            when length(kit_password) = 2 then '000000' || kit_password
            when length(kit_password) = 1 then '0000000' || kit_password
            else kit_password
        end,
        kit_verification_code = case
            when length(kit_verification_code) = 4 then '0' || kit_verification_code
            when length(kit_verification_code) = 3 then '00' || kit_verification_code
            when length(kit_verification_code) = 2 then '000' || kit_verification_code
            when length(kit_verification_code) = 1 then '0000' || kit_verification_code
            else kit_verification_code
        end;
        
commit;

/*
select * from tmp_handout_kits order by barcode;
*/

-------------------------------------------
-- LOADING
-------------------------------------------

insert  into ag_handout_kits
        (kit_id, password, barcode, swabs_per_kit, 
        verification_code, sample_barcode_file)
select  kit_id, kit_password, barcode, swabs_per_kit, 
        kit_verification_code, barcode || '.jpg'
from    tmp_handout_kits;

commit;

/*
select * from ag_handout_kits order by barcode desc;
*/

-------------------------------------------
-- UPDATE MASTER BARCODE TABLES
-------------------------------------------

/*
If this is a new project type, insert the new type here
select * from project;
*/

insert  into project
        (project_id, project)
values  (4, 'Office Succession Sample');

insert  into barcode
        (barcode)
select  barcode
from    tmp_handout_kits;

-- Make sure to insert the correct project type here:
select * from project;

insert  into project_barcode
        (project_id, barcode)
select  6, barcode
from    tmp_handout_kits;

commit;

/*

select * from barcode order by barcode desc;

select * from tmp_handout_kits order by barcode desc;
select * from ag_handout_kits order by barcode desc;

*/


