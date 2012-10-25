
--------------------------------------------------------
--  DDL for Procedure GET_SEQ_RUN_ID_USING_MD5
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "SFF"."GET_SEQ_RUN_ID_USING_MD5" 
/* 
This procedure returns a sequence run id given the md5_checksum of the SFF.
*/
(
  -- define the input/output variables to the procedure
  I_md5_checksum IN VARCHAR2, 
  sequence_run_id OUT NUMBER
) as 
begin
  -- get the sequence run id given the SFF file md5_checksum  
  SELECT s.SEQ_RUN_ID 
  INTO sequence_run_id 
  FROM SEQ_RUN_TO_SFF_FILE s
  inner join SFF_FILE f on s.sff_file_id=f.sff_file_id
  WHERE f.md5_checksum=I_md5_checksum;
  
  commit;
  
  exception
    when NO_DATA_FOUND 
      then null;
    when others 
      then null;

  
end get_seq_run_id_using_md5;


/* 
variable seq_run_id NUMBER;
execute get_seq_run_id_using_md5('314f4000857668d45a413d2e94a755fc',:seq_run_id);
print seq_run_id;

variable seq_run_id NUMBER;
execute get_seq_run_id_using_md5('aaaa',:seq_run_id);
print seq_run_id;
*/