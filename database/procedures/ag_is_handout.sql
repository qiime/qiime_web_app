create or replace procedure ag_is_handout
(
    is_handout_ in out char,
    kit_id_ in varchar2,
    password_ in varchar2
)
as
    cnt number;
begin

    is_handout_ := 'n';

    select  count(*) into cnt
    from    ag_handout_kits
    where   kit_id = kit_id_
            and password = password_;
            
    if (cnt > 0)
    then
        is_handout_ := 'y';
    end if;    

end;
