
/*------------------------------------------------------------------------------------------------

Procedure SFF_main is the "driver" procedure of the SFF file loading process.

Currently, SFF_main calls the following procedures in order:

PROCEDURE load_qual_file; PROCEDURE load_flow_file;


Requirements:

Oracle Directory - currently defined as "/SFF_Files" on microbiome1 (NEW Server).

Status File - currently defined as "sff.status".
QUAL File - currently defined as "qual.dat".
FLOW (Text) File - currently defined as "flow.dat".


Error Handling:

All error reporting is written to the status file.

The file handler (vOutHandle_SFF_Status) is a global variable.

Stored procedures try to detect errors/exceptions at the very lowest level.
The Oracle SQLCODE and SQLERRM will be written to the status file.
The stored procedure will exit and set the global variable "severe_error_flag" to 1.

SFF_main will exit immediately when a stored procedure completes and sets the "severe_error_flag" to 1.

Tables that will be loaded:

SEQUENCING_RUN
SSU_SEQUENCE
READ_454
QUAL_INDEX

---------------------------------------------------------------------------------------------------

Original Author: Bob Larsen

Modifications:


--------------------------------------------------------------------------------------------------*/

CREATE OR REPLACE PACKAGE Process_SFF_Files AS


/*------------------------------------------------------------------

Directories are owned by: oracle/oinstall

Directory for Input Files: /SFF_Files

Default Statuts File for Process_SFF_Files is: sff.status

-------------------------------------------------------------------*/

/*--- GLOBAL Variables ---*/

TYPE min_value_tab IS TABLE OF READ_454.QUAL_MIN%TYPE INDEX BY BINARY_INTEGER;
TYPE max_value_tab IS TABLE OF READ_454.QUAL_MAX%TYPE INDEX BY BINARY_INTEGER;
TYPE avg_value_tab IS TABLE OF READ_454.QUAL_AVG%TYPE INDEX BY BINARY_INTEGER;

min_value_array         min_value_tab;
max_value_array         max_value_tab;
avg_value_array         avg_value_tab;

empty_min_value_array   min_value_tab;
empty_max_value_array   max_value_tab;
empty_avg_value_array   avg_value_tab;

vOutHandle_SFF_Status   UTL_FILE.file_type;

SFF_Extra_Information   VARCHAR2(500);

Flow_Lines_Processed    NUMBER(12);
Flow_Sequence_Count     NUMBER(12);

Qual_Lines_Processed    NUMBER(12);
Qual_Sequence_Count     NUMBER(12);

severe_error_flag       NUMBER(1);

Global_ANALYSIS_ID      ANALYSIS.ANALYSIS_ID%TYPE;
Global_FILE_ID          SFF_FILE.SFF_FILE_ID%TYPE;
Global_FILENAME         SFF_FILE.SFF_FILENAME%TYPE;
Global_SEQ_RUN_ID       READ_454.SEQ_RUN_ID%TYPE;

PROCEDURE SFF_main(I_File_Name IN VARCHAR2, I_MD5_CHECKSUM IN VARCHAR2, P_SEQ_RUN_ID IN OUT NUMBER,
                       P_ANALYSIS_ID IN OUT NUMBER, I_ANALYSIS_NOTES IN VARCHAR2, error_flag OUT NUMBER);

PROCEDURE load_flow_file;

PROCEDURE load_qual_file;

END Process_SFF_Files;
/

/*------------------------------------------------------------------------------------------------

Procedure SFF_main is the "driver" procedure of the SFF file loading process.

Currently, SFF_main calls the following procedures in order:

PROCEDURE load_qual_file; PROCEDURE load_flow_file;


Requirements:

Oracle Directory - currently defined as "/SFF_Files" on microbiome1 (NEW Server).

Status File - currently defined as "sff.status".
QUAL File - currently defined as "qual.dat".
FLOW (Text) File - currently defined as "flow.dat".


Error Handling:

All error reporting is written to the status file.

The file handler (vOutHandle_SFF_Status) is a global variable.

Stored procedures try to detect errors/exceptions at the very lowest level.
The Oracle SQLCODE and SQLERRM will be written to the status file.
The stored procedure will exit and set the global variable "severe_error_flag" to 1.

SFF_main will exit immediately when a stored procedure completes and sets the "severe_error_flag" to 1.

Tables that will be loaded:

SEQUENCING_RUN
SSU_SEQUENCE
READ_454
QUAL_INDEX

---------------------------------------------------------------------------------------------------

Original Author: Bob Larsen

Modifications:


--------------------------------------------------------------------------------------------------*/

CREATE OR REPLACE PACKAGE BODY Process_SFF_Files IS


PROCEDURE SFF_main(I_FILE_NAME IN VARCHAR2, I_MD5_CHECKSUM IN VARCHAR2, P_SEQ_RUN_ID IN OUT NUMBER,
                       P_ANALYSIS_ID IN OUT NUMBER, I_ANALYSIS_NOTES IN VARCHAR2, error_flag OUT NUMBER) IS

local_sqlcode           NUMBER(8);
local_sqlerrm           VARCHAR2(1000);

l_Filename              SFF_FILE.SFF_FILENAME%TYPE;

l_MD5_Checksum          SFF_FILE.MD5_CHECKSUM%TYPE;

l_SEQ_RUN_ID            SEQ_RUN_TO_SFF_FILE.SEQ_RUN_ID%TYPE;

l_Analysis_ID           ANALYSIS.ANALYSIS_ID%TYPE;

l_Analysis_Notes        ANALYSIS.NOTES%TYPE;

check_SEQ_RUN_ID        SEQ_RUN_TO_SFF_FILE.SEQ_RUN_ID%TYPE;

file_name_count         NUMBER(2);

instant_exit_flag       NUMBER(1) := 0;

time_value              VARCHAR2(50);

period_pos              NUMBER(2);
num_chars_to_cut        NUMBER(6);

orig_filename           SFF_FILE.SFF_FILENAME%TYPE;


BEGIN
       /* Copy all INPUT Parameters to Local Variables */

       Global_FILENAME := I_FILE_NAME;
       l_MD5_Checksum := I_MD5_CHECKSUM;
       l_SEQ_RUN_ID := P_SEQ_RUN_ID;
       l_Analysis_ID := P_ANALYSIS_ID;
       l_Analysis_Notes := I_ANALYSIS_NOTES;



       /* Creating actual 'status' file name */

       orig_filename := Global_FILENAME;

       period_pos := INSTR(orig_filename, '.');

       num_chars_to_cut := period_pos - 1;

       l_Filename := SUBSTR(orig_filename, 1, num_chars_to_cut) || '.status';


       /* Open SFF Status File */

       BEGIN

       vOutHandle_SFF_Status := UTL_FILE.FOPEN('SFF_DEV_DIR', l_Filename, 'w', 32000);

       EXCEPTION
         WHEN OTHERS THEN
               DBMS_OUTPUT.PUT_LINE('*** SFF_main : OPEN ERROR on sff.status Output File ***');
               goto main_finish;
       END;


       /* Get Process Start Time */

       SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
       INTO time_value
       FROM dual;

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '-----------------------------------------------------');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, 'Status File: ' || l_Filename);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, 'SFF File Process Start Time: ' || time_value);

       UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

       /* Clear (Global) Severe Error Flag */

       severe_error_flag := 0;

       /* Make sure that P_SEQ_RUN_ID is not NULL */

       IF(l_SEQ_RUN_ID IS NULL) THEN
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: Parameter P_RUN_ID IS NULL ***');
               SFF_Extra_Information := '*** SFF_main: Parameter P_RUN_ID IS NULL ***';
               severe_error_flag := 1;
               goto main_finish;
       END IF;

       /* Make sure that P_ANALYSIS_ID is not NULL */

       IF(l_Analysis_ID IS NULL) THEN
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: Parameter P_ANALYSIS_ID IS NULL ***');
               SFF_Extra_Information := '*** SFF_main: Parameter P_ANALYSIS_ID IS NULL ***';
               severe_error_flag := 1;
               goto main_finish;
       END IF;

       /* Make sure that I_File_Name has a value */

       IF(l_Filename IS NULL) THEN
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: Parameter I_FILE_NAME IS NULL ***');
               SFF_Extra_Information := '*** SFF_main: Parameter I_FILE_NAME IS NULL ***';
               severe_error_flag := 1;
               goto main_finish;
       END IF;

       /* Make sure that I_File_Name has a value */

       IF(l_MD5_Checksum IS NULL) THEN
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: Parameter I_MD5_CHECKSUM IS NULL ***');
               SFF_Extra_Information := '*** SFF_main: Parameter I_MD5_CHECKSUM IS NULL ***';
               severe_error_flag := 1;
               goto main_finish;
       END IF;


       /* Check to see if "File Exists" in Table SFF_FILE  */

       BEGIN
               SELECT COUNT(*)
               INTO file_name_count
               FROM SFF_FILE
               WHERE MD5_CHECKSUM = l_MD5_Checksum;
       EXCEPTION
         WHEN OTHERS THEN
               local_sqlcode := SQLCODE;
               local_sqlerrm := SQLERRM;
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: SELECT COUNT(*) Error - SFF_FILE Table ***');
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
               SFF_Extra_Information := '*** SFF_main: SELECT COUNT(*) Error - SFF_FILE Table ***';
               severe_error_flag := 1;
               goto main_finish;
       END;

       CASE (file_name_count)

       WHEN 0 THEN     --- File DOES NOT EXIST in SFF_FILE

           BEGIN

               IF (l_SEQ_RUN_ID = 0) THEN

                       /* Create new row in SFF_FILE */

                       Global_FILE_ID := FILE_ID_SEQ.NEXTVAL;

                       BEGIN
                               INSERT INTO SFF_FILE(SFF_FILE_ID, SFF_FILENAME, LOAD_DATE, MD5_CHECKSUM)
                               VALUES(Global_FILE_ID, Global_FILENAME, SYSDATE, l_MD5_Checksum);

                               COMMIT;

                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: INSERT Error (1) - SFF_FILE Table ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: INSERT Error - SFF_FILE Table ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

                       /* Get new SEQ_RUN_ID and create new row in SEQUENCING_RUN */


                       Global_SEQ_RUN_ID := SEQ_RUN_ID_SEQ.NEXTVAL;

                       BEGIN
                               INSERT INTO SEQUENCING_RUN(SEQ_RUN_ID)
                               VALUES(Global_SEQ_RUN_ID);

                               COMMIT;
                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: INSERT Error (1) - SEQUENCING_RUN Table ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: INSERT Error - SEQUENCING_RUN Table ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

                       /* Create new row in SEQ_RUN_TO_SFF_FILE */

                       BEGIN
                               INSERT INTO SEQ_RUN_TO_SFF_FILE(SEQ_RUN_ID, SFF_FILE_ID)
                               VALUES(Global_SEQ_RUN_ID, Global_FILE_ID);

                               COMMIT;

                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: INSERT Error (1) - SEQ_RUN_TO_SFF_FILE Table ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: INSERT Error - SEQ_RUN_TO_SFF_FILE Table ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

               ELSE  --- File DOES NOT EXIST in SFF_FILE, SEQ_RUN_ID passed in (non-zero)

                       Global_SEQ_RUN_ID := l_SEQ_RUN_ID;


                       Global_FILE_ID := FILE_ID_SEQ.NEXTVAL;

                       BEGIN
                               INSERT INTO SFF_FILE(SFF_FILE_ID, SFF_FILENAME, LOAD_DATE, MD5_CHECKSUM)
                               VALUES(Global_FILE_ID, l_Filename, SYSDATE, l_MD5_Checksum);

                               COMMIT;

                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: INSERT Error (2) - SFF_FILE TABLE ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: INSERT Error (2) - SFF_FILE TABLE ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

                       /* Create row in SEQ_RUN_TO_SFF_FILE */

                       BEGIN
                               INSERT INTO SEQ_RUN_TO_SFF_FILE(SEQ_RUN_ID, SFF_FILE_ID)
                               VALUES(Global_SEQ_RUN_ID, Global_FILE_ID);

                               COMMIT;

                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: INSERT Error (2) - SEQ_RUN_TO_SFF_FILE Table ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: INSERT Error (2) - SEQ_RUN_TO_SFF_FILE Table ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

               END IF; --- end of SEQ_RUN_ID = 0 (IF statement)

           END; --- end of WHEN 0

       /*--------------------------------------------------------------------------------------*/

       WHEN 1 THEN     --- File EXISTS in SFF_FILE

           BEGIN
                       BEGIN
                               SELECT SFF_FILE_ID
                               INTO Global_FILE_ID
                               FROM SFF_FILE
                               WHERE MD5_CHECKSUM = l_MD5_Checksum;
                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: SELECT Error (3) - SFF_FILE Table ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: SELECT Error (3) - SFF_FILE Table ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

                       /* Fetch SEQ_RUN_ID from SEQ_RUN_TO_SFF_FILE */

                       BEGIN
                               SELECT SEQ_RUN_ID
                               INTO Global_SEQ_RUN_ID
                               FROM SEQ_RUN_TO_SFF_FILE
                               WHERE SFF_FILE_ID =  Global_FILE_ID;
                       EXCEPTION
                         WHEN OTHERS THEN
                               local_sqlcode := SQLCODE;
                               local_sqlerrm := SQLERRM;
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: SELECT Error (3) - SEQ_RUN_TO_SFF_FILE Table ***');
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                               SFF_Extra_Information := '*** SFF_main: SELECT Error (3) - SEQ_RUN_TO_SFF_FILE Table ***';
                               severe_error_flag := 1;
                               goto main_finish;
                       END;

                       instant_exit_flag := 1;

           END; --- end of WHEN 1

       /*--------------------------------------------------------------------------------------*/

       ELSE    --- MD5_CHECKSUM appears in SFF_FILE multiple times

           UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - MD5_CHECKSUM is in SFF_FILE Table > 2 times');
           SFF_Extra_Information := '*** SFF_main: - MD5_CHECKSUM is in SFF_FILE Table > 2 times ***';
           severe_error_flag := 1;
           goto main_finish;

       END CASE;


       /*-- Analysis Table Processing --*/


       /* If Input Parameter P_ANALYSIS_ID is zero, create new row in ANALYSIS Table */

       /***** NOTE - GLOBAL_SEQ_RUN_ID may be different than original P_SEQ_RUN_ID parameter *****/

       IF (l_Analysis_ID = 0) THEN

               GLOBAL_ANALYSIS_ID :=  ANALYSIS_ID_SEQ.NEXTVAL;

               BEGIN

                       INSERT INTO ANALYSIS(ANALYSIS_ID, SEQ_RUN_ID, SPLIT_LIBRARY_RUN_ID, OTU_PICKING_RUN_ID,
                                       OTU_RUN_SET_ID, NOTES)
                       VALUES(GLOBAL_ANALYSIS_ID, GLOBAL_SEQ_RUN_ID, -1, -1, -1, I_ANALYSIS_NOTES);

               EXCEPTION
                 WHEN OTHERS THEN
                       local_sqlcode := SQLCODE;
                       local_sqlerrm := SQLERRM;
                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: INSERT Error - ANALYSIS Table ***');
                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
                       SFF_Extra_Information := '*** SFF_main: INSERT Error - ANALYSIS Table ***';
                       severe_error_flag := 1;
                       goto main_finish;
               END;


       ELSE --- fetch existing SEQ_RUN_ID based on P_ANALYSIS_ID */

           BEGIN
               SELECT SEQ_RUN_ID
               INTO GLOBAL_SEQ_RUN_ID
               FROM ANALYSIS
               WHERE ANALYSIS_ID = l_Analysis_ID;

               Global_ANALYSIS_ID := l_Analysis_ID;

           EXCEPTION
             WHEN OTHERS THEN
               local_sqlcode := SQLCODE;
               local_sqlerrm := SQLERRM;
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: SELECT Error - ANALYSIS Table ***');
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLCODE: ' || TO_CHAR(local_sqlcode));
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main - SQLERRM: ' || local_sqlerrm);
               SFF_Extra_Information := '*** SFF_main: SELECT Error - ANALYSIS Table ***';
               severe_error_flag := 1;
               goto main_finish;
           END;

       END IF;


       /* Put Values in Output Parameters */

       P_SEQ_RUN_ID := Global_SEQ_RUN_ID;

       P_ANALYSIS_ID := Global_ANALYSIS_ID;

       IF (instant_exit_flag = 1) THEN
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** SFF_main: Taking INSTANT EXIT ***');
               severe_error_flag := 0;
               goto main_finish;
       END IF;

/*----------------------------------------------------------------------------------------------------------*/


       /********** Load QUAL File **********/

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, 'Loading Filename: qual.dat');

       load_qual_file();

       /* Exit if Severe Error */

       IF (severe_error_flag = 1) THEN
           UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'** SEVERE ERROR: Loading of QUAL File Aborted ... ');
           UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'** Extra Information: ' || SFF_Extra_Information);
           UTL_FILE.FFLUSH(vOutHandle_SFF_Status);
           goto main_finish;
       END IF;

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '** Qual_Lines_Processed: ' ||
               TO_CHAR(Qual_Lines_Processed,'999,999,999'));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '** Qual_Sequence_Count: ' ||
               TO_CHAR(Qual_Sequence_Count,'999,999,999'));

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'** QUAL File Loaded Successfully ...');
       UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

       /* Get load_qual Completion Time */

       SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
       INTO time_value
       FROM dual;

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'load_qual Completion Time: ' || time_value);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '-----------------------------------------------------');

       /******* Load FLOW (txt) File ******/

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, 'Loading Filename: flow.dat');
       UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

       load_flow_file();

       /* Exit if Severe Error */

       IF (severe_error_flag = 1) THEN
           UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'** SEVERE ERROR: Loading of FLOW File Aborted ... ');
           UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'** Extra Information: ' || SFF_Extra_Information);
           UTL_FILE.FFLUSH(vOutHandle_SFF_Status);
           goto main_finish;
       END IF;

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '** Flow_Lines_Processed: ' ||
               TO_CHAR(Flow_Lines_Processed,'999,999,999'));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '** Flow_Sequence_Count: ' ||
               TO_CHAR(Flow_Sequence_Count,'999,999,999'));

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'** FLOW File Loaded Successfully ...');
       UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

       /* Get load_flow Completion Time */

       SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
       INTO time_value
       FROM dual;

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'load_flow Completion Time: ' || time_value);
       UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

<<main_finish>>

       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,'-----------------------------------------------------');

       /* Set OUT Parameter - error_flag */

       error_flag := severe_error_flag;

       /* Final COMMIT */

       IF (severe_error_flag = 0) THEN
               COMMIT;
       END IF;

       /* Close Status File */

       IF (UTL_FILE.IS_OPEN(vOutHandle_SFF_Status)) THEN
               UTL_FILE.FCLOSE(vOutHandle_SFF_Status);
       END IF;

EXCEPTION
 WHEN OTHERS THEN
    local_sqlcode := SQLCODE;
    local_sqlerrm := SQLERRM;

END SFF_main;


/*---------------------------------------------------------------------------*/


PROCEDURE load_flow_file IS

   vInHandle_FLOW              UTL_FILE.file_type;

   input_line                  VARCHAR2(10000);

   value                       VARCHAR2(8000);
   value_length                NUMBER(5);

   r_year                      CHAR(4);
   r_month                     CHAR(2);
   r_day                       CHAR(2);
   r_hour                      CHAR(2);
   r_minute                    CHAR(2);
   r_sec                       CHAR(2);
   r_date_string               VARCHAR2(50);

   chunk_size                  NUMBER(6) := 500000;

   first_6_chars               CHAR(6);
   first_8_chars               CHAR(8);

   curr_tab_pos                NUMBER(5);
   next_tab_pos                NUMBER(5);

   start_pos                   NUMBER(5);
   num_chars_to_cut            NUMBER(5);

   underscore_pos              NUMBER(2);
   period_pos                  NUMBER(2);
   colon_pos                   NUMBER(5);

   line_length                 NUMBER(6);

   read_identifier             READ_454.READ_ID%TYPE := '*** NOT SET ***';

   loopctr                     BINARY_INTEGER;


   /* Values not currently being Saved */

   x_full_path                 VARCHAR2(250);
   x_read_header_length        VARCHAR2(20);
   x_run_analysis_name         VARCHAR2(150);
   X_name_length               NUMBER(5);
   x_run_prefix                VARCHAR2(200);

   l_instrument_code           SEQUENCING_RUN.INSTRUMENT_CODE%TYPE := '454';
   l_version                   SEQUENCING_RUN.VERSION%TYPE;


   l_num_reads                 SFF_FILE.NUMBER_OF_READS%TYPE;
   l_header_length             SFF_FILE.HEADER_LENGTH%TYPE;
   l_key_length                SFF_FILE.KEY_LENGTH%TYPE;
   l_num_flows                 SFF_FILE.NUMBER_OF_FLOWS%TYPE;
   l_flowgram_code             SFF_FILE.FLOWGRAM_CODE%TYPE;
   l_flow_characters           SFF_FILE.FLOW_CHARACTERS%TYPE;
   l_key_sequence              SFF_FILE.KEY_SEQUENCE%TYPE;

   l_region                    READ_454.REGION%TYPE;
   l_X_Location                READ_454.X_LOCATION%TYPE;
   l_Y_Location                READ_454.Y_LOCATION%TYPE;
   l_num_bases                 READ_454.READ_SEQUENCE_LENGTH%TYPE;
   l_bases_string              READ_454.READ_SEQUENCE%TYPE;
   l_clip_qual_left            READ_454.CLIP_QUAL_LEFT%TYPE;
   l_clip_qual_right           READ_454.CLIP_QUAL_RIGHT%TYPE;
   l_clip_adap_left            READ_454.CLIP_ADAP_LEFT%TYPE;
   l_clip_adap_right           READ_454.CLIP_ADAP_RIGHT%TYPE;
   l_run_name                  READ_454.RUN_NAME%TYPE;
   l_run_date                  READ_454.RUN_DATE%TYPE;

   l_flowgram_string           READ_454.FLOWGRAM_STRING%TYPE;
   l_flow_index_string         READ_454.FLOW_INDEX_STRING%TYPE;

   l_min_value                 READ_454.QUAL_MIN%TYPE;
   l_max_value                 READ_454.QUAL_MAX%TYPE;
   l_avg_value                 READ_454.QUAL_MAX%TYPE;

   orig_filename               SFF_FILE.SFF_FILENAME%TYPE;
   l_filename                  VARCHAR2(50);

   XY_string_length            NUMBER(2);
   XY_Location                 VARCHAR2(30);

   time_value                  VARCHAR2(50);

   local_sqlcode               NUMBER(8);
   local_sqlerrm               VARCHAR2(1000);

BEGIN

   Flow_Lines_Processed := 0;

   Flow_Sequence_Count := 0;

   SFF_Extra_Information := NULL;


   orig_filename := Global_FILENAME;

   period_pos := INSTR(orig_filename, '.');

   num_chars_to_cut := period_pos - 1;

   l_filename := SUBSTR(orig_filename, 1, num_chars_to_cut) || '.txt';

   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - Filename to open: ' || l_filename);

   /* Open Input File */

   BEGIN

   vInHandle_FLOW := UTL_FILE.FOPEN('SFF_DEV_DIR', l_filename, 'R', 32000);

   EXCEPTION
     WHEN OTHERS THEN
       local_sqlcode := SQLCODE;
       local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: OPEN ERROR on flow.dat Input File ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       SFF_Extra_Information := '*** load_flow_file: OPEN ERROR on flow.dat Input File ***';
       severe_error_flag := 1;
       goto error_exit_flow;
   END;


   /*================== PROCESSING HEADER ==================*/

   LOOP

       BEGIN

           /* Read in next line from FLOW File Header */

          UTL_FILE.GET_LINE(vInHandle_FLOW, input_line);

          /* If input line IS NULL (GET_LINE strips off the newline character) ... ignore line */

          IF (input_line IS NULL) THEN
               goto skip_over_line;
          END IF;

       EXCEPTION
         WHEN NO_DATA_FOUND THEN
               local_sqlcode := SQLCODE;
               local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status,
               '*** load_flow_file: GET_LINE NO_DATA_FOUND on flow.dat HEADER ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       SFF_Extra_Information := '*** load_flow_file: GET_LINE NO_DATA_FOUND on flow.dat HEADER ***';
               severe_error_flag := 1;
               goto error_exit_flow;

         WHEN OTHERS THEN
               local_sqlcode := SQLCODE;
               local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: GET_LINE ERROR on flow.dat Header ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       SFF_Extra_Information := '*** load_flow_file: GET_LINE ERROR on flow.dat Header ***';
               severe_error_flag := 1;
               goto error_exit_flow;
       END;

       /* Take off Leading Blanks */

       input_line :=  LTRIM(input_line, ' ');

       /* Check for end of Header Section */

       IF (SUBSTR(input_line, 1, 1) = '>') THEN
               EXIT;
       END IF;

       /* Locate First Colon */

       colon_pos := INSTR(input_line, ':', 1, 1);

       /* Skip lines without a ':' */

       IF (colon_pos = 0) THEN
           goto skip_over_line;
       END IF;

       first_8_chars := SUBSTR(input_line, 1, 8);

   ---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** First 8 Characters: ' || '||' || first_8_chars || '||');


       /* There is no value for - 'Common Header' */

       IF (first_8_chars = 'Common H') THEN
               goto skip_over_line;
       END IF;

       /* Take off Trailing Blanks */

       input_line :=  RTRIM(input_line, ' ');

       line_length := LENGTH(input_line);

       /* Take out the Value following the colon */

       num_chars_to_cut := line_length - colon_pos;

       value := LTRIM(SUBSTR(input_line, colon_pos+1, num_chars_to_cut), ' ');

       /* Grab values based on first 8 characters in line */

       CASE (first_8_chars)

       WHEN 'Common H' THEN
               NULL;

       WHEN 'Magic Nu' THEN
               NULL;

       WHEN 'Version:' THEN
               l_version := value;

       WHEN 'Index Of' THEN
               NULL;

       WHEN 'Index Le' THEN
               NULL;

       WHEN '# of Rea' THEN
               l_num_reads := TO_NUMBER(value);

       WHEN 'Header L' THEN
               l_header_length := TO_NUMBER(value);

       WHEN 'Key Leng' THEN
               l_key_length := TO_NUMBER(value);

       WHEN '# of Flo' THEN
               l_num_flows := TO_NUMBER(value);

       WHEN 'Flowgram' THEN
               l_flowgram_code := value;

       WHEN 'Flow Cha' THEN
               l_flow_characters := value;

       WHEN 'Key Sequ' THEN
               l_key_sequence := value;

       ELSE  /* Bogus Header Statement */

         NULL;

       END CASE;

<<skip_over_line>>

       NULL;

   END LOOP;

   /* Derive Instrument Code Value - eventually will add IlluminaI and llumina Hiseq 2000 */

   CASE (l_num_flows)
     WHEN 168 THEN
       l_instrument_code := 'GS20';
     WHEN 400 THEN
       l_instrument_code := 'GS FLX';
     WHEN 800 THEN
       l_instrument_code := 'Titanium';
   ELSE
       l_instrument_code := 'Unknown';
   END CASE;

   /*---------- Insert row in SEQUENCING_RUN Table  ----------*/

   BEGIN

       UPDATE SEQUENCING_RUN
       SET INSTRUMENT_CODE = l_instrument_code, VERSION = l_version
       WHERE SEQ_RUN_ID = Global_SEQ_RUN_ID;

   EXCEPTION
       WHEN OTHERS THEN
           local_sqlcode := SQLCODE;
           local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: UPDATE Error - SEQUENCING_RUN TABLE ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       SFF_Extra_Information := '*** load_flow_file: UPDATE Error on SEQUENCING_RUN Table ***';
           severe_error_flag := 1;
           goto error_exit_flow;
   END;

   COMMIT;

   /*------------ UPDATE SFF_FILE Row ------------*/

   BEGIN

       UPDATE SFF_FILE
           SET NUMBER_OF_READS = l_num_reads,
               HEADER_LENGTH = l_header_length,
               KEY_LENGTH = l_key_length,
               NUMBER_OF_FLOWS = l_num_flows,
               FLOWGRAM_CODE = l_flowgram_code,
               FLOW_CHARACTERS = l_flow_characters,
               KEY_SEQUENCE = l_key_sequence
       WHERE SFF_FILE_ID = Global_FILE_ID;

   EXCEPTION
       WHEN OTHERS THEN
           local_sqlcode := SQLCODE;
           local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: UPDATE Error - SFF_FILE TABLE ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       SFF_Extra_Information := '*** load_flow_file: UPDATE Error on SFF_FILE Table ***';
           severe_error_flag := 1;
           goto error_exit_flow;
   END;

   COMMIT;


   /*---------- PROCESSING SEQUENCE PORTION of the FLOW file ----------*/

   LOOP

       /* Take off Leading Blanks */

       input_line :=  LTRIM(input_line, ' ');

       /* Locate 1st Colon */

       colon_pos := INSTR(input_line, ':', 1, 1);

       /* Take off Trailing Blanks */

       input_line :=  RTRIM(input_line, ' ');

       /* Take off Trailing TABs */

       input_line :=  RTRIM(input_line, CHR(9));

       /* Calculate length of Line after stripped off leading blanks and trailing "stuff" */

       line_length := LENGTH(input_line);

       /* Take out the Value following the colon */

       num_chars_to_cut := line_length - colon_pos;

       value := LTRIM(SUBSTR(input_line, colon_pos+1, num_chars_to_cut), ' ');

       /* Grab first 6 characters to drive CASE Statement */

       IF (SUBSTR(input_line, 1, 1) = '>') THEN
               first_6_chars := '>ZZZZZ';
       ELSE
               first_6_chars := SUBSTR(input_line, 1, 6);
       END IF;

       /*---------------------------------------------------------------------------------------*/

       CASE (first_6_chars)

       WHEN '>ZZZZZ' THEN

               read_identifier := SUBSTR(input_line, 2, line_length-1);


       WHEN 'Run Pr' THEN              /* Run Prefix  R_2009_07_27_13_43_24_ */

               x_run_prefix := value;

               r_year := SUBSTR(x_run_prefix, 3, 4);
               r_month := SUBSTR(x_run_prefix, 8, 2);
               r_day := SUBSTR(x_run_prefix, 11, 2);
               r_hour:= SUBSTR(x_run_prefix, 14, 2);
               r_minute := SUBSTR(x_run_prefix, 17, 2);
               r_sec := SUBSTR(x_run_prefix, 20, 2);

               r_date_string := r_year || r_month || r_day || r_hour || r_minute || r_sec;

               l_run_date :=  TO_DATE(r_date_string, 'YYYYMMDDHH24MISS');

       WHEN 'Region' THEN              /* Region Number */

               l_region := TO_NUMBER(value);

       WHEN 'XY Loc'THEN               /* XY Location */

               XY_Location := value;
               XY_string_length := LENGTH(XY_Location);
               underscore_pos := INSTR(XY_location, '_', 1, 1);

               l_X_Location := TO_NUMBER(SUBSTR(XY_Location, 1, underscore_pos-1));
               l_Y_Location := TO_NUMBER(SUBSTR(XY_Location, underscore_pos+1,
                               XY_string_length - underscore_pos));

       WHEN 'Run Na' THEN              /* Run Name */

               l_run_name := value;

       WHEN 'Analys' THEN              /* Analysis Name (NOT being saved) */

               x_run_analysis_name := NULL;

       WHEN 'Full P' THEN              /* Full Path (NOT being saved) */

               x_full_path := NULL;

       WHEN 'Read H' THEN              /* Read Header Length (not being saved) */

               x_read_header_length := -1;

       WHEN 'Name L' THEN              /* Name Length (NOT being saved) */

               x_name_length := TO_NUMBER(value);

       WHEN '# of B' THEN              /* Number of Bases */

               l_num_bases := TO_NUMBER(value);

       WHEN 'Clip Q' THEN

       /* Clip Qual Left or Clip Qual Right */

               IF (SUBSTR(input_line, 1, 11) = 'Clip Qual L') THEN
                       l_clip_qual_left := TO_NUMBER(value);
               ELSE
                       l_clip_qual_right := TO_NUMBER(value);
               END IF;

       WHEN 'Clip A' THEN              /* Clip Qual Adap Left or Clip Qual Right */

               IF (SUBSTR(input_line, 1, 11) = 'Clip Adap L') THEN
                       l_clip_adap_left := TO_NUMBER(value);
               ELSE
                       l_clip_adap_right := TO_NUMBER(value);
               END IF;

       WHEN 'Flowgr' THEN              /* Flowgram */

               l_flowgram_string := value;


       WHEN 'Flow I' THEN              /* Flow Indexes */

               l_flow_index_string := value;

       WHEN 'Bases:' THEN              /* Bases */

               curr_tab_pos := INSTR(value, CHR(9), 1);

               value_length := LENGTH(value) - 1;

               /* Size Check on 'bases' */

               IF (value_length > 2000) THEN
                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** BASES Value too long ...' ||
                               ' Length is: ' || TO_CHAR(value_length));
                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** Read ID: ' || read_identifier);
                       severe_error_flag := 1;
                       goto error_exit_flow;
               END IF;

               l_bases_string := SUBSTR(value, curr_tab_pos+1, value_length);


       WHEN 'Qualit' THEN

               l_min_value := min_value_array(Flow_Sequence_Count);
               l_max_value := max_value_array(Flow_Sequence_Count);
               l_avg_value := avg_value_array(Flow_Sequence_Count);

               BEGIN
                       INSERT INTO TEMP_READ_454(SEQ_RUN_ID, READ_ID, READ_SEQUENCE, READ_SEQUENCE_LENGTH,
                               RUN_NAME, RUN_DATE, REGION, X_Location, Y_Location,
                               FLOWGRAM_STRING, FLOW_INDEX_STRING,
                               CLIP_QUAL_LEFT, CLIP_QUAL_RIGHT, CLIP_ADAP_LEFT, CLIP_ADAP_RIGHT,
                               QUAL_MIN, QUAL_MAX, QUAL_AVG)

                       VALUES(Global_SEQ_RUN_ID, read_identifier, l_bases_string, l_num_bases,
                               l_run_name, l_run_date, l_region, l_X_Location, l_Y_Location,
                               l_flowgram_string, l_flow_index_string,
                               l_clip_qual_left, l_clip_qual_right, l_clip_adap_left, l_clip_adap_right,
                               l_min_value, l_max_value, l_avg_value);

                       Flow_Sequence_Count := Flow_Sequence_Count + 1;

               EXCEPTION
                 WHEN OTHERS THEN
                   local_sqlcode := SQLCODE;
                   local_sqlerrm := SQLERRM;
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: UPDATE Error - on READ_454 Table ***');
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
                   SFF_Extra_Information := '*** load_flow_file: UPDATE READ_454 Error - on READ_454 Table ***';
                   severe_error_flag := 1;
                   goto error_exit_flow;
               END;

      ELSE    /*** BOGUS (Undefined) LINE ****/

               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '** UNDEFINED LINE **');

      END CASE;


<<nextline>>

       Flow_Lines_Processed := Flow_Lines_Processed + 1;

       /***** Read in next line from FLOW File *****/

       BEGIN

               UTL_FILE.GET_LINE(vInHandle_FLOW, input_line);

               /* If input line IS NULL (GET_LINE strips off the newline character) ... ignore line */

               IF (input_line IS NULL) THEN
                       goto nextline;
               END IF;

       EXCEPTION
         WHEN NO_DATA_FOUND THEN
           goto finish_flow;

         WHEN OTHERS THEN
           local_sqlcode := SQLCODE;
           local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: first_6_chars: ' || first_6_chars);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** lines_processed: ' || TO_CHAR(Flow_Lines_Processed));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: read_identifier: ' || read_identifier);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: first_6_chars: ' || first_6_chars);
           SFF_Extra_Information := '*** load_flow_file: GET_LINE Error (bottom) ***';
           severe_error_flag := 1;
           goto error_exit_flow;
       END;


   END LOOP; /* Loop reading lines from file */


<<finish_flow>>

   BEGIN

       INSERT /*+ append */ INTO READ_454 (SELECT * FROM TEMP_READ_454);

   EXCEPTION
     WHEN OTHERS THEN
       local_sqlcode := SQLCODE;
       local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: INSERT (Append) Error - on READ_454 Table ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       SFF_Extra_Information := '*** load_flow_file: INSERT (Append) - on READ_454 Table ***';
       severe_error_flag := 1;
       goto error_exit_flow;
   END;

   COMMIT;


   SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
   INTO time_value
   FROM dual;

   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, 'load_flow Completion Time: ' || time_value);
   UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

<<error_exit_flow>>

   /* Close Input File */

   IF (UTL_FILE.IS_OPEN(vInHandle_FLOW)) THEN
       UTL_FILE.FCLOSE(vInHandle_FLOW);
   END IF;

EXCEPTION
 WHEN OTHERS THEN
       local_sqlcode := SQLCODE;
       local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: Exception Handler - Unexpected Error ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file - SQLERRM: ' || local_sqlerrm);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: lines_processed: ' || TO_CHAR(Flow_Lines_Processed));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: read_identifier: ' || read_identifier);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_flow_file: first_6_chars: ' || first_6_chars);
       SFF_Extra_Information := '*** load_flow_file: Exception Handler - Unexpected Error ***';
       severe_error_flag := 1;

END load_flow_file;


/*----------------------------------------------------------------------------------------------------------------*/

PROCEDURE load_qual_file IS

   vInHandle_QUAL              UTL_FILE.file_type;

   input_line                  VARCHAR2(4000);

   line_length                 NUMBER(3);

   last_entry_flag             NUMBER(1) := 0;

   read_identifier             QUAL_INDEX.READ_ID%TYPE;

   next_blank_pos              NUMBER(6);
   start_pos                   NUMBER(6);
   num_chars_to_cut            NUMBER(6);

   qual_string                 VARCHAR2(4000) := NULL;

   total_qual_value_cnt        NUMBER(12) := 0; -- counts total number of qual values in SFF file

   local_sqlcode               NUMBER(8);
   local_sqlerrm               VARCHAR2(1000);

   max_int                     NUMBER(3);
   min_int                     NUMBER(3);

   qual_value                  QUAL_INDEX.QUAL_INDEX_VALUE%TYPE;

   count_qual_vals             NUMBER(5); -- counts qual values per read_id
   sum_qual_vals               NUMBER(8);
   avg_qual_val                NUMBER(5,2);

   rows_updated                NUMBER(5);

   /* Variable for partial Bulk Inserts */

   chunk_number                NUMBER(4);
   chunk_size                  NUMBER(6) := 500000;

   first_cell                  NUMBER(10) := 1;
   last_cell                   NUMBER(10);

   max_loop_count              NUMBER(4);

   loop_counter                NUMBER(4) := 0;

   period_pos                  NUMBER(2);

   orig_filename               SFF_FILE.SFF_FILENAME%TYPE;
   l_filename                  VARCHAR2(50);

   /*----- Data Structures for BULK INSERT of the QUAL_INDEX Table -----*/

   TYPE read_id_tab        IS TABLE OF QUAL_INDEX.READ_ID%TYPE INDEX BY BINARY_INTEGER;
   TYPE qual_index_tab     IS TABLE OF QUAL_INDEX.QUAL_INDEX_VALUE%TYPE INDEX BY BINARY_INTEGER;
   TYPE position_index_tab IS TABLE OF QUAL_INDEX.POSITION%TYPE INDEX BY BINARY_INTEGER;

   read_id_array               read_id_tab;
   qual_index_array            qual_index_tab;
   position_array              position_index_tab;

   empty_read_id_array         read_id_tab;
   empty_qual_index_array      qual_index_tab;
   empty_position_array        position_index_tab;


BEGIN

   /* Initialize Global Variables */

   Qual_Lines_Processed := 0;
   Qual_Sequence_Count := 0;


   orig_filename := Global_FILENAME;

   period_pos := INSTR(orig_filename, '.');

   num_chars_to_cut := period_pos - 1;

   l_filename := SUBSTR(orig_filename, 1, num_chars_to_cut) || '.qual';

   /* Open File using Oracle Directory */

   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - Filename to open: ' || l_filename);

   vInHandle_QUAL := UTL_FILE.FOPEN('SFF_DEV_DIR',  l_filename, 'R');


   /******** FILE OPEN ERROR CODE NEEDED *********/

   LOOP

       BEGIN

         /* Read in next line from QUAL File */

       UTL_FILE.GET_LINE(vInHandle_QUAL, input_line);

       EXCEPTION
         WHEN NO_DATA_FOUND THEN
           input_line := '>';
           last_entry_flag := 1;

         WHEN OTHERS THEN
           local_sqlcode := SQLCODE;
           local_sqlerrm := SQLERRM;
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file: GET_LINE Error ***');
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLCODE: ' || local_sqlcode);
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLERRM: ' || local_sqlerrm);
           SFF_Extra_Information := '*** load_qual_file: GET_LINE Error ***';
           severe_error_flag := 1;
           goto error_exit_qual;
       END;

       line_length := LENGTH(input_line);


       /* Find beginning of next Sequence "chunk" in the QUAL file */

       IF (SUBSTR(input_line, 1, 1) = '>') THEN

           IF (Qual_Lines_Processed > 0) THEN

               BEGIN

                   /* Set initial MAX and MIN values */

                   min_int := 41;
                   max_int := -1;

                   /* Initialize count and sum of QUAL Values (per sequence) */

                   count_qual_vals := 0;
                   sum_qual_vals := 0;

                   start_pos := 1;

                       qual_string := LTRIM(qual_string, ' '); /* Strip off leading blanks */

                       /* Process QUAL Scores */

                       LOOP
                               next_blank_pos := INSTR(qual_string, ' ', start_pos);

                               /* Look for End-of-Line */

                               IF (next_blank_pos = 0) THEN
                                   num_chars_to_cut := LENGTH(qual_string) - start_pos + 1;
                               ELSE
                                   num_chars_to_cut := next_blank_pos - start_pos;
                               END IF;

                               /* Pull out current QUAL Value (integer) */

                               qual_value := TO_NUMBER(SUBSTR(qual_string, start_pos, num_chars_to_cut));

                               total_qual_value_cnt := total_qual_value_cnt + 1;

                               ---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** Qual Value: ' || qual_value);

                               /* Range Check on Quality Value */

                               IF (qual_value > 40) THEN
                                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** BAD Qual Value: ' || qual_value);
                                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** Read ID: ' || read_identifier);
                                       severe_error_flag := 1;
                                       goto error_exit_qual;
                               END IF;

                               /* Range Check on Quantity of QUAL Values */

                               IF (count_qual_vals > 1200) THEN
                                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** WARNING: LARGE Position Value: ');
                                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** ' || TO_CHAR(count_qual_vals));
                                       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** Read ID: ' || read_identifier);
                                       severe_error_flag := 1;
                                       goto error_exit_qual;
                               END IF;

                               /* Populating Arrays for BULK INSERT into the QUAL_INDEX Table */

                               BEGIN
                                       read_id_array(total_qual_value_cnt) := read_identifier;
                                       qual_index_array(total_qual_value_cnt) := qual_value;
                                       position_array(total_qual_value_cnt) := count_qual_vals;

                               EXCEPTION
                                 WHEN OTHERS THEN
                                   local_sqlcode := SQLCODE;
                                   local_sqlerrm := SQLERRM;
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string: INSERT ARRAY Populating Error ***');
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLERRM: ' || local_sqlerrm);
               UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** Current Read Identifier: ' || read_identifier);
               SFF_Extra_Information := '*** process_qual_string: INSERT Array Populating Error ***';
                                   severe_error_flag := 1;
                                   goto error_exit_qual;
                               END;

                               IF (MOD(total_qual_value_cnt, chunk_size) = 0) THEN

                                       chunk_number := (total_qual_value_cnt / chunk_size);

                                       first_cell := ((chunk_number - 1) * chunk_size) + 1;
                                       last_cell := total_qual_value_cnt;

               ---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '-------------------------------------------');
               ---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string - chunk_number: ' || TO_CHAR(chunk_number));
               ---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string - first_cell: ' || TO_CHAR(first_cell));
                  UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string - last_cell: ' || TO_CHAR(last_cell));
                  UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

                                       FORALL indx in first_cell..total_qual_value_cnt
                                       INSERT INTO QUAL_INDEX(SEQ_RUN_ID, READ_ID, POSITION, QUAL_INDEX_VALUE)
                                       VALUES(Global_SEQ_RUN_ID, read_id_array(indx),
                                               position_array(indx), qual_index_array(indx));

                                       COMMIT;

                                       /* Clear ARRAYS by "assigning" new value of an empty table ... */
                                       /* frees up PGA (process memory) */

                                       read_id_array := empty_read_id_array;
                                       position_array := empty_position_array;
                                       qual_index_array :=  empty_qual_index_array;

                                       DBMS_SESSION.FREE_UNUSED_USER_MEMORY;
                               END IF;

                               /*------------ Calculate Values for the SEQUENCE Table  ------------*/

                               count_qual_vals := count_qual_vals + 1;

                               sum_qual_vals := sum_qual_vals + qual_value;

                               IF (qual_value > max_int) THEN
                                       max_int := qual_value;
                               END IF;

                               IF (qual_value < min_int) THEN
                                       min_int := qual_value;
                               END IF;

                               IF (next_blank_pos = 0) THEN
                                       EXIT;
                               END IF;

                               start_pos := next_blank_pos + 1;

                       END LOOP;

               /* Compute AVG QUAL Value */

               avg_qual_val := sum_qual_vals / count_qual_vals;

               /* Populating Arrays MIN/MAX/AVG Qual Score */

               BEGIN
                   min_value_array(Qual_Sequence_Count) := min_int;
                   max_value_array(Qual_Sequence_Count) := max_int;
                   avg_value_array(Qual_Sequence_Count) := avg_qual_val;

               EXCEPTION
                 WHEN OTHERS THEN
                   local_sqlcode := SQLCODE;
                   local_sqlerrm := SQLERRM;
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string: Array Populating Error ***');
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLERRM: ' || local_sqlerrm);
       UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** Current Read Identifier: ' || read_identifier);
       SFF_Extra_Information := '*** process_qual_string: Array Populating Error ***';
                   severe_error_flag := 1;
                   goto error_exit_qual;
               END;

               /* Clear qual_string, increment sequence count */

               qual_string := NULL;

               Qual_Sequence_Count := Qual_Sequence_Count + 1;

               END;

            END IF; /* for lines_processed > 0 */


            /*---- If NO MORE DATA ... Quit ----*/

            IF (last_entry_flag = 1) THEN
               goto partial_bulk_insert_qual;
            END IF;

            /* Pull out Read ID Value */

            start_pos := 2;

            next_blank_pos := INSTR(input_line, ' ', start_pos);

            num_chars_to_cut := next_blank_pos - start_pos;

            read_identifier := SUBSTR(input_line, start_pos, num_chars_to_cut);

          ELSE /* Line not beginning with a '>' */

            /* Add blank space at end of intermediate input lines */

            qual_string := qual_string || ' ' || input_line;

          END IF;

          Qual_Lines_Processed := Qual_Lines_Processed + 1;

 END LOOP; /* Loop reading lines from file */

/*-----------------------------------------------------------------------------------------------------*/

<<partial_bulk_insert_qual>>


     /* Performing Final PARTIAL BULK INSERT into the QUAL_INDEX Table */

     BEGIN
       chunk_number := (total_qual_value_cnt / chunk_size) + 1;

       first_cell := ( (chunk_number - 1) * chunk_size) + 1;
       last_cell := total_qual_value_cnt;

---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '-----------------------------------------------');
---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** FINAL CHUNK - chunk_number: ' || TO_CHAR(chunk_number));
---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string - first_cell: ' || TO_CHAR(first_cell));
---UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** process_qual_string - last_cell: ' || TO_CHAR(last_cell));
---UTL_FILE.FFLUSH(vOutHandle_SFF_Status);

       FORALL indx in first_cell..last_cell
          INSERT INTO QUAL_INDEX(SEQ_RUN_ID, READ_ID, POSITION, QUAL_INDEX_VALUE)
          VALUES(Global_SEQ_RUN_ID, read_id_array(indx), position_array(indx), qual_index_array(indx));

       COMMIT;

     EXCEPTION
       WHEN OTHERS THEN
         local_sqlcode := SQLCODE;
         local_sqlerrm := SQLERRM;
         UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file: BULK INSERT Error - QUAL_INDEX TABLE ***');
         UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - first_cell: ' || TO_CHAR(first_cell));
         UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - last_cell: ' || TO_CHAR(last_cell));
         UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
         UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLERRM: ' || local_sqlerrm);
         SFF_Extra_Information := '*** load_flow_file: BULK INSERT Error - QUAL_INDEX TABLE ***';
         severe_error_flag := 1;
         goto error_exit_qual;
     END;

     /* Clear read_id/position/qual_index ARRAYS by "assigning" new value of an empty table ... */

     read_id_array := empty_read_id_array;
     position_array := empty_position_array;
     qual_index_array :=  empty_qual_index_array;

     DBMS_SESSION.FREE_UNUSED_USER_MEMORY;


     /********************************************************************************************/

<<error_exit_qual>>

   IF (UTL_FILE.IS_OPEN(vInHandle_QUAL)) THEN
       UTL_FILE.FCLOSE(vInHandle_QUAL);
   END IF;

EXCEPTION
 WHEN OTHERS THEN
   local_sqlcode := SQLCODE;
   local_sqlerrm := SQLERRM;
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file: Exception Handler - Unexpected Error ***');
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** load_qual_file - SQLERRM: ' || local_sqlerrm);
   UTL_FILE.PUT_LINE(vOutHandle_SFF_Status, '*** read_ID: - ' || TO_CHAR(read_identifier));
   SFF_Extra_Information := '*** load_qual_file: Exception Handler - Unexpected Error ***';
   severe_error_flag := 1;

END load_qual_file;












PROCEDURE load_gg_fasta_file(I_REFERENCE_SET_ID IN NUMBER) IS

    	vInHandle_GG_FASTA	UTL_FILE.file_type;
    	vOutHandle_GG_FASTA	UTL_FILE.file_type;
  
    	input_line			VARCHAR2(4000);
    	line_length			NUMBER(8);

    	next_blank_pos			NUMBER(5);
    	start_pos			NUMBER(5);
        
    	num_chars_to_cut		NUMBER(5);

	time_value			VARCHAR2(50);
   
    	local_sqlcode			NUMBER(8);
    	local_sqlerrm			VARCHAR2(1000);

	GG_ID_Lines_Processed		NUMBER(8) := 0;

    	GG_Fasta_Lines_Processed	NUMBER(8) := 0;

    	TYPE gg_prok_msa_id_tab 	IS TABLE OF NUMBER(8) INDEX BY BINARY_INTEGER; 

    	TYPE gg_fasta_seq_string_tab    IS TABLE OF SSU_SEQUENCE.SEQUENCE_STRING%TYPE INDEX BY BINARY_INTEGER;
    
   	TYPE gg_fasta_seq_length_tab    IS TABLE OF SSU_SEQUENCE.SEQUENCE_LENGTH%TYPE INDEX BY BINARY_INTEGER;

	TYPE ssu_sequence_tab		IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;

    	gg_prok_msa_id_array		gg_prok_msa_id_tab;	 	
    
    	gg_seq_string_array		gg_fasta_seq_string_tab;

    	gg_seq_length_array		gg_fasta_seq_length_tab;

   	ssu_sequence_array		ssu_sequence_tab;
		
 BEGIN
   
    	/* Open STATUS File using SFF_DEV directory */

    	BEGIN
    
    	vOutHandle_GG_FASTA := UTL_FILE.FOPEN('SFF_DEV_DIR', 'gg.status', 'w');

    	EXCEPTION
      	  WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		goto error_exit_gg_fasta;
    	END;

    	/* Get Process Start Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '-----------------------------------------------------------');

	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, 'Start Time - Greengenes File Load: ' || time_value);
    
	UTL_FILE.FFLUSH(vOutHandle_GG_FASTA);
    	
	/* Open INPUT File using Oracle Directory */

    	BEGIN
    
    		vInHandle_GG_FASTA := UTL_FILE.FOPEN('SFF_DEV_DIR', 'gg97.dat', 'r', 32000);

    	EXCEPTION
      	  WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file: OPEN Error on greengenes Input File ***');
  		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLERRM: ' || local_sqlerrm);	
  		goto error_exit_gg_fasta;
    	END;
  
	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** gg97.dat Input File has been opened ...');
	UTL_FILE.FFLUSH(vOutHandle_GG_FASTA); 

	/* Loop to read in lines from the greengenes fasta Input file */

    	LOOP

	    BEGIN
		 /* Read in next line from GG_FASTA File */

       		UTL_FILE.GET_LINE(vInHandle_GG_FASTA, input_line);
      
	    EXCEPTION
	      WHEN NO_DATA_FOUND THEN
	      	goto bulk_insert_gg_fasta;
	      WHEN OTHERS THEN
	       	 local_sqlcode := SQLCODE;
    	       	 local_sqlerrm := SQLERRM;
  		 UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file: GET_LINE Error ***');
       		 UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
		 UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLERRM: ' || local_sqlerrm);
	      	 goto error_exit_gg_fasta;
       	    END;
	
        	line_length := LENGTH(input_line);

		/* Find greengenes ID line */

    		IF (SUBSTR(input_line, 1, 1) = '>') THEN

			BEGIN
  	
             			/* Get Greengenes ID */

         			start_pos := 2;

	    			num_chars_to_cut := line_length - start_pos + 1;

				GG_ID_Lines_Processed := GG_ID_Lines_Processed + 1;

				gg_prok_msa_id_array(GG_ID_Lines_Processed) :=
				    TO_NUMBER(SUBSTR(input_line, start_pos, num_chars_to_cut));

				ssu_sequence_array(GG_ID_Lines_Processed) := SSU_SEQUENCE_ID_SEQ.NEXTVAL;	
	    		END;

        	ELSE /* Line not beginning with a '>' */

			BEGIN
		
				GG_Fasta_Lines_Processed := GG_Fasta_Lines_Processed + 1;

    				gg_seq_string_array(GG_Fasta_Lines_Processed) :=  input_line;
       				gg_seq_length_array(GG_Fasta_Lines_Processed) :=  LENGTH(input_line); 

         		EXCEPTION
      	    	  	  WHEN OTHERS THEN
				local_sqlcode := SQLCODE;
    				local_sqlerrm := SQLERRM;
     				UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA,  '*** load_gg_fasta_file: Sequence String Processing Error ***');
        			UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA,  '*** load_gg_fasta_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
				UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA,  '*** load_gg_fasta_file - SQLERRM: ' || local_sqlerrm);
     				goto error_exit_gg_fasta;
	  		END;

        	END IF;
   
    	END LOOP; /* Loop reading lines from file */

    
<<bulk_insert_gg_fasta>>

	/* Performing BULK INSERT of SSU_SEQUENCE table.  Note: SOURCE_TYPE_ID of 4 means REFERENCE */

 	BEGIN
		FORALL indx in ssu_sequence_array.first..ssu_sequence_array.last
	      	
		INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SOURCE_TYPE_ID, SEQUENCE_LENGTH, SEQUENCE_STRING) 
		VALUES(ssu_sequence_array(indx), 4, gg_seq_length_array(indx), gg_seq_string_array(indx)); 
			
		COMMIT;
	
    	EXCEPTION
          WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
     		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file: BULK INSERT Error - SSU_SEQUENCE Table ***');
        	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLERRM: ' || local_sqlerrm);
		goto error_exit_gg_fasta;
    	END;
   
	/*----------------------- Performing BULK INSERT of GREENGENES_REFERENCE table. ----------------------


	BEGIN
		FORALL indx in gg_seq_string_array.first..gg_seq_string_array.last
	      	
		INSERT INTO GREENGENES_REFERENCE(REFERENCE_SET_ID, PROK_MSA_ID, SSU_SEQUENCE_ID,
			TAXON_ID, CORE_SET_MEMBER, QUAL_SCORES)  
		VALUES(I_REFERENCE_SET_ID, gg_prok_msa_id_array(indx), ssu_sequence_array(indx), -1, -1, 'UNKNOWN');
						
		COMMIT;
	
    	EXCEPTION
          WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
     		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file: BULK INSERT Error - GREENGENES_REF Table ***');
        	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
		UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** load_gg_fasta_file - SQLERRM: ' || local_sqlerrm);
		goto error_exit_gg_fasta;
    	END;

       -----------------------------------------------------------------------------------------------------------*/


/*--------------------------------------------------------------------------------------------------------------------*/

UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '*** Greengenes FASTA Lines Loaded: ' || TO_CHAR(GG_Fasta_Lines_Processed));

/* Get Process End Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, 'End Time - Greengenes File Load: ' || time_value);
    
	UTL_FILE.PUT_LINE(vOutHandle_GG_FASTA, '-----------------------------------------------------------');
	UTL_FILE.FFLUSH(vOutHandle_GG_FASTA);

<<error_exit_gg_fasta>>

    IF (UTL_FILE.IS_OPEN(vInHandle_GG_FASTA)) THEN
       	UTL_FILE.FCLOSE(vInHandle_GG_FASTA);
    END IF;    
    
   	IF (UTL_FILE.IS_OPEN(vOutHandle_GG_FASTA)) THEN
       	UTL_FILE.FCLOSE(vOutHandle_GG_FASTA);
    END IF;    

EXCEPTION
  WHEN OTHERS THEN
    local_sqlcode := SQLCODE;		
    local_sqlerrm := SQLERRM;
   DBMS_OUTPUT.PUT_LINE('*** load_gg_fasta_file: Exception Handler - Unexpected Error ***');	
   DBMS_OUTPUT.PUT_LINE('*** load_gg_fasta_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
   DBMS_OUTPUT.PUT_LINE('*** load_gg_fasta_file - SQLERRM: ' || local_sqlerrm);

END load_gg_fasta_file;




/*-----------------------------------------------------------------------------------

1234567890123456789012345678901234567890123456789012

>v45D_23.1.08_1 F7EB3GO1AY2R8 orig_bc=ATGCCTGAGCAG new_bc=ATGCCTGAGCAG bc_diffs=0
CTGGGCCGTBTCTCAG .....

------------------------------------------------------------------------------------*/

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

BEGIN

	/* Open STATUS File using SFF_DEV directory */
	
	BEGIN
    
    		vOutHandle_FNA_File := UTL_FILE.FOPEN('SFF_DEV_DIR', 'fna.status', 'w');

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
    
    		vInHandle_FNA_File := UTL_FILE.FOPEN('SFF_DEV_DIR', l_FNA_Filename, 'r', 32000);

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







PROCEDURE load_Greengenes_TAXONOMY(I_G2_FILENAME IN VARCHAR2, I_HUGENHOLTZ_FILENAME IN VARCHAR2,
	I_LUDWIG_FILENAME IN VARCHAR2, I_NCBI_FILENAME IN VARCHAR2, I_PACE_FILENAME IN VARCHAR2,
	I_RDP_FILENAME IN VARCHAR2,  O_ERROR_FLAG OUT NUMBER) IS 


    	vInHandle_G2_CHIP	UTL_FILE.file_type;
	vInHandle_HUGENHOLTZ	UTL_FILE.file_type;
	vInHandle_LUDWIG	UTL_FILE.file_type;
	vInHandle_NCBI		UTL_FILE.file_type;
	vInHandle_PACE		UTL_FILE.file_type;
	vInHandle_RDP		UTL_FILE.file_type;

    	vOutHandle_TAXON	UTL_FILE.file_type;
  
    	input_line			VARCHAR2(4000);
    	line_length			NUMBER(8);

	start_pos			NUMBER(5);
    	next_blank_pos			NUMBER(5);
	next_tab_pos			NUMBER(5);
        
    	num_chars_to_cut		NUMBER(5);

	time_value			VARCHAR2(50);
   
    	local_sqlcode			NUMBER(8);
    	local_sqlerrm			VARCHAR2(1000);

	l_error_flag			NUMBER(1) := 0;

	loop_ctr			NUMBER(8) := 0;

	ID_String			OTU.OTU_ID%TYPE;

	Taxon_String			GREENGENES_TAXONOMY.G2_CHIP_TAXONOMY%TYPE;	

	input_filename_count 		NUMBER(1) := 1;	

	G2_CHIP_Lines_Processed		NUMBER(8) := 0;
	
	HUGENHOLTZ_Lines_Processed	NUMBER(8) := 0;

	LUDWIG_Lines_Processed		NUMBER(8) := 0;
	
	NCBI_Lines_Processed		NUMBER(8) := 0;

	PACE_Lines_Processed		NUMBER(8) := 0;
	
	RDP_Lines_Processed		NUMBER(8) := 0;

	
    	TYPE TAXON_ID_tab		IS TABLE OF GREENGENES_TAXONOMY.TAXON_ID%TYPE INDEX BY BINARY_INTEGER;

	TYPE G2_CHIP_TAXON_tab		IS TABLE OF GREENGENES_TAXONOMY.G2_CHIP_TAXONOMY%TYPE INDEX BY BINARY_INTEGER;

	TYPE HUGENHOLTZ_TAXON_tab	IS TABLE OF GREENGENES_TAXONOMY.HUGENHOLTZ_TAXONOMY%TYPE INDEX BY BINARY_INTEGER;	

	TYPE LUDWIG_TAXON_tab		IS TABLE OF GREENGENES_TAXONOMY.LUDWIG_TAXONOMY%TYPE INDEX BY BINARY_INTEGER;	
		
	TYPE NCBI_TAXON_tab		IS TABLE OF GREENGENES_TAXONOMY.NCBI_TAXONOMY%TYPE INDEX BY BINARY_INTEGER;	
	
	TYPE PACE_TAXON_tab		IS TABLE OF GREENGENES_TAXONOMY.PACE_TAXONOMY%TYPE INDEX BY BINARY_INTEGER;		

	TYPE RDP_TAXON_tab		IS TABLE OF GREENGENES_TAXONOMY.RDP_TAXONOMY%TYPE INDEX BY BINARY_INTEGER;		

    	
	TAXON_ID_array			TAXON_ID_tab;

	G2_CHIP_TAXON_array		G2_CHIP_TAXON_tab;	

	HUGENHOLTZ_TAXON_array		HUGENHOLTZ_TAXON_tab; 

	LUDWIG_TAXON_array		LUDWIG_TAXON_tab;

	NCBI_TAXON_array		NCBI_TAXON_tab;

	PACE_TAXON_array		PACE_TAXON_tab;

	RDP_TAXON_array			RDP_TAXON_tab;		
 
BEGIN
   
	/* Open STATUS File using SFF directory */

    	BEGIN
    
    	vOutHandle_TAXON := UTL_FILE.FOPEN('SFF_DEV_DIR', 'taxon.status', 'w');

    	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "taxon.status" file ***');
		l_error_flag := 1;
  		goto error_exit;
    	END;

	/* Get Process Start Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '---------------------------------------------------------------');
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, 'Load Greengenes Taxonomy Process Start Time: ' || time_value);
    	UTL_FILE.FFLUSH(vOutHandle_TAXON);

    	COMMIT;
    	
	/* Open File Handlers for all of the Input Files */

    	BEGIN
    
    	vInHandle_G2_CHIP := UTL_FILE.FOPEN('SFF_DEV_DIR', 'G2_Chip.dat', 'r', 32000);
    	
	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "G2_Chip.dat" file ***');
		l_error_flag := 1;
		goto error_exit;
    	END;

	BEGIN
        	vInHandle_HUGENHOLTZ := UTL_FILE.FOPEN('SFF_DEV_DIR', 'Hugenholtz.dat', 'r', 32000);
    	
	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "Hugenholtz.dat" file ***');
		l_error_flag := 1;
  		goto error_exit;
    	END;

	BEGIN
    	   	vInHandle_LUDWIG := UTL_FILE.FOPEN('SFF_DEV_DIR', 'Ludwig.dat', 'r', 32000);
    	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "Ludwig.dat" file ***');
		l_error_flag := 1;
  		goto error_exit;
    	END;

	BEGIN
       		vInHandle_NCBI := UTL_FILE.FOPEN('SFF_DEV_DIR', 'NCBI.dat', 'r', 32000);
    	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "NCBI.dat" file ***');		
		l_error_flag := 1;
  		goto error_exit;
    	END;

	BEGIN
        	vInHandle_PACE := UTL_FILE.FOPEN('SFF_DEV_DIR', 'Pace.dat', 'r', 32000);
    	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "Pace.dat" file ***');	
		l_error_flag := 1;
  		goto error_exit;
    	END;

	BEGIN
		vInHandle_RDP := UTL_FILE.FOPEN('SFF_DEV_DIR', 'RDP.dat', 'r', 32000);
    	EXCEPTION
      	  WHEN OTHERS THEN
		UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: Open Error on "RDP.dat" file ***');	
		l_error_flag := 1;
  		goto error_exit;
    	END;

	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '** All input files have been opened successfully ...');
    	UTL_FILE.FFLUSH(vOutHandle_TAXON);

        /*----------------------------------------------------------------------------------------*/

		/* 1- G2_CHIP, 2 - HUGENHOLTZ, 3 - LUDWIG, 4 - NCBI, 5 - PACE, 6 - RGP */

	input_filename_count := 1;
        
	LOOP
		/* Loop to read in lines from the TAXON Input file */

       	    LOOP

		BEGIN
  		    CASE
			WHEN input_filename_count = 1 THEN
	    			UTL_FILE.GET_LINE(vInHandle_G2_CHIP, input_line);	
							
			WHEN input_filename_count = 2 THEN
	    			UTL_FILE.GET_LINE(vInHandle_HUGENHOLTZ, input_line);

			WHEN input_filename_count = 3 THEN
				UTL_FILE.GET_LINE(vInHandle_LUDWIG, input_line);

			WHEN input_filename_count = 4 THEN
				UTL_FILE.GET_LINE(vInHandle_NCBI, input_line);

			WHEN input_filename_count = 5 THEN
				UTL_FILE.GET_LINE(vInHandle_PACE, input_line);

			WHEN input_filename_count = 6 THEN
           			UTL_FILE.GET_LINE(vInHandle_RDP, input_line);
			
			ELSE
	    			UTL_FILE.PUT_LINE(vInHandle_RDP, '*** SFF_main - FILE_NAME is in SFF_FILE Table > 2 times');
               			l_error_flag := 1;
            			goto error_exit; 
	  	    END CASE;
			 
		EXCEPTION
	            WHEN NO_DATA_FOUND THEN
	      		goto next_file;
	  	    WHEN OTHERS THEN
	       	 	local_sqlcode := SQLCODE;
    	       	 	local_sqlerrm := SQLERRM;
  			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file: GET_LINE Error ***');
       			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - SQLERRM: ' || local_sqlerrm);
			UTL_FILE.PUT_LINE(vOutHandle_TAXON, 'Input_Filename_Count: ' || TO_CHAR(input_filename_count));
			l_error_flag := 1;	      	
			goto error_exit;
            	END;


		/* Trim off leading blank spaces */

		input_line := LTRIM(input_line, ' ');

		line_length := LENGTH(input_line);

      		next_tab_pos := INSTR(input_line, CHR(9), 1, 1);

  		num_chars_to_cut := next_tab_pos - 1;

		ID_String := SUBSTR(input_line, 1, num_chars_to_cut);

		IF (input_filename_count = 1) THEN
			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** ID: ' || ID_String);
		END IF;

		num_chars_to_cut := line_length - next_tab_pos; 

		Taxon_String := SUBSTR(input_line, next_tab_pos + 1, num_chars_to_cut);

		CASE 
			WHEN (input_filename_count = 1) THEN
				TAXON_ID_array(G2_CHIP_Lines_Processed) := ID_String;
				
				G2_CHIP_TAXON_array(G2_CHIP_Lines_Processed) := Taxon_String;
				G2_CHIP_Lines_Processed	:= G2_CHIP_Lines_Processed + 1;
	    										
			WHEN (input_filename_count = 2) THEN	
				HUGENHOLTZ_TAXON_array(HUGENHOLTZ_Lines_Processed) := Taxon_String;
	    			HUGENHOLTZ_Lines_Processed := HUGENHOLTZ_Lines_Processed + 1;

			WHEN (input_filename_count = 3) THEN
				LUDWIG_TAXON_array(LUDWIG_Lines_Processed) := Taxon_String;
				LUDWIG_Lines_Processed := LUDWIG_Lines_Processed + 1;

			WHEN input_filename_count = 4 THEN
				NCBI_TAXON_array(NCBI_Lines_Processed) := Taxon_String;
				NCBI_Lines_Processed := NCBI_Lines_Processed + 1;

			WHEN input_filename_count = 5 THEN
				PACE_TAXON_array(PACE_Lines_Processed) := Taxon_String;
				PACE_Lines_Processed := PACE_Lines_Processed + 1;

			WHEN input_filename_count = 6 THEN 
				RDP_TAXON_array(RDP_Lines_Processed) := Taxon_String;	
           			RDP_Lines_Processed := RDP_Lines_Processed + 1;
			ELSE
	    			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** Invalid Input_FileName_Count: ' ||
					TO_CHAR(input_filename_count));
               			l_error_flag := 1;
            			goto error_exit; 

		END CASE;
		
	    END LOOP;

<<next_file>>

	    input_filename_count := input_filename_count + 1;

	    EXIT WHEN (input_filename_count > 6);

    END LOOP;

<<good_exit>>

	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - G2_CHIP_Lines_Processed: ' ||
		TO_CHAR(G2_CHIP_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - HUGENHOLTZ_Lines_Processed: ' ||
		TO_CHAR(HUGENHOLTZ_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - LUDWIG_Lines_Processed: ' ||
		TO_CHAR(LUDWIG_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - NCBI_Lines_Processed: ' ||
		TO_CHAR(NCBI_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - PACE_Lines_Processed: ' ||
		TO_CHAR(PACE_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** load_TAXON_file - RDP_Lines_Processed: ' ||
		TO_CHAR(RDP_Lines_Processed));

	/* Populate GREENGENES_REFERENCE Table */

	loop_ctr := 0;

	LOOP
		BEGIN
			INSERT INTO GREENGENES_TAXONOMY(TAXON_ID, G2_CHIP_TAXONOMY, HUGENHOLTZ_TAXONOMY,
				LUDWIG_TAXONOMY, NCBI_TAXONOMY,	PACE_TAXONOMY, RDP_TAXONOMY)
			VALUES(TAXON_ID_array(loop_ctr), G2_CHIP_TAXON_array(loop_ctr), HUGENHOLTZ_TAXON_array(loop_ctr),
				LUDWIG_TAXON_array(loop_ctr), NCBI_TAXON_array(loop_ctr),
				PACE_TAXON_array(loop_ctr), RDP_TAXON_array(loop_ctr));

		EXCEPTION
                  WHEN OTHERS THEN
			local_sqlcode := SQLCODE;
			local_sqlerrm := SQLERRM;
			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** INSERT Error ***');
			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** SQLERRM: ' || local_sqlerrm);
			l_error_flag := 1;
			goto error_exit; 
    	    	END;		
		
		loop_ctr := loop_ctr + 1;

		EXIT WHEN (loop_ctr >= G2_CHIP_Lines_Processed);

	END LOOP;

	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '*** INSERTED ' || TO_CHAR(loop_ctr) || ' Rows ...');
		
	/* Get Process End Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;
	
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, 'Load Greengenes Taxonomy Process End Time: ' || time_value);
	UTL_FILE.PUT_LINE(vOutHandle_TAXON, '---------------------------------------------------------------');
	UTL_FILE.FFLUSH(vOutHandle_TAXON);

    	COMMIT;

<<error_exit>>

	O_ERROR_FLAG := l_error_flag;
	
	IF (UTL_FILE.IS_OPEN(vInHandle_G2_CHIP)) THEN
       		UTL_FILE.FCLOSE(vInHandle_G2_CHIP);
    	END IF;    

	IF (UTL_FILE.IS_OPEN(vInHandle_HUGENHOLTZ)) THEN
       		UTL_FILE.FCLOSE(vInHandle_HUGENHOLTZ);
    	END IF; 

	IF (UTL_FILE.IS_OPEN(vInHandle_LUDWIG)) THEN
       		UTL_FILE.FCLOSE(vInHandle_LUDWIG);
    	END IF;  

	IF (UTL_FILE.IS_OPEN(vInHandle_NCBI)) THEN
       		UTL_FILE.FCLOSE(vInHandle_NCBI);
    	END IF;  

	IF (UTL_FILE.IS_OPEN(vInHandle_PACE)) THEN
       		UTL_FILE.FCLOSE(vInHandle_PACE);
    	END IF;  

	IF (UTL_FILE.IS_OPEN(vInHandle_RDP)) THEN
       		UTL_FILE.FCLOSE(vInHandle_RDP);
    	END IF;  

	IF (UTL_FILE.IS_OPEN(vOutHandle_TAXON)) THEN
       		UTL_FILE.FCLOSE(vOutHandle_TAXON);
    	END IF;   
 
EXCEPTION
  WHEN OTHERS THEN
    local_sqlcode := SQLCODE;		
    local_sqlerrm := SQLERRM;
    DBMS_OUTPUT.PUT_LINE('*** *** load_TAXON_file: Exception Handler - Unexpected Error ***');	
    DBMS_OUTPUT.PUT_LINE('*** *** load_TAXON_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
    DBMS_OUTPUT.PUT_LINE('*** load_TAXON_file - SQLERRM: ' || local_sqlerrm);
    O_ERROR_FLAG := 1;

END load_Greengenes_TAXONOMY;  	









PROCEDURE REGISTER_SPLIT_LIBRARY_RUN(
	I_ANALYSIS_ID IN NUMBER, I_RUN_DATE_STRING IN VARCHAR2, I_COMMAND IN VARCHAR2, 
	I_SVN_VERSION IN VARCHAR2, I_LOG_FILE IN CLOB, I_HISTOGRAM_FILE IN CLOB, 
	I_MD5_CHECKSUM IN VARCHAR2, O_SPLIT_LIBRARY_RUN_ID OUT NUMBER, O_ERROR_FLAG OUT NUMBER) IS

  	vOUTHandle_SLR_Status 	UTL_FILE.file_type;

	local_sqlcode		NUMBER(8);
	local_sqlerrm		VARCHAR2(1000);

	l_analysis_ID		ANALYSIS.ANALYSIS_ID%TYPE;

	l_log_file		SPLIT_LIBRARY_RUN.LOG_FILE%TYPE; 
	l_histogram_file	SPLIT_LIBRARY_RUN.HISTOGRAM_FILE%TYPE; 

	l_md5_Checksum		SPLIT_LIBRARY_RUN.MD5_CHECKSUM%TYPE;

	l_command		SPLIT_LIBRARY_RUN.COMMAND%TYPE;

	l_svn_version		SPLIT_LIBRARY_RUN.SVN_VERSION%TYPE;

	l_run_date		DATE;
	l_run_date_string	VARCHAR2(80);

	l_split_library_run_ID	SPLIT_LIBRARY_RUN.SPLIT_LIBRARY_RUN_ID%TYPE;

	time_value		VARCHAR2(50);

BEGIN
	O_ERROR_FLAG := 0;

    	/* Open SFF Status File */

    	BEGIN
    
    	vOutHandle_SLR_Status :=  UTL_FILE.FOPEN('SFF_DEV_DIR', 'slr.status', 'w', 32000);

    	EXCEPTION
      	  WHEN OTHERS THEN
  		DBMS_OUTPUT.PUT_LINE('*** OPEN ERROR on slr.status Output File ***');
		O_ERROR_FLAG := 1;
        	goto main_finish;
    	END;

        /* Get Process Start Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	l_run_date_string := I_RUN_DATE_STRING;

	l_run_date := TO_DATE(l_run_date_string, 'MM/DD/YYYY/HH24/MI/SS');

	UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '-----------------------------------------------------');

	UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, 'Split Library Registration Time ' || time_value);
    	UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, 'Run Date String: ' || l_run_date_string);
	UTL_FILE.FFLUSH(vOutHandle_SLR_Status);

	l_command := I_COMMAND;

	l_svn_version := I_SVN_VERSION;

	l_log_file := I_LOG_FILE;		--- CLOB
	
	l_histogram_file := I_HISTOGRAM_FILE;	--- CLOB

	l_md5_checksum :=  I_MD5_CHECKSUM;
	
		
	/*---------- Insert Row into SPLIT_LIBRARY_RUN Table  ----------*/
    
    	BEGIN	
		l_split_library_run_ID := SPLIT_LIBRARY_RUN_ID_SEQ.NEXTVAL;

	      	INSERT INTO SPLIT_LIBRARY_RUN(SPLIT_LIBRARY_RUN_ID, SPLIT_LIBRARY_RUN_DATE, COMMAND, SVN_VERSION,
			LOG_FILE, HISTOGRAM_FILE, MD5_CHECKSUM)
  		VALUES(l_split_library_run_ID, l_run_date, l_command, l_svn_version,
			l_log_file, l_histogram_file, l_md5_Checksum);
    	
		COMMIT;

	EXCEPTION
          WHEN OTHERS THEN
	    local_sqlcode := SQLCODE;
    	    local_sqlerrm := SQLERRM;
    	    UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** INSERT Error - SPLIT_LIBRARY_RUN TABLE ***');
    	    UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** SQLCODE: ' || TO_CHAR(local_sqlcode));
    	    UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** SQLERRM: ' || local_sqlerrm);
      	    O_ERROR_FLAG := 1;
	    goto main_finish;
    	END;	

	l_analysis_ID := I_ANALYSIS_ID;

	UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** INPUT Parameter - I_ANALYSIS_ID: ' || TO_CHAR(l_analysis_ID));
	UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** New Split Library Run ID: ' || TO_CHAR(l_split_library_run_ID));
	UTL_FILE.FFLUSH(vOutHandle_SLR_Status);

	/* UPDATE the Analysis Table */

	BEGIN
		UPDATE ANALYSIS
		SET SPLIT_LIBRARY_RUN_ID = l_split_library_run_ID
		WHERE ANALYSIS_ID = l_analysis_ID;
	COMMIT;
	
	EXCEPTION
          WHEN OTHERS THEN
	    local_sqlcode := SQLCODE;
    	    local_sqlerrm := SQLERRM;
    	    UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** UPDATE Error - ANALYSIS TABLE ***');
    	    UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** SQLCODE: ' || TO_CHAR(local_sqlcode));
    	    UTL_FILE.PUT_LINE(vOutHandle_SLR_Status, '*** SQLERRM: ' || local_sqlerrm);
      	    O_ERROR_FLAG := 1;
	    goto main_finish;
    	END;

	/* Return new SPLIT_LIBRARY_RUN_ID */	

	O_SPLIT_LIBRARY_RUN_ID := l_Split_Library_Run_ID;

<<main_finish>>

    	NULL;

END REGISTER_SPLIT_LIBRARY_RUN;		













PROCEDURE REGISTER_OTU_PICKING_RUN(I_RUN_ID IN NUMBER, I_OTU_RUN_SET_ID IN NUMBER, 
	I_OTU_PICKING_DATE_STRING IN VARCHAR2, I_OTU_PICKING_METHOD IN VARCHAR2, I_THRESHOLD IN NUMBER,
	I_SVN_VERSION IN VARCHAR2, I_COMMAND IN VARCHAR2, I_LOG_FILE IN CLOB, I_MD5_SUM_INPUT_FILE IN VARCHAR2, 
	ERROR_FLAG OUT NUMBER) IS
	
     	vOUTHandle_OTU_Status 	UTL_FILE.file_type;

	local_sqlcode		NUMBER(8);
	local_sqlerrm		VARCHAR2(1000);

	
	l_otu_run_date		DATE;
	l_otu_run_date_string	VARCHAR2(80);

	l_otu_picking_method 	VARCHAR2(80);

	l_OTU_picking_method_ID OTU_PICKING_RUN.OTU_PICKING_METHOD_ID%TYPE;

	l_threshold		OTU_PICKING_RUN.THRESHOLD%TYPE; 

	time_value		VARCHAR2(50);

BEGIN
	ERROR_FLAG := 0;

    	/* Open SFF Status File */

    	BEGIN
    
    	vOutHandle_OTU_Status :=  UTL_FILE.FOPEN('SFF_DEV_DIR', 'otu.status', 'w', 32000);

    	EXCEPTION
      	  WHEN OTHERS THEN
  		DBMS_OUTPUT.PUT_LINE('*** OPEN ERROR on otu.status Output File ***');
		ERROR_FLAG := 1;
        	goto main_finish;
    	END;

        /* Get Process Start Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	l_otu_run_date_string := I_OTU_PICKING_DATE_STRING;

	l_otu_run_date := TO_DATE(l_otu_run_date_string, 'MM/DD/YYYY/HH24/MI/SS');

	UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, '-----------------------------------------------------');

	UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, 'OTU Picking Run Registration Time ' || time_value);
    	UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, 'OTU Run Date String: ' || l_otu_run_date_string);
	UTL_FILE.FFLUSH(vOutHandle_OTU_Status);


	/* Validate OTU_PICKING_METHOD Input Parameter */

	l_otu_picking_method := I_OTU_PICKING_METHOD;
 
	
	/* Validate THRESHOLD Input Parameter */
			
	l_threshold := I_THRESHOLD;
 
	IF(l_threshold < 0.00 OR l_threshold > 100.00) THEN
 		UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, '*** REGISTER_OTU_PICKING_RUN: ' ||
			'Threshold Value is not in range (0.00 thru 100.00) ***');
    		ERROR_FLAG := 1;
            	goto main_finish; 
	END IF;	
	
	/*---------- Insert Row into OTU_PICKING_RUN Table  ----------*/
    
	BEGIN	
	      	INSERT INTO OTU_PICKING_RUN(RUN_ID, OTU_RUN_SET_ID, OTU_PICKING_METHOD_ID, OTU_PICKING_DATE,
			SVN_VERSION, COMMAND, LOG_FILE, THRESHOLD, MD5_SUM_INPUT_FILE)
		VALUES(I_RUN_ID, I_OTU_RUN_SET_ID, l_otu_picking_method_ID, l_otu_run_date,
			I_SVN_VERSION, I_COMMAND, I_LOG_FILE, l_threshold, I_MD5_SUM_INPUT_FILE);

	EXCEPTION
          WHEN OTHERS THEN
	    local_sqlcode := SQLCODE;
    	    local_sqlerrm := SQLERRM;
    	    UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, '*** INSERT Error - OTU_PICKING_RUN TABLE ***');
    	    UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, '*** SQLCODE: ' || TO_CHAR(local_sqlcode));
    	    UTL_FILE.PUT_LINE(vOutHandle_OTU_Status, '*** SQLERRM: ' || local_sqlerrm);
	    ERROR_FLAG := 1;
    	END;	
  
	COMMIT;

<<main_finish>>

    	NULL;

END REGISTER_OTU_PICKING_RUN;	














PROCEDURE load_otu_file(I_RUN_ID NUMBER, error_flag OUT NUMBER) IS

    	vInHandle_OTU			UTL_FILE.file_type;
    	vOutHandle_OTU			UTL_FILE.file_type;
  
    	input_line		CLOB;		--- some input lines are approximately 30,000 characters in length.
    	
	line_length			NUMBER(8);

    	next_blank_pos			NUMBER(5);

	next_tab_pos			NUMBER(5);
            
    	num_chars_to_cut		NUMBER(5);

	start_pos			NUMBER(5);

	time_value			VARCHAR2(50); 

	l_RUN_ID			NUMBER(8);
	
	l_cnt_RUN_ID			NUMBER(8);

	l_OTU_ID			NUMBER(12);

	l_SSU_Sequence_ID		NUMBER(24);
   
    	local_sqlcode			NUMBER(8);
    	local_sqlerrm			VARCHAR2(1000);

	exit_flag			NUMBER(1) := 0;

    	SEQ_Lines_Processed		NUMBER(8) := 0;

	OTU_Strings_Processed		NUMBER(8) := 0;

	OTU_String			VARCHAR2(50);

  	SEQ_String			VARCHAR2(30);
   
 BEGIN
   
    	error_flag := 0;

	l_RUN_ID := I_RUN_ID;

    	/* Open STATUS File using SFF_DIR directory */

    	BEGIN
    
    	vOutHandle_OTU := UTL_FILE.FOPEN('SFF_DEV_DIR', 'otu.status', 'w');

    	EXCEPTION
      	  WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		goto error_exit_otu;
    	END;

    	UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** Starting load_otu_file ...');
	
	/* Get Process Start Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_OTU, '-----------------------------------------------------');

	UTL_FILE.PUT_LINE(vOutHandle_OTU, 'OTU Load Process Start Time: ' || time_value);
    
	UTL_FILE.FFLUSH(vOutHandle_OTU);
    	
	
	/* Verify that OTU_PICKING_RUN_ID is Valid */

	SELECT COUNT(RUN_ID) 
	INTO l_cnt_RUN_ID
	FROM OTU_PICKING_RUN
	WHERE RUN_ID = l_RUN_ID;

	IF (l_cnt_RUN_ID = 0) THEN
		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** RUN_ID for OTU_PICKING_RUN_ID IS INVALID ***');
		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** REGISTER the OTU_PICKING_RUN ***');
		error_flag := 1;  
		goto error_exit_otu;
	END IF;

	/* Open INPUT File using Oracle Directory */

    	BEGIN
    
    	vInHandle_OTU := UTL_FILE.FOPEN('SFF_DEV_DIR', 'otu.dat', 'r', 32000);

    	EXCEPTION
      	  WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file: OPEN Error on Input File ***');
  		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLERRM: ' || local_sqlerrm);	
		error_flag := 1;
  		goto error_exit_otu;
    	END;
  

    	/* Loop to read in lines from the OTU Input file */

    	LOOP

		BEGIN

			 /* Read in next line from OTU File */
       			
			UTL_FILE.GET_LINE(vInHandle_OTU, input_line);
		
		EXCEPTION
	            WHEN NO_DATA_FOUND THEN
	      		goto good_exit;
	  	    WHEN OTHERS THEN
	       	 	local_sqlcode := SQLCODE;
    	       	 	local_sqlerrm := SQLERRM;
  			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file: GET_LINE Error ***');
       			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLERRM: ' || local_sqlerrm);
			error_flag := 1;	      	
			goto error_exit_otu;
            	END;

		/* Trim off leading blank spaces */

		input_line := LTRIM(input_line, ' ');

		line_length := LENGTH(input_line);

      		next_tab_pos := INSTR(input_line, CHR(9), 1, 1);

  		num_chars_to_cut := next_tab_pos - 1;

		SEQ_String := SUBSTR(input_line, 1, num_chars_to_cut);

		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** SEQ_String: ' || SEQ_String);
		
		SEQ_Lines_Processed := SEQ_Lines_Processed + 1;

		/* Process the OTU_String */


		BEGIN
			SELECT SSU_SEQUENCE_ID
			INTO l_SSU_Sequence_ID
			FROM READ_454
			WHERE READ_ID = SEQ_String;
		EXCEPTION
		  WHEN NO_DATA_FOUND THEN
			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** PROBLEM - SEQUENCE STRING matches 0 Rows in SSU_SEQUENCE ***');  
			error_flag := 1;
			goto get_next_line;
		  WHEN OTHERS THEN
			local_sqlcode := SQLCODE;
    			local_sqlerrm := SQLERRM;
  			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file: SELECT Error on SSU_SEQUENCE Query ***');
  			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  			UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLERRM: ' || local_sqlerrm);
			error_flag := 1;	
  			goto error_exit_otu;
      		END;

		UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** SSU_SEQUENCE_ID Value: ' || TO_CHAR(l_SSU_Sequence_ID));	
		
		/* Loop to process OTU IDs associated with the Sequence String */


		/* Skip over SEQ_String and 1st tab */

		start_pos := num_chars_to_cut + 2;

		LOOP
			/* Safety Valve */

			IF (start_pos > line_length) THEN EXIT; END IF;

			next_tab_pos := INSTR(input_line, CHR(9), start_pos + 1);

			/* If no more TAB chars, then process last SEQ_String and exit loop */

			IF (next_tab_pos = 0) THEN 

				num_chars_to_cut := line_length - start_pos + 1;

				OTU_String := SUBSTR(input_line, start_pos, num_chars_to_cut);

				OTU_Strings_Processed := OTU_Strings_Processed + 1;
				
				---UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** OTU_String: ' || '|' || OTU_String || '|');
				
				exit_flag := 1;

			ELSE
				num_chars_to_cut := next_tab_pos - start_pos;

				OTU_String := SUBSTR(input_line, start_pos, num_chars_to_cut);

				OTU_Strings_Processed := OTU_Strings_Processed + 1;

				---UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** OTU_String: ' || '|' || OTU_String || '|');
				
				start_pos := next_tab_pos + 1;

			END IF;
		
			/*--- INSERT a Row the OTU Table ---*/


			l_OTU_ID := OTU_ID_SEQ.NEXTVAL;

			/*  Must fetch TAXON_ID from GREENGENES_REFERENCE
			--- Must fetch TAXON_ID from GREENGENES_REFERENCE 

			SELECT TAXON_ID
			FROM GREENGENES_REFERENCE
			WHERE PROK_MSA_ID = SEQ_String;

			--- Must fetch TAXON_ID from GREENGENES_REFERENCE 
			--- Must fetch TAXON_ID from GREENGENES_REFERENCE */
			
			BEGIN
				INSERT INTO OTU(OTU_ID, TAXON_ID)
				VALUES(l_OTU_ID, -1);
			EXCEPTION
		 	  WHEN OTHERS THEN
				local_sqlcode := SQLCODE;
    				local_sqlerrm := SQLERRM;
  				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file: INSERT Error on OTU Table ***');
  				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLERRM: ' || local_sqlerrm);
				error_flag := 1;	
  				goto error_exit_otu;
      			END;

			/*--- INSERT a Row the OTU_MAP Table ---*/
			
			BEGIN
	
				INSERT INTO OTU_MAP(OTU_ID, RUN_ID, SSU_SEQUENCE_ID)
				VALUES(l_OTU_ID, l_RUN_ID, l_SSU_Sequence_ID);

			EXCEPTION
		 	  WHEN OTHERS THEN
				local_sqlcode := SQLCODE;
    				local_sqlerrm := SQLERRM;
  				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file: INSERT Error on OTU_MAP Table ***');
  				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
  				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_otu_file - SQLERRM: ' || local_sqlerrm);
				error_flag := 1;	
  				goto error_exit_otu;
      			END;
			
			IF (exit_flag = 1) THEN 
				exit_flag := 0;
				EXIT;
			END IF;
			
			IF(MOD(SEQ_Lines_Processed, 100) = 0) THEN
				UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_OTU_file - SEQ_Lines_Processed: ' || 
					TO_CHAR(SEQ_Lines_Processed));
				UTL_FILE.FFLUSH(vOutHandle_OTU);
			END IF;
			
		END LOOP;

<<get_next_line>>

		NULL;	
	
    	END LOOP; /* Loop reading lines from file */

/*---------------------------------------------------------------------------------------*/

<<good_exit>>

	UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_OTU_file - SEQ_Lines_Processed: ' || TO_CHAR(SEQ_Lines_Processed));
	UTL_FILE.PUT_LINE(vOutHandle_OTU, '*** load_OTU_file - OTU_Strings_Processed: ' || TO_CHAR(OTU_Strings_Processed));
	
	/* Get Process End Time */

	SELECT TO_CHAR(SYSDATE, 'MON DD, YYYY - HH24:MI:SS')
	INTO time_value
	FROM dual;

	UTL_FILE.PUT_LINE(vOutHandle_OTU, 'OTU Load Process End Time: ' || time_value);
    	UTL_FILE.PUT_LINE(vOutHandle_OTU, '-----------------------------------------------------');
	UTL_FILE.FFLUSH(vOutHandle_OTU);

    	COMMIT;

<<error_exit_otu>>

    	IF (UTL_FILE.IS_OPEN(vInHandle_OTU)) THEN
       		UTL_FILE.FCLOSE(vInHandle_OTU);
    	END IF;    
    
   	IF (UTL_FILE.IS_OPEN(vOutHandle_OTU)) THEN
       		UTL_FILE.FCLOSE(vOutHandle_OTU);
    	END IF;    

EXCEPTION
  WHEN OTHERS THEN
    local_sqlcode := SQLCODE;		
    local_sqlerrm := SQLERRM;
    DBMS_OUTPUT.PUT_LINE('*** load_otu_file: Exception Handler - Unexpected Error ***');	
    DBMS_OUTPUT.PUT_LINE('*** load_otu_file - SQLCODE: ' || TO_CHAR(local_sqlcode));
    DBMS_OUTPUT.PUT_LINE('*** load_otu_file - SQLERRM: ' || local_sqlerrm);
    error_flag := 1;

END load_otu_file;











-- probably deprecated
/*-------------------------------------------------------------------------------

FASTA Record Format

>FZTHQMS01B8T1H length=284 xy=0803_2435 region=1 run=R_2009_07_27_13_43_24_
                           --------------------------------------------------
			   Optional Comments, values gotten from mapping file.


 -------------------------------------------------------------------------------*/
/*
PROCEDURE load_clipped_sequences(I_run_ID IN NUMBER, O_ERROR_FLAG OUT NUMBER) IS 

    vInHandle_FASTA 	UTL_FILE.file_type;
    vOutHandle_Status	UTL_FILE.file_type;
  
    input_line			VARCHAR2(4000);
    
    length_info			VARCHAR2(20);
          
    equal_pos			NUMBER(5);
    next_blank_pos		NUMBER(5);
    start_pos			NUMBER(5);
        
    num_chars_to_cut		NUMBER(5);

    line_length			NUMBER(8);
   
    clipped_seq_length		VARCHAR2(8);
    clipped_seq_string		VARCHAR2(4000):= NULL;

    local_sqlcode		NUMBER(8);
    local_sqlerrm		VARCHAR2(1000);

    l_error_flag		NUMBER(1) := 0;

    Clipped_Sequence_Count 	NUMBER(12) := 0;

    TYPE read_id_tab 		IS TABLE OF READ_454.READ_ID%TYPE INDEX BY BINARY_INTEGER;
	
    read_id_array		read_id_tab;

    
    TYPE clipped_seq_string_tab	IS TABLE OF READ_454.CLIPPED_SEQ_STRING%TYPE INDEX BY BINARY_INTEGER;
   
    TYPE clipped_seq_length_tab	IS TABLE OF READ_454.CLIPPED_SEQ_LENGTH%TYPE INDEX BY BINARY_INTEGER;
   
    clipped_seq_string_array	clipped_seq_string_tab;

    clipped_seq_length_array	clipped_seq_length_tab;

 
BEGIN

    	-- Open Input File using Oracle Directory

    	BEGIN
    
    	vInHandle_FASTA := UTL_FILE.FOPEN('SFF_DEV_DIR', 'clipped.dat', 'R');

    	EXCEPTION
          WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences: OPEN Error on clipped.dat Input File ***');
  		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLCODE: ' || TO_CHAR(local_sqlcode));
  		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLERRM: ' || local_sqlerrm);	
 		l_error_flag := 1;
        	goto error_exit;
    	END;
	
	  -- Open Output File using Oracle Directory

    	BEGIN
    
    	vOutHandle_Status := UTL_FILE.FOPEN('SFF_DEV_DIR', 'clipped.status', 'R');

    	EXCEPTION
          WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
  		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences: OPEN Error on clipped.status Output File ***');
  		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLCODE: ' || TO_CHAR(local_sqlcode));
  		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLERRM: ' || local_sqlerrm);	
 		l_error_flag := 1;
        	goto error_exit;
    	END;
    
	-- Loop to read in lines from the clipped.dat file

    	LOOP

		BEGIN

	  	-- Read in next line from FASTA (clipped sequence) File

        	UTL_FILE.GET_LINE(vInHandle_FASTA, input_line);
      
		EXCEPTION
	  	  WHEN NO_DATA_FOUND THEN
	      		goto bulk_update;
	  	  WHEN OTHERS THEN
	        	local_sqlcode := SQLCODE;
    			local_sqlerrm := SQLERRM;
  			UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences: GET_LINE Error ***');
        		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLERRM: ' || local_sqlerrm);
	       		l_error_flag := 1;
              		goto error_exit;
        	END;
	
        	line_length := LENGTH(input_line);

		-- Find beginning of next Sequence Data "chunk" in the FASTA file

    		IF (SUBSTR(input_line, 1, 1) = '>') THEN

	      		Clipped_Sequence_Count := Clipped_Sequence_Count + 1;

	      		BEGIN

				clipped_seq_string := NULL;

	        		-- Find 1st Value (Read ID)

                		start_pos := 2;

	    			next_blank_pos := INSTR(input_line, ' ', start_pos);

                		num_chars_to_cut := next_blank_pos - start_pos;

				read_id_array(Clipped_Sequence_Count) := SUBSTR(input_line, start_pos, num_chars_to_cut);

      				-- Find length info

				start_pos := next_blank_pos + 1;

            			next_blank_pos := INSTR(input_line, ' ', start_pos);
		
				num_chars_to_cut := next_blank_pos - start_pos;

	      			length_info := SUBSTR(input_line, start_pos, num_chars_to_cut);

				equal_pos := INSTR(length_info, '=', 1);

				clipped_seq_length := SUBSTR(length_info, equal_pos+1, LENGTH(length_info) - equal_pos);

				clipped_seq_length_array(Clipped_Sequence_Count) := TO_NUMBER(clipped_seq_length);
	
    	  		END;

        	ELSE -- Line not beginning with a '>'

          		BEGIN  -- Concatenate input_line to existing sequence string

				clipped_seq_string := clipped_seq_string || input_line;

    				clipped_seq_string_array(Clipped_Sequence_Count) :=  clipped_seq_string;
        				
          		EXCEPTION
      	    		  WHEN OTHERS THEN
				local_sqlcode := SQLCODE;
    				local_sqlerrm := SQLERRM;
     			UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences: Sequence String Concatenation Error ***');
        		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLCODE: ' || TO_CHAR(local_sqlcode));
			UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLERRM: ' || local_sqlerrm);
     				l_error_flag := 1;
				goto error_exit;
	  		END;

        	END IF;
   
        END LOOP; -- Loop reading lines from file

    
<<bulk_update>>
*/

    /* Performing BULK UPDATE of the READ_454 table 

    	BEGIN
		FORALL indx in read_id_array.first..read_id_array.last

			UPDATE READ_454 
			    SET RUN_ID = I_run_ID,
			 	READ_ID = read_id_array(indx),
				CLIPPED_SEQ_STRING = clipped_seq_string_array(indx),
				CLIPPED_SEQ_LENGTH = clipped_seq_length_array(indx));
	      		
	      	COMMIT;
	
    	EXCEPTION
      	  WHEN OTHERS THEN
		local_sqlcode := SQLCODE;
    		local_sqlerrm := SQLERRM;
     		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences: BULK UPDATE Error - SEQUENCE Table ***');
        	UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLCODE: ' || TO_CHAR(local_sqlcode));
		UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLERRM: ' || local_sqlerrm);
     		l_error_flag := 1;
		goto error_exit;
    	END;
   
---------------------------------------------------------------------------------------*/

/*
    	-- Clear User Process Memory

    	DBMS_SESSION.FREE_UNUSED_USER_MEMORY;  

	UTL_FILE.PUT_LINE(vOutHandle_Status, '*** UPDATED READ_454 CLIPPED_SEQ_STRING: ' || 
		TO_CHAR(Clipped_Sequence_Count) || ' Sequences');

<<error_exit>>

	O_ERROR_FLAG := l_error_flag;

    	IF (UTL_FILE.IS_OPEN(vInHandle_FASTA)) THEN
       		UTL_FILE.FCLOSE(vInHandle_FASTA);
    	END IF;  

	IF (UTL_FILE.IS_OPEN(vOutHandle_Status)) THEN
       		UTL_FILE.FCLOSE(vOutHandle_Status);
    	END IF;    
       
EXCEPTION
  WHEN OTHERS THEN
    local_sqlcode := SQLCODE;		
    local_sqlerrm := SQLERRM;
    UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences: Exception Handler - Unexpected Error ***');	
    UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLCODE: ' || TO_CHAR(local_sqlcode));
    UTL_FILE.PUT_LINE(vOutHandle_Status, '*** load_clipped_sequences - SQLERRM: ' || local_sqlerrm);
    O_ERROR_FLAG := 1;
  
END load_clipped_sequences;
*/
















END;  /* End of PACKAGE BODY */