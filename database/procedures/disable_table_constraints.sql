create or replace 
PROCEDURE "DISABLE_TABLE_CONSTRAINTS" 
/* This procedure disables some of the table constraints. */
(
  error_flag IN OUT NUMBER
) as 
begin
  -- disable table constraints
 EXECUTE IMMEDIATE 'ALTER index IDX_SLRM_SLRI unusable ';
 EXECUTE IMMEDIATE 'ALTER index SEQ_NAME_INDEX unusable' ;  
 EXECUTE IMMEDIATE 'ALTER index IDX_SLRM_READ_ID unusable' ;  
 EXECUTE IMMEDIATE 'ALTER index IDX_SLRM_SEQ_RUN_ID unusable' ;  
 EXECUTE IMMEDIATE 'ALTER index SEQ_NAME_SSU_ID_IDX unusable' ;  
 EXECUTE IMMEDIATE 'ALTER index IDX_SLRM_SAMPLE_NAME unusable' ;  
 EXECUTE IMMEDIATE 'ALTER index IDX_SLRM_SEQRUNID_SLRID unusable' ;  
 EXECUTE IMMEDIATE 'ALTER index IDX_SLRM_SSU_SEQUENCE_ID unusable' ;
 EXECUTE IMMEDIATE 'ALTER index IX_SLRM_SRID_RID unusable' ; 
 -- EXECUTE IMMEDIATE 'ALTER index PK_SPLIT_LIBRARY_READ_MAP unusable' ;  
  commit;
  error_flag:=0;
end disable_table_constraints;

/*
variable error_flag NUMBER;
execute disable_table_constraints(:error_flag);
print error_flag;
*/