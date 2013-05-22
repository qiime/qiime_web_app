create or replace procedure ag_update_barcode
(
    barcode_ in varchar2,
    ag_kit_id_ in varchar2, 
    site_sampled_ in varchar2, 
    environment_sampled_ in varchar2, 
    sample_date_ in varchar2, 
    sample_time_ in varchar2, 
    participant_name_ in varchar2, 
    notes_ in varchar2
)
as
begin

    update  ag_kit_barcodes
    set     ag_kit_id = ag_kit_id_,
            site_sampled = site_sampled_,
            environment_sampled = environment_sampled_,
            sample_date = sample_date_,
            sample_time = sample_time_,
            participant_name = participant_name_,
            notes = notes_
    where   barcode = barcode_; 
  
    commit;

end;