create or replace procedure ag_get_map_markers
(
    results_ in out types.ref_cursor
)
as
begin

    -- Highest priority: completed
    insert  into ag_map_markers
            (zipcode, latitude, longitude, marker_color, order_by)
    select  agl.zip, agl.latitude, agl.longitude, '00FF00', 0
    from    ag_login agl
    where   (
                select  count(*)
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = agl.ag_login_id
            ) =
            (
                select  count(*)
                from    ag_kit_barcodes akb
                        inner join ag_kit ak
                        on akb.ag_kit_id = ak.ag_kit_id
                where   ak.ag_login_id = agl.ag_login_id
                        and akb.site_sampled is not null
            );
    
    -- Second priority: verified
    insert  into ag_map_markers
            (zipcode, latitude, longitude, marker_color, order_by)
    select  agl.zip, agl.latitude, agl.longitude, 'FFFF00', 1
    from    ag_login agl
    where   (
                select  count(*)
                from    ag_kit ak
                where   ak.ag_login_id = agl.ag_login_id
                        and kit_verified = 'y'
            ) > 0
            and agl.zip not in
            (
                select  zipcode
                from    ag_map_markers
            );
            
    -- Finally, existing participants
    insert  into ag_map_markers
            (zipcode, latitude, longitude, marker_color, order_by)
    select  agl.zip, agl.latitude, agl.longitude, '00B2FF', 2
    from    ag_login agl
    where   agl.zip not in
            (
                select  zipcode
                from    ag_map_markers
            );

    open results_ for
        select  zipcode, latitude, longitude, marker_color
        from    ag_map_markers
        order by order_by desc;
end;

