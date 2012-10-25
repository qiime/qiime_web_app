CREATE OR REPLACE PACKAGE "LOAD_FLOW_DATA" as 

/* 
This package takes the processed flow file and imports the data into
the READ_454 table.
*/

  -- Declare all the array tables that are input to the package.
  TYPE seq_run_id_array_tab                 IS TABLE OF 
              READ_454.SEQ_RUN_ID%TYPE INDEX BY PLS_INTEGER;
  TYPE read_id_array_tab                    IS TABLE OF 
              READ_454.READ_ID%TYPE INDEX BY PLS_INTEGER;
  TYPE read_sequence_array_tab              IS TABLE OF 
              READ_454.READ_SEQUENCE%TYPE INDEX BY PLS_INTEGER;
  TYPE read_sequence_length_array_tab       IS TABLE OF 
              READ_454.READ_SEQUENCE_LENGTH%TYPE INDEX BY PLS_INTEGER;
  TYPE run_name_array_tab                   IS TABLE OF 
              READ_454.RUN_NAME%TYPE INDEX BY PLS_INTEGER;
  TYPE run_date_array_tab                   IS TABLE OF 
              READ_454.RUN_DATE%TYPE INDEX BY PLS_INTEGER;              
  TYPE region_array_tab                     IS TABLE OF 
              READ_454.REGION%TYPE INDEX BY PLS_INTEGER;
  TYPE x_location_array_tab                 IS TABLE OF 
              READ_454.X_LOCATION%TYPE INDEX BY PLS_INTEGER;              
  TYPE y_location_array_tab                 IS TABLE OF 
              READ_454.Y_LOCATION%TYPE INDEX BY PLS_INTEGER;
  TYPE flowgram_string_idx_array_tab        IS TABLE OF 
              NUMBER INDEX BY PLS_INTEGER;
  TYPE flow_index_str_idx_array_tab         IS TABLE OF 
              NUMBER INDEX BY PLS_INTEGER;
  TYPE clip_qual_left_array_tab             IS TABLE OF 
              READ_454.CLIP_QUAL_LEFT%TYPE INDEX BY PLS_INTEGER;            
  TYPE clip_qual_right_array_tab            IS TABLE OF 
              READ_454.CLIP_QUAL_RIGHT%TYPE INDEX BY PLS_INTEGER;                
  TYPE clip_adap_left_array_tab             IS TABLE OF 
              READ_454.CLIP_ADAP_LEFT%TYPE INDEX BY PLS_INTEGER;  
  TYPE clip_adap_right_array_tab            IS TABLE OF 
              READ_454.CLIP_ADAP_RIGHT%TYPE INDEX BY PLS_INTEGER;  
  TYPE qual_min_array_tab                   IS TABLE OF 
              READ_454.QUAL_MIN%TYPE INDEX BY PLS_INTEGER;                
  TYPE qual_max_array_tab                   IS TABLE OF 
              READ_454.QUAL_MAX%TYPE INDEX BY PLS_INTEGER;
  TYPE qual_avg_array_tab                   IS TABLE OF 
              READ_454.QUAL_AVG%TYPE INDEX BY PLS_INTEGER;
  TYPE qual_string_idx_array_tab            IS TABLE OF 
              NUMBER INDEX BY PLS_INTEGER;              
              
  -- Define the procedure call for the package. The actual workload for this
  -- package is located in the body section.
  procedure array_insert (seq_run_id_array in seq_run_id_array_tab,
                          read_id_array in read_id_array_tab,
                          read_sequence_array in read_sequence_array_tab,
                          read_sequence_length_array in read_sequence_length_array_tab,
                          run_name_array in run_name_array_tab,
                          run_date_array in run_date_array_tab,
                          region_array in region_array_tab,
                          x_location_array in x_location_array_tab,
                          y_location_array in y_location_array_tab,
                          flowgram_string in CLOB,
                          flowgram_string_idx_array in flowgram_string_idx_array_tab,
                          flow_index_string in CLOB,
                          flow_index_string_idx_array in flow_index_str_idx_array_tab,
                          clip_qual_left_array in clip_qual_left_array_tab,
                          clip_qual_right_array in clip_qual_right_array_tab,
                          clip_adap_left_array in clip_adap_left_array_tab,
                          clip_adap_right_array in clip_adap_right_array_tab,
                          qual_min_array in qual_min_array_tab,
                          qual_max_array in qual_max_array_tab,
                          qual_avg_array in qual_avg_array_tab,
                          qual_string in CLOB,
                          qual_string_idx_array in qual_string_idx_array_tab);

end load_flow_data;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_FLOW_DATA" as

  /* Define the input fields to stored procedure. */
  procedure array_insert (
    seq_run_id_array in seq_run_id_array_tab,
    read_id_array in read_id_array_tab,
    read_sequence_array in read_sequence_array_tab,
    read_sequence_length_array in read_sequence_length_array_tab,
    run_name_array in run_name_array_tab,
    run_date_array in run_date_array_tab,
    region_array in region_array_tab,
    x_location_array in x_location_array_tab,
    y_location_array in y_location_array_tab,
    flowgram_string in CLOB,
    flowgram_string_idx_array in flowgram_string_idx_array_tab,
    flow_index_string in CLOB,
    flow_index_string_idx_array in flow_index_str_idx_array_tab,
    clip_qual_left_array in clip_qual_left_array_tab,
    clip_qual_right_array in clip_qual_right_array_tab,
    clip_adap_left_array in clip_adap_left_array_tab,
    clip_adap_right_array in clip_adap_right_array_tab,
    qual_min_array in qual_min_array_tab,
    qual_max_array in qual_max_array_tab,
    qual_avg_array in qual_avg_array_tab,
    qual_string in CLOB,
    qual_string_idx_array in qual_string_idx_array_tab
  ) is

  -- Declare clob arrays that will be populated, since an array of clobs
  -- cannot be passed to a stored procedure.
  TYPE flowgram_string_clob_array_tab              IS TABLE OF 
              READ_454.FLOWGRAM_STRING%TYPE INDEX BY PLS_INTEGER; 
  TYPE flow_index_str_clob_array_tab              IS TABLE OF 
              READ_454.FLOW_INDEX_STRING%TYPE INDEX BY PLS_INTEGER;
  TYPE qual_string_clob_array_tab              IS TABLE OF 
              READ_454.QUAL_STRING%TYPE INDEX BY PLS_INTEGER;              
flowgram_string_clob_array  flowgram_string_clob_array_tab;
flow_index_str_clob_array  flow_index_str_clob_array_tab;
qual_string_clob_array  qual_string_clob_array_tab;

fsc_pos NUMBER;
fsc_last_pos NUMBER;
fisc_pos NUMBER;
fisc_last_pos NUMBER;
qsc_pos NUMBER;
qsc_last_pos NUMBER;
  
  begin
    
    fsc_pos := 0;
    fsc_last_pos:=1;
    fisc_pos := 0;
    fisc_last_pos:=1;
    qsc_pos := 0;
    qsc_last_pos:=1;
    
    -- Loop through one of the input arrays to populate the clob arrays.  The 
    -- input clob is one string that is split and appended to the clob arrays.
    FOR idx in seq_run_id_array.first..seq_run_id_array.last
    LOOP
    fsc_pos := flowgram_string_idx_array(idx);
    flowgram_string_clob_array(idx):=SUBSTR(flowgram_string,fsc_last_pos, fsc_pos-fsc_last_pos);
    fsc_last_pos:=fsc_pos+1;
    
    fisc_pos := flow_index_string_idx_array(idx);
    flow_index_str_clob_array(idx):=SUBSTR(flow_index_string,fisc_last_pos, fisc_pos-fisc_last_pos);
    fisc_last_pos:=fisc_pos+1;
    
    qsc_pos := qual_string_idx_array(idx);
    qual_string_clob_array(idx):=SUBSTR(qual_string,qsc_last_pos, qsc_pos-qsc_last_pos);
    qsc_last_pos:=qsc_pos+1;

    -- Insert the flow file data into the READ_454 table.
    INSERT INTO READ_454(SEQ_RUN_ID,READ_ID,READ_SEQUENCE,READ_SEQUENCE_LENGTH,
                         RUN_NAME,RUN_DATE,REGION,X_LOCATION,Y_LOCATION,
                         FLOWGRAM_STRING,FLOW_INDEX_STRING,CLIP_QUAL_LEFT,
                         CLIP_QUAL_RIGHT,CLIP_ADAP_LEFT,CLIP_ADAP_RIGHT,
                         QUAL_MIN,QUAL_MAX,QUAL_AVG,QUAL_STRING)
    VALUES(seq_run_id_array(idx),read_id_array(idx),read_sequence_array(idx),
           read_sequence_length_array(idx),run_name_array(idx),
           run_date_array(idx),region_array(idx),x_location_array(idx),
           y_location_array(idx),flowgram_string_clob_array(idx),
           flow_index_str_clob_array(idx),clip_qual_left_array(idx),
           clip_qual_right_array(idx),clip_adap_left_array(idx),
           clip_adap_right_array(idx),qual_min_array(idx),qual_max_array(idx),
           qual_avg_array(idx),qual_string_clob_array(idx));
    END LOOP;
    COMMIT;
    
  end array_insert;

end load_flow_data;
/
