insert into sequence_source (sequence_source_id, source_name, threshold, version)
values (9, '454V2', 97, '5jan2012');

insert into sequence_source (sequence_source_id, source_name, threshold, version)
values (10, '454V4', 97, '5jan2012');
commit;

insert  into otu_picking_method 
        (otu_picking_method_id, otu_picking_method_name, otu_picking_ref_set_name, otu_picking_method_threshold)
values  (8, 'UCLUST', '454V2', 97);
commit;

insert  into otu_picking_method 
        (otu_picking_method_id, otu_picking_method_name, otu_picking_ref_set_name, otu_picking_method_threshold)
values  (9, 'UCLUST', '454V4', 97);
commit;

alter table otu_run_set drop column otu_picking_run_id;
alter table otu_picking_failures add processed integer default 0;


create table gg_plus_denovo_reference
(
  genbank_acc_id varchar2(40) null,
  decision varchar2(50) null,
  core_set_member number(1),
  ssu_sequence_id number(24) not null,
  sequence_source_id number not null,
  reference_id varchar2(200) not null,
  
  constraint pk_gg_pl_deno_ref_ref_id primary key (reference_id)
);

create index ggd_PROK_SSU_ID on gg_plus_denovo_reference (REFERENCE_ID, SSU_SEQUENCE_ID);
create index ggd_REF_SSU_ID_INDEX on gg_plus_denovo_reference (SSU_SEQUENCE_ID);
create index ggd_REF_SSU_ID on gg_plus_denovo_reference (SEQUENCE_SOURCE_ID);

create table gg_plus_denovo_taxonomy
(
  taxonomy_name varchar2(1000) null,
  taxonomy_str varchar2(1000) null,
  reference_id varchar2(200) not null,
  
  constraint fk_gg_taxa_to_ref_ref_id foreign key (reference_id)
    references gg_plus_denovo_reference (reference_id)
);

create index idx_gg_taxon_ref_name on gg_plus_denovo_taxonomy(reference_id, TAXONOMY_NAME);
create index idx_gg_taxon_name on gg_plus_denovo_taxonomy(TAXONOMY_NAME);
create index idx_gg_taxon_ref on gg_plus_denovo_taxonomy(reference_id);

insert  into gg_plus_denovo_reference
        (genbank_acc_id, decision, core_set_member, ssu_sequence_id, sequence_source_id, reference_id)
select  genbank_acc_id, decision, core_set_member, ssu_sequence_id, sequence_source_id, prokmsa_id
from    greengenes_reference;
commit;

insert  into gg_plus_denovo_taxonomy
        (taxonomy_name, taxonomy_str, reference_id)
select  taxonomy_name, taxonomy_str, prokmsa_id
from    greengenes_taxonomy;
commit;








alter table otu_table add reference_id varchar2(200);

merge into otu_table o
using
(
  select  ot.rowid as rid, r.reference_id as ref_id
  from    otu_table ot
          inner join otu o
          on ot.otu_id = o.otu_id
          inner join gg_plus_denovo_reference r
          on o.ssu_sequence_id = r.ssu_sequence_id
          inner join source_map s
          on r.reference_id = s.reference_id
  where   s.sequence_source_id = 4
)
on (o.rowid = rid)
when matched then
  update set reference_id = ref_id;

commit;

alter table otu_table modify (reference_id varchar2(200) not null);

drop table otu_map;
drop table otu;






