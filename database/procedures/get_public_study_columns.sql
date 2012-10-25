
--------------------------------------------------------
--  DDL for Procedure GET_PUBLIC_STUDY_COLUMNS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_PUBLIC_STUDY_COLUMNS" 
(
  user_id_ in int,
  is_admin_ in int,
  user_data_ out types.ref_cursor
)as 
begin
  
  if is_admin_ = 1 then
  open user_data_ for
    select  distinct upper(sac.column_name), sac.table_name, sac.study_id
    from    study_actual_columns sac
            inner join sample s on s.study_id = sac.study_id
            inner join study st on sac.study_id = st.study_id
            inner join sff.analysis an on st.study_id = an.study_id
    where   st.metadata_complete = 'y';  
  else 
  open user_data_ for
    select  distinct upper(sac.column_name), sac.table_name, sac.study_id
    from    study_actual_columns sac
            inner join sample s on s.study_id = sac.study_id
            inner join study st on sac.study_id = st.study_id
            inner join user_study us on st.study_id = us.study_id
            inner join sff.analysis an on st.study_id = an.study_id
    where   (s."PUBLIC" = 'y' or us.web_app_user_id = user_id_) 
            and st.metadata_complete = 'y';
  end if;
  
end;

/*
variable user_data REFCURSOR;
execute get_public_study_columns(12171,:user_data);
print user_data;
*/