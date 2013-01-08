create or replace 
PROCEDURE "GET_FLOWFILE_HEADER" 
(
  seq_runid IN NUMBER,
  header_cur OUT types.ref_cursor
) AS 
BEGIN
/*
    -- get seq_file_id
  SELECT SFF_FILE_ID
  INTO sff_fid
  FROM SEQ_RUN_TO_SFF_FILE
  WHERE SEQ_RUN_ID=seq_runid;
  
  -- get machine version
  SELECT s."VERSION" 
  INTO mach_version
  FROM SEQUENCING_RUN s
  WHERE SEQ_RUN_ID=seq_runid;
  
  -- get additional header information
  SELECT sf.NUMBER_OF_READS, sf.HEADER_LENGTH, sf."KEY_LENGTH", sf.NUMBER_OF_FLOWS, 
         sf.FLOWGRAM_CODE, sf.FLOW_CHARACTERS,sf.KEY_SEQUENCE
  INTO num_reads, header_len, key_len, num_flows, flowgram_code, flow_chars,
        key_seq
  FROM SFF_FILE sf
  WHERE SFF_FILE_ID=sff_fid;
  */
  open header_cur for
    SELECT sr."VERSION", sf.NUMBER_OF_READS, sf.HEADER_LENGTH, sf."KEY_LENGTH", sf.NUMBER_OF_FLOWS, 
         sf.FLOWGRAM_CODE, sf.FLOW_CHARACTERS,sf.KEY_SEQUENCE
    FROM SEQUENCING_RUN sr
      INNER JOIN SEQ_RUN_TO_SFF_FILE srsf ON sr.SEQ_RUN_ID=srsf.SEQ_RUN_ID
      INNER JOIN SFF_FILE sf on srsf.SFF_FILE_ID=sf.SFF_FILE_ID
    WHERE sr.SEQ_RUN_ID=seq_runid;
  
END GET_FLOWFILE_HEADER;

/*
variable header_data REFCURSOR;
execute GET_FLOWFILE_HEADER(497,:header_data);
print header_data;
*/