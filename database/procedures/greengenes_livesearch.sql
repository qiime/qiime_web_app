create or replace
procedure greengenes_livesearch
(
  query_string in varchar,
  column_values in out types.ref_cursor
)
as
begin    
  open column_values for  
     select distinct NCBI_ACC_W_VER 
     from   greengenes_taxonomy_map 
     where  NCBI_ACC_W_VER like '%' || query_string || '%'
            and rownum <= 20;

END GREENGENES_LIVESEARCH;