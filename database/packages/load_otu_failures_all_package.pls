CREATE OR REPLACE PACKAGE "LOAD_OTU_FAILURES_ALL_PACKAGE" as 
/* This package loads the otu failures file from the otu_picking step into the
OTU_PICKING_FAILURES table. */ 

  -- Define the array tables input to the table insert.
  TYPE otu_seq_run_id_failures_tab      IS TABLE OF OTU_PICKING_FAILURES.OTU_PICKING_RUN_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE otu_seq_sample_ids_tab           IS TABLE OF SPLIT_LIBRARY_READ_MAP.SEQUENCE_NAME%TYPE INDEX BY BINARY_INTEGER;

  -- define the procedure for inserting data into the table.
  procedure array_insert (otu_seq_sample_ids in otu_seq_sample_ids_tab,
                          otu_seq_run_id_failures in otu_seq_run_id_failures_tab);

end load_otu_failures_all_package;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_OTU_FAILURES_ALL_PACKAGE" 
AS
  -- procedure for inserting otu failures into the table.
PROCEDURE array_insert(
    otu_seq_sample_ids      IN otu_seq_sample_ids_tab,
    otu_seq_run_id_failures IN otu_seq_run_id_failures_tab)
AS
  -- define an array table for the otu failure ssu sequence id's
TYPE otu_failures_ssu_id_tab
IS
  TABLE OF OTU_PICKING_FAILURES.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
  otu_failures_ssu_id otu_failures_ssu_id_tab;
  otu_failure_cnt NUMBER;
  has_error       NUMBER;
BEGIN
  -- Loop through the otu failures, get their ssu sequence ids and
  -- insert the data into the OTU_PICKING_FAILURES table
  FOR idx IN otu_seq_sample_ids.first..otu_seq_sample_ids.last
  LOOP
    BEGIN
      SELECT SSU_SEQUENCE_ID
      INTO otu_failures_ssu_id(idx)
      FROM SPLIT_LIBRARY_READ_MAP
      WHERE SEQUENCE_NAME =otu_seq_sample_ids(idx)
            and rownum = 1;
      has_error:=0;
    EXCEPTION
    WHEN NO_DATA_FOUND THEN
      has_error:=1;
    END;
    IF (has_error=0) THEN
      SELECT COUNT(1)
      INTO otu_failure_cnt
      FROM OTU_PICKING_FAILURES
      WHERE OTU_PICKING_RUN_ID=otu_seq_run_id_failures(idx)
      AND SSU_SEQUENCE_ID     =otu_failures_ssu_id(idx);
      IF (otu_failure_cnt     =0) THEN
        INSERT
        INTO OTU_PICKING_FAILURES
          (
            OTU_PICKING_RUN_ID,
            SSU_SEQUENCE_ID
          )
          VALUES
          (
            otu_seq_run_id_failures(idx),
            otu_failures_ssu_id(idx)
          );
        COMMIT;
      END IF;
    END IF;
  END LOOP;
END array_insert;
END load_otu_failures_all_package;
/
