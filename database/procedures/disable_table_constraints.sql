--------------------------------------------------------
--  DDL for Procedure DISABLE_TABLE_CONSTRAINTS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."DISABLE_TABLE_CONSTRAINTS" 
/* This procedure disables some of the table constraints. */
(
  error_flag IN OUT NUMBER
) as 
begin
  -- disable table constraints
  EXECUTE IMMEDIATE 'ALTER TABLE READ_454 DISABLE CONSTRAINT READ_454_PK';
  /*EXECUTE IMMEDIATE 'ALTER TABLE READ_454 DISABLE CONSTRAINT READ_454_TO_SSU_SEQ_ID_FK';*/

  error_flag:=0;
end disable_table_constraints;

/*
variable error_flag NUMBER;
execute disable_table_constraints(:error_flag);
print error_flag;
*/
