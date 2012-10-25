
create or replace procedure get_controlled_vocab_values
(
  controlled_vocab_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  vocab_value_id, term
    from    controlled_vocab_values
    where   controlled_vocab_id = controlled_vocab_id_
            and vocab_value_id > 0
    order by  term;

end;

/*

variable results REFCURSOR;
execute get_controlled_vocab_values(1, :results);
print results;

*/