
--------------------------------------------------------
--  DDL for Procedure GET_META_ANALYSIS_FILEPATHS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_META_ANALYSIS_FILEPATHS" 
( 
  meta_ana_id IN NUMBER,
  user_data OUT types.ref_cursor
)
as 
begin
  open user_data for
    SELECT maf.file_path, maf.processing_date,mat.meta_analysis_type,maf.file_type
    from meta_analysis_files maf
    inner join meta_analysis_type mat on maf.meta_analysis_type_id=mat.meta_analysis_type_id
    where maf.meta_analysis_id=meta_ana_id;
    
end get_meta_analysis_filepaths;

/*
variable user_data REFCURSOR;
execute get_meta_analysis_filepaths(81,:user_data);
print user_data;
*/
