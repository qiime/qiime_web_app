
create or replace procedure get_otu_failures
(
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  ss.ssu_sequence_id, ss.sequence_string
    from    otu_picking_failures opf
            inner join ssu_sequence ss
            on opf.ssu_sequence_id = ss.ssu_sequence_id;

end;