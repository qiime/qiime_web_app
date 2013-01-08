create or replace 
PACKAGE "LOAD_OTU_FAILURES_ALL_PACKAGE" as 
/* This package loads the otu failures file from the otu_picking step into the
OTU_PICKING_FAILURES table. */ 

  -- Define the array tables input to the table insert.
  TYPE otu_seq_run_id_failures_tab      IS TABLE OF OTU_PICKING_FAILURES.OTU_PICKING_RUN_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE otu_seq_sample_ids_tab           IS TABLE OF SPLIT_LIBRARY_READ_MAP.SEQUENCE_NAME%TYPE INDEX BY BINARY_INTEGER;

  -- define the procedure for inserting data into the table.
  procedure array_insert (otu_seq_sample_ids in otu_seq_sample_ids_tab,
                          otu_seq_run_id_failures in otu_seq_run_id_failures_tab);

end load_otu_failures_all_package;