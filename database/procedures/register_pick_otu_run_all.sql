create or replace
PROCEDURE "REGISTER_OTU_PICK_RUN_ALL" 
/* 
This procedure loads the information related to the QIIME OTU-picking run 
and will most likely be replaced in future releases.
*/
(
  -- define input/output variable for this procedure
  analysis_id_ in number,
  O_OTU_RUN_SET_ID IN OUT NUMBER,
	I_OTU_PICKING_DATE_STRING IN VARCHAR2, 
  I_OTU_PICKING_METHOD IN VARCHAR2, 
  I_THRESHOLD IN NUMBER,
	I_SVN_VERSION IN VARCHAR2, 
  I_COMMAND IN VARCHAR2, 
  I_LOG_FILE IN CLOB, 
  I_MD5_SUM_INPUT_FILE IN VARCHAR2, 
  I_REF_SET_NAME IN VARCHAR2,
  I_REF_SET_THRESHOLD IN NUMBER,
	ERROR_FLAG OUT NUMBER, 
  O_OTU_PICKING_RUN_ID OUT NUMBER
) 
IS	

	l_otu_run_date		      TIMESTAMP;
	l_otu_run_date_string	  VARCHAR2(80);
	l_otu_picking_method 	  VARCHAR2(80);
	l_otu_picking_method_ID OTU_PICKING_RUN.OTU_PICKING_METHOD_ID%TYPE;
	l_threshold		          OTU_PICKING_RUN.THRESHOLD%TYPE; 
  l_otu_picking_run_ID	  OTU_PICKING_RUN.OTU_PICKING_RUN_ID%TYPE;
  l_otu_run_set_ID        OTU_PICKING_RUN.OTU_RUN_SET_ID%TYPE;
  l_OTU_Status_Filename   VARCHAR2(200);

BEGIN
  ERROR_FLAG:=0;
    
	/* Validate THRESHOLD Input Parameter */
			
	l_threshold := I_THRESHOLD;
 
	
	/*---------- Insert Row into OTU_PICKING_RUN Table  ----------*/
  
  l_otu_picking_run_ID := OTU_PICKING_RUN_ID_SEQ.NEXTVAL;
  if (O_OTU_RUN_SET_ID=0) THEN
  	l_otu_run_set_ID := OTU_RUN_SET_ID_SEQ.NEXTVAL;
  else
    l_otu_run_set_ID := O_OTU_RUN_SET_ID;
  end if;
  O_OTU_PICKING_RUN_ID :=l_otu_picking_run_ID;
  O_OTU_RUN_SET_ID:=l_otu_run_set_id;
  l_otu_run_date:=TO_TIMESTAMP(I_OTU_PICKING_DATE_STRING, 'DD/MM/YYYY/HH24/MI/SS');
  
  
  INSERT INTO OTU_RUN_SET(OTU_RUN_SET_ID)
  VALUES(l_otu_run_set_ID);


  SELECT OTU_PICKING_METHOD_ID
  INTO l_otu_picking_method_ID
  FROM OTU_PICKING_METHOD m
  inner join SEQUENCE_SOURCE s on m.otu_picking_ref_set_name=s.source_name and m.otu_picking_method_threshold=s.threshold
  WHERE m.OTU_PICKING_METHOD_NAME=I_OTU_PICKING_METHOD 
  and s.source_name=I_REF_SET_NAME 
  and s.threshold=I_REF_SET_THRESHOLD;

  INSERT INTO OTU_PICKING_RUN(OTU_PICKING_RUN_ID, OTU_RUN_SET_ID, OTU_PICKING_METHOD_ID, OTU_PICKING_DATE,
                              SVN_VERSION, COMMAND, LOG_FILE, THRESHOLD, MD5_SUM_INPUT_FILE)
  VALUES(l_otu_picking_run_ID, l_otu_run_set_ID, l_otu_picking_method_ID, l_otu_run_date,
         I_SVN_VERSION, I_COMMAND, I_LOG_FILE, l_threshold, I_MD5_SUM_INPUT_FILE);

  update  analysis
  set     otu_picking_run_id = l_otu_picking_run_ID,
          otu_run_set_id = l_otu_run_set_ID
  where   analysis_id = analysis_id_;


END REGISTER_OTU_PICK_RUN_ALL;