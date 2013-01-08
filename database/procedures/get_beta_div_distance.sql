create or replace 
PROCEDURE "GET_BETA_DIV_DISTANCE" 
(
  beta_samp1 IN VARCHAR2,
  beta_samp2 IN VARCHAR2,
  beta_metric IN VARCHAR2,
  beta_rarefied IN NUMBER,
  beta_distance OUT BINARY_DOUBLE
)
as 
begin

  begin
    SELECT DISTANCE into beta_distance FROM BETA_DIVERSITY_DISTANCES
    where (rarefied=beta_rarefied and metric=beta_metric) and 
     ((sample_name1=beta_samp1 and sample_name2=beta_samp2) or
     (sample_name1=beta_samp2 and sample_name2=beta_samp1));
  EXCEPTION
        WHEN NO_DATA_FOUND
        THEN NULL;
  end;        

end get_beta_div_distance;


/* 
variable dist BINARY_DOUBLE;
execute get_beta_div_distance('PC.354','PC.634','weighted_unifrac',1000,:dist);
print dist;
*/