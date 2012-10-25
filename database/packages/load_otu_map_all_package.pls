CREATE OR REPLACE PACKAGE "LOAD_OTU_MAP_ALL_PACKAGE" as 
/* This package loads the otu to sample mapping file intot the OTU and OTU MAP 
tables*/

  -- define an associative array type for each array passed into the packeage
  TYPE otu_prokmsa_id_tab 	    IS TABLE OF VARCHAR2(200) INDEX BY BINARY_INTEGER; 
  TYPE otu_sample_id_tab      	IS TABLE OF VARCHAR2(100) INDEX BY BINARY_INTEGER;
  TYPE otu_run_set_id_tab      	IS TABLE OF OTU_MAP.OTU_RUN_SET_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE seq_source_tab      	    IS TABLE OF VARCHAR2(100) INDEX BY BINARY_INTEGER;
  
  -- define the procedure for inserting data into OTU tables
  procedure array_insert (otu_prokmsa_id_array in otu_prokmsa_id_tab,
                          otu_sample_id_array in otu_sample_id_tab,
                          otu_run_set_id_array in otu_run_set_id_tab,
                          seq_source_array in seq_source_tab); 

end load_otu_map_all_package;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_OTU_MAP_ALL_PACKAGE" 
AS
  -- procedure for inserting otu mapping data into the OTU tables
PROCEDURE array_insert(
    otu_prokmsa_id_array IN otu_prokmsa_id_tab,
    otu_sample_id_array  IN otu_sample_id_tab,
    otu_run_set_id_array IN otu_run_set_id_tab,
    seq_source_array     IN seq_source_tab)
IS
  -- define table arrays for OTU and ssu sequence id's
TYPE map_otu_id_tab
IS
  TABLE OF OTU_MAP.OTU_ID%TYPE INDEX BY BINARY_INTEGER;
TYPE map_ssu_id_tab
IS
  TABLE OF OTU_MAP.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
TYPE otu_ssu_id_tab
IS
  TABLE OF OTU_MAP.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
  map_otu_id_array map_otu_id_tab;
  map_ssu_id_array map_ssu_id_tab;
  otu_ssu_id_array otu_ssu_id_tab;
  l_otu_ssu_id types.ref_cursor;
  otu_id_cnt  NUMBER;
  l_otu_id    NUMBER;
  otu_map_cnt NUMBER;
  has_error   NUMBER;
BEGIN
  -- Loop through the sample id's
  FOR idx IN otu_sample_id_array.first..otu_sample_id_array.last
  LOOP
    -- get the ssu sequence id for the OTU
    -- from a 'reference' table using the prokmsa id
    /* TEMP disabled
    open l_otu_ssu_id for
    'SELECT SSU_SEQUENCE_ID FROM ' || seq_source_array(1) || ' WHERE PROKMSA_ID=' || otu_prokmsa_id_array(idx);
    fetch l_otu_ssu_id into otu_ssu_id_array(idx);
    */
    SELECT SSU_SEQUENCE_ID
    INTO otu_ssu_id_array(idx)
    FROM GREENGENES_REFERENCE
    WHERE PROKMSA_ID=otu_prokmsa_id_array(idx);
    -- get the ssu sequence id for each samaple from the READ_454 table
    BEGIN
      SELECT SSU_SEQUENCE_ID
      INTO map_ssu_id_array(idx)
      FROM SPLIT_LIBRARY_READ_MAP
      WHERE SEQUENCE_NAME=otu_sample_id_array(idx)
            and rownum = 1;
      has_error:=0;
    EXCEPTION
    WHEN NO_DATA_FOUND THEN
      has_error:=1;
    END;
    -- check if the OTU has already been assigned an id
    IF (has_error =0) THEN
      SELECT COUNT(1)
      INTO otu_id_cnt
      FROM OTU
      WHERE SSU_SEQUENCE_ID=otu_ssu_id_array(idx);
      -- if OTU id was not assigned, then append to the OTU table
      IF (otu_id_cnt=0) THEN
        l_otu_id   :=OTU_ID_SEQ.nextval;
        INSERT
        INTO OTU
          (
            OTU_ID,
            SSU_SEQUENCE_ID
          )
          VALUES
          (
            l_otu_id,
            otu_ssu_id_array(idx)
          );
        COMMIT;
        -- else return the OTU id
      ELSE
        SELECT OTU_ID
        INTO l_otu_id
        FROM OTU
        WHERE SSU_SEQUENCE_ID=otu_ssu_id_array(idx);
      END IF;
      map_otu_id_array(idx):=l_otu_id;
      -- check if the sample sequence was already assigned to the map within
      -- the same otu picking run
      SELECT COUNT(1)
      INTO otu_map_cnt
      FROM OTU_MAP
      WHERE OTU_RUN_SET_ID=otu_run_set_id_array(idx)
      AND SSU_SEQUENCE_ID =map_ssu_id_array(idx);
      -- if sample seq id not in the OTU_MAP table, insert it into the table
      IF (otu_map_cnt=0) THEN
        INSERT
        INTO OTU_MAP
          (
            OTU_ID,
            OTU_RUN_SET_ID,
            SSU_SEQUENCE_ID
          )
          VALUES
          (
            map_otu_id_array(idx),
            otu_run_set_id_array(idx),
            map_ssu_id_array(idx)
          );
        COMMIT;
      END IF;
    END IF;
  END LOOP;
END array_insert;
END load_otu_map_all_package;
/
