create or replace 
PACKAGE "LOAD_GG_TAX_DATA_PACKAGE" as 
/* This package loads the Greengenes associated taxonomy assignments into 
the TAXONOMY table. */

  -- Declare the associative arrays passed to this package.
  TYPE gg_taxonomy_name_tab       IS TABLE OF 
                GREENGENES_TAXONOMY.TAXONOMY_NAME%TYPE INDEX BY BINARY_INTEGER;
  TYPE gg_taxonomy_string_tab     IS TABLE OF 
              GREENGENES_TAXONOMY.TAXONOMY_STR%TYPE INDEX BY BINARY_INTEGER;
  TYPE gg_taxonomy_prokmsa_tab    IS TABLE OF 
               GREENGENES_REFERENCE.PROKMSA_ID%TYPE INDEX BY BINARY_INTEGER;

  -- define stored procdure for inserting arrays 
  procedure array_insert (gg_taxonomy_prokmsa in gg_taxonomy_prokmsa_tab,
                          gg_taxonomy_name in gg_taxonomy_name_tab,
                          gg_taxonomy_string in gg_taxonomy_string_tab);

end load_gg_tax_data_package;