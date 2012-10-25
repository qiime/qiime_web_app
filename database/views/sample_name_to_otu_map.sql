
--------------------------------------------------------
--  DDL for View SAMPLE_NAME_TO_OTU_MAP
--------------------------------------------------------

  CREATE OR REPLACE FORCE VIEW "SFF"."SAMPLE_NAME_TO_OTU_MAP" ("OTU_ID", "SEQUENCE_NAME", "OTU_PICKING_METHOD_NAME", "OTU_PICKING_REF_SET_NAME", "OTU_PICKING_METHOD_THRESHOLD", "THRESHOLD", "SEQ_RUN_ID", "SAMPLE_NAME", "PROKMSA_ID") AS 
  SELECT o.otu_id,
    slrm.sequence_name,
    b.otu_picking_method_name,
    b.otu_picking_ref_set_name,
    b.otu_picking_method_threshold,
    p.threshold,
    slrm.seq_run_id,
    slrm.sample_name,ggr.prokmsa_id
  FROM split_library_read_map slrm
  INNER JOIN ANALYSIS an
  ON slrm.split_library_run_id=an.split_library_run_id
  INNER JOIN OTU_MAP m
  ON slrm.ssu_sequence_id=m.ssu_sequence_id
  AND an.otu_run_set_id =m.otu_run_set_id
  INNER JOIN OTU o
  ON m.otu_id=o.otu_id
  INNER JOIN OTU_PICKING_RUN p
  ON an.otu_run_set_id=p.otu_run_set_id
  INNER JOIN OTU_PICKING_METHOD b
  ON p.otu_picking_method_id=b.otu_picking_method_id
  INNER JOIN SEQUENCE_SOURCE ss on b.otu_picking_ref_set_name=ss.source_name
  and b.otu_picking_method_threshold=ss.threshold
  INNER JOIN SOURCE_MAP sm on ss.sequence_source_id=sm.sequence_source_id
  INNER JOIN GREENGENES_REFERENCE ggr on o.ssu_sequence_id=ggr.ssu_sequence_id and sm.reference_id=ggr.prokmsa_id;
