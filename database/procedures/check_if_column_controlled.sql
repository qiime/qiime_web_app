
--------------------------------------------------------
--  DDL for Procedure CHECK_IF_COLUMN_CONTROLLED
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."CHECK_IF_COLUMN_CONTROLLED" 
(
  column_header IN VARCHAR2,
  valid OUT NUMBER
)
as 
begin
  select count(1) into valid
  from column_controlled_vocab
  where upper(column_name)=column_header;
end check_if_column_controlled;


/*
variable valid NUMBER;
execute check_if_column_controlled('TEST',:valid);
print valid;
*/
