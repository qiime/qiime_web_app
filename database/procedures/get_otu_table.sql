create or replace 
PROCEDURE       "GET_OTU_TABLE" 
(
  sample_ids IN VARCHAR2,
  otu_method IN VARCHAR2,
  otu_threshold IN NUMBER,
  ss_source_name IN VARCHAR2,
  ss_threshold IN NUMBER,
  user_data OUT types.ref_cursor
)
as 
begin
  open user_data for
    select reference_id, "COUNT"
    from otu_table_to_reference
    where sample_name=sample_ids
      and otu_picking_method_name=otu_method
      and otu_picking_method_threshold=otu_threshold
      and source_name=ss_source_name
      and threshold=ss_threshold;
    
end get_otu_table;

/*
variable user_data REFCURSOR;
execute get_otu_table('PCx420.140896','UCLUST_REF',97,'GREENGENES_REFERENCE',97,:user_data);
print user_data;
*/