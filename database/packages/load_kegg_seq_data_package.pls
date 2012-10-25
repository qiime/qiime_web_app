CREATE OR REPLACE PACKAGE "LOAD_KEGG_SEQ_DATA_PACKAGE" AS 

  TYPE kegg_guid_tab IS TABLE OF KEGG_REFERENCE.GENE_GUID%TYPE INDEX BY BINARY_INTEGER;
  TYPE kegg_fasta_seq_string_tab  IS TABLE OF SSU_SEQUENCE.SEQUENCE_STRING%TYPE INDEX BY BINARY_INTEGER;
  TYPE kegg_fasta_seq_length_tab  IS TABLE OF SSU_SEQUENCE.SEQUENCE_LENGTH%TYPE INDEX BY BINARY_INTEGER;
  TYPE ssu_sequence_md5_tab IS TABLE OF SSU_SEQUENCE.MD5_CHECKSUM%TYPE INDEX BY BINARY_INTEGER;

  /* TODO enter package declarations (types, exceptions, methods etc) here */ 
  procedure array_insert (I_REFERENCE_SET_ID in NUMBER,
                          kegg_guid in kegg_guid_tab,
                          kegg_fasta_seq_string in kegg_fasta_seq_string_tab,
                          kegg_md5_seq_hash in ssu_sequence_md5_tab);
END LOAD_KEGG_SEQ_DATA_PACKAGE;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_KEGG_SEQ_DATA_PACKAGE" AS

  procedure array_insert (I_REFERENCE_SET_ID in NUMBER,
                          kegg_guid in kegg_guid_tab,
                          kegg_fasta_seq_string in kegg_fasta_seq_string_tab,
                          kegg_md5_seq_hash in ssu_sequence_md5_tab) AS
                          
  TYPE ssu_sequence_len_tab         IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
  ssu_sequence_len_array          ssu_sequence_len_tab;
  TYPE ssu_sequence_tab         IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
  ssu_sequence_array          ssu_sequence_tab;

  -- these next variables hold the actual data that will populate the 
  -- SSU_SEQUENCE table. 
  ssu_sequence_len_load_array   ssu_sequence_len_tab;
  ssu_sequence_load_array   ssu_sequence_tab;
  kegg_fasta_seq_load_array   kegg_fasta_seq_string_tab;
  kegg_md5_seq_hash_load_array  ssu_sequence_md5_tab;
  ssu_id NUMBER;
  curr_idx NUMBER;

  BEGIN
      curr_idx := 1;
  
      -- for all of our sequences, check if the exist. if the sequence exists,
      -- obtain is SSU_SEQUENCE_ID. If it does not exist, collect a new
      -- SSU_SEQUENCE_ID and populate the SSU_SEQUENCE load arrays 
      FOR indx in kegg_fasta_seq_string.first..kegg_fasta_seq_string.last      
      LOOP
      SELECT COUNT(1) INTO ssu_id FROM SSU_SEQUENCE WHERE MD5_CHECKSUM=kegg_md5_seq_hash(indx);      
      if (ssu_id=0) then
        -- this code is crying for a refactor... fucking fucking ugly ghetto garbage
        ssu_id := SSU_SEQUENCE_ID_SEQ.NEXTVAL;
        ssu_sequence_array(indx) := ssu_id;

        ssu_sequence_load_array(curr_idx) := ssu_id;
        ssu_sequence_len_load_array(curr_idx) := length(kegg_fasta_seq_string(indx));
        kegg_fasta_seq_load_array(curr_idx) := kegg_fasta_seq_string(indx);
        kegg_md5_seq_hash_load_array(curr_idx) := kegg_md5_seq_hash(indx);
        
        --INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SEQUENCE_STRING, SEQUENCE_LENGTH, MD5_CHECKSUM)
        --VALUES(ssu_sequence_load_array(curr_idx),gg_fasta_seq_load_array(curr_idx), ssu_sequence_len_load_array(curr_idx), gg_md5_seq_hash_load_array(curr_idx));
        --COMMIT;
        curr_idx := curr_idx + 1;

      else
        SELECT SSU_SEQUENCE_ID INTO ssu_id from SSU_SEQUENCE WHERE MD5_CHECKSUM=kegg_md5_seq_hash(indx);
        ssu_sequence_array(indx) := ssu_id;
      end if;
      END LOOP;

      FORALL indx in kegg_fasta_seq_string.first..kegg_fasta_seq_string.last
      INSERT INTO KEGG_REFERENCE(GENE_GUID, SSU_SEQUENCE_ID, SEQUENCE_SOURCE_ID)
      VALUES(kegg_guid(indx), ssu_sequence_array(indx), I_REFERENCE_SET_ID);
      COMMIT;

      FORALL indx in kegg_fasta_seq_load_array.first..kegg_fasta_seq_load_array.last
      INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SEQUENCE_STRING, SEQUENCE_LENGTH, MD5_CHECKSUM)
      VALUES(ssu_sequence_load_array(indx),kegg_fasta_seq_load_array(indx), ssu_sequence_len_load_array(indx), kegg_md5_seq_hash_load_array(indx));
      COMMIT;

      --FORALL indx in ssu_sequence_load_array.first..ssu_sequence_load_array.last
      --INSERT INTO SEQUENCE_SOURCE_MAP(ID, SEQUENCE_SOURCE_ID)
      --VALUES(kegg_guid(indx), I_REFERENCE_SET_ID);
      --COMMIT;
  END array_insert;

END LOAD_KEGG_SEQ_DATA_PACKAGE;
/
