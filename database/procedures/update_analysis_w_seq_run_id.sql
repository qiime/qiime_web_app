
--------------------------------------------------------
--  DDL for Procedure UPDATE_ANALYSIS_W_SEQ_RUN_ID
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."UPDATE_ANALYSIS_W_SEQ_RUN_ID" 
/* This procedure appends the ANALYSIS table with the new sequence run id. */
(
  -- define the input to this procedure
  anal_id IN NUMBER,
  run_id IN NUMBER
)
as 
begin
  -- update ANALYSIS table with sequence run id
  UPDATE ANALYSIS
  SET SEQ_RUN_ID=run_id
  WHERE ANALYSIS_ID=anal_id;
  
  commit;
  
end update_analysis_w_seq_run_id;

/*
execute update_analysis_w_seq_run_id(1,1);

*/
