create or replace
package body otu_check 
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
      
        select  gr.prokmsa_id into otu_results_(idx)                
        from    ssu_sequence ss
                inner join otu o
                on ss.ssu_sequence_id = o.ssu_sequence_id
                inner join greengenes_reference gr
                on gr.ssu_sequence_id = ss.ssu_sequence_id
        where   ss.md5_checksum = md5_array_(idx);
      exception
        when no_data_found then
          otu_results_(idx) := null;
          md5_results_(idx) := null;
          
      end;
    end loop;
  end check_existing_otus;
end otu_check;