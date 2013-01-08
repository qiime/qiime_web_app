create or replace 
PROCEDURE "GET_QIIME_SFF_SAMPLES_COUNT" 
(
  sample_name_ in VARCHAR2,
  results in out number
)
as
begin
    select  count(1)
    into results
    from    split_library_read_map slrm
    where   slrm.sample_name = sample_name_;
end get_qiime_sff_samples_count;


/*
variable results NUMBER;
execute get_qiime_sff_samples_count(TS7.V2N14, :results);
print results;
*/