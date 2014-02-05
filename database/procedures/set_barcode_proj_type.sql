create or replace procedure set_barcode_proj_type 
(
  project_ in varchar2
, barcode_ in varchar2 
) as 
  project_code number;
--  results_ types.ref_cursor;
begin
  select project_id into project_code from project where project = project_;
  update project_barcode set project_id = project_code where barcode = barcode_;
  commit;
  null;
end set_barcode_proj_type;

/*
execute set_barcode_proj_type('American Gut Handout kit' , '000000001');
execute set_barcode_proj_type('American Gut Project' , '000000001');
*/