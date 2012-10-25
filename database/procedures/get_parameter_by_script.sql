create or replace
procedure get_parameter_by_script
(
  parameter_type in varchar,
  script_type in varchar,
  parameter_values in out types.ref_cursor
)
as
begin    
  open parameter_values for  
    'select distinct p.DEFAULT_VALUE  
     from PARAMETER p 
     inner join SCRIPT s
     on p.SCRIPT_ID = s.SCRIPT_ID
     where p.PARAM = ' || parameter_type || ' and s.SCRIPT_NAME = ' || script_type;
end;

/*

variable parameter_values REFCURSOR;
execute get_parameter_by_script( '''otu_picking_method'''  ,  '''pick_otus'''   , :parameter_values );
print parameter_values;

*/