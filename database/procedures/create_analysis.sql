create or replace 
PROCEDURE "CREATE_ANALYSIS" 
/* This procedure creates a row in the ANALYSIS table, which is the table
that links all the information for a given study analyzed. */
(
  -- define variable output from this procedure
  metadata_study_id IN NUMBER,
  ana_id OUT NUMBER
) as 
begin
  -- get the analysis id next value 
  ana_id:=ANALYSIS_ID_SEQ.nextval;
  
  -- insert the analysis id into the ANALYSIS table
  INSERT INTO ANALYSIS(ANALYSIS_ID,STUDY_ID) VALUES(ana_id,metadata_study_id);
  COMMIT;
end create_analysis;


/*
variable analysis_id NUMBER;
execute create_analysis(:analysis_id);
print analysis_id;
*/