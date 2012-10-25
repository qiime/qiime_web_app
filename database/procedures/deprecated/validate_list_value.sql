
create or replace procedure validate_list_value
(
  list_name in controlled_vocabs.vocab_name%type,
  list_value in controlled_vocab_values.term%type,
  results out int
)
as
begin
  select  cvv.vocab_value_id into results
  from    controlled_vocab_values cvv
          inner join controlled_vocabs cv
          on cvv.controlled_vocab_id = cv.controlled_vocab_id
  where   cv.vocab_name = list_name
          and lower(cvv.term) = lower(list_value);
exception
  when no_data_found then
    results := 0;
end;

/*

set serveroutput on;
declare
  results int;
begin
  validate_list_value( 'Investigation Type', 'eukaryote', results );
  dbms_output.put_line(results);
end;

*/