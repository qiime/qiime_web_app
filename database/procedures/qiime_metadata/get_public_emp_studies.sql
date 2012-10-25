create or replace procedure get_public_emp_studies
(
    studies_ in out types.ref_cursor
)
as
begin

    open studies_ for
        select  s.study_id, s.project_name, sf.file_path, s.*
        from    study_files sf
                inner join study s
                on sf.study_id = s.study_id
        where   file_type = 'SPLIT_LIB_SEQS_MAPPING'
                and portal_type = 'emp'
                and 
                (
                    select  count(*)
                    from    sample sa
                    where   sa.study_id = s.study_id
                            and sa."PUBLIC" = 'n'
                ) = 0
        order by s.project_name;
 
end;

/*

variable data REFCURSOR;
execute get_public_emp_studies(:data);
print data;

*/
