create or replace 
PROCEDURE "GET_GG_TAXONOMY" 
(
  prok IN VARCHAR2,
  tax_name IN VARCHAR2,
  results in out types.ref_cursor
)
as 
begin
open results for
    SELECT taxonomy_str FROM greengenes_taxonomy
    where (prokmsa_id=prok and taxonomy_name=tax_name);

END GET_GG_TAXONOMY;

/*
variable tax_string REFCURSOR;
execute get_gg_taxonomy('10039','PHPR_tax_string',:tax_string);
print tax_string;
*/