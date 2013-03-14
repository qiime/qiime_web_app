create or replace procedure ag_log_participant_sample
(
    barcode_ varchar2, 
    sample_site_ varchar2, 
    sample_date_ varchar2, 
    hours_ integer, 
    minutes_ integer, 
    meridian_ varchar2,
    participant_name_ varchar2
)
as
begin

    update  ag_kit_barcodes
    set     site_sampled = sample_site_,
            sample_date = sample_date_,
            hour = hours_,
            minute = minutes_,
            meridian = meridian_,
            participant_name = participant_name_
    where   barcode = barcode_;
    
    commit;

end;