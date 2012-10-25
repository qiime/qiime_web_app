
--------------------------------------------------------
--  DDL for Procedure GET_USER_STUDY_NAMES
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_USER_STUDY_NAMES" 
(
  user_id_ in int,
  results_ in out types.ref_cursor
)
as
begin    

  if user_id_ in (12169, 12171) then

    open results_ for  
      select  s.study_id, '(' || wau.email || ') ' || s.project_name
      from    study s
              inner join user_study us
              on s.study_id = us.study_id
              inner join web_app_user wau
              on us.web_app_user_id = wau.web_app_user_id
      order by wau.email, project_name;
    
  else
  
    open results_ for  
      select  s.study_id, s.project_name
      from    study s
              inner join user_study us
              on s.study_id = us.study_id
      where   us.web_app_user_id = user_id_
      order by project_name;
    
  end if;
    
end;

/*

variable study_names REFCURSOR;
execute get_user_study_names( 12169, :study_names );
print study_names;

*/