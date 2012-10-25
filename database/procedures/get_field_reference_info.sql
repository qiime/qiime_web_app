
--------------------------------------------------------
--  DDL for Procedure GET_FIELD_REFERENCE_INFO
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_FIELD_REFERENCE_INFO" 
(
  col_name IN VARCHAR2,
  user_data OUT types.ref_cursor
)
as 
begin
  open user_data for
    select data_type, desc_or_value,definition 
    from column_dictionary
    where upper(column_name)=col_name;
end get_field_reference_info;

/* 
variable user_data REFCURSOR;
execute get_field_reference_info('RUN_PREFIX',:user_data);
print user_data;
*/
