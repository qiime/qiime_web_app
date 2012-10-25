
CREATE OR REPLACE procedure get_study_names 
(
  study_names in out types.ref_cursor
)
AS
BEGIN
  OPEN study_names FOR 
    select  distinct project_name 
    from    study;
END;

/*

variable study_names REFCURSOR;
execute get_study_names( :study_names );
print study_names;

*/
