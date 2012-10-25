
CREATE OR REPLACE PACKAGE Process_SFF_Files AS 


/*------------------------------------------------------------------

Directories are owned by: oracle/oinstall

Directory for Input Files: /SFF_Files

Default Input File for fasta is: fasta.dat

Default Statuts File for Process_SFF_Files is: sff.status 

-------------------------------------------------------------------*/

/*--- GLOBAL Variables ---*/

TYPE min_value_tab IS TABLE OF READ_454.QUAL_MIN%TYPE INDEX BY BINARY_INTEGER;
TYPE max_value_tab IS TABLE OF READ_454.QUAL_MAX%TYPE INDEX BY BINARY_INTEGER;
TYPE avg_value_tab IS TABLE OF READ_454.QUAL_AVG%TYPE INDEX BY BINARY_INTEGER;

min_value_array		min_value_tab;
max_value_array		max_value_tab;
avg_value_array		avg_value_tab;

empty_min_value_array	min_value_tab;
empty_max_value_array	max_value_tab;
empty_avg_value_array	avg_value_tab;
  
vOutHandle_SFF_Status	UTL_FILE.file_type;

SFF_Extra_Information	VARCHAR2(500);

Flow_Lines_Processed	NUMBER(12);
Flow_Sequence_Count	NUMBER(12);

Qual_Lines_Processed	NUMBER(12);
Qual_Sequence_Count	NUMBER(12);

severe_error_flag	NUMBER(1);

Global_ANALYSIS_ID	ANALYSIS.ANALYSIS_ID%TYPE; 
Global_FILE_ID		SFF_FILE.SFF_FILE_ID%TYPE;
Global_SEQ_RUN_ID	READ_454.SEQ_RUN_ID%TYPE;

PROCEDURE SFF_main(I_File_Name IN VARCHAR2, I_MD5_CHECKSUM IN VARCHAR2, P_SEQ_RUN_ID IN OUT NUMBER, 
			P_ANALYSIS_ID IN OUT NUMBER, I_ANALYSIS_NOTES IN VARCHAR2, error_flag OUT NUMBER); 

PROCEDURE load_flow_file; 

PROCEDURE load_qual_file;

PROCEDURE load_gg_fasta_file(I_REFERENCE_SET_ID IN NUMBER);

PROCEDURE load_fna_file(I_FNA_FILE_NAME IN VARCHAR2, I_SEQ_RUN_ID IN NUMBER,
		 O_Error_Flag OUT NUMBER, O_Warning_Flag OUT NUMBER);

PROCEDURE load_Greengenes_TAXONOMY(I_G2_FILENAME IN VARCHAR2, I_HUGENHOLTZ_FILENAME IN VARCHAR2,
	I_LUDWIG_FILENAME IN VARCHAR2, I_NCBI_FILENAME IN VARCHAR2, I_PACE_FILENAME IN VARCHAR2,
	I_RDP_FILENAME IN VARCHAR2,  O_ERROR_FLAG OUT NUMBER);

PROCEDURE REGISTER_SPLIT_LIBRARY_RUN(
	I_ANALYSIS_ID IN NUMBER, I_RUN_DATE_STRING IN VARCHAR2, I_COMMAND IN VARCHAR2, 
	I_SVN_VERSION IN VARCHAR2, I_LOG_FILE IN CLOB, I_HISTOGRAM_FILE IN CLOB, 
	I_MD5_CHECKSUM IN VARCHAR2, O_SPLIT_LIBRARY_RUN_ID OUT NUMBER, O_ERROR_FLAG OUT NUMBER);

PROCEDURE REGISTER_OTU_PICKING_RUN(I_RUN_ID IN NUMBER, I_OTU_RUN_SET_ID IN NUMBER, 
	I_OTU_PICKING_DATE_STRING IN VARCHAR2, I_OTU_PICKING_METHOD IN VARCHAR2, I_THRESHOLD IN NUMBER,
	I_SVN_VERSION IN VARCHAR2, I_COMMAND IN VARCHAR2, I_LOG_FILE IN CLOB, I_MD5_SUM_INPUT_FILE IN VARCHAR2, 
	ERROR_FLAG OUT NUMBER);
  
PROCEDURE load_otu_file(I_RUN_ID NUMBER, error_flag OUT NUMBER);

PROCEDURE load_clipped_sequences(I_run_ID IN NUMBER, O_ERROR_FLAG OUT NUMBER);


END Process_SFF_Files;
