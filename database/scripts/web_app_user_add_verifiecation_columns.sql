alter table web_app_user
  add activation_code varchar2(20 char) null;
  
alter table web_app_user
  add verified char(1) default 'n' not null;
  
update  web_app_user
set     verified = 'y';
commit;