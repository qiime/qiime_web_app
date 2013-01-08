create or replace 
PROCEDURE "REGISTER_SPLIT_LIBRARY_RUN" 
/* 
This procedure loads the information related to the QIIME split-library run 
and will most likely be replaced in future releases.
*/
(
  -- define input/output variable for this procedure
  I_ANALYSIS_ID IN NUMBER, 
  I_RUN_DATE_STRING IN VARCHAR2, 
  I_COMMAND IN VARCHAR2, 
  I_SVN_VERSION IN VARCHAR2, 
  I_LOG_FILE IN CLOB, 
  I_HISTOGRAM_FILE IN CLOB, 
  I_MD5_CHECKSUM IN VARCHAR2, 
  O_SPLIT_LIBRARY_RUN_ID OUT NUMBER, 
  O_ERROR_FLAG OUT NUMBER
)
IS
  l_analysis_ID		        ANALYSIS.ANALYSIS_ID%TYPE;
  l_log_file		          SPLIT_LIBRARY_RUN.LOG_FILE%TYPE; 
  l_histogram_file	      SPLIT_LIBRARY_RUN.HISTOGRAM_FILE%TYPE; 
  l_md5_Checksum		      SPLIT_LIBRARY_RUN.MD5_CHECKSUM%TYPE;
  l_command		            SPLIT_LIBRARY_RUN.COMMAND%TYPE;
  l_svn_version		        SPLIT_LIBRARY_RUN.SVN_VERSION%TYPE;
  l_run_date		          TIMESTAMP;
  l_run_date_string	      VARCHAR2(80);
  l_split_library_run_ID	SPLIT_LIBRARY_RUN.SPLIT_LIBRARY_RUN_ID%TYPE;
  time_value		          VARCHAR2(50);
  testing DATE;
  id_exists int;
  
BEGIN
    O_ERROR_FLAG := 0;

  
  	l_command := I_COMMAND;
  	l_svn_version := I_SVN_VERSION;
  	l_log_file := I_LOG_FILE;		--- CLOB
  	l_histogram_file := I_HISTOGRAM_FILE;	--- CLOB
  	l_md5_checksum :=  I_MD5_CHECKSUM;
    l_run_date:=TO_TIMESTAMP(I_RUN_DATE_STRING, 'DD/MM/YYYY/HH24/MI/SS');
		
  select  count(*) into id_exists
  from    split_library_run
  where   md5_checksum = l_md5_Checksum
          and command = l_command;
                
    if id_exists > 0 then
      -- Matched, just get the ID from the table
      select  split_library_run_id into l_split_library_run_ID
      from    split_library_run
      where   md5_checksum = l_md5_Checksum
              and command = l_command;
    else
    
      l_split_library_run_ID := SPLIT_LIBRARY_RUN_ID_SEQ.NEXTVAL;
    
      insert into split_library_run
              (SPLIT_LIBRARY_RUN_ID, SPLIT_LIBRARY_RUN_DATE, COMMAND, SVN_VERSION,
              LOG_FILE, HISTOGRAM_FILE, MD5_CHECKSUM)
      values  (l_split_library_run_ID, l_run_date, l_command, l_svn_version,
              l_log_file, l_histogram_file, l_md5_Checksum);

    end if;
    
    commit;
   

    l_analysis_ID := I_ANALYSIS_ID;


    /* UPDATE the Analysis Table */

    
      UPDATE ANALYSIS
      SET SPLIT_LIBRARY_RUN_ID = l_split_library_run_ID
      WHERE ANALYSIS_ID = l_analysis_ID;
      COMMIT;
    
    /* Return new SPLIT_LIBRARY_RUN_ID */	

    O_SPLIT_LIBRARY_RUN_ID := l_Split_Library_Run_ID;


END REGISTER_SPLIT_LIBRARY_RUN;