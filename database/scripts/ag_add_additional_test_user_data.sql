
select * from ag_kit where supplied_kit_id = 'test';

insert into ag_kit (ag_login_id, supplied_kit_id, kit_password, swabs_per_kit, kit_verification_code)
values ('D74F7B48C264494CE0408A80115D11FD', 'test2', 'test2', 2, 'test2');

select * from ag_kit where supplied_kit_id = 'test2';

commit;

select * from ag_kit_barcodes;

insert into ag_kit_barcodes (ag_kit_id, barcode, sample_barcode_file, sample_barcode_file_md5)
values ('D7E9CEFF8641E113E0408A80115D29E7', '000000002', '000000002.jpg', '');

insert into ag_kit_barcodes (ag_kit_id, barcode, sample_barcode_file, sample_barcode_file_md5)
values ('D7E9CEFF8641E113E0408A80115D29E7', '000000003', '000000003.jpg', '');

commit;