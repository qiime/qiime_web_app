
create or replace procedure get_controlled_vocab_list
(
  controlled_vocab_list in out types.ref_cursor,
  col_name in varchar2
)
as
begin    
  open controlled_vocab_list for  
    select  cv.vocab_name
    from    column_controlled_vocab ccv
            inner join controlled_vocabs cv
            on ccv.controlled_vocab_id = cv.controlled_vocab_id
    where   ccv.column_name = col_name;
end;


/*

variable controlled_vocab_list REFCURSOR;
execute get_controlled_vocab_list( :controlled_vocab_list, 'investigation_type' );
print controlled_vocab_list;

*/
