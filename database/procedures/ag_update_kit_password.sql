create or replace PROCEDURE AG_UPDATE_KIT_PASSWORD 
(
  KIT_ID_ IN VARCHAR2 
, PASS_ IN VARCHAR2 
) AS 
BEGIN
  UPDATE AG_KIT  set kit_password = PASS_, pass_reset_code = null
  where supplied_kit_id = KIT_ID_;
  commit;
  
END AG_UPDATE_KIT_PASSWORD;
 

/*
execute AG_UPDATE_KIT_PASSWORD('test', 'test!@#$');
*/