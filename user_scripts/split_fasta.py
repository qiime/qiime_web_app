from qiime.parallel.util import split_fasta

input_fp='/home/wwwuser/full_db_split_lib_seqs_5_9_2012.fna'

output_dir='/home/wwwuser/full_db_split_fasta/'

output_prefix='full_dbs'

split_fasta(open(input_fp,'U'), 70000000, output_prefix, output_dir)
