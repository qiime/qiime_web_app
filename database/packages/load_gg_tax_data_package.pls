CREATE OR REPLACE PACKAGE "LOAD_GG_TAX_DATA_PACKAGE" as 
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
/


CREATE OR REPLACE PACKAGE BODY "LOAD_GG_TAX_DATA_PACKAGE" as

  -- define the procedure call
  procedure array_insert (gg_taxonomy_prokmsa in gg_taxonomy_prokmsa_tab,
                          gg_taxonomy_name in gg_taxonomy_name_tab,
                          gg_taxonomy_string in gg_taxonomy_string_tab) as
    
    -- Declare an ssu_sequence_id table array.
    
    --TYPE gg_taxonomy_ssu_id_tab       IS TABLE OF 
    --           TAXONOMY.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
    --gg_taxonomy_ssu_id gg_taxonomy_ssu_id_tab;
    
    begin
      
      -- Loop through the prokmsa's and get the ssu_sequence_id's associated
      --FOR idx in gg_taxonomy_prokmsa.first..gg_taxonomy_prokmsa.last
      --LOOP
      --  SELECT SSU_SEQUENCE_ID INTO gg_taxonomy_ssu_id(idx)
      --  FROM GREENGENES_REFERENCE
      --  WHERE PROKMSA_ID=gg_taxonomy_prokmsa(idx);
      --END LOOP;

      -- Insert the table arrays into the TAXONOMY table.
      FORALL idx in gg_taxonomy_prokmsa.first..gg_taxonomy_prokmsa.last
        INSERT INTO GREENGENES_TAXONOMY(PROKMSA_ID, TAXONOMY_NAME, TAXONOMY_STR)
        VALUES(gg_taxonomy_prokmsa(idx),
               gg_taxonomy_name(idx),
               gg_taxonomy_string(idx));
      COMMIT;

  end array_insert;
end load_gg_tax_data_package;
/
