
--------------------------------------------------------
--  DDL for Procedure GET_VALID_CONTROL_VOCAB_TERMS
--------------------------------------------------------
set define off;

  CREATE OR REPLACE PROCEDURE "QIIME_METADATA"."GET_VALID_CONTROL_VOCAB_TERMS" 
(
  column_header IN VARCHAR2,
  user_data OUT types.ref_cursor
)
as 
begin
  open user_data for
    select cvv.vocab_value_id,cvv.term from controlled_vocab_values cvv
    inner join column_controlled_vocab cv on cvv.controlled_vocab_id=cv.controlled_vocab_id
    where upper(cv.column_name)=column_header;
end get_valid_control_vocab_terms;

/* 
variable user_data REFCURSOR;
execute get_valid_control_vocab_terms('SEX',:user_data);
print user_data;
*/
