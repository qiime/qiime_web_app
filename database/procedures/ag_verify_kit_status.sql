create or replace 
PROCEDURE "AG_VERIFY_KIT_STATUS"
/* This procedure appends the ANALYSIS table with the new sequence run id. */
(
  -- define the input to this procedure
  supplied_kit_id IN NUMBER
)
as 
begin
  -- update ANALYSIS table with sequence run id
  UPDATE AG_KIT
  SET KIT_VERIFIED='y'
  WHERE SUPPLIED_KIT_ID=supplied_kit_id;
  
  commit;
  
end ag_verify_kit_status;

/*
execute ag_verify_kit_status(1);
*/