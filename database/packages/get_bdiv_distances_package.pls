CREATE OR REPLACE PACKAGE "GET_BDIV_DISTANCES_PACKAGE" as 

/* This package loads the beta-diversity distance matrices*/

  -- define an associative array type for each array passed into the packeage
  TYPE beta_sample1_tab 	    IS TABLE OF BETA_DIVERSITY_DISTANCES.SAMPLE_NAME1%TYPE INDEX BY BINARY_INTEGER; 
  TYPE beta_sample2_tab      	IS TABLE OF BETA_DIVERSITY_DISTANCES.SAMPLE_NAME2%TYPE INDEX BY BINARY_INTEGER;
  TYPE beta_distance_tab      IS TABLE OF BETA_DIVERSITY_DISTANCES.DISTANCE%TYPE INDEX BY BINARY_INTEGER;
  TYPE beta_metric_tab      	IS TABLE OF BETA_DIVERSITY_DISTANCES.METRIC%TYPE INDEX BY BINARY_INTEGER;
  TYPE beta_rarefied_tab      IS TABLE OF BETA_DIVERSITY_DISTANCES.RAREFIED%TYPE INDEX BY BINARY_INTEGER;  
  -- define the procedure for inserting data into OTU tables
  procedure array_get (beta_sample1 in beta_sample1_tab,
                          beta_sample2 in beta_sample2_tab,
                          beta_distance in out beta_distance_tab,
                          beta_metric in beta_metric_tab,
                          beta_rarefied in beta_rarefied_tab); 
end get_bdiv_distances_package;
/


CREATE OR REPLACE PACKAGE BODY "GET_BDIV_DISTANCES_PACKAGE" as

  procedure array_get (beta_sample1 in beta_sample1_tab,
                          beta_sample2 in beta_sample2_tab,
                          beta_distance in out beta_distance_tab,
                          beta_metric in beta_metric_tab,
                          beta_rarefied in beta_rarefied_tab) as
                          

  begin

    FOR idx in beta_sample1.first..beta_sample1.last
      LOOP
  begin
    SELECT DISTANCE into beta_distance(idx) FROM BETA_DIVERSITY_DISTANCES
    where (rarefied=beta_rarefied(idx) and metric=beta_metric(idx)) and 
     ((sample_name1=beta_sample1(idx) and sample_name2=beta_sample2(idx)) or
     (sample_name1=beta_sample2(idx) and sample_name2=beta_sample1(idx)));
  EXCEPTION
        WHEN NO_DATA_FOUND
        THEN beta_distance(idx):=NULL;
  end;   

      END LOOP;

  end array_get;

end get_bdiv_distances_package;
/
