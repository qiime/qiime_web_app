
-- Add our own ontologies to the mix

declare
  new_ontology_id integer;

begin

  select max(ontology_id) + 1 into new_ontology_id from ontology;
  insert into ontology (ontology_id, shortname, fully_loaded, fullname, load_date)
  values (new_ontology_id, 'OBI', 1, 'Ontology for Biomedical Investigations', current_date);
  
  select max(ontology_id) + 1 into new_ontology_id from ontology;
  insert into ontology (ontology_id, shortname, fully_loaded, fullname, load_date)
  values (new_ontology_id, 'GAZ', 1, 'Gazetteer Ontology', current_date);
  
  select max(ontology_id) + 1 into new_ontology_id from ontology;
  insert into ontology (ontology_id, shortname, fully_loaded, fullname, load_date)
  values (new_ontology_id, 'DO', 1, 'Disease Ontology', current_date);
  
  select max(ontology_id) + 1 into new_ontology_id from ontology;
  insert into ontology (ontology_id, shortname, fully_loaded, fullname, load_date)
  values (new_ontology_id, 'EFO', 1, 'Experimental Factor Ontology', current_date);
  
end;

