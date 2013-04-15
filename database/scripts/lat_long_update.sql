alter table ag_login add latitude float;
alter table ag_login add longitude float;
alter table ag_login add cannot_geocode char(1);

update
(
    select  z.latitude as zlat, 
            z.longitude as zlong, 
            z.zipcode as zzip,
            ag.latitude as aglat,
            ag.longitude as aglong,
            ag.zip as agzip
    from    zipcodes z
            inner join ag_login ag
            on z.zipcode = ag.zip
    where   z.zipcode = ag.zip
            and ag.latitude is null
            and ag.longitude is null
) x
set     x.aglat = x.zlat,
        x.aglong = x.zlong;

commit;

--select * from ag_login where latitude is null;

select city, state, zip, country, cast(ag_login_id as varchar2(100)) from ag_login where latitude is null and cannot_geocode is null;


update ag_login set cannot_geocode = '';
commit;

select * from ag_login where latitude is null and cannot_geocode is null;

select * from ag_login where cannot_geocode is not null;
select * from ag_login where latitude is null;