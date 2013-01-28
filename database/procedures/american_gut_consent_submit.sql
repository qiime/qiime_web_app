create or replace procedure 
american_gut_consent_submit
(
  participant_name_ in varchar2,
  contact_code_ in varchar2,
  is_7_to_3_ in varchar2,
  parent_1_name_ in varchar2,
  parent_2_name_ in varchar2,
  parent_1_code_ in varchar2,
  parent_2_code_ in varchar2,
  deceased_parent_ in varchar2
)
as
begin

    insert  into american_gut_consent  
            (participant_name, contact_code,is_7_to_3, parent_1_name,
            parent_2_name, parent_1_code, parent_2_code, deceased_parent)
    values  (participant_name_, contact_code_,is_7_to_3_, parent_1_name_,
            parent_2_name_, parent_1_code_, parent_2_code_, deceased_parent_);
            
    commit;
  
end;

/*

drop table american_gut_consent;

create table american_gut_consent
(
    participant_name varchar2(200), 
    contact_code varchar2(200),
    is_7_to_3 varchar2(10),
    parent_1_name varchar2(200),
    parent_2_name varchar2(200), 
    parent_1_code varchar2(200), 
    parent_2_code varchar2(200),
    deceased_parent varchar2(10)
);

*/
 