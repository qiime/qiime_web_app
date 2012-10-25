create or replace
PROCEDURE load_fna_file(I_FNA_FILE_NAME IN VARCHAR2, I_SEQ_RUN_ID IN NUMBER,
		 O_Error_Flag OUT NUMBER, O_Warning_Flag OUT NUMBER) IS

	OBJECT_EXISTS EXCEPTION;

  	PRAGMA EXCEPTION_INIT(OBJECT_EXISTS,-955);

    	vInHandle_FNA_File	UTL_FILE.file_type;
    	vOutHandle_FNA_File	UTL_FILE.file_type;
  
    	input_line		VARCHAR2(4000);

    	line_length		NUMBER(8);

	first_blank_pos		NUMBER(5);
   
 	next_blank_pos		NUMBER(5);

	next_equal_pos		NUMBER(5);

	next_tab_pos		NUMBER(5);
        
    	num_chars_to_cut	NUMBER(5);

	start_read_ID_pos	NUMBER(5); 
	
	sql_stmt1		VARCHAR2(250); 

	sql_stmt2		VARCHAR2(250); 

	sql_stmt3		VARCHAR2(250); 

	LoopCtr			NUMBER(8);

	loop_end_ctr		NUMBER(8) := 0;

	l_error_flag 		NUMBER(1) := 0;

	l_warning_flag		NUMBER(1) := 0;

	l_SEQ_RUN_ID		READ_454.SEQ_RUN_ID%TYPE;

	l_read_ID		READ_454.READ_ID%TYPE;

	l_sample_ID		READ_454.SAMPLE_ID%TYPE;

	l_orig_barcode		READ_454.ORIG_BARCODE_SEQ%TYPE; 

	l_new_barcode		READ_454.NEW_BARCODE_SEQ%TYPE;  

	l_barcode_diff	 	READ_454.BARCODE_DIFF%TYPE;  
   	
	l_barcode_diff_string 	VARCHAR2(4);

	l_split_lib_gen_string	VARCHAR2(12);


	l_FNA_Filename		VARCHAR2(200);
  l_FNA_Status_Filename		VARCHAR2(200);
  
    	local_sqlcode		NUMBER(8);
    	local_sqlerrm		VARCHAR2(1000);

	start_position		NUMBER(5);

    	FNA_Lines_Processed	NUMBER(8) := 0;

	FNA_parsed_lines	NUMBER(8) := 0;

 	Sample_ID_Count		NUMBER(5);

	time_value		VARCHAR2(50);
	
	/* Declaration of Parameters for INSERT Statement */

	l_SSU_SEQ_ID		SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE;

	p_SSU_SEQ_ID 		SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE;

	p_Sequence_String	SSU_SEQUENCE.SEQUENCE_STRING%TYPE;

	p_Sequence_Length 	SSU_SEQUENCE.SEQUENCE_LENGTH%TYPE;

	/* TYPE Definitions */

	TYPE orig_barcode_tab 	IS TABLE OF READ_454.ORIG_BARCODE_SEQ%TYPE INDEX BY BINARY_INTEGER;

    	TYPE new_barcode_tab 	IS TABLE OF READ_454.NEW_BARCODE_SEQ%TYPE INDEX BY BINARY_INTEGER;
    
    	TYPE barcode_diff_tab	IS TABLE OF READ_454.BARCODE_DIFF%TYPE INDEX BY BINARY_INTEGER;

	TYPE sample_ID_tab	IS TABLE OF READ_454.SAMPLE_ID%TYPE INDEX BY BINARY_INTEGER;

	TYPE read_ID_tab	IS TABLE OF READ_454.READ_ID%TYPE INDEX BY BINARY_INTEGER;

	TYPE SSU_SEQ_LENGTH_tab IS TABLE OF SSU_SEQUENCE.SEQUENCE_LENGTH%TYPE INDEX BY BINARY_INTEGER;
	
	TYPE SSU_SEQUENCE_tab	IS TABLE OF SSU_SEQUENCE.SEQUENCE_STRING%TYPE INDEX BY BINARY_INTEGER;

	TYPE SSU_SEQ_ID_tab	IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;

	/* Array Declarations */

	orig_barcode_array	orig_barcode_tab;
   
	new_barcode_array	new_barcode_tab;   

	barcode_diff_array	barcode_diff_tab;

	read_ID_array		read_ID_tab; 
	
	sample_ID_array		sample_ID_tab;

	SSU_SEQ_LENGTH_Array	SSU_SEQ_LENGTH_tab;

	SSU_SEQUENCE_Array	SSU_SEQUENCE_tab;

	SSU_SEQ_ID_Array	SSU_SEQ_ID_tab;
  
  period_pos		NUMBER(2); 


BEGIN

	/* Open STATUS File using SFF_DEV directory */
	
	BEGIN
      	period_pos := INSTR(I_FNA_FILE_NAME, '.');

      	num_chars_to_cut := period_pos - 1;
        
        l_FNA_Status_Filename := 'seq_id_'|| TO_CHAR(I_SEQ_RUN_ID) || '_' || SUBSTR(I_FNA_FILE_NAME, 1, num_chars_to_cut) || '.status';
    		vOutHandle_FNA_File := UTL_FILE.FOPEN('SFF_DIR', l_FNA_Status_Filename, 'w');

	EXCEPTION
      	    WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
		l_error_flag := 1;
  		goto bailout_fna;
    	END;

    	/* Get Process Start Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '-----------------------------------------------------');

	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, 'FNA Load Process Start Time: ' || time_value);
    
	UTL_FILE.FFLUSH(vOutHandle_FNA_File);
    	
	
	/* Open INPUT File using Oracle Directory */

	l_FNA_Filename := I_FNA_FILE_NAME;

	
	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, 'FNA FILE_NAME: ' || l_FNA_Filename);
    	UTL_FILE.FFLUSH(vOutHandle_FNA_File);
    	
	BEGIN
    
    		vInHandle_FNA_File := UTL_FILE.FOPEN('SFF_DIR', l_FNA_Filename, 'r', 32000);

    	EXCEPTION
            WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file: OPEN Error on FNA Input File ***');
  		UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  		UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file - SQLERRM: ' || local_sqlerrm);	
  		l_error_flag := 1;
		goto bailout_fna;
    		END;
  
	/* Index needed for: SELECT SSU_SEQUENCE_ID FROM SSU_SEQUENCE WHERE SEQUENCE_STRING = :value; */

	BEGIN

	EXECUTE IMMEDIATE 'CREATE INDEX SSU_SEQUENCE_SEQ_STR_IDX ON SSU_SEQUENCE(SUBSTR(SEQUENCE_STRING, 1, 60))';

	EXCEPTION 
	  WHEN OBJECT_EXISTS THEN 		--- if index exists already, then do nothing
		NULL;

	  WHEN OTHERS THEN
	  	local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file: CREATE INDEX Error ***');
  		UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  		UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file - SQLERRM: ' || local_sqlerrm);	
  		l_error_flag := 1;
		goto bailout_fna;
    	END;

/*-------------------------------- Possible Index for Performance Reasons ---------------------------

	CREATE INDEX READ_454_READ_ID_SAMPLE_ID_IDX ON READ_454(READ_ID, SAMPLE_ID);

    SQL statement being issued: SELECT COUNT(*) FROM READ_454 WHERE READ_ID = :1 AND SAMPLE_ID = :2
-----------------------------------------------------------------------------------------------------*/


	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, 'INDEX SSU_SEQUENCE_SEQ_STR_IDX has been built ...');
  

	/* PK CONSTRAINT needed for: UPDATE READ_454 WHERE SEQ_RUN_ID = :value1 AND READ_ID = :value2 */ 

	EXECUTE IMMEDIATE 'ALTER TABLE READ_454 ENABLE CONSTRAINT READ_454_PK';

	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, 'CONSTRAINT READ_454_PK has been enabled ...');
	UTL_FILE.FFLUSH(vOutHandle_FNA_File);

    	/* Loop to read in lines from the FNA Input file */

    	LOOP

		BEGIN

		/* Read in next line from FNA File */

       		UTL_FILE.GET_LINE(vInHandle_FNA_File, input_line);
      
		EXCEPTION
	  	    WHEN NO_DATA_FOUND THEN
	      		goto begin_insert_fna;
	  	    WHEN OTHERS THEN
	       	 	local_sqlcode := SQLCODE;
    	       	 	local_sqlerrm := SQLERRM;
  			UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file: GET_LINE Error ***');
       			UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** load_fna_file - SQLERRM: ' || local_sqlerrm);
			l_error_flag := 1;      		
			goto bailout_fna;
           	END;
	
		/* Take off Leading and Trailing Blanks */
	
		input_line :=  LTRIM(input_line, ' ');

		input_line :=  RTRIM(input_line, ' ');

        	line_length := LENGTH(input_line);

		/* Find Sample_ID / Barcode line */

    		IF (SUBSTR(input_line, 1, 1) = '>') THEN

	     	    BEGIN

			/* Find 1st Blank Space after the Sample_ID String */

			next_blank_pos := INSTR(input_line, ' ', 2, 1);
				
			/* Pull out sample_ID */
			
			num_chars_to_cut := next_blank_pos - 2;

			l_sample_ID := SUBSTR(input_line, 2, num_chars_to_cut);

		---UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** Sample_ID: ' || l_sample_ID);
		
			/* Example: >v45D_23.1.08_1 F7EB3GO1AY2R8 */
			/*          1234567890123456789012345     */
			
			/* Pull out read_ID */

			start_read_ID_pos := next_blank_pos + 1; 

			next_blank_pos := INSTR(input_line, ' ', start_read_ID_pos, 1);

			num_chars_to_cut := next_blank_pos - start_read_ID_pos;
		
			l_read_ID := SUBSTR(input_line, start_read_ID_pos, num_chars_to_cut);

		---UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** Read_ID: ' || l_read_ID);
		---UTL_FILE.FFLUSH(vOutHandle_FNA_File);
			
			/* Pull out original barcode */

			next_equal_pos := INSTR(input_line, '=', (start_read_ID_pos + num_chars_to_cut), 1);

			next_blank_pos := INSTR(input_line, ' ', next_equal_pos, 1);

			num_chars_to_cut := next_blank_pos - next_equal_pos - 1;
			
			l_orig_barcode := SUBSTR(input_line, (next_equal_pos + 1), num_chars_to_cut);
	
		---UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** Original_Barcode: ' || l_orig_barcode);
		
			/* Pull out new barcode */
			
			next_equal_pos := INSTR(input_line, '=', (next_blank_pos + 1), 1);

			next_blank_pos := INSTR(input_line, ' ', next_equal_pos, 1);
			
			num_chars_to_cut := next_blank_pos - next_equal_pos - 1;
			
			l_new_barcode := SUBSTR(input_line, (next_equal_pos + 1), num_chars_to_cut);
		
		---UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** New_Barcode: ' || l_new_barcode);
				
			/* Pull out barcode diff */
		
			next_equal_pos := INSTR(input_line, '=', (next_blank_pos + 1), 1);

			num_chars_to_cut := line_length - next_equal_pos;

			l_barcode_diff_string := SUBSTR(input_line, (next_equal_pos + 1), num_chars_to_cut);
      			
			l_barcode_diff := TO_NUMBER(l_barcode_diff_string);		
		
			/* Load up the Arrays */

			sample_ID_array(FNA_Lines_Processed) := l_sample_ID;
			
			read_ID_array(FNA_Lines_Processed) := l_read_ID;
	
			orig_barcode_array(FNA_Lines_Processed) := l_orig_barcode;
   
			new_barcode_array(FNA_Lines_Processed) := l_new_barcode;

			barcode_diff_array(FNA_Lines_Processed) := l_barcode_diff;

			FNA_Lines_Processed := FNA_Lines_Processed + 1;
						
	    	    END;

        	ELSE /* Line not beginning with a '>' */

          	    BEGIN
			SSU_SEQUENCE_Array(FNA_Lines_Processed-1) :=  input_line;
       			SSU_SEQ_LENGTH_Array(FNA_Lines_Processed-1) :=  LENGTH(input_line); 

                    EXCEPTION
      	    	      WHEN OTHERS THEN
			local_sqlcode := SQLCODE;
    			local_sqlerrm := SQLERRM;
     			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file: Sequence String Processing Error ***');
        		UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
			l_error_flag := 1;     			
			goto bailout_fna;
	  	    END;

		    /* Debug - only read a few rows */
		
		  ---IF(FNA_Lines_Processed > 4) THEN EXIT; END IF;

   		END IF;
		   
    	END LOOP; /* Loop reading lines from file */

   
<<begin_insert_fna>>

	FNA_parsed_lines := FNA_Lines_Processed * 2;

	UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Total_FNA_Lines Parsed: ' || TO_CHAR(FNA_parsed_lines));
	UTL_FILE.FFLUSH(vOutHandle_FNA_File);

	/* Setup Parameterized Queries */

	sql_stmt1 := 'SELECT SSU_SEQUENCE_ID FROM SSU_SEQUENCE WHERE SEQUENCE_STRING = :1';

	sql_stmt2 := 'INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SOURCE_TYPE_ID, SEQUENCE_LENGTH, SEQUENCE_STRING) ' || 	
		 	'VALUES (:1, :2, :3, :4)';

       	sql_stmt3 := 'SELECT COUNT(*) FROM READ_454 WHERE READ_ID = :1 AND SAMPLE_ID = :2';
	
	loop_end_ctr :=  FNA_Lines_Processed - 1;

	/*--- Major Processing Loop ---*/

	FOR LoopCtr IN 0..loop_end_ctr
	
	LOOP
		/*-----------------------------------------------------------------------------------
		
		 -- If ROW EXISTS in READ_454 with the same READ_ID and SAMPLE_ID as in the FNA file,
	  
		 -- then write information out to Status File. Return Warning: ERROR_FLAG of value -1 
        
		 ------------------------------------------------------------------------------------*/
		
		BEGIN
			EXECUTE IMMEDIATE sql_stmt3 INTO Sample_ID_Count 
				USING read_ID_array(loopctr), sample_ID_array(loopctr);
		
		EXCEPTION
		  WHEN OTHERS THEN
			  	local_sqlcode := SQLCODE;
    			 	local_sqlerrm := SQLERRM;
     				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file: SELECT COUNT Error ***');
        			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Loopctr: ' || TO_CHAR(Loopctr));	
				l_error_flag := 1; 
				goto bailout_fna;    			
		END;
		
		CASE (Sample_ID_Count)

		WHEN 0 THEN
			NULL;
		ELSE		
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** Warning Duplicate READ_ID/SAMPLE_ID found in READ_454');
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Sample_ID_Count: ' || TO_CHAR(Sample_ID_Count));
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** READ_ID: ' || read_ID_array(loopctr));
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** SAMPLE_ID: ' || sample_ID_array(loopctr));
			UTL_FILE.FFLUSH(vOutHandle_FNA_File);
			l_warning_flag := 1;
		
		END CASE;
		
		BEGIN
			p_Sequence_String := SSU_SEQUENCE_Array(LoopCtr); 

			p_Sequence_Length := SSU_SEQ_LENGTH_Array(LoopCtr);
		
		EXCEPTION
		  WHEN OTHERS THEN
			  	local_sqlcode := SQLCODE;
    			 	local_sqlerrm := SQLERRM;
     				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file: SSU Array Assignment Error ***');
        			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Loopctr: ' || TO_CHAR(Loopctr));	
				l_error_flag := 1; 
				goto bailout_fna;    			
		END;

		
		/*----------------------------------------------------------------------------------
		
		--- If Sequence String already exists in SSU_SEQUENCE, then "fetch" SSU_SEQUENCE_ID.
	  
		--- If Sequence String does not exist, then create a New Row 
        
		-----------------------------------------------------------------------------------*/
		
		BEGIN
			EXECUTE IMMEDIATE sql_stmt1 INTO l_SSU_SEQ_ID USING p_Sequence_String;

			SSU_SEQ_ID_Array(LoopCtr) := l_SSU_SEQ_ID;
				
		EXCEPTION
		  WHEN NO_DATA_FOUND THEN

			SSU_SEQ_ID_Array(LoopCtr) := SSU_SEQUENCE_ID_SEQ.NEXTVAL;

			p_SSU_SEQ_ID := SSU_SEQ_ID_Array(LoopCtr);

			BEGIN

				EXECUTE IMMEDIATE sql_stmt2 USING p_SSU_SEQ_ID, 2, p_Sequence_Length, p_Sequence_String;
        
			EXCEPTION
      	    	          WHEN OTHERS THEN
			  	local_sqlcode := SQLCODE;
    			 	local_sqlerrm := SQLERRM;
     				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file: INSERT IMMEDIATE Error ***');
        			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Loopctr: ' || TO_CHAR(Loopctr));
				UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** SSU_SEQ_ID: ' || TO_CHAR(p_SSU_SEQ_ID));	
				l_error_flag := 1;
				goto bailout_fna;     			
		    	END;

		  WHEN OTHERS THEN
          		local_sqlcode := SQLCODE;
    			local_sqlerrm := SQLERRM;
     			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SELECT SSU_SEQUENCE Error ***');
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Loopctr: ' || TO_CHAR(Loopctr));
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** SSU_SEQ_ID: ' || TO_CHAR(p_SSU_SEQ_ID));
			l_error_flag := 1;
			goto bailout_fna;  
		END;
		
		IF (MOD(LoopCtr, 10000) = 0) THEN
			UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** FNA Lines Processed: '  || TO_CHAR(LoopCtr) || ' ***');
			UTL_FILE.FFLUSH(vOutHandle_FNA_File);		
		END IF;

	END LOOP;

	COMMIT;

	/*-------------------------------------------------------------------------------------*/	   
	
	/* Performing BULK UPDATE of READ_454 Table */

	UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** Beginning BULK UPDATE of READ_454 Table ***');
	UTL_FILE.FFLUSH(vOutHandle_FNA_File);	
	
	l_SEQ_RUN_ID := I_SEQ_RUN_ID;

	BEGIN
		FORALL indx in sample_ID_array.first..sample_ID_array.last
		
			UPDATE READ_454
			SET	SSU_SEQUENCE_ID = SSU_SEQ_ID_array(indx),
				SAMPLE_ID = sample_ID_array(indx),
				BARCODE_READ_GROUP_TAB = sample_ID_array(indx),
        ORIG_BARCODE_SEQ = orig_barcode_array(indx),
				NEW_BARCODE_SEQ = new_barcode_array(indx),
				BARCODE_DIFF = barcode_diff_array(indx)
			WHERE SEQ_RUN_ID = l_SEQ_RUN_ID AND READ_ID = read_ID_array(indx); 
		
		

	EXCEPTION
          WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
     		UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - BULK UPDATE Error - ' ||
			'SSU_SEQUENCE Table ***');
        	UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
		UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
		l_error_flag := 1;
		goto bailout_fna;
    	END;

	COMMIT; 

/*-------------------------------------------------------------------------------------*/
  
	
	/* Get Process End Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** FNA_Lines_Processed: ' || TO_CHAR(FNA_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, 'FNA Load Process End Time: ' || time_value);
    	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '-----------------------------------------------------');
	
<<bailout_fna>>
	
	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** Warning Flag: ' || TO_CHAR(l_warning_flag)); 
	UTL_FILE.PUT_LINE(vOutHandle_FNA_File, '*** Error Flag: ' || TO_CHAR(l_error_flag)); 	
	UTL_FILE.FFLUSH(vOutHandle_FNA_File);
    	
	IF (UTL_FILE.IS_OPEN(vInHandle_FNA_File)) THEN
       		UTL_FILE.FCLOSE(vInHandle_FNA_File);
    	END IF;    
    
   	IF (UTL_FILE.IS_OPEN(vOutHandle_FNA_File)) THEN
       		UTL_FILE.FCLOSE(vOutHandle_FNA_File);
    	END IF; 

	/* Set Output ERROR_FLAG Parameter */


	O_Error_Flag := l_error_flag;
	
        O_Warning_Flag := l_warning_flag;
	
EXCEPTION
  WHEN OTHERS THEN
    	local_sqlcode := SQLCODE;		
    	local_sqlerrm := SQLERRM;
   	UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - Exception Handler - Unexpected Error ***');	
   	UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
   	UTL_FILE.PUT_LINE(vOutHandle_FNA_File,'*** load_fna_file - SQLERRM: ' || local_sqlerrm);
	O_Error_Flag := 1;
	
END load_fna_file;