create or replace procedure ag_log_participant_sample
(
    barcode_ varchar2,
    sample_site_ varchar2,
    environment_sampled_ varchar2,
    sample_date_ varchar2,
    sample_time_ varchar2,
    participant_name_ varchar2,
    notes_ varchar2
)
as
begin

    update  ag_kit_barcodes
    set     site_sampled = sample_site_,
            environment_sampled = environment_sampled_,
            sample_date = sample_date_,
            sample_time = sample_time_,
            participant_name = participant_name_,
            notes = notes_
    where   barcode = barcode_;
    
    commit;

end;