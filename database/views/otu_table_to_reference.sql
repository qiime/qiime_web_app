--------------------------------------------------------
--  DDL for View OTU_TABLE_TO_PROKMSA
--------------------------------------------------------


  CREATE OR REPLACE FORCE VIEW "SFF"."OTU_TABLE_TO_REFERENCE" ("SAMPLE_NAME", "REFERENCE_ID", "OTU_PICKING_METHOD_NAME", "OTU_PICKING_METHOD_THRESHOLD", "SOURCE_NAME", "THRESHOLD", "COUNT") AS 
  SELECT distinct ot.sample_name,
    gg.reference_id,
    opm.otu_picking_method_name,
    opm.otu_picking_method_threshold,
    ss.source_name,
    ss.threshold,
    ot.count
  FROM otu_table ot
  INNER JOIN gg_plus_denovo_reference gg
  ON ot.reference_id = gg.reference_id
  INNER JOIN source_map sm
  ON gg.reference_id = sm.reference_id
  INNER JOIN sequence_source ss
  ON sm.sequence_source_id = ss.sequence_source_id
  INNER JOIN otu_run_set ors
  ON ot.otu_run_set_id = ors.otu_run_set_id
  INNER JOIN otu_picking_run opr
  ON ors.otu_run_set_id = opr.otu_run_set_id
  INNER JOIN otu_picking_method opm
  ON opr.otu_picking_method_id = opm.otu_picking_method_id;
 
