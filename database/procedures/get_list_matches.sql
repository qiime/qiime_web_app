create or replace procedure get_list_matches
(
  col in varchar2,
  val in varchar2,
  results in out types.ref_cursor
)
as
begin

  insert into tmp_id_table (ident)
  select  controlled_vocab_id
  from    column_controlled_vocab
  where   column_name = col;

  open results for
    select  cvv.vocab_value_id, cvv.term
    from    controlled_vocab_values cvv
            inner join tmp_id_table tid
            on cvv.controlled_vocab_id = tid.ident
    where   lower(cvv.term) like '%' || lower(val) || '%'
            and cvv.vocab_value_id > 0;

end;

/*

variable results REFCURSOR;
execute get_list_matches('country', 'zamb', :results);
print results;
commit;

select * from tmp_id_table;

*/