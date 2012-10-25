
create or replace procedure get_study_info
(
  stud_id in int,
  results in out types.ref_cursor
)
as
begin

  open results for
    select  s."PUBLIC", s.submit_to_insdc, cvv0.term as investigation_type, 
            s.project_name, s.experimental_factor, cvv1.term as env_package, 
            cvv2.term as study_complt_stat, s.study_alias, s.study_title, s.study_type, 
            s.study_abstract, s.study_description, s.center_name, s.center_project_name, 
            s.project_id, s.pmid
    from    study s
            inner join controlled_vocab_values cvv0
            on s.investigation_type = cvv0.vocab_value_id
            inner join controlled_vocab_values cvv1
            on s.env_package = cvv1.vocab_value_id
            inner join controlled_vocab_values cvv2
            on s.study_complt_stat = cvv2.vocab_value_id
    where   s.study_id = stud_id;

end;

/*

variable results REFCURSOR;
execute get_study_info(2, :results);
print results;

*/
