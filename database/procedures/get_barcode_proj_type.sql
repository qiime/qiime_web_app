create or replace procedure get_barcode_proj_type
(
   barcode_ in varchar2,
   proj_type_ out types.ref_cursor
)
as
begin

    open proj_type_ for
        select  p.project
        from    project_barcode pb
                inner join project p
                on pb.project_id = p.project_id
        where   pb.barcode = barcode_;

end;
