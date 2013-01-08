create or replace 
PACKAGE BODY "LOAD_SEQ_TO_SOURCE_PACKAGE" as

  procedure array_insert (prokmsa_id_array in prokmsa_id_array_tab,
                          threshold_array in threshold_array_tab,
                          ref_dataset_array in ref_dataset_array_tab) is
   
  TYPE seq_source_id_array_tab         IS TABLE OF 
              SOURCE_MAP.SEQUENCE_SOURCE_ID%TYPE INDEX BY PLS_INTEGER;   
  
  seq_source_id_array seq_source_id_array_tab;
  ssu_id_cursor types.ref_cursor;
  
  begin
   FOR idx in prokmsa_id_array.first..prokmsa_id_array.last
    LOOP

      select sequence_source_id into seq_source_id_array(idx) from SEQUENCE_SOURCE
      where source_name=ref_dataset_array(idx) and threshold=threshold_array(idx);
      
      INSERT INTO SOURCE_MAP(SEQUENCE_SOURCE_ID,REFERENCE_ID) 
      VALUES(seq_source_id_array(idx),prokmsa_id_array(idx));
      
    END LOOP;
    COMMIT;
  end array_insert;

end load_seq_to_source_package;