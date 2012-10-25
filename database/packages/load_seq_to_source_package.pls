CREATE OR REPLACE PACKAGE "LOAD_SEQ_TO_SOURCE_PACKAGE" as

/* 
This package loads the prokmsa to source mapping in the SEQUENCE_SOURCE_MAP 
table.
*/

  -- Declare all the array tables that are input to the package.
  TYPE prokmsa_id_array_tab                 IS TABLE OF 
              SOURCE_MAP.REFERENCE_ID%TYPE INDEX BY PLS_INTEGER;
  TYPE threshold_array_tab                    IS TABLE OF 
              SEQUENCE_SOURCE.THRESHOLD%TYPE INDEX BY PLS_INTEGER;
  TYPE ref_dataset_array_tab                    IS TABLE OF 
              VARCHAR2(100) INDEX BY PLS_INTEGER;

  -- package is located in the body section.           
  procedure array_insert (prokmsa_id_array in prokmsa_id_array_tab,
                          threshold_array in threshold_array_tab,
                          ref_dataset_array in ref_dataset_array_tab);
              
end load_seq_to_source_package;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_SEQ_TO_SOURCE_PACKAGE" as

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
/
