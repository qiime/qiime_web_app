create global temporary table ag_map_markers
(
    zipcode varchar2(20), 
    latitude float, 
    longitude float, 
    marker_color varchar2(10),
    order_by integer
) on commit delete rows;

create index ix_ag_map_markers_zip on ag_map_markers (zipcode);
create index ix_ag_map_markers_lat on ag_map_markers (latitude);
create index ix_ag_map_markers_long on ag_map_markers (longitude);
create index ix_ag_map_markers_mc on ag_map_markers (marker_color);
create index ix_ag_map_markers_ob on ag_map_markers (order_by);

-- drop table ag_map_markers;

