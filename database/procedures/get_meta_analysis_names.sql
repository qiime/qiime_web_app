
--------------------------------------------------------
--  DDL for Procedure GET_META_ANALYSIS_NAMES
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_META_ANALYSIS_NAMES" 
(
  user_id IN NUMBER,
  user_data OUT types.ref_cursor
)as
begin
  open user_data for
    select distinct i.meta_analysis_id,i.meta_analysis_name
    from meta_analysis i
    where i.web_app_user_id=user_id;

end get_meta_analysis_names;

/*
variable user_data REFCURSOR;
execute get_meta_analysis_names(12171,:user_data);
print user_data;
*/
