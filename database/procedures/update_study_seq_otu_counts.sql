create or replace procedure update_study_seq_otu_counts
(
    sequence_prep_id_ in int,
    num_sequences_ in int,
    num_otus_ in int
)
as
begin
  
    update  sequence_prep
    set     num_sequences = num_sequences_,
            num_otus = num_otus_
    where   sequence_prep_id = sequence_prep_id_;
    
    commit;

end;

