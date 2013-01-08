create or replace 
PACKAGE BODY "CHECK_SSU_SEQ_ID_CTS_PKG" as

  procedure array_get (ssu_sequence_id_array in ssu_sequence_id_tab,
                       ssu_sequence_str_array in ssu_sequence_str_tab,
                       user_data1 IN OUT user_data1_tab,
                       user_data2 IN OUT user_data2_tab) as


  begin
    
    -- Loop through the sample id's
  for idx in ssu_sequence_id_array.first..ssu_sequence_id_array.last
      LOOP
        select count(slrm.ssu_sequence_id) INTO user_data1(idx)
        from split_library_read_map slrm 
        where slrm.ssu_sequence_id=ssu_sequence_id_array(idx);
   
        select count(distinct slrm.sample_name) INTO user_data2(idx)
        from split_library_read_map slrm 
        where slrm.ssu_sequence_id=ssu_sequence_id_array(idx);
        
      END LOOP;

  end array_get;
  
end CHECK_SSU_SEQ_ID_CTS_PKG;