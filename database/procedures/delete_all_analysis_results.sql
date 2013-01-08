create or replace 
procedure delete_all_analysis_results
(
  study_id_ IN NUMBER,
  error_flag OUT NUMBER
) 
as 
begin

  -- delete the appropriate rows from the DB
  delete  
  from    split_library_read_map
  where   split_library_run_id in
          (
            select  split_library_run_id
            from    analysis
            where   study_id = study_id_
          );

  delete 
  from    otu_picking_failures 
  where   otu_picking_run_id in 
          (
            select  otu_picking_run_id
            from    analysis
            where   study_id = study_id_
          );
    
  delete 
  from    otu_picking_run 
  where   otu_picking_run_id in 
          (
            select  otu_picking_run_id
            from    analysis
            where   study_id = study_id_
          );
    
  delete 
  from    otu_run_set 
  where   otu_run_set_id in 
          (
            select  otu_run_set_id
            from    analysis
            where   study_id = study_id_
          );
  
  delete 
  from    otu_table 
  where   otu_run_set_id in 
          (
            select  otu_run_set_id
            from    analysis
            where   study_id = study_id_
          );

  delete 
  from    analysis 
  where   analysis_id in 
          (
            select  analysis_id
            from    analysis
            where   study_id = study_id_
          );
  
  delete 
  from    split_library_run 
  where   split_library_run_id in 
          (
            select  split_library_run_id
            from    analysis
            where   study_id = study_id_
          );
  
  
  error_flag := 0;
  commit;

  
end;

/*
variable error_flag NUMBER;
execute delete_all_analysis_results(22,:error_flag);
print error_flag;
*/