create or replace
package qiime_assets
as

procedure find_metadata_table
(
  tab_name in out types.ref_cursor
);

procedure get_column_details
(
  column_details in out types.ref_cursor,
  col_name in varchar2
);

procedure get_column_dictionary
(
  dictionary_values in out types.ref_cursor
);

procedure get_column_ontologies
(
  col in varchar2,
  results in out types.ref_cursor
);

procedure get_controlled_vocab_list_all
(
  controlled_vocab_list in out types.ref_cursor
);

procedure get_controlled_vocab_list
(
  controlled_vocab_list in out types.ref_cursor,
  col_name in varchar2
);

procedure get_controlled_vocab_values
(
  controlled_vocab_id_ in int,
  results in out types.ref_cursor
);

procedure get_distinct_column_values
(
  column_name in varchar,
  column_values in out types.ref_cursor
);

procedure get_field_details
(
  field_name in varchar2,
  results in out types.ref_cursor
);

procedure get_list_matches
(
  col in varchar2,
  val in varchar2,
  results in out types.ref_cursor
);

procedure get_list_values
(
  results in out types.ref_cursor,
  list_name in controlled_vocabs.vocab_name%type
);

procedure get_ontology_list
(
  ontology_list in out types.ref_cursor,
  col_name in varchar2
);

procedure get_package_columns
(
  pack_type_id in int,
  results in out types.ref_cursor
);

procedure get_study_info
(
  study_id_ in int,
  web_app_user_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_study_names 
(
  study_names in out types.ref_cursor
);

procedure get_study_packages
(
  stdy_id in int,
  results in out types.ref_cursor
);

procedure get_user_study_names
(
  user_id_ in int,
  is_admin_ in int,
  portal_type_ in varchar2,
  results_ in out types.ref_cursor
);

procedure host_insert
(
  stud_id in int,
  samp_name in varchar2,
  host_subj_id in varchar2
);

procedure prep_insert
(
  study_id_ in int,
  sample_name_ in varchar2,
  row_number_ in number,
  barcode_ in varchar2, 
  linker_ in varchar2, 
  primer_ in varchar2, 
  run_prefix_ in varchar2
);

procedure sample_insert
(
  study_id_ in int,
  sample_name_ in varchar2
);

procedure study_insert
(
  study_id_ in out int,
  user_id_ in int,
  project_name_ in varchar2,
  investigation_type_ in int,
  miens_comp_ in varchar2,
  submit_ in varchar2,
  portal_type_ in varchar2,
  study_title_ in varchar2,
  study_alias_ in varchar2, 
  pmid_ in varchar2, 
  study_abstract_ in varchar2, 
  study_description_ in varchar2,
  principal_investigator_ in varchar2, 
  principal_investigator_contac_ in varchar2, 
  lab_person_ in varchar2, 
  lab_person_contact_ in varchar2,
  includes_timeseries_ in int
);

procedure study_update
(
  study_id_ in int,
  study_name_ in varchar2,
  investigation_type_ in int,
  miens_comp_ in varchar2,
  submit_ in varchar2,
  portal_type_ in varchar2,
  study_title_ in varchar2,
  study_alias_ in varchar2, 
  pmid_ in varchar2, 
  study_abstract_ in varchar2, 
  study_description_ in varchar2,
  principal_investigator_ in varchar2, 
  principal_investigator_contac_ in varchar2, 
  lab_person_ in varchar2, 
  lab_person_contact_ in varchar2,
  includes_timeseries_ in int
);

procedure emp_study_insert
(
  study_id_ in out int,
  user_id_ in int,
  project_name_ in varchar2,
  investigation_type_ in int,
  miens_comp_ in varchar2,
  submit_ in varchar2,
  portal_type_ in varchar2,
  study_title_ in varchar2,
  study_alias_ in varchar2, 
  pmid_ in varchar2, 
  study_abstract_ in varchar2, 
  study_description_ in varchar2,
  number_samples_collected_ in varchar2, 
  number_samples_promised_ in varchar2, 
  lab_person_ in varchar2,
  lab_person_contact_ in varchar2, 
  emp_person_ in varchar2, 
  first_contact_ in varchar2, 
  most_recent_contact_ in varchar2, 
  sample_type_ in varchar2, 
  has_physical_specimen_ in varchar2, 
  has_extracted_data_ in varchar2, 
  timeseries_ in varchar2, 
  spatial_series_ in varchar2,
  principal_investigator_ in varchar2, 
  principal_investigator_contac_ in varchar2,
  default_emp_status_ in varchar2, 
  funding_ in varchar2,
  includes_timeseries_ in int
);

procedure emp_study_update
(
  study_id_ in int,
  study_name_ in varchar2,
  investigation_type_ in int,
  miens_comp_ in varchar2,
  submit_ in varchar2,
  portal_type_ in varchar2,
  study_title_ in varchar2,
  study_alias_ in varchar2, 
  pmid_ in varchar2, 
  study_abstract_ in varchar2, 
  study_description_ in varchar2,
  number_samples_collected_ in varchar2, 
  number_samples_promised_ in varchar2, 
  lab_person_ in varchar2,
  lab_person_contact_ in varchar2, 
  emp_person_ in varchar2, 
  first_contact_ in varchar2, 
  most_recent_contact_ in varchar2, 
  sample_type_ in varchar2, 
  has_physical_specimen_ in varchar2, 
  has_extracted_data_ in varchar2, 
  timeseries_ in varchar2, 
  spatial_series_ in varchar2,
  principal_investigator_ in varchar2, 
  principal_investigator_contac_ in varchar2,
  default_emp_status_ in varchar2, 
  funding_ in varchar2,
  includes_timeseries_ in int
);

procedure study_packages_insert
(
  stud_id in int,
  env_pkg in int
);

procedure study_packages_delete
(
  study_id_ in int
);

procedure validate_list_value
(
  list_name in controlled_vocabs.vocab_name%type,
  list_value in controlled_vocab_values.term%type,
  results out int
);
/*
procedure get_new_queue_jobs
(
  results in out types.ref_cursor
);
*/
procedure update_job_status
(
  jid in qiime_queue.job_id%type,
  new_status in qiime_queue.status%type
);

procedure update_metadata_flag
(
  study_id_ in study.study_id%type,
  status_ in study.metadata_complete%type
);
/*
procedure create_queue_job
(
  study_id_ in qiime_queue.study_id%type, 
  user_id_ in qiime_queue.user_id%type, 
  mapping_file_ in qiime_queue.mapping_file%type, 
  sff_file_ in qiime_queue.sff_file%type, 
  job_id_ in out qiime_queue.job_id%type
);

procedure get_job_info
(
  study_id_ in qiime_queue.study_id%type,
  results in out types.ref_cursor
);
*/
procedure get_minimal_mapping_data 
(
  run_id in varchar2,
  mapping_values in out types.ref_cursor
);

procedure add_seq_file
(
  study_id_ in int,
  path_ in varchar2,
  file_type_ in varchar2
);

procedure add_mapping_file
(
  study_id_ in int,
  mapping_file_path_ in varchar2
);

procedure add_template_file
(
  study_id_ in int,
  template_file_path_ in varchar2
);

procedure clear_study_templates
(
  study_id_ in int
);

procedure get_sff_files
(
  study_id_ in int,
  results in out types.ref_cursor
);

procedure get_mapping_files
(
  study_id_ in int,
  results in out types.ref_cursor
);

procedure get_metadata_fields
(
  study_id_ in int,
  results in out types.ref_cursor
);

procedure get_sample_list
(
  study_id_ in int,
  results in out types.ref_cursor
);

procedure get_sample_detail_list
(
  study_id_ in int,
  results in out types.ref_cursor
);

procedure get_prep_list
(
  sample_id_ in int,
  results in out types.ref_cursor
);

procedure add_study_actual_column
(
  study_id_ in int,
  column_name_ in varchar2,
  table_name_ in varchar2
);

procedure remove_study_actual_column
(
  study_id_ in int,
  column_name_ in varchar2
);

procedure get_study_actual_columns
(
  study_id_ in int,
  results_ in out types.ref_cursor
);

procedure prepare_study_for_update
(
  study_id_ in int
);

procedure study_delete
(
  study_id_ in int,
  full_delete in int
);

procedure extra_column_metadata_insert
(
  study_id_ in int,
  table_level_ in varchar2,
  column_name_ in varchar2,
  description_ in varchar2,
  data_type_ in varchar2
);

procedure get_study_extra_columns
(
  study_id_ in int,
  results_ in out types.ref_cursor
);

procedure find_extra_column_match 
(
  column_name_ in varchar2,
  results_ in out types.ref_cursor
);

procedure delete_study_extra_columns
(
  study_id_ in int
);

procedure get_split_libarary_data
(
  study_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_run_prefix_bc_lengths
(
  study_id_ in int,
  run_prefix_ in varchar2,
  results_ in out types.ref_cursor
);

procedure clear_sff_file
(
  study_id_ in int,
  sff_file_ in varchar2
);

procedure clear_split_lib_map_files
(
  study_id_ in int
);

procedure authenticate_user
(
  username in VARCHAR2,
  pwd in VARCHAR2,
  user_data in out types.ref_cursor
);

procedure get_user_details
(
  user_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_sample_ids_from_study
(
  study_id_ in int,
  results_ in out types.ref_cursor
);
 
procedure get_sequences_for_fasta
(
  study_id_ in int,
  sample_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_sequences_for_fasta_fulldb
(
  results_ in out types.ref_cursor
);

procedure get_list_field_value
(
  vocab_value_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_emp_sample_list
(
  study_id_ in int,
  web_app_user_id_ int,
  results_ in out types.ref_cursor
);
 
procedure update_emp_sample_data
(
  sample_id_ in int,
  sample_score_ in int,
  emp_status_ in int,
  web_app_user_id_ in int
);
  
procedure update_emp_study_data
(
  study_id_ in int,
  study_score_ in int,
  web_app_user_id_ in int
);

procedure get_study_platform
(
  study_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_study_templates
(
  study_id_ in int,
  results_ in out types.ref_cursor
);

procedure get_immutable_database_fields
(
  study_id_ in int,
  results_ in out types.ref_cursor
);

end qiime_assets;
 