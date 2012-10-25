create or replace package body get_sequences_for_fasta_pkg
as

  procedure get_sequences_for_fasta 
  (
    study_id_ in int,
    sample_ids_ in sample_ids_tab,
    sequence_names_ in out sequence_names_tab,
    sequence_strings_ in out sequence_strings_tab
  )
  as
  begin
    
    for idx in sample_ids_.first..sample_ids_.last
    loop
    
      -- Oracle sucks. Perform first array insert...
      begin
        select  sl.sequence_name into sequence_names_(idx)
        from    sample sa
                inner join sff.analysis an
                on sa.study_id = an.study_id
                inner join sff.split_library_read_map sl
                on an.split_library_run_id = sl.split_library_run_id
                inner join sff.ssu_sequence ssu
                on sl.ssu_sequence_id = ssu.ssu_sequence_id
        where   sa.sample_id = sample_ids_(idx)
                and an.analysis_id = 
                (
                  select  max(analysis_id)
                  from    sff.analysis 
                  where   study_id = study_id_
                );
      exception
        when NO_DATA_FOUND then 
          sequence_names_(idx) := NULL;
      end;
      
    -- Oracle sucks. Perform second array insert...
    begin
        select  ssu.sequence_string into sequence_strings_(idx)
        from    sample sa
                inner join sff.analysis an
                on sa.study_id = an.study_id
                inner join sff.split_library_read_map sl
                on an.split_library_run_id = sl.split_library_run_id
                inner join sff.ssu_sequence ssu
                on sl.ssu_sequence_id = ssu.ssu_sequence_id
        where   sa.sample_id = sample_ids_(idx)
                and an.analysis_id = 
                (
                  select  max(analysis_id)
                  from    sff.analysis 
                  where   study_id = study_id_
                );
      exception
        when NO_DATA_FOUND then 
          sequence_strings_(idx) := NULL;
      end;

    end loop;
      
  end get_sequences_for_fasta;
  
end get_sequences_for_fasta_pkg;