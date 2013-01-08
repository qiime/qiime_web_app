create or replace 
PROCEDURE "GET_FLOWFILE" 
(
  seq_runid IN NUMBER,
  read454_data OUT types.ref_cursor
) as

begin
  -- open cursor for pulling out the glorious flows
  open read454_data for
    SELECT r.READ_ID, r.READ_SEQUENCE, r.READ_SEQUENCE_LENGTH, r.RUN_NAME, r.RUN_DATE, 
           r.REGION, r.X_LOCATION, r.Y_LOCATION, r.FLOWGRAM_STRING, r.FLOW_INDEX_STRING,
           r.CLIP_QUAL_LEFT, r.CLIP_QUAL_RIGHT, r.CLIP_ADAP_LEFT, r.CLIP_ADAP_RIGHT,
           r.QUAL_STRING
    FROM READ_454 r
    WHERE r.SEQ_RUN_ID=seq_runid;
    
end GET_FLOWFILE;

/*
variable flow_data REFCURSOR;
execute GET_FLOWFILE(497,:flow_data);
print flow_data;
*/