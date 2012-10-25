CREATE OR REPLACE PACKAGE "LOAD_FNA_FILE_PACKAGE" as 

  TYPE split_library_run_id_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.SPLIT_LIBRARY_RUN_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE seq_run_id_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.SEQ_RUN_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE sequence_name_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.SEQUENCE_NAME%TYPE INDEX BY BINARY_INTEGER;
  TYPE sample_name_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.SAMPLE_NAME%TYPE INDEX BY BINARY_INTEGER;
  TYPE read_id_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.READ_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE orig_barcode_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.ORIG_BARCODE_SEQ%TYPE INDEX BY BINARY_INTEGER;
  TYPE new_barcode_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.NEW_BARCODE_SEQ%TYPE INDEX BY BINARY_INTEGER;
  TYPE barcode_diff_tab IS TABLE OF SPLIT_LIBRARY_READ_MAP.BARCODE_DIFF%TYPE INDEX BY BINARY_INTEGER;
  TYPE sequence_length_tab IS TABLE OF SSU_SEQUENCE.SEQUENCE_LENGTH%TYPE INDEX BY BINARY_INTEGER;
  TYPE md5_checksum_tab IS TABLE OF SSU_SEQUENCE.MD5_CHECKSUM%TYPE INDEX BY BINARY_INTEGER;
  TYPE sequence_string_tab IS TABLE OF SSU_SEQUENCE.SEQUENCE_STRING%TYPE INDEX BY BINARY_INTEGER;
  

  procedure array_insert 
  (
    split_library_run_ids in split_library_run_id_tab,
    seq_run_ids in seq_run_id_tab,
    sequence_names in sequence_name_tab,
    sample_names in sample_name_tab,
    read_ids in read_id_tab,
    orig_barcodes in orig_barcode_tab,
    new_barcodes in new_barcode_tab,
    barcode_diffs in barcode_diff_tab,
    sequence_lengths in sequence_length_tab,
    md5_checksums in md5_checksum_tab,
    sequence_strings in sequence_string_tab
  );

end load_fna_file_package;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_FNA_FILE_PACKAGE" as

  procedure array_insert 
  (
    split_library_run_ids in split_library_run_id_tab,
    seq_run_ids in seq_run_id_tab,
    sequence_names in sequence_name_tab,
    sample_names in sample_name_tab,
    read_ids in read_id_tab,
    orig_barcodes in orig_barcode_tab,
    new_barcodes in new_barcode_tab,
    barcode_diffs in barcode_diff_tab,
    sequence_lengths in sequence_length_tab,
    md5_checksums in md5_checksum_tab,
    sequence_strings in sequence_string_tab
  )
  as
  
    ssu_sequence_id_ ssu_sequence.ssu_sequence_id%type;
  
  begin
    
    for idx in split_library_run_ids.first .. split_library_run_ids.last
    loop
    
      -- Update the ssu_sequence table
      merge into ssu_sequence
      using dual
      on (dual.dummy is not null and ssu_sequence.md5_checksum = md5_checksums(idx))
      when not matched then 
        insert (ssu_sequence_id, sequence_length, sequence_string, md5_checksum) 
        values (ssu_sequence_id_seq.nextval, sequence_lengths(idx), sequence_strings(idx), md5_checksums(idx));
      
      -- Get the ssu_sequence_id
      select  ssu_sequence_id into ssu_sequence_id_
      from    ssu_sequence
      where   md5_checksum = md5_checksums(idx);

      -- update the split_library_read_map table      
      merge into split_library_read_map
      using dual
      on 
      (
        dual.dummy is not null 
        and split_library_read_map.seq_run_id = seq_run_ids(idx) 
        and split_library_read_map.sequence_name = sequence_names(idx)
      )
      when not matched then
        insert (split_library_run_id, read_id, seq_run_id, sample_name, orig_barcode_seq,
                new_barcode_seq, barcode_diff, sequence_name, ssu_sequence_id)
        values  (split_library_run_ids(idx), read_ids(idx), seq_run_ids(idx), sample_names(idx), orig_barcodes(idx),
                new_barcodes(idx), barcode_diffs(idx), sequence_names(idx), ssu_sequence_id_);
      commit;
      --when matched then
      --  update
      --    set   read_id = read_ids(idx), 
      --          seq_run_id = seq_run_ids(idx), 
      --         sample_name = sample_names(idx), 
      --          orig_barcode_seq = orig_barcodes(idx),
      --          new_barcode_seq = new_barcodes(idx), 
      --          barcode_diff = barcode_diffs(idx), 
      --          ssu_sequence_id = ssu_sequence_id_;

      
    end loop;
    
  end array_insert;

end load_fna_file_package;
/
