create or replace
PACKAGE "OTU_CHECK" 
as 

  -- Define the input type
  TYPE md5_tab IS TABLE OF SSU_SEQUENCE.MD5_CHECKSUM%TYPE INDEX BY BINARY_INTEGER; 
  TYPE otu_tab IS TABLE OF SOURCE_MAP.REFERENCE_ID%TYPE INDEX BY BINARY_INTEGER; 

  -- define the procedure for inserting data into OTU tables
  procedure check_existing_otus
  (
    md5_array_ in md5_tab,
    otu_results_ in out otu_tab,
    md5_results_ in out md5_tab
  ); 

end otu_check;
/


create or replace
PACKAGE BODY "OTU_CHECK" 
as
  procedure check_existing_otus
  (
    md5_array_ in md5_tab,
    otu_results_ in out otu_tab,
    md5_results_ in out md5_tab
  )
  as                        
  begin
    for idx in md5_array_.first..md5_array_.last loop
      begin
        md5_results_(idx) := md5_array_(idx);
      
        select  distinct gr.reference_id into otu_results_(idx)
            from    ssu_sequence ss
                inner join gg_plus_denovo_reference gr on ss.ssu_sequence_id = gr.ssu_sequence_id
                inner join source_map sm on gr.reference_id=sm.reference_id
                inner join sequence_source sso on sm.sequence_source_id=sso.sequence_source_id
                inner join otu_table ot on gr.reference_id=ot.reference_id
                inner join otu_run_set ors on ot.otu_run_set_id=ors.otu_run_set_id
                inner join otu_picking_run opr on ors.otu_run_set_id=opr.otu_run_set_id
                inner join otu_picking_method opm on opr.otu_picking_method_id=opm.otu_picking_method_id
                
        where   ss.md5_checksum = md5_array_(idx)
                and opm.otu_picking_method_name='UCLUST_REF'
                and opm.otu_picking_method_threshold=97 
                and opm.otu_picking_ref_set_name='GREENGENES_REFERENCE'
                and sso.threshold=97 
                and sso.source_name='GREENGENES_REFERENCE';
      exception
        when no_data_found then
          otu_results_(idx) := null;
          md5_results_(idx) := null;
          
      end;
    end loop;
  end check_existing_otus;
end otu_check;/
