--------------------------------------------------------
--  DDL for View OTU_TABLE_TO_PROKMSA
--------------------------------------------------------

CREATE OR REPLACE VIEW "SFF"."OTU_TABLE_TO_REFERENCE" 
(
  "SAMPLE_NAME", "REFERENCE_ID", "OTU_PICKING_METHOD_NAME", "OTU_PICKING_METHOD_THRESHOLD", "SOURCE_NAME", "THRESHOLD", "COUNT"
) AS 
select  ot.sample_name, gg.reference_id,  opm.otu_picking_method_name,  opm.otu_picking_method_threshold,
        ss.source_name, ss.threshold, ot.count 
from    otu_table ot
        inner join otu o 
          on ot.otu_id = o.otu_id
        inner join gg_plus_denovo_reference gg 
          on o.ssu_sequence_id = gg.ssu_sequence_id
        inner join source_map sm 
          on gg.reference_id = sm.reference_id
        inner join sequence_source ss 
          on sm.sequence_source_id = ss.sequence_source_id
        inner join otu_run_set ors 
          on ot.otu_run_set_id = ors.otu_run_set_id
        inner join otu_picking_run opr 
          on ors.otu_run_set_id = opr.otu_run_set_id
        inner join otu_picking_method opm 
          on opr.otu_picking_method_id = opm.otu_picking_method_id;