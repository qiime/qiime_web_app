create or replace 
PACKAGE "LOAD_SEQ_TO_SOURCE_PACKAGE" as

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