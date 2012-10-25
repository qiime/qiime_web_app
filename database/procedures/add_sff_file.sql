--------------------------------------------------------
--  File created - Monday-April-18-2011   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Procedure ADD_SFF_FILE
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."ADD_SFF_FILE" 
/* This procedure adds the SFF file information into the SFF_FILE table */
(
  -- define the input fields for this procedure
  sff_fname IN VARCHAR2,
  num_reads IN NUMBER,
  head_len IN NUMBER,
  key_len IN NUMBER,
  num_flows IN NUMBER,
  flow_code IN VARCHAR2,
  flow_chars IN VARCHAR2,
  key_seq IN VARCHAR2,
  md5sum IN VARCHAR2,
  v_sequence_run_id IN NUMBER
)
as 
begin
  declare
  v_sff_file_id NUMBER;
  begin
    -- get an sff_file_id for the new SFF
    v_sff_file_id := FILE_ID_SEQ.nextval;
    
    -- insert the file information to the SFF_FILE table
    INSERT INTO SFF_FILE(SFF_FILE_ID,SFF_FILENAME,LOAD_DATE,NUMBER_OF_READS,
                         HEADER_LENGTH,KEY_LENGTH,NUMBER_OF_FLOWS,FLOWGRAM_CODE,
                         FLOW_CHARACTERS,KEY_SEQUENCE,MD5_CHECKSUM) 
    VALUES (v_sff_file_id,sff_fname,SYSDATE,num_reads,head_len,key_len,
            num_flows,flow_code,flow_chars,key_seq,md5sum);
    
    -- add the sff id to sequence run id association into the
    -- SEQ_RUN_TO_SFF_FILE table
    INSERT INTO SEQ_RUN_TO_SFF_FILE(SEQ_RUN_ID,SFF_FILE_ID) 
    VALUES (v_sequence_run_id,v_sff_file_id);
    COMMIT;
  end;
end add_sff_file;


/*
variable sff_file_id NUMBER;
execute add_sff_file('test.sff',4,10,4,10,'GS FLX','TEST','TCAG','314f4000857668d45a413d2e94a755fc',:sff_file_id);
print sff_file_id;
*/

/

