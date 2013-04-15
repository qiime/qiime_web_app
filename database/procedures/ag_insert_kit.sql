create or replace procedure ag_insert_kit
(
    ag_login_id_ varchar2, 
    kit_id_ varchar2, 
    kit_password_ varchar2, 
    swabs_per_kit_ varchar2, 
    kit_verification_code_ varchar2
)
as
begin

  insert    into ag_kit
            (ag_login_id, supplied_kit_id, kit_password, swabs_per_kit, kit_verification_code)
  values    (ag_login_id_, kit_id_, kit_password_, swabs_per_kit_, kit_verification_code_);
  
  commit;

end;