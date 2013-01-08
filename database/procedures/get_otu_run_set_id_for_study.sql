create or replace 
PROCEDURE "GET_OTU_RUN_SET_ID_FOR_STUDY" 
(
  metadata_study_id IN NUMBER,
  otu_pm_name IN VARCHAR2,
  otu_pm_threshold IN NUMBER,
  otu_pm_ref_set_name IN VARCHAR2,
  otu_pm_ref_set_threshold IN NUMBER,
  otu_rs_id OUT NUMBER,
  otu_pr_id OUT NUMBER
)
as 
begin
  select an.otu_run_set_id,an.otu_picking_run_id into otu_rs_id,otu_pr_id
  from analysis an
  inner join otu_picking_run opr on an.otu_picking_run_id=opr.otu_picking_run_id
  inner join otu_picking_method opm on opr.otu_picking_method_id=opm.otu_picking_method_id
  where an.study_id=metadata_study_id
  and opm.otu_picking_method_name=otu_pm_name
  and opr.threshold=otu_pm_threshold
  and opm.otu_picking_ref_set_name=otu_pm_ref_set_name
  and opm.otu_picking_method_threshold=otu_pm_ref_set_threshold;
end get_otu_run_set_id_for_study;

/*
variable otu_run_set_id NUMBER;
variable otu_pr_id NUMBER;
execute get_otu_run_set_id_for_study(77,'UCLUST_REF',97,'GREENGENES_REFERENCE',97,:otu_run_set_id,:otu_pr_id);
print otu_run_set_id;
print otu_pr_id;
*/