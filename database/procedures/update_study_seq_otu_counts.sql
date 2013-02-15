
create or replace procedure update_seq_otu_counts
(
    sequence_prep_id_ in int,
    num_sequences_ in int,
    num_otus_ in int,
    otu_percent_hit_ in int
)
as
begin
  
    update  sequence_prep
    set     num_sequences = num_sequences_,
            num_otus = num_otus_,
            otu_percent_hit = otu_percent_hit_
    where   sequence_prep_id = sequence_prep_id_;
    
    commit;

end;




