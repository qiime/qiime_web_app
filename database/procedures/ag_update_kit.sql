create or replace procedure ag_update_kit
(
    ag_kit_id_ varchar2,
    supplied_kit_id_ varchar2, 
    kit_password_ varchar2, 
    swabs_per_kit_ varchar2, 
    kit_verification_code_ varchar2
)
as
begin

    update  ag_kit
    set     supplied_kit_id = supplied_kit_id_,
            kit_password = kit_password_,
            swabs_per_kit = swabs_per_kit_,
            kit_verification_code = kit_verification_code_
    where   ag_kit_id = ag_kit_id_; 
  
    commit;

end;