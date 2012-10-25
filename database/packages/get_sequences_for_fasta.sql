create or replace package get_sequences_for_fasta_pkg 
as 

  -- Define the array tables input to the table insert.
  type sample_ids_tab is table of sample.sample_id%TYPE INDEX BY BINARY_INTEGER;
  type sequence_names_tab is table of sff.split_library_read_map.sequence_name%TYPE INDEX BY BINARY_INTEGER;
  type sequence_strings_tab is table of sff.ssu_sequence.sequence_string%TYPE INDEX BY BINARY_INTEGER;

  -- define the procedure for inserting data into the table.
  procedure get_sequences_for_fasta 
  (
    study_id_ in int,
    sample_ids_ in sample_ids_tab,
    sequence_names_ in out sequence_names_tab,
    sequence_strings_ in out sequence_strings_tab
  );

end get_sequences_for_fasta_pkg;
