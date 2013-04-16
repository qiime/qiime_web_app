create or replace
package body qiime_assets
as
  
procedure find_metadata_table
(
  tab_name in out types.ref_cursor
)
as
begin

  open tab_name for
  
    select  distinct table_name, column_name
    from    all_tab_columns
    where   owner = 'QIIME_METADATA'
            and (
                  table_name in ('AIR', 'COMMON_EXTRA_PREP', 'COMMON_EXTRA_SAMPLE', 'COMMON_FIELDS', 'HOST', 'HOST_ASSOC_VERTIBRATE', 'HOST_ASSOCIATED_PLANT', 'HOST_SAMPLE', 'HUMAN_ASSOCIATED', 'MICROBIAL_MAT_BIOFILM', 'OTHER_ENVIRONMENT', 'SAMPLE', 'SAMPLE_SEQUENCE_PREP', 'SEDIMENT', 'SEQUENCE_PREP', 'SOIL', 'STUDY', 'WASTEWATER_SLUDGE', 'WATER')
                  or table_name like 'EXTRA_SAMPLE_%'
                  or table_name like 'EXTRA_PREP_%'
                )
    order by table_name, column_name;
    
  /*
    select  table_name
    from    all_tab_columns
    where   column_name = upper(col_name)
            and owner = 'QIIME_METADATA';
  */

end;

/*

variable tab_name REFCURSOR;
execute find_metadata_table('COUNTRY', :tab_name);
print tab_name;

select column_name from all_tab_columns

*/

procedure get_column_details
(
  column_details in out types.ref_cursor,
  col_name in varchar2
)
as
begin    
  open column_details for  
    select  data_type
    from    column_dictionary 
    where   column_name = col_name
            and active = 1;
end;


/*

variable column_details REFCURSOR;
execute get_column_details( :column_details, 'drug_usage' );
print column_details;

*/

procedure get_column_dictionary
(
  dictionary_values in out types.ref_cursor
)
as
begin    
  open dictionary_values for  
    select  cd.column_name, cd.desc_or_value, cd.definition, cd.data_type, 
            atc.data_length, cd.min_length, cd.active
    from    column_dictionary cd
            left join all_tab_columns atc
    --from    all_tab_columns atc
    --        left join column_dictionary cd
            on upper(cd.column_name) = upper(atc.column_name)
              and atc.owner = 'QIIME_METADATA'
    order by  column_name;
end;

/*

variable dictionary_values REFCURSOR;
execute get_column_dictionary( :dictionary_values );
print dictionary_values;

select * from all_tab_columns where owner = 'QIIME_TEST'

*/

procedure get_column_ontologies
(
  col in varchar2,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  ontology_short_name, bioportal_id, ontology_branch_id
    from    column_ontology
    where   column_name = col;

end;

/*

variable results REFCURSOR;
execute get_column_ontologies('body_habitat', :results);
print results;

*/

procedure get_controlled_vocab_list_all
(
  controlled_vocab_list in out types.ref_cursor
)
as
begin    
  open controlled_vocab_list for  
    select  controlled_vocab_id, vocab_name
    from    controlled_vocabs
    order by  vocab_name;
end;


/*

variable controlled_vocab_list REFCURSOR;
execute get_controlled_vocab_list( :controlled_vocab_list, 'investigation_type' );
print controlled_vocab_list;

*/

procedure get_controlled_vocab_list
(
  controlled_vocab_list in out types.ref_cursor,
  col_name in varchar2
)
as
begin    
  open controlled_vocab_list for  
    select  cv.vocab_name
    from    column_controlled_vocab ccv
            inner join controlled_vocabs cv
            on ccv.controlled_vocab_id = cv.controlled_vocab_id
    where   ccv.column_name = col_name;
end;


/*

variable controlled_vocab_list REFCURSOR;
execute get_controlled_vocab_list( :controlled_vocab_list, 'investigation_type' );
print controlled_vocab_list;

*/

procedure get_controlled_vocab_values
(
  controlled_vocab_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  vocab_value_id, term
    from    controlled_vocab_values
    where   controlled_vocab_id = controlled_vocab_id_
            and vocab_value_id > 0
    order by  term;

end;

/*

variable results REFCURSOR;
execute get_controlled_vocab_values(1, :results);
print results;

*/

procedure get_distinct_column_values
(
  column_name in varchar,
  column_values in out types.ref_cursor
)
as
begin
    
  open column_values for
    'select distinct ' || column_name || ' from microbe_metadata order by ' || column_name;

end;

/*

variable column_values REFCURSOR;
execute get_distinct_column_values( 'study_name', :column_values );
print column_values;

variable column_values REFCURSOR;
execute get_distinct_column_values( 'host_age', :column_values );
print column_values;

*/

procedure get_field_details
(
  field_name in varchar2,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  column_name, data_type, desc_or_value, definition, active
    from    column_dictionary
    where   column_name = field_name;

end;

/*

variable results REFCURSOR;
execute qiime_assets.get_field_details( 'investigation_type', :results );
print results;

*/

procedure get_list_matches
(
  col in varchar2,
  val in varchar2,
  results in out types.ref_cursor
)
as
begin

  insert into tmp_id_table (ident)
  select  controlled_vocab_id
  from    column_controlled_vocab
  where   column_name = col;

  open results for
    select  cvv.vocab_value_id, cvv.term
    from    controlled_vocab_values cvv
            inner join tmp_id_table tid
            on cvv.controlled_vocab_id = tid.ident
    where   lower(cvv.term) like '%' || lower(val) || '%'
            and cvv.vocab_value_id > 0;

end;

/*

variable results REFCURSOR;
execute get_list_matches('country', 'zamb', :results);
print results;
commit;

select * from tmp_id_table;

*/

procedure get_list_values
(
  results in out types.ref_cursor,
  list_name in controlled_vocabs.vocab_name%type
)
as
begin
  open results for
    select  cvv.vocab_value_id, cvv.term
    from    controlled_vocab_values cvv
            inner join controlled_vocabs cv
            on cvv.controlled_vocab_id = cv.controlled_vocab_id
    where   cv.vocab_name = list_name;  
end;

/*

variable results REFCURSOR;
execute get_list_values( :results, 'Package Type' );
print results;

*/

procedure get_ontology_list
(
  ontology_list in out types.ref_cursor,
  col_name in varchar2
)
as
begin    
  open ontology_list for  
    select  oo.ontology_short_name
    from    column_ontology oo
    where   oo.column_name = col_name;
end;


/*

variable ontology_list REFCURSOR;
execute get_ontology_list( :ontology_list, 'body_habitat' );
print ontology_list;

*/

procedure get_package_columns
(
  pack_type_id in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  cd.column_name, sc.required, cd.data_type, cd.desc_or_value, cd.definition 
    from    column_dictionary cd
            inner join study_columns sc
            on cd.column_name = sc.column_name
    where   sc.package_type_id = pack_type_id
            and cd.active = 1;

end;

/*

variable results REFCURSOR;
execute get_package_columns( 1, :results );
print results;

*/

procedure get_study_info
(
  study_id_ in int,
  web_app_user_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  s.submit_to_insdc, cvv0.term as investigation_type, 
            s.project_name, s.experimental_factor, 
            s.study_alias, s.study_title, 
            (
              select  term
              from    controlled_vocab_values
              where   vocab_value_id = s.study_type
            ) as study_type,
            s.study_abstract, s.study_description, s.center_name, s.center_project_name, 
            s.project_id, 
            case
              when s.pmid is null then ' '
              else s.pmid
            end as pmid, 
            s.metadata_complete,
            case 
              when exists 
              (
                select  study_id 
                from    study_files sf
                where   s.study_id = sf.study_id
                        and (sf.file_type = 'SFF' or sf.file_type = 'FASTQ' or sf.file_type = 'FNA')
              ) then 'y'
              else 'n'
            end as sff_complete,
            case 
              when exists 
              (
                select  study_id 
                from    study_files sf
                where   s.study_id = sf.study_id
                        and sf.file_type = 'MAPPING'
              ) then 'y'
              else 'n'
            end as mapping_file_complete,
            s.miens_compliant,
            case
              when exists
              (
                select  *
                from    sample sa
                where   s.study_id = sa.study_id
                        and sa."PUBLIC" = 'y'
              ) then 'n'
              else 'y'
            end as can_delete,
            (
              select  avg(emp_score)
              from    study_emp_score
              where   study_id = s.study_id
            ) as avg_emp_score,
            ses.emp_score as user_emp_score, 
            number_samples_promised,
            number_samples_collected, 
            case
              when principal_investigator is null then ' '
              else principal_investigator
            end as principal_investigator,
            (
              select  count(*)
              from    sample
              where   study_id = s.study_id
            ) as sample_count,
            case
              when lab_person is null then ' '
              else lab_person
            end as lab_person, 
            case 
              when lab_person_contact is null then ' '
              else lab_person_contact
            end as lab_person_contact, 
            case
              when emp_person is null then ' '
              else emp_person
            end as emp_person, 
            case
              when first_contact is null then ' '
              else first_contact
            end as first_contact,
            case
              when most_recent_contact is null then ' '
              else most_recent_contact
            end as most_recent_contact, 
            case
              when sample_type is null then ' '
              else sample_type
            end as sample_type, 
            case
              when has_physical_specimen is null then ' '
              else has_physical_specimen
            end as has_physical_specimen,
            case
              when has_extracted_data is null then ' '
              else has_extracted_data
            end as has_extracted_data, 
            case
              when timeseries is null then ' '
              else timeseries
            end as timeseries, 
            case
              when spatial_series is null then ' '
              else spatial_series
            end as spatial_series,
            case
              when principal_investigator is null then ' '
              else principal_investigator
            end as principal_investigator, 
            case
              when principal_investigator_contact is null then ' '
              else principal_investigator_contact
            end as principal_investigator_contact,
            (
              select  term
              from    controlled_vocab_values
              where   vocab_value_id = s.default_emp_status
            ) as default_emp_status,
            case
              when funding is null then ' '
              else funding
            end as funding,
            includes_timeseries,
            (
              select  count(*)
              from    sample sa
              where   s.study_id = sa.study_id
            ) as sample_count,
            ebi_study_accession,
            locked
    from    study s
            inner join controlled_vocab_values cvv0
            on s.investigation_type = cvv0.vocab_value_id
            left join study_emp_score ses
            on s.study_id = ses.study_id
              and ses.web_app_user_id = web_app_user_id_
    where   s.study_id = study_id_;

end;

/*

variable results REFCURSOR;
execute qiime_assets.get_study_info(2, :results);
print results;

*/

procedure get_study_names 
(
  study_names in out types.ref_cursor
)
AS
BEGIN
  OPEN study_names FOR 
    select  distinct project_name 
    from    study;
END;

/*

variable study_names REFCURSOR;
execute get_study_names( :study_names );
print study_names;

*/

procedure get_study_packages
(
  stdy_id in int,
  results in out types.ref_cursor
)
as
begin
  
  open results for
    select  env_package
    from    study_packages
    where   study_id = stdy_id
    order by env_package;

end;

/*

variable results REFCURSOR;
execute get_study_packages(17, :results);
print results;


select * from study_packages
*/

procedure get_user_study_names
(
  user_id_ in int,
  is_admin_ in int,
  portal_type_ in varchar2,
  results_ in out types.ref_cursor
)
as
begin

  -- If the user_id = 0, no user specified so show only
  -- studies with fully public data
  if user_id_ = 0 then
  
    open results_ for  
      select  s.study_id, s.project_name,s.study_title,s.study_abstract
      from    study s
              inner join user_study us
              on s.study_id = us.study_id
              inner join web_app_user wau
              on us.web_app_user_id = wau.web_app_user_id
      where   (
                select  count(*)
                from    sample sa2
                where   sa2.study_id = s.study_id
                        and sa2."PUBLIC" = 'n'
              ) = 0
              and
              (
                select  count(*)
                from    sample sa2
                where   sa2.study_id = s.study_id
              ) > 0
              and s.project_name is not null
              and s.portal_type = portal_type_
      order by s.project_name;

  elsif is_admin_ = 1 then

    open results_ for  
      select  distinct s.study_id, s.project_name, s.study_title, s.study_abstract
      from    study s
              inner join user_study us
              on s.study_id = us.study_id
              inner join web_app_user wau
              on us.web_app_user_id = wau.web_app_user_id
      where   s.project_name is not null
              and s.portal_type = portal_type_
      order by project_name;
    
  else
  
    open results_ for  
      select  s.study_id, s.project_name,s.study_title,s.study_abstract
      from    study s
              inner join user_study us
              on s.study_id = us.study_id
      where   us.web_app_user_id = user_id_
              and s.portal_type = portal_type_
      order by project_name;
    
  end if;
    
end;


/*

variable study_names REFCURSOR;
execute get_user_study_names( 10020, :study_names );
print study_names;

*/

procedure host_insert
(
  stud_id in int,
  samp_name in varchar2,
  host_subj_id in varchar2
)
as
  h_id int;
  samp_id int;
begin

  merge into host
  using dual
  on (dual.dummy is not null and host.host_subject_id = host_subj_id)
  when not matched then insert (host_id, host_subject_id) values (seq_host.nextval, host_subj_id);
  
  select  host_id into h_id
  from    host h
  where   host_subject_id = host_subj_id;
  
  select  sample_id into samp_id
  from    study st
          inner join "SAMPLE" sa
          on st.study_id = sa.study_id
  where   st.study_id = stud_id
          and sa.sample_name = samp_name;
  
  merge into host_sample
  using dual
  on (dual.dummy is not null and host_sample.host_id = h_id and host_sample.sample_id = samp_id)
  when not matched then insert (host_id, sample_id) values (h_id, samp_id);
  
  commit;
  
end;

/*

execute host_insert(2, 'F2M.2', 'F2');
select * from study;
select * from host;
select * from host_sample;

*/

procedure prep_insert
(
  study_id_ in int,
  sample_name_ in varchar2,
  row_number_ in number,
  barcode_ in varchar2, 
  linker_ in varchar2, 
  primer_ in varchar2, 
  run_prefix_ in varchar2
)
as
  sample_id_ int;
begin

  select  sample_id into sample_id_
  from    "SAMPLE" sa
          inner join study st
          on sa.study_id = st.study_id
  where   sa.sample_name = sample_name_
          and st.study_id = study_id_;

  merge into sequence_prep
  using dual
  on 
  (
    dual.dummy is not null
    and sequence_prep.sample_id = sample_id_
    and nvl(sequence_prep.barcode, 'none') = nvl(barcode_, 'none')
    and nvl(sequence_prep.linker, 'none') = nvl(linker_, 'none')
    and nvl(sequence_prep.primer, 'none') = nvl(primer_, 'none')
    and nvl(sequence_prep.run_prefix, 'none') = nvl(run_prefix_, 'none')
  )
  when not matched then 
    insert (sequence_prep_id, sample_id, row_number, barcode, linker, primer, run_prefix) 
    values (seq_prep.nextval, sample_id_, row_number_, barcode_, linker_, primer_, run_prefix_)
  when matched then
    update
      set row_number = row_number_;
  
  commit;
  
end;

/*

execute prep_insert(2, 'F2M.2');
select * from sequence_prep;
select * from study;

*/

procedure sample_insert
(
  study_id_ in int,
  sample_name_ in varchar2
)
as
begin

  merge into "SAMPLE"
  using dual
  on (dual.dummy is not null and "SAMPLE".SAMPLE_NAME = sample_name_  and "SAMPLE".study_id = study_id_)
  when not matched then insert (sample_id, study_id, sample_name) values (seq_sample.nextval, study_id_, sample_name_);
  
  commit;

end;

/*

execute sample_insert(2, 'BF1.2');
select * from sample;
select * from study;

*/

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
)
as
begin
  
  insert  into study (study_id, project_name, investigation_type, submit_to_insdc, miens_compliant, portal_type,
          study_title, study_alias, pmid, study_abstract, study_description, 
          principal_investigator, principal_investigator_contact, lab_person, lab_person_contact, includes_timeseries)
  values  (seq_study.nextval, project_name_, investigation_type_, submit_, miens_comp_, portal_type_,
          study_title_, study_alias_, pmid_, study_abstract_, study_description_, 
          principal_investigator_, principal_investigator_contac_, lab_person_, lab_person_contact_, includes_timeseries_)
  returning study_id into study_id_;
  
  insert  into user_study (web_app_user_id, study_id)
  values  (user_id_, study_id_);
  
  commit;

end;

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
)
as
begin
  
  update  study
  set     project_name = study_name_,
          investigation_type = investigation_type_, 
          submit_to_insdc = submit_, 
          miens_compliant = miens_comp_, 
          portal_type = portal_type_,
          study_title = study_title_, 
          study_alias = study_alias_, 
          pmid = pmid_, 
          study_abstract = study_abstract_, 
          study_description = study_description_,
          principal_investigator = principal_investigator_, 
          principal_investigator_contact = principal_investigator_contac_, 
          lab_person = lab_person_, 
          lab_person_contact = lab_person_contact_,
          includes_timeseries = includes_timeseries_
  where   study_id = study_id_;
  
  commit;

end;

/*

variable stdy_id NUMBER;
execute study_insert(1, 'test_study_2', 'eukaryote', 'human-gut', 'complete', 'y', 'n', :stdy_id);
print std_id;

select * from user_study;
select * from study;

delete from user_study;
delete from study;
commit;
*/

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
)
as
begin
  
  insert  into study 
          (study_id, project_name, investigation_type, submit_to_insdc, miens_compliant, portal_type,
          study_title, study_alias, pmid, study_abstract, study_description,
          number_samples_collected, number_samples_promised, lab_person, lab_person_contact, 
          emp_person, first_contact, most_recent_contact, sample_type, has_physical_specimen, 
          has_extracted_data, timeseries, spatial_series, principal_investigator, 
          principal_investigator_contact, default_emp_status, funding, includes_timeseries)
  values  (seq_study.nextval, project_name_, investigation_type_, submit_, miens_comp_, portal_type_,
          study_title_, study_alias_, pmid_, study_abstract_, study_description_,
          number_samples_collected_, number_samples_promised_, lab_person_, lab_person_contact_, 
          emp_person_, first_contact_, most_recent_contact_, sample_type_, has_physical_specimen_, 
          has_extracted_data_, timeseries_, spatial_series_, principal_investigator_, 
          principal_investigator_contac_, default_emp_status_, funding_, includes_timeseries_)
  returning study_id into study_id_;
  
  insert  into user_study (web_app_user_id, study_id)
  values  (user_id_, study_id_);
  
  commit;

end;

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
)
as
begin

  update  study
  set     project_name = study_name_,
          investigation_type = investigation_type_,
          submit_to_insdc = submit_, 
          miens_compliant = miens_comp_, 
          portal_type = portal_type_,
          study_title = study_title_, 
          study_alias = study_alias_, 
          pmid = pmid_, 
          study_abstract = study_abstract_, 
          study_description = study_description_,
          number_samples_collected = number_samples_collected_, 
          number_samples_promised = number_samples_promised_, 
          lab_person = lab_person_, 
          lab_person_contact = lab_person_contact_, 
          emp_person = emp_person_, 
          first_contact = first_contact_, 
          most_recent_contact = most_recent_contact_, 
          sample_type = sample_type_, 
          has_physical_specimen = has_physical_specimen_, 
          has_extracted_data = has_extracted_data_, 
          timeseries = timeseries_, 
          spatial_series = spatial_series_, 
          principal_investigator = principal_investigator_, 
          principal_investigator_contact = principal_investigator_contac_, 
          default_emp_status = default_emp_status_, 
          funding = funding_,
          includes_timeseries = includes_timeseries_
  where   study_id = study_id_;

  commit;

end;

procedure study_packages_insert
(
  stud_id in int,
  env_pkg in int
)
as
begin
  
  insert into study_packages (study_id, env_package)
  values (stud_id, env_pkg);
  
  commit;

end;

/*

execute study_packages_insert(2, 4);

select * from study_packages;

delete from study_packages;
commit;

*/

procedure study_packages_delete
(
  study_id_ in int
)
as
begin
  
  delete  study_packages
  where   study_id = study_id_;
  
  commit;

end;

procedure validate_list_value
(
  list_name in controlled_vocabs.vocab_name%type,
  list_value in controlled_vocab_values.term%type,
  results out int
)
as
begin
  select  cvv.vocab_value_id into results
  from    controlled_vocab_values cvv
          inner join controlled_vocabs cv
          on cvv.controlled_vocab_id = cv.controlled_vocab_id
  where   cv.vocab_name = list_name
          and lower(cvv.term) = lower(list_value);
exception
  when no_data_found then
    results := 0;
end;

/*

set serveroutput on;
declare
  results int;
begin
  validate_list_value( 'Investigation Type', 'eukaryote', results );
  dbms_output.put_line(results);
end;

*/
/*
procedure get_new_queue_jobs
(
  results in out types.ref_cursor
)
as
begin

  open results for
    select  job_id, user_id, submission_date
    from    qiime_queue
    where   status = 'new';

end;
*/
/*

exec get_new_queue_jobs

*/

procedure update_job_status
(
  jid in qiime_queue.job_id%type,
  new_status in qiime_queue.status%type
)
as
begin

  update  qiime_queue
  set     status = new_status
  where   job_id = jid;
  
  commit;

end;

/*

exec get_new_queue_jobs

*/  

procedure update_metadata_flag
(
  study_id_ in study.study_id%type,
  status_ in study.metadata_complete%type
)
as
begin

  update  study
  set     metadata_complete = status_
  where   study_id = study_id_;
  
  commit;

end;

/*

exec qiime_assets.update_metadata_flag(2, 'n');

*/  
/*
procedure create_queue_job
(
  study_id_ in qiime_queue.study_id%type, 
  user_id_ in qiime_queue.user_id%type, 
  mapping_file_ in qiime_queue.mapping_file%type, 
  sff_file_ in qiime_queue.sff_file%type, 
  job_id_ in out qiime_queue.job_id%type
)
as
begin

  insert into qiime_queue (job_id, study_id, user_id, mapping_file, sff_file)
  values (seq_job.nextval, study_id_, user_id_, mapping_file_, sff_file_)
  returning job_id into job_id_;
  commit;

end;
*/
/*

variable job_id NUMBER;
execute qiime_assets.create_queue_job(2, 10020, 'asdf', :job_id );
print job_id; 

select * from qiime_queue;
delete from qiime_queue where job_id = job_id;
commit;

*/
/*
procedure get_job_info
(
  study_id_ in qiime_queue.study_id%type,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  job_id, submission_date, status
    from    qiime_queue
    where   study_id = study_id_
            and submission_date = 
            (
              select  max(submission_date)
              from    qiime_queue
              where   study_id = study_id_
            );

end;
*/
/*

*/

procedure add_seq_file
(
  study_id_ in int,
  path_ in varchar2,
  file_type_ in varchar2
)
as
begin

  merge into study_files
  using dual
  on (dual.dummy is not null and study_files.study_id = study_id_ and study_files.file_path = path_)
  when not matched then insert (study_id, file_path, file_type) values (study_id_, path_, file_type_);
  
  commit;
  
end;

procedure add_mapping_file
(
  study_id_ in int,
  mapping_file_path_ in varchar2
)
as
begin

  merge into study_files
  using dual
  on (dual.dummy is not null and study_files.study_id = study_id_ and study_files.file_path = mapping_file_path_)
  when not matched then insert (study_id, file_path, file_type) values (study_id_, mapping_file_path_, 'MAPPING');
    
  commit;
  
end;

procedure add_template_file
(
  study_id_ in int,
  template_file_path_ in varchar2
)
as
begin

  merge into study_files
  using dual
  on (dual.dummy is not null and study_files.study_id = study_id_ and study_files.file_path = template_file_path_)
  when not matched then insert (study_id, file_path, file_type) values (study_id_, template_file_path_, 'TEMPLATE');
    
  commit;
  
end;

procedure clear_study_templates
(
  study_id_ in int
)
as
begin

  delete  study_files
  where   study_id = study_id_
          and file_type = 'TEMPLATE';
    
  commit;
  
end;

procedure get_mapping_files
(
  study_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  file_path
    from    study_files
    where   study_id = study_id_
            and file_type = 'MAPPING';

end;

procedure get_sff_files
(
  study_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  file_path
    from    study_files
    where   study_id = study_id_
            and (file_type = 'SFF' or file_type = 'FASTQ' or file_type = 'FNA');

end;

procedure get_metadata_fields
(
  study_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  upper(column_name), upper(table_name)
    from    study_actual_columns
    where   study_id = study_id_
    order by  upper(column_name);

end;

/*

*/

procedure get_sample_list
(
  study_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  sample_name, sample_id
    from    "SAMPLE"
    where   study_id = study_id_
    order by  sample_name;

end;

/*

*/

procedure get_prep_list
(
  sample_id_ in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  sample_id, row_number, num_sequences
    from    "SEQUENCE_PREP"
    where   sample_id = sample_id_;

end;

/*

*/

procedure add_study_actual_column
(
  study_id_ in int,
  column_name_ in varchar2,
  table_name_ in varchar2
)
as
begin

  merge into study_actual_columns
  using dual
  on (dual.dummy is not null and study_actual_columns.study_id = study_id_ and study_actual_columns.column_name = column_name_)
  when not matched then insert (study_id, column_name, table_name) values (study_id_, column_name_, table_name_);
    
  commit;
  
end;

/*

*/

procedure remove_study_actual_column
(
  study_id_ in int,
  column_name_ in varchar2
)
as
begin

  delete  study_actual_columns
  where   study_id = study_id_
          and column_name = column_name_;
    
  commit;
  
end;

/*

*/

procedure get_study_actual_columns
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  column_name, table_name
    from    study_actual_columns
    where   study_id = study_id_;

end;

/*

*/

procedure get_minimal_mapping_data 
(
  run_id in varchar2,
  mapping_values in out types.ref_cursor
)
as
begin 

  open mapping_values for  
     'select distinct s.sample_name, m.barcode, concat(m.linker, m.primer), m.region, m.experiment_title
     from SEQUENCE_PREP m
     inner join SAMPLE s
     on m.sample_id = s.sample_id
     where m.run_prefix in (' || run_id ||')';
end;

/*
variable mapping_values REFCURSOR;
execute qiime_assets.get_minimal_mapping_data('''V6_n5'',''V2_n14''', :mapping_values);
print mapping_values;
*/

procedure prepare_study_for_update
(
  study_id_ in int
)
as
  extra_study_exists int;
  extra_sample_exists int;
  extra_prep_exists int;
begin

  -- Extra Study
  select  count(*) into extra_study_exists
  from    all_tables
  where   table_name = 'EXTRA_STUDY_' || study_id_;
  
  if extra_study_exists > 0 then
    execute immediate 'drop table extra_study_' || study_id_;
  end if;
  
  -- Extra Sample
  select  count(*) into extra_sample_exists
  from    all_tables
  where   table_name = 'EXTRA_SAMPLE_' || study_id_;
  
  if extra_sample_exists > 0 then
    execute immediate 'drop table extra_sample_' || study_id_;
  end if;
  
  -- Extra Prep
  select  count(*) into extra_prep_exists
  from    all_tables
  where   table_name = 'EXTRA_PREP_' || study_id_;
  
  if extra_prep_exists > 0 then
    execute immediate 'drop table extra_prep_' || study_id_;
  end if;


  delete  study_actual_columns
  where   study_id = study_id_;

end;

procedure study_delete
(
  study_id_ in int,
  full_delete in int
)
as
  extra_study_exists int;
  extra_sample_exists int;
  extra_prep_exists int;
begin

  -- Extra Study
  select  count(*) into extra_study_exists
  from    all_tables
  where   table_name = 'EXTRA_STUDY_' || study_id_;
  
  if extra_study_exists > 0 then
    execute immediate 'drop table extra_study_' || study_id_;
  end if;
  
  -- Extra Sample
  select  count(*) into extra_sample_exists
  from    all_tables
  where   table_name = 'EXTRA_SAMPLE_' || study_id_;
  
  if extra_sample_exists > 0 then
    execute immediate 'drop table extra_sample_' || study_id_;
  end if;
  
  -- Extra Prep
  select  count(*) into extra_prep_exists
  from    all_tables
  where   table_name = 'EXTRA_PREP_' || study_id_;
  
  if extra_prep_exists > 0 then
    execute immediate 'drop table extra_prep_' || study_id_;
  end if;

  -- Grab the list of sample_ids and host_ids for use here
  insert  into sample_ids (sample_id)
  select  sample_id
  from    sample
  where   study_id = study_id_;
  
  insert  into host_ids (host_id)
  select  hs.host_id
  from    host_sample hs
          inner join sample sa
          on hs.sample_id = sa.sample_id
  where   sa.study_id = study_id_;

  -- Group
  delete  group_timeline
  where   group_id in
          (
            select  group_id
            from    "GROUP"
            where   study_id = study_id_
          );

  delete  timeline
  where   study_id = study_id_;
  
  delete  "GROUP"
  where   study_id = study_id_;
  
  -- Host/human
  
  delete  host_group
  where   host_id in
          (
            select  host_id
            from    host_ids
          );
          
  delete  host_relationship
  where   host_id_1 in
          (
            select  host_id
            from    host_ids
          )
          or host_id_2 in
          (
            select  host_id
            from    host_ids
          );
  
  delete  host_timeline
  where   host_id in
          (
            select  host_id
            from    host_ids
          );

  delete  host_sample
  where   host_id in
          (
            select  host_id
            from    host_ids
          );
          
  delete  from host
  where   host_id in
          (
            select  host_id
            from    host_ids
          );
  
  -- Sample based
  delete  human_associated
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );

  delete  host_assoc_vertibrate
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );

  delete  host_associated_plant
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
  
  delete  common_fields
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );

  delete  microbial_mat_biofilm
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  other_environment
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  sediment
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  soil
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  wastewater_sludge
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  water
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );

  delete  air
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );


  delete  sample_sequence_prep
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  sample_timeline
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  sampling_event
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );

  
  delete  common_extra_sample
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  common_extra_prep
  where   sample_id in
          (
            select  sample_id
            from    sample_ids
          );
          
  delete  study_actual_columns
  where   study_id = study_id_;
  
  update  study
  set     metadata_complete = 'n'
  where   study_id = study_id_;
  
  -- This is the 'replace' option when loading metadata
  if full_delete >= 1 then
  
    delete  sequence_prep
    where   sample_id in
            (
              select  sample_id
              from    sample_ids
            );
  
    delete  "SAMPLE"
    where   sample_id in
            (
              select  sample_id
              from    sample_ids
            );
            
    end if;
      
  -- This is the complete study delete accessed by clicking 'delete study' on the website
  if full_delete >= 2 then
    /*
    delete  qiime_queue
    where   study_id = study_id_;
    */
    delete  extra_column_metadata
    where   study_id = study_id_;
    
    delete  study_files
    where   study_id = study_id_;
  
    delete  study_packages
    where   study_id = study_id_;
  
    delete  user_study
    where   study_id = study_id_;
    
    delete  sra_submission
    where   study_id = study_id_;
    
    delete  study
    where   study_id = study_id_;
  end if;
  
  -- Clear the temp tables
  delete from sample_ids;
  delete from host_ids;
  
  commit;

end;

/*
select * from study order by study_id
execute study_delete(14);

*/

procedure extra_column_metadata_insert
(
  study_id_ in int,
  table_level_ in varchar2,
  column_name_ in varchar2,
  description_ in varchar2,
  data_type_ in varchar2
)
as
begin

  merge into extra_column_metadata
  using dual
  on 
  (
    dual.dummy is not null 
    and extra_column_metadata.study_id = study_id_
    and extra_column_metadata.table_level = table_level_
    and extra_column_metadata.column_name = column_name_
  )
  when not matched then 
  insert (study_id, table_level, column_name, description, data_type)
  values (study_id_, table_level_, column_name_, description_, data_type_);
  
  commit;

end;

procedure get_study_extra_columns 
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin 

  open results_ for  
     select table_level, column_name, description, data_type
     from   extra_column_metadata
     where  study_id = study_id_;
     
end;

procedure find_extra_column_match 
(
  column_name_ in varchar2,
  results_ in out types.ref_cursor
)
as
begin 

  open results_ for  
    select  table_name
    from    all_tab_columns
    where   column_name = column_name_
            and table_name like 'EXTRA_%';
     
end;

procedure delete_study_extra_columns 
(
  study_id_ in int
)
as
begin 

  delete  extra_column_metadata
  where   study_id = study_id_;
  
  commit;
     
end;

procedure get_split_libarary_data
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin 

  open results_ for  
      select  sa.sample_name || '.' || sp.sequence_prep_id as "#SampleID", 
              sp.barcode as "BarcodeSequence", 
              sp.linker as "Linker",
              sp.primer as "Primer",
              sp.run_prefix as "RunPrefix",
              sp.experiment_title as "Description"
      from    study s
              inner join sample sa
              on s.study_id = sa.study_id
              inner join sequence_prep sp
              on sa.sample_id = sp.sample_id
      where   s.study_id = study_id_
      order by  sp.run_prefix;
     
end;

procedure get_run_prefix_bc_lengths
(
  study_id_ in int,
  run_prefix_ in varchar2,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  length(sp.barcode) as barcode_length
    from    sample sa
            inner join sequence_prep sp
            on sa.sample_id = sp.sample_id
    where   sa.study_id = study_id_
            and sp.run_prefix = run_prefix_
    group by  length(sp.barcode);

end;

procedure get_study_platform
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  distinct sp.platform
    from    sample sa
            inner join sequence_prep sp
            on sa.sample_id = sp.sample_id
    where   sa.study_id = study_id_;

end;

procedure clear_sff_file
(
  study_id_ in int,
  sff_file_ in varchar2
)
as
begin

  delete  study_files
  where   study_id = study_id_
          and file_path like '%' || sff_file_;
          
  commit;

end;

procedure clear_split_lib_map_files
(
  study_id_ in int
)
as
begin

  delete  study_files
  where   study_id = study_id_
          and file_path like '%__split_libraries_mapping_file.txt';
          
  commit;

end;

procedure authenticate_user
(
  username in VARCHAR2,
  pwd in VARCHAR2,
  user_data in out types.ref_cursor
)
as
begin

  open user_data for
    select  web_app_user_id, email, password, is_admin, is_locked, last_login,verified
    from    web_app_user
    where   email = username
            and password = pwd;

end;


/*

variable user_data REFCURSOR;
execute authenticate_user( 'test', 'test', :user_data );
print user_data;

*/

procedure get_user_details
(
  user_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  email, is_admin, is_locked, last_login
    from    web_app_user
    where   web_app_user_id = user_id_;

end;

procedure get_sample_ids_from_study
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  sample_id
    from    sample
    where   study_id = study_id_;

end;

procedure get_sequences_for_fasta
(
  study_id_ in int,
  sample_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  sl.sequence_name, ssu.sequence_string
    from    sff.analysis a 
            inner join sff.split_library_read_map sl 
            on a.split_library_run_id = sl.split_library_run_id 
            inner join sff.ssu_sequence ssu
            on sl.ssu_sequence_id = ssu.ssu_sequence_id
            inner join sample s
            on s.study_id = a.study_id
    where   a.study_id = study_id_
            and s.sample_id = sample_id_
            and substr(sl.sample_name, 1, length(s.sample_name)) = s.sample_name
            and a.study_id = study_id_;

end;

procedure get_sequences_for_fasta_fulldb
(
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  sl.sequence_name, ssu.sequence_string
    from    sff.split_library_read_map sl
            inner join sff.ssu_sequence ssu
            on sl.ssu_sequence_id = ssu.ssu_sequence_id;

end;

procedure get_list_field_value
(
  vocab_value_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  term
    from    controlled_vocab_values
    where   vocab_value_id = vocab_value_id_;

end;

procedure get_emp_sample_list
(
  study_id_ in int,
  web_app_user_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  sa.sample_id,
            (
              select  avg(emp_score)
              from    sample_emp_score
              where   sample_id = sa.sample_id
            ) as avg_emp_score,
            ses.emp_score as user_emp_score, 
            sa.sample_name,            
            (
              select  term
              from    controlled_vocab_values
              where   vocab_value_id = sa.emp_status
            ) as emp_status,
            case
              when sa.sample_location is null then ' '
              else sa.sample_location
            end as sample_location,
            case
              when sa.sample_progress is null then ' '
              else sa.sample_progress
            end as sample_progress,
            case
              when sa.description is null then ' '
              else sa.description
            end as description, 
            sa.altitude, 
            sa.samp_size,
            sa.temp, 
            sa.samp_store_temp, 
            case
              when sa.country is null then ' '
              else sa.country
            end as country, 
            sa.depth, 
            sa.elevation, 
            case
              when sa.env_biome is null then ' '
              else sa.env_biome
            end as env_biome, 
            case
              when sa.env_feature is null then ' '
              else sa.env_feature
            end as env_feature, 
            case
              when sa.env_matter is null then ' '
              else sa.env_matter
            end as env_matter, 
            sa.ph, 
            sa.latitude, 
            sa.longitude, 
            case
              when sa.chem_administration is null then ' '
              else sa.chem_administration
            end as chem_administration, 
            case
              when sa.samp_store_loc is null then ' '
              else sa.samp_store_loc
            end as samp_store_loc
    from    sample sa
            left join sample_emp_score ses
            on sa.sample_id = ses.sample_id
              and ses.web_app_user_id = web_app_user_id_
    where   sa.study_id = study_id_
    order by sa.sample_name;

end;

procedure update_emp_sample_data
(
  sample_id_ in int,
  sample_score_ in int,
  emp_status_ in int,
  web_app_user_id_ in int
)
as
begin

  merge into sample_emp_score ses
  using dual
  on (dual.dummy is not null 
    and ses.sample_id = sample_id_
    and ses.web_app_user_id = web_app_user_id_)
  when matched then
    update set  emp_score = sample_score_
  when not matched then 
    insert (sample_id, emp_score, web_app_user_id) 
    values (sample_id_, sample_score_, web_app_user_id_);
    
  update  sample
  set     emp_status = emp_status_
  where   sample_id = sample_id_;
  
  commit;

end;

procedure update_emp_study_data
(
  study_id_ in int,
  study_score_ in int,
  web_app_user_id_ in int
)
as
begin

  merge into study_emp_score ses
  using dual
  on (dual.dummy is not null 
    and ses.study_id = study_id_
    and ses.web_app_user_id = web_app_user_id_)
  when matched then
    update set emp_score = study_score_
  when not matched then 
    insert (study_id, emp_score, web_app_user_id) 
    values (study_id_, study_score_, web_app_user_id_);

  commit;

end;

procedure get_study_templates
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  file_path
    from    study_files
    where   study_id = study_id_
            and file_type = 'TEMPLATE';

end;

procedure get_immutable_database_fields
(
  study_id_ in int,
  results_ in out types.ref_cursor
)
as
begin

  open results_ for
    select  s.sample_name, sp.linker, sp.primer, sp.barcode, sp.run_prefix, sp.platform
    from    sample s
            inner join sequence_prep sp
            on s.sample_id = sp.sample_id
    where   s.study_id = study_id_
    order by sample_name;

end;


end qiime_assets;