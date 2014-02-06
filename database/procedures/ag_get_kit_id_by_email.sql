create or replace PROCEDURE AG_GET_KIT_ID_BY_EMAIL(
      email_ in varchar2,
      user_data_ OUT types.ref_cursor
)AS 
BEGIN
     open user_data_ for
         select  k.supplied_kit_id 
         from ag_kit k 
              inner join ag_login l 
              on k.ag_login_id = l.ag_login_id 
         where l.email = email_; 

END AG_GET_KIT_ID_BY_EMAIL;

/*variable user_data_ REFCURSOR;
execute ag_get_kit_id_by_email('ejteravest@gmail.com', :user_data_);
print user_data_;
*/