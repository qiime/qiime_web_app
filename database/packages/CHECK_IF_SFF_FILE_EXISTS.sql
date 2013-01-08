create or replace 
PROCEDURE "CHECK_IF_SFF_FILE_EXISTS" 
/* This procedure checks if the sff file is already in the db */
(
  -- define the variables passed into this procedure
  I_md5_checksum IN VARCHAR2, 
  sff_exists OUT NUMBER
) as 
begin
  -- count the number of occcurrences of this SFF using its md5_checksum value  
  SELECT COUNT(1) 
  INTO sff_exists 
  FROM SFF_FILE 
  WHERE md5_checksum=I_md5_checksum;
end check_if_sff_file_exists;

/* 
variable sff_exists NUMBER;
execute check_if_sff_file_exists('314f4000857668d45a413d2e94a755fc',:sff_exists);
print sff_exists;

variable sff_exists NUMBER;
execute check_if_sff_file_exists('aaaa',:sff_exists);
print sff_exists;
*/