create or replace
procedure get_minimal_mapping_data 
(
  run_id in varchar2,
  mapping_values in out types.ref_cursor
)
as
begin    
  open mapping_values for  
     'select distinct s.sample_name, m.barcode,concat(m.linker, m.primer),m.region, m.experiment_title
     from SEQUENCE_PREP m
     inner join SAMPLE s
     on m.sample_id = s.sample_id
     where m.run_prefix in (' || run_id ||')';
end get_minimal_mapping_data;

/*
variable mapping_values REFCURSOR;
execute get_minimal_mapping_data('''V6_n5'',''V2_n14''', :mapping_values);
print mapping_values;
*/