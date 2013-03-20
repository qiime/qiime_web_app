create or replace procedure ag_delete_participant
(
    ag_login_id_ varchar2,
    participant_name_ varchar2
)
as
begin

    -- Delete the associated samples
    update  ag_kit_barcodes
    set     participant_name = '',
            site_sampled = '',
            sample_time = ''
    where   barcode in
            (
                select  akb.barcode
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = ag_login_id_
                        and akb.participant_name = participant_name_
            );
    
    -- Remove the backup log
    delete  ag_survey_answer
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    -- Remove the multiple answers
    delete  ag_survey_multiples
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    -- Remove the participant/survey/consent
    delete  ag_human_survey
    where   ag_login_id = ag_login_id_
            and participant_name = participant_name_;
            
    commit;

end;