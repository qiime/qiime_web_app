create or replace
PROCEDURE GET_SAMPLE_CATEGORIES 
(
  metadata_header in VARCHAR2,
  studies in varchar2,  
  sample_categories out types.ref_cursor  
)
AS 
BEGIN
open sample_categories for
  SELECT DISTINCT metadata_header
  FROM microbe_metadata
  WHERE study_name=studies;
END GET_SAMPLE_CATEGORIES;

/*
variable sample_categories REFCURSOR;
variable metadata_header VARCHAR2;
variable studies VARCHAR2;
execute get_sample_categories('HOST_AGE','WHOLE_BODY',:sample_categories );
print sample_categories;
*/
