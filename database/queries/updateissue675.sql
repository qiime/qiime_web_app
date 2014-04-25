alter table ag_kit add print_results varchar(1) default ('N');
alter table ag_handout_kits add print_results varchar(1) default('N');
update ag_handout_kits set print_results = 'Y';
update ag_handout_kits set print_results = 'N' where kit_id like 'ts_%';
update ag_handout_kits set print_results = 'N' where kit_id like 'pgp_%';
commit;

update ag_kit set print_results = 'Y';
update ag_kit set print_results = 'N' where SUPPLIED_KIT_ID like 'ts_%';
update ag_kit set print_results = 'N' where SUPPLIED_KIT_ID like 'pgp_%';
commit;