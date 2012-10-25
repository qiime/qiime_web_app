
create or replace procedure get_list_values
(
  results in out types.ref_cursor,
  list_name in controlled_vocabs.vocab_name%type
)
as
begin
  open results for
    select  cvv.vocab_value_id, cvv.term
    from    controlled_vocab_values cvv
            inner join controlled_vocabs cv
            on cvv.controlled_vocab_id = cv.controlled_vocab_id
    where   cv.vocab_name = list_name;  
end;

/*

variable results REFCURSOR;
execute get_list_values( :results, 'Package Type' );
print results;

*/
