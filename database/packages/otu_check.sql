create or replace 
PACKAGE "OTU_CHECK" 
as 

  -- Define the input type
  TYPE md5_tab IS TABLE OF SSU_SEQUENCE.MD5_CHECKSUM%TYPE INDEX BY BINARY_INTEGER; 
  TYPE otu_tab IS TABLE OF SOURCE_MAP.REFERENCE_ID%TYPE INDEX BY BINARY_INTEGER; 

  -- define the procedure for inserting data into OTU tables
  procedure check_existing_otus
  (
    md5_array_ in md5_tab,
    otu_results_ in out otu_tab,
    md5_results_ in out md5_tab
  ); 

end otu_check;