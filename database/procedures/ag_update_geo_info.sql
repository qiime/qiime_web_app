create or replace procedure ag_update_geo_info
(
    ag_login_id_ raw,
    lat_ float,
    lon_ float,
    cannot_geocode_ char
)
as
begin

    update  ag_login
    set     latitude = lat_,
            longitude = lon_,
            cannot_geocode = cannot_geocode_
    where   ag_login_id = ag_login_id_;
  
  commit;
  
end;