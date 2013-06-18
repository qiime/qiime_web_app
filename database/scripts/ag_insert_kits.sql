-------------------------------------------
-- GLOBAL TEMP TABLE
-------------------------------------------

/*

create global temporary table ag_import_stats_tmp 
(
  tmp_login_count number,
  tmp_kit_count number,
  tmp_barcode_count number,
  before_login_count number,
  before_kit_count number,
  before_barcode_count number,
  after_login_count number,
  after_kit_count number,
  after_barcode_count number,
  login_diff number,
  kit_diff number,
  barcode_diff number
)
on commit delete rows;

drop table ag_import_stats_tmp;

*/

-------------------------------------------
-- LOADING
-------------------------------------------

-- Drop the table first
/*
drop table tmp_kits;
select * from tmp_kits;
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

update  tmp_kits
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
        zip = case
            -- US zip codes with decimal values
            when length(zip) = 7 and instr(zip, '.') > 0 and lower(country) in ('us', 'united states') then substr(zip, 0, instr(zip, '.') - 1)
            when length(zip) = 6 and instr(zip, '.') > 0 and lower(country) in ('us', 'united states') then '0' || substr(zip, 0, instr(zip, '.') - 1)
            when length(zip) = 5 and instr(zip, '.') > 0 and lower(country) in ('us', 'united states') then '00' || substr(zip, 0, instr(zip, '.') - 1)
            when length(zip) = 4 and instr(zip, '.') > 0 and lower(country) in ('us', 'united states') then '000' || substr(zip, 0, instr(zip, '.') - 1)
            when length(zip) = 3 and instr(zip, '.') > 0 and lower(country) in ('us', 'united states') then '0000' || substr(zip, 0, instr(zip, '.') - 1)
            -- US zip codes without decimal places
            when length(zip) = 4 and lower(country) in ('us', 'united states') then '0' || zip
            when length(zip) = 3 and lower(country) in ('us', 'united states') then '00' || zip
            when length(zip) = 2 and lower(country) in ('us', 'united states') then '000' || zip
            when length(zip) = 1 and lower(country) in ('us', 'united states') then '0000' || zip
            -- Non US zip codes with decimal places
            when instr(zip, '.') > 0 then substr(zip, 0, instr(zip, '.') - 1)
            -- Everyting else
            else zip
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
        end,
        state = case
            when state = '-' then ''
            else state
        end;

commit;

/*
select * from tmp_kits;
select * from tmp_kits order by barcode;
select barcode from ag_kit_barcodes order by barcode desc;
*/

-------------------------------------------
-- INITIAL STATS
-------------------------------------------

insert  into ag_import_stats_tmp
        (tmp_login_count, tmp_kit_count, tmp_barcode_count, 
        before_login_count, before_kit_count, before_barcode_count)
select  (select count(distinct email) from tmp_kits),
        (select count(distinct kit_id) from tmp_kits),
        (select count(distinct barcode) from tmp_kits),
        (select count(*) from ag_login),
        (select count(*) from ag_kit),
        (select count(*) from ag_kit_barcodes)
from    dual;

/*
select * from ag_import_stats_tmp;
*/

-------------------------------------------
-- LOADING
-------------------------------------------

declare
    ag_login_id_ raw(16);
    ag_kit_id_ raw(16);
begin
    DBMS_OUTPUT.ENABLE;
    for r in (select * from tmp_kits) loop
        --dbms_output.put_line(r.email);
        
        merge into ag_login
        using dual
        on (dual.dummy is not null and lower(ag_login.email) = lower(r.email))
        when not matched then 
            insert (email, name, address, city, state, zip, country) 
            values (r.email, r.name, r.address, r.city, r.state, r.zip, r.country);

        select  ag_login_id into ag_login_id_ 
        from    ag_login
        where   email = r.email;
        
        --dbms_output.put_line(ag_login_id_);
        
        merge into ag_kit
        using dual
        on (dual.dummy is not null and supplied_kit_id = r.kit_id)
        when not matched then
            insert (ag_login_id, supplied_kit_id, kit_password, swabs_per_kit, kit_verification_code)
            values(ag_login_id_, r.kit_id, r.kit_password, r.swabs_per_kit, r.kit_verification_code);
        
        select  ag_kit_id into ag_kit_id_
        from    ag_kit
        where   supplied_kit_id = r.kit_id;
        
        merge into ag_kit_barcodes
        using dual
        on (dual.dummy is not null and barcode = r.barcode)
        when not matched then
            insert (ag_kit_id, barcode, sample_barcode_file, sample_barcode_file_md5)
            values (ag_kit_id_, r.barcode, r.barcode || '.jpg', '');
        
        --dbms_output.put_line(ag_kit_id_);
        
    end loop;
end;

-------------------------------------------
-- UPDATE MASTER BARCODE TABLES
-------------------------------------------

insert  into barcode
        (barcode)
select  barcode
from    tmp_kits;

insert  into project_barcode
        (project_id, barcode)
select  1, barcode
from    tmp_kits;

-------------------------------------------
-- POST-LOADING STATS
-------------------------------------------

update  ag_import_stats_tmp
set     after_login_count = (select count(*) from ag_login),
        after_kit_count = (select count(*) from ag_kit),
        after_barcode_count = (select count(*) from ag_kit_barcodes),
        login_diff = (select count(*) from ag_login) - before_login_count,
        kit_diff = (select count(*) from ag_kit) - before_kit_count,
        barcode_diff = (select count(*) from ag_kit_barcodes) - before_barcode_count;

select  case
            when login_diff = tmp_login_count then 'Login load looks GOOD'
            when login_diff > tmp_login_count then 'Login load FAILED'
            when login_diff < tmp_login_count then 'Fewer logins inserted. May be OK but check.'
        end as login_load_status,
        case
            when kit_diff = tmp_kit_count then 'Kit load looks GOOD'
            else 'Kit load FAILED'
        end as kit_load_status,
        case
            when barcode_diff = tmp_barcode_count then 'Barcode load looks GOOD'
            else 'Barcode load FAILED'
        end as barcode_load_status
from    ag_import_stats_tmp;

commit;

-------------------------------------------
-- SANITY CHECKS
-------------------------------------------

/*

select * from ag_login where cannot_geocode is not null;
update ag_login set cannot_geocode = '' where cannot_geocode is not null;
commit;

select  barcode
from    tmp_kits
where   barcode in
        (
            select  barcode
            from    barcode
        );

select * from tmp_kits;

select * from ag_import_stats_tmp;

select count(distinct email) from tmp_kits;
select count(distinct kit_id) from tmp_kits;
select count(distinct barcode) from tmp_kits;

select count(*) from ag_login;
select count(*) from ag_kit;
select count(*) from ag_kit_barcodes;

select * from ag_login;
select * from ag_kit;
select * from ag_kit_barcodes;
select * from tmp_kits;

*/