create or replace
PROCEDURE GET_MAPPING_FILE_DATA 
(
  studies in varchar,
  samples_to_get in varchar, 
  meta_headers in varchar,
  mapping_values in out types.ref_cursor
)
as
begin    
  open mapping_values for  
     'select ' || samples_to_get || ' 
     from MICROBE_METADATA 
     where study_name in (' || studies || ') and ' || meta_headers;
END GET_MAPPING_FILE_DATA;

/*

variable mapping_values REFCURSOR;
execute get_mapping_file_data('''MALAWI_081209'',''SOIL''', 'HOST_FAMILY', 'HOST_FAMILY in (''84'',''46'')' , :mapping_values);
print mapping_values;

*/
