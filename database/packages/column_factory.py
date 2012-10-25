CREATE OR REPLACE PACKAGE "GET_GREENGENES_TAXONOMIES" as 
  TYPE otu_id_array_tab  IS TABLE OF NUMBER INDEX BY BINARY_INTEGER;

  /* TODO enter package declarations (types, exceptions, methods etc) here */ 

  procedure array_return (otu_id_array in otu_id_array_tab,
                          user_data OUT types.ref_cursor);

end get_greengenes_taxonomies;
/


CREATE OR REPLACE PACKAGE BODY "GET_GREENGENES_TAXONOMIES" as

  procedure array_return (otu_id_array in otu_id_array_tab,
                          user_data OUT types.ref_cursor) as
  begin
  open user_data for
    begin(
    for idx in otu_id_array.first..otu_id_array.last
    LOOP
    ---
    END LOOP;)
  end array_return;

end get_greengenes_taxonomies;
/
