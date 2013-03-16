create or replace 
PROCEDURE AG_VERIFY_KIT_STATUS
(
  -- define the input to this procedure
  supplied_kit_id_ IN VARCHAR2
)
as 
begin
  UPDATE AG_KIT
  SET KIT_VERIFIED='y'
  WHERE SUPPLIED_KIT_ID=supplied_kit_id_;
  
  commit;
  
end ag_verify_kit_status;
