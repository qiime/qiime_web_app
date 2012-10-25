create or replace
PROCEDURE "GET_TEST_OTU_FAILURE_DATA" 
/* 
This procedure returns a set of data given an analysis id for testing 
purposes. 
*/
(
  -- define input/output variable for the procedure
  test_analysis_id IN NUMBER,
  test_sample IN VARCHAR2,
  user_data in out types.ref_cursor
) as 
begin
  BEGIN
    -- get a set of data for validation that the input data equals the data 
    -- in the DB
    open user_data for
      select distinct j.seq_run_id,f.ssu_sequence_id
      from analysis j
      inner join read_454 r on j.seq_run_id=r.seq_run_id 
      inner join split_library_read_map slrm on r.seq_run_id=slrm.seq_run_id and r.read_id=slrm.read_id
      inner join otu_picking_failures f on slrm.ssu_sequence_id=f.ssu_sequence_id
      where j.analysis_id=test_analysis_id and slrm.sequence_name=test_sample;
  END;
end get_test_otu_failure_data;

/*
variable user_data REFCURSOR;
execute get_test_otu_failure_data(455,'test_PCx634_1',:user_data);
print user_data;
*/