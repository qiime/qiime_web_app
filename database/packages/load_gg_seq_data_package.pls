CREATE OR REPLACE PACKAGE "LOAD_GG_SEQ_DATA_PACKAGE" as 
/* This package loads the full greengenes sequence set into the 
GREENGENES_REFRENCE table.*/

  -- define an associative array type for each column in the jobs table
  TYPE gg_prokmsa_id_tab 	    IS TABLE OF GREENGENES_REFERENCE.PROKMSA_ID%TYPE INDEX BY BINARY_INTEGER; 
  TYPE gg_genbank_acc_id_tab	IS TABLE OF GREENGENES_REFERENCE.GENBANK_ACC_ID%TYPE INDEX BY BINARY_INTEGER;
  TYPE gg_decision_tab		    IS TABLE OF GREENGENES_REFERENCE.DECISION%TYPE INDEX BY BINARY_INTEGER;
  TYPE gg_core_set_member_tab	IS TABLE OF GREENGENES_REFERENCE.CORE_SET_MEMBER%TYPE INDEX BY BINARY_INTEGER;
  TYPE gg_fasta_seq_string_tab  IS TABLE OF SSU_SEQUENCE.SEQUENCE_STRING%TYPE INDEX BY BINARY_INTEGER;
  TYPE gg_fasta_seq_length_tab  IS TABLE OF SSU_SEQUENCE.SEQUENCE_LENGTH%TYPE INDEX BY BINARY_INTEGER;
  TYPE ssu_sequence_md5_tab IS TABLE OF SSU_SEQUENCE.MD5_CHECKSUM%TYPE INDEX BY BINARY_INTEGER;

  -- define the procedure that will perform the array insert
  procedure array_insert (I_REFERENCE_SET_ID in NUMBER,gg_prokmsa_id in gg_prokmsa_id_tab,
                                   gg_genbank_acc_id in gg_genbank_acc_id_tab,
                                   gg_decision in gg_decision_tab,
                                   gg_core_set_member in gg_core_set_member_tab,
                                   gg_fasta_seq_string in gg_fasta_seq_string_tab,
                                   gg_md5_seq_hash in ssu_sequence_md5_tab);
end load_gg_seq_data_package;
/


CREATE OR REPLACE PACKAGE BODY "LOAD_GG_SEQ_DATA_PACKAGE" as
  -- implement the procedure that will perform the array insert

  procedure array_insert (I_REFERENCE_SET_ID in NUMBER, gg_prokmsa_id in gg_prokmsa_id_tab,
                                   gg_genbank_acc_id in gg_genbank_acc_id_tab,
                                   gg_decision in gg_decision_tab,
                                   gg_core_set_member in gg_core_set_member_tab,
                                   gg_fasta_seq_string in gg_fasta_seq_string_tab,
                                   gg_md5_seq_hash in ssu_sequence_md5_tab) is

  TYPE ssu_sequence_len_tab         IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
  ssu_sequence_len_array          ssu_sequence_len_tab;
  TYPE ssu_sequence_tab         IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;
  ssu_sequence_array          ssu_sequence_tab;

  -- these next variables hold the actual data that will populate the 
  -- SSU_SEQUENCE table. 
  ssu_sequence_len_load_array   ssu_sequence_len_tab;
  ssu_sequence_load_array   ssu_sequence_tab;
  gg_fasta_seq_load_array   gg_fasta_seq_string_tab;
  gg_md5_seq_hash_load_array  ssu_sequence_md5_tab;
  ssu_id NUMBER;
  curr_idx NUMBER;
  begin
      curr_idx := 1;
  
      -- for all of our sequences, check if the exist. if the sequence exists,
      -- obtain is SSU_SEQUENCE_ID. If it does not exist, collect a new
      -- SSU_SEQUENCE_ID and populate the SSU_SEQUENCE load arrays 
      FOR indx in gg_fasta_seq_string.first..gg_fasta_seq_string.last      
      LOOP
      SELECT COUNT(1) INTO ssu_id FROM SSU_SEQUENCE WHERE MD5_CHECKSUM=gg_md5_seq_hash(indx);      
      if (ssu_id=0) then
        -- this code is crying for a refactor... fucking fucking ugly ghetto garbage
        ssu_id := SSU_SEQUENCE_ID_SEQ.NEXTVAL;
        ssu_sequence_array(indx) := ssu_id;

        ssu_sequence_load_array(curr_idx) := ssu_id;
        ssu_sequence_len_load_array(curr_idx) := length(gg_fasta_seq_string(indx));
        gg_fasta_seq_load_array(curr_idx) := gg_fasta_seq_string(indx);
        gg_md5_seq_hash_load_array(curr_idx) := gg_md5_seq_hash(indx);
        
        --INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SEQUENCE_STRING, SEQUENCE_LENGTH, MD5_CHECKSUM)
        --VALUES(ssu_sequence_load_array(curr_idx),gg_fasta_seq_load_array(curr_idx), ssu_sequence_len_load_array(curr_idx), gg_md5_seq_hash_load_array(curr_idx));
        --COMMIT;
        curr_idx := curr_idx + 1;

      else
        SELECT SSU_SEQUENCE_ID INTO ssu_id from SSU_SEQUENCE WHERE MD5_CHECKSUM=gg_md5_seq_hash(indx);
        ssu_sequence_array(indx) := ssu_id;
      end if;
      END LOOP;

      FORALL indx in gg_fasta_seq_string.first..gg_fasta_seq_string.last
      INSERT INTO GREENGENES_REFERENCE(SEQUENCE_SOURCE_ID, PROKMSA_ID, GENBANK_ACC_ID,DECISION,CORE_SET_MEMBER,SSU_SEQUENCE_ID)
      VALUES(I_REFERENCE_SET_ID, gg_prokmsa_id(indx), gg_genbank_acc_id(indx),gg_decision(indx),gg_core_set_member(indx),ssu_sequence_array(indx));
      COMMIT;

      FORALL indx in gg_fasta_seq_load_array.first..gg_fasta_seq_load_array.last
      INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SEQUENCE_STRING, SEQUENCE_LENGTH, MD5_CHECKSUM)
      VALUES(ssu_sequence_load_array(indx),gg_fasta_seq_load_array(indx), ssu_sequence_len_load_array(indx), gg_md5_seq_hash_load_array(indx));
      COMMIT;

      FORALL indx in gg_prokmsa_id.first..gg_prokmsa_id.last
      INSERT INTO SOURCE_MAP(REFERENCE_ID, SEQUENCE_SOURCE_ID)
      VALUES(gg_prokmsa_id(indx), I_REFERENCE_SET_ID);
      COMMIT;

  end array_insert;

end load_gg_seq_data_package;


/*
create or replace
package body load_gg_seq_data_package as
  -- implement the procedure that will perform the array insert

  procedure array_insert (I_REFERENCE_SET_ID in NUMBER,gg_prokmsa_id in gg_prokmsa_id_tab,
                                   gg_genbank_acc_id in gg_genbank_acc_id_tab,
                                   gg_decision in gg_decision_tab,
                                   gg_core_set_member in gg_core_set_member_tab,
                                   gg_fasta_seq_string in gg_fasta_seq_string_tab) is
                                   
  TYPE ssu_sequence_len_tab		    IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;      
  ssu_sequence_len_array          ssu_sequence_len_tab;
  TYPE ssu_sequence_tab		    IS TABLE OF SSU_SEQUENCE.SSU_SEQUENCE_ID%TYPE INDEX BY BINARY_INTEGER;      
  ssu_sequence_array          ssu_sequence_tab;
  begin
  
      
      FOR indx in gg_fasta_seq_string.first..gg_fasta_seq_string.last
      LOOP
      ssu_sequence_array(indx):=SSU_SEQUENCE_ID_SEQ.NEXTVAL;
      ssu_sequence_len_array(indx):=length(gg_fasta_seq_string(indx));
      END LOOP;
      
      FORALL indx in gg_fasta_seq_string.first..gg_fasta_seq_string.last  	
      INSERT INTO GREENGENES_REFERENCE(SEQUENCE_SOURCE_ID, PROKMSA_ID, GENBANK_ACC_ID,DECISION,CORE_SET_MEMBER,SSU_SEQUENCE_ID)  
      VALUES(I_REFERENCE_SET_ID, gg_prokmsa_id(indx), gg_genbank_acc_id(indx),gg_decision(indx),gg_core_set_member(indx),ssu_sequence_array(indx));			
      COMMIT;	

      FORALL indx in gg_fasta_seq_string.first..gg_fasta_seq_string.last
      INSERT INTO SSU_SEQUENCE(SSU_SEQUENCE_ID, SEQUENCE_STRING, SEQUENCE_LENGTH)  
      VALUES(ssu_sequence_array(indx),gg_fasta_seq_string(indx), ssu_sequence_len_array(indx));			
      COMMIT;

      FORALL indx in gg_fasta_seq_string.first..gg_fasta_seq_string.last
      INSERT INTO SEQUENCE_SOURCE_MAP(SSU_SEQUENCE_ID, SEQUENCE_SOURCE_ID)  
      VALUES(ssu_sequence_array(indx), I_REFERENCE_SET_ID);			
      COMMIT;
      
  end array_insert;

end load_gg_seq_data_package;
*/
/
