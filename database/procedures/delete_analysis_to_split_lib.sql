
--------------------------------------------------------
--  DDL for Procedure DELETE_ANALYSIS_TO_SPLIT_LIB
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."DELETE_ANALYSIS_TO_SPLIT_LIB" 
/* This procedure deletes the test data from the DB. */
(
  -- define input/output fields for this procedure
  test_analysis_id IN NUMBER,
  error_flag OUT NUMBER
) as 

begin
  DECLARE
    run_id NUMBER;
    split_lib_run_id NUMBER;
    otu_run_id NUMBER;
    otu_set_id NUMBER;
    sff_id NUMBER;
  BEGIN
    -- get the appropriate fields for identifying a particular analysis
    select j.seq_run_id, j.split_library_run_id, j.otu_picking_run_id,j.otu_run_set_id
    into run_id, split_lib_run_id, otu_run_id, otu_set_id
    from analysis j
    where j.analysis_id=test_analysis_id;

    -- delete the appropriate rows from the DB
    delete from analysis where analysis_id=test_analysis_id;
    delete from split_library_read_map where split_library_run_id=split_lib_run_id;
    delete from split_library_run where split_library_run_id=split_lib_run_id;

    error_flag:=0;
  END;

end delete_analysis_to_split_lib;

/*
variable error_flag NUMBER;
execute delete_analysis_to_split_lib(22,:error_flag);
print error_flag;
*/
