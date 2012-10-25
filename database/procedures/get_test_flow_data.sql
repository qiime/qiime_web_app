
--------------------------------------------------------
--  DDL for Procedure GET_TEST_FLOW_DATA
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."GET_TEST_FLOW_DATA" 
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
      select j.seq_run_id,f.sff_filename,f.number_of_reads,f.md5_checksum,
      h.instrument_code,r.read_id,r.read_sequence,r.flowgram_string,r.qual_string
      from analysis j
      inner join seq_run_to_sff_file s on j.seq_run_id=s.seq_run_id
      inner join sff_file f on f.sff_file_id=s.sff_file_id
      inner join read_454 r on r.seq_run_id=j.seq_run_id
      inner join split_library_read_map slrm on r.seq_run_id=slrm.seq_run_id and r.read_id=slrm.read_id
      inner join sequencing_run h on h.seq_run_id=s.seq_run_id
      where j.analysis_id=test_analysis_id and slrm.sequence_name=test_sample;
  END;
end get_test_flow_data;

/*
variable user_data REFCURSOR;
execute get_test_flow_data(455,'test_PCx634_1',:user_data);
print user_data;
*/