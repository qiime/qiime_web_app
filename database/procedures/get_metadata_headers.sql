CREATE OR REPLACE
PROCEDURE GET_METADATA_HEADERS 
(
  metadata_headers in out types.ref_cursor
)
AS
BEGIN
OPEN metadata_headers FOR
    select  column_name
    from    all_tab_columns
    where   table_name = 'MICROBE_METADATA'
            and column_name <> 'STUDY_NAME'
    order by column_name;
    
END GET_METADATA_HEADERS;

/*

variable metadata_headers REFCURSOR;
execute get_metadata_headers( :metadata_headers );
print metadata_headers;

*/