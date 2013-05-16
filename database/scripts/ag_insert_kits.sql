/*


IMPORT SPREADSHEET AS 'tmp_kits"
PAD BARCODES WITH 5 ZEROS

drop table tmp_kits;

select * from ag_kit where supplied_kit_id = 'Ezhod';
select * from ag_kit_barcodes where ag_kit_id = 'D9F2A0F20C7AAF51E0408A800C5D0A21';

*/

select * from tmp_kits;

-- remove decimal point
select  '00000' || substr(barcode, 0, instr(barcode, '.') - 1) as barcode
from    tmp_kits;

update  tmp_kits
set     barcode = '00000' || substr(barcode, 0, instr(barcode, '.') - 1);
commit;

-- CLEANUP OF NUMERIC VALUES for US ONLY zip codes
update  tmp_kits
set     zip = '0' || zip
where   length(zip) = 4;

update  tmp_kits
set     zip = '00' || zip
where   length(zip) = 3;

update  tmp_kits
set     zip = '000' || zip
where   length(zip) = 2;

update  tmp_kits
set     zip = '0000' || zip
where   length(zip) = 1;

update  tmp_kits
set     kit_password = '0' || kit_password
where   length(kit_password) = 7;

update  tmp_kits
set     kit_password = '00' || kit_password
where   length(kit_password) = 6;

update  tmp_kits
set     kit_password = '000' || kit_password
where   length(kit_password) = 5;

update  tmp_kits
set     kit_password = '0000' || kit_password
where   length(kit_password) = 4;

update  tmp_kits
set     kit_password = '00000' || kit_password
where   length(kit_password) = 3;

update  tmp_kits
set     kit_password = '000000' || kit_password
where   length(kit_password) = 2;

update  tmp_kits
set     kit_password = '0000000' || kit_password
where   length(kit_password) = 1;

update  tmp_kits
set     kit_verification_code = '0' || kit_verification_code
where   length(kit_verification_code) = 4;

update  tmp_kits
set     kit_verification_code = '00' || kit_verification_code
where   length(kit_verification_code) = 3;

update  tmp_kits
set     kit_verification_code = '000' || kit_verification_code
where   length(kit_verification_code) = 2;

update  tmp_kits
set     kit_verification_code = '0000' || kit_verification_code
where   length(kit_verification_code) = 1;

commit;

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

-- spot checks
select * from ag_login where email = 'mark@brightmedicineclinic.com';
select * from ag_login al inner join ag_kit ak on al.ag_login_id = ak.ag_login_id where al.email = 'mark@brightmedicineclinic.com';
select * from ag_login al inner join ag_kit ak on al.ag_login_id = ak.ag_login_id inner join ag_kit_barcodes akb on ak.ag_kit_id = akb.ag_kit_id where al.email = 'mark@brightmedicineclinic.com';

rollback;

commit;

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
