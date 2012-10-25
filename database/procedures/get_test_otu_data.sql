create or replace
PROCEDURE "GET_TEST_OTU_DATA" 
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
      select distinct j.seq_run_id,slrm.ssu_sequence_id,ot.reference_id,gr.ssu_sequence_id,
      ot.reference_id,j.otu_picking_run_id,p.command,p.md5_sum_input_file,
      p.threshold
      from analysis j
      inner join read_454 r on j.seq_run_id=r.seq_run_id 
      inner join split_library_read_map slrm on r.seq_run_id=slrm.seq_run_id and r.read_id=slrm.read_id and j.split_library_run_id=slrm.split_library_run_id
      inner join otu_table ot on j.otu_run_set_id=ot.otu_run_set_id and slrm.sample_name=ot.sample_name
      inner join gg_plus_denovo_reference gr on ot.reference_id=gr.reference_id
      -- inner join otu_map m on j.otu_run_set_id=m.otu_run_set_id and slrm.ssu_sequence_id=m.ssu_sequence_id
      -- inner join otu o on m.otu_id=o.otu_id
      inner join otu_picking_run p on j.otu_picking_run_id=p.otu_picking_run_id
      where j.analysis_id=test_analysis_id and slrm.sequence_name=test_sample;
  END;
end get_test_otu_data;

/*
variable user_data REFCURSOR;
execute get_test_otu_data(455,'test_PCx634_2',:user_data);
print user_data;
*/