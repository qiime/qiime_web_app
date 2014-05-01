alter table ag_kit add print_results varchar(1) default ('n');
alter table ag_handout_kits add print_results varchar(1) default('n');
update ag_handout_kits set print_results = 'y';
update ag_handout_kits set print_results = 'n' where kit_id like 'ts_%';
update ag_handout_kits set print_results = 'n' where kit_id like 'pgp_%';
commit;

update ag_kit set print_results = 'y';
update ag_kit set print_results = 'n' where SUPPLIED_KIT_ID like 'ts_%';
update ag_kit set print_results = 'n' where SUPPLIED_KIT_ID like 'pgp_%';
commit;