create or replace 
PACKAGE BODY "LOAD_OTU_TABLE_PACKAGE" as

  procedure array_insert (otu_prokmsa_id_array in otu_prokmsa_id_tab,
                          otu_sample_id_array in otu_sample_id_tab,
                          otu_run_set_id_array in otu_run_set_id_tab,
                          count_array in count_tab) is

  -- define table arrays for OTU and ssu sequence id's
  --TYPE map_otu_id_tab  IS TABLE OF gg_plus_denovo_reference.reference_id%TYPE INDEX BY BINARY_INTEGER;
  --map_otu_id_array     map_otu_id_tab;
  begin
    
    -- Loop through the sample id's
    FOR idx in otu_sample_id_array.first..otu_sample_id_array.last
    LOOP
        
      merge into otu_table
      using dual
      on (dual.dummy is not null 
          and otu_table.reference_id = otu_prokmsa_id_array(idx)
          and otu_table.sample_name=otu_sample_id_array(idx)
          and otu_table.otu_run_set_id=otu_run_set_id_array(idx)
         )
      when not matched then 
        -- if sample seq id not in the OTU_MAP table, insert it into the table
        INSERT (REFERENCE_ID, OTU_RUN_SET_ID,SAMPLE_NAME,"COUNT")
        VALUES (otu_prokmsa_id_array(idx),otu_run_set_id_array(idx),
                 otu_sample_id_array(idx),count_array(idx));
        COMMIT;

      
    END LOOP;

  end array_insert;


end load_otu_table_package;