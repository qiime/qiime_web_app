create or replace 
PACKAGE "CHECK_SSU_SEQ_ID_CTS_PKG" as 
/* This package loads the otu to sample mapping file intot the OTU and OTU MAP 
tables*/

  -- define an associative array type for each array passed into the packeage
  TYPE ssu_sequence_id_tab 	    IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER; 
   TYPE ssu_sequence_str_tab 	    IS TABLE OF SSU_SEQUENCE.SEQUENCE_STRING%TYPE INDEX BY BINARY_INTEGER;
  TYPE user_data1_tab 	    IS TABLE OF NUMBER INDEX BY BINARY_INTEGER; 
  TYPE user_data2_tab 	    IS TABLE OF NUMBER INDEX BY BINARY_INTEGER; 
  -- define the procedure for inserting data into OTU tables
  procedure array_get (ssu_sequence_id_array in ssu_sequence_id_tab,
                       ssu_sequence_str_array in ssu_sequence_str_tab,
                       user_data1 IN OUT user_data1_tab,
                       user_data2 IN OUT user_data2_tab); 

end CHECK_SSU_SEQ_ID_CTS_PKG;