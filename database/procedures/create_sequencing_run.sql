create or replace 
PROCEDURE "CREATE_SEQUENCING_RUN" 
/* This procedure creates a sequencing run in the SEQUENCING_RUN table. */
(
  -- define the input/output fields to this procedure.
  instr_code IN VARCHAR2,
  instr_version IN VARCHAR2,
  v_sequence_run_id OUT NUMBER
)
as 
begin
  -- get a sequencing run id
  v_sequence_run_id := SEQ_RUN_ID_SEQ.nextval;
  
  -- insert row into SEQUENCING_RUN table
  INSERT INTO SEQUENCING_RUN(SEQ_RUN_ID,INSTRUMENT_CODE,VERSION) 
  VALUES (v_sequence_run_id,instr_code,instr_version);
  COMMIT;
end create_sequencing_run;

/*
variable seq_run_id NUMBER;
execute create_sequencing_run('TEST','1',:seq_run_id);
print seq_run_id;
*/