
create table script
(
  script_id integer primary key,
  script_name varchar(200) not null,
  header_text varchar(4000) default '' not null
);

insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'pick_otus', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'pick_rep_set', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'align_seqs', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'filter_alignment', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'assign_taxonomy', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_phylogeny', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_otu_table', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'beta_diversity', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_3d_plots', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'rarefaction', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'alpha_diversity', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_rarefaction_plots', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'collate_alpha', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_otu_heatmap_html', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'summarize_taxa', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_pie_charts', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_distance_histograms', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'beta_diversity', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'make_2d_plots', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'hierarchical_cluster', '# replace me' );
insert into script (script_id, script_name, header_text) values (script_sequence.nextval, 'tree_compare', '# replace me' );

/*

select * from script;

*/

create table parameter
(
  parameter_id integer primary key,
  script_id integer not null,
  param varchar(200) not null,
  default_value varchar(200) default '' not null,
  constraint fk_script_id 
    foreign key (script_id) 
    references script (script_id)
);

-- Controlled Vocabularies

drop table script;
drop table parameter;