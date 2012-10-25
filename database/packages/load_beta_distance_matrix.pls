CREATE OR REPLACE PACKAGE "LOAD_BETA_DISTANCE_MATRIX" as 

/* This package loads the beta-diversity distance matrices*/

  -- define an associative array type for each array passed into the packeage
  TYPE beta_sample1_tab 	    IS TABLE OF BETA_DIVERSITY_DISTANCES.SAMPLE_NAME1%TYPE INDEX BY BINARY_INTEGER; 
  TYPE beta_sample2_tab      	IS TABLE OF BETA_DIVERSITY_DISTANCES.SAMPLE_NAME2%TYPE INDEX BY BINARY_INTEGER;
  TYPE beta_distance_tab      IS TABLE OF BETA_DIVERSITY_DISTANCES.DISTANCE%TYPE INDEX BY BINARY_INTEGER;
  TYPE beta_metric_tab      	IS TABLE OF BETA_DIVERSITY_DISTANCES.METRIC%TYPE INDEX BY BINARY_INTEGER;
  TYPE beta_rarefied_tab      IS TABLE OF BETA_DIVERSITY_DISTANCES.RAREFIED%TYPE INDEX BY BINARY_INTEGER;  
  -- define the procedure for inserting data into OTU tables
  procedure array_insert (beta_sample1 in beta_sample1_tab,
                          beta_sample2 in beta_sample2_tab,
                          beta_distance in beta_distance_tab,
                          beta_metric in beta_metric_tab,
                          beta_rarefied in beta_rarefied_tab); 
end load_beta_distance_matrix;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_BETA_DISTANCE_MATRIX" as

  procedure array_insert (beta_sample1 in beta_sample1_tab,
                          beta_sample2 in beta_sample2_tab,
                          beta_distance in beta_distance_tab,
                          beta_metric in beta_metric_tab,
                          beta_rarefied in beta_rarefied_tab) as
                          
  samp1_cnt NUMBER;
  samp2_cnt NUMBER;
  begin

    FOR idx in beta_sample1.first..beta_sample1.last
      LOOP

        /* TEMP disabled

        
        -- get the ssu sequence id for each samaple from the READ_454 table
        SELECT count(1) INTO samp1_cnt FROM SPLIT_LIBRARY_READ_MAP 
        WHERE SAMPLE_NAME=beta_sample1(idx);
        SELECT count(1) INTO samp2_cnt FROM SPLIT_LIBRARY_READ_MAP 
        WHERE SAMPLE_NAME=beta_sample2(idx);
        */
        -- if sample seq id not in the OTU_MAP table, insert it into the table
        
          INSERT INTO BETA_DIVERSITY_DISTANCES(SAMPLE_NAME1, SAMPLE_NAME2,METRIC,DISTANCE,RAREFIED)
          VALUES(beta_sample1(idx),beta_sample2(idx),beta_metric(idx),
                  beta_distance(idx),beta_rarefied(idx));
          COMMIT;

      END LOOP;

  end array_insert;

end load_beta_distance_matrix;
/
