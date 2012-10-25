create or replace
PROCEDURE GET_FASTA_FILE_DATA 
(
  studies in varchar,
  samples_to_get in varchar,  
  fasta_values in out types.ref_cursor
)
as
begin    
  open fasta_values for  
     'select SAMPLE_ID || ''_'' || SEQUENCE_ID || '' '' || STUDY_NAME,
     SEQUENCE_VALUE 
     from DNA_SEQUENCE 
     where study_name in (' || studies || ') and sample_id in (' || samples_to_get || ')';
END GET_FASTA_FILE_DATA;

/*

variable fasta_values REFCURSOR;
execute get_fasta_file_data('''MALAWI_081209''','''84Mom'',''84Binf3RUTF''', :fasta_values);
print fasta_values;

*/
