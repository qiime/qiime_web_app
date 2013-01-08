create or replace 
PACKAGE "LOAD_OTU_TABLE_PACKAGE" as 
/* This package loads the otu to sample mapping file intot the OTU and OTU MAP 
tables*/

  -- define an associative array type for each array passed into the packeage
  TYPE otu_prokmsa_id_tab 	    IS TABLE OF VARCHAR2(200) INDEX BY BINARY_INTEGER; 
  TYPE otu_sample_id_tab      	IS TABLE OF VARCHAR2(100) INDEX BY BINARY_INTEGER;
  TYPE otu_run_set_id_tab      	IS TABLE OF OTU_RUN_SET.OTU_RUN_SET_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE count_tab          	    IS TABLE OF NUMBER(12,0) INDEX BY BINARY_INTEGER;
  
  -- define the procedure for inserting data into OTU tables
  procedure array_insert (otu_prokmsa_id_array in otu_prokmsa_id_tab,
                          otu_sample_id_array in otu_sample_id_tab,
                          otu_run_set_id_array in otu_run_set_id_tab,
                          count_array in count_tab); 

end load_otu_table_package;