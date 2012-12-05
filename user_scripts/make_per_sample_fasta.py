

from qiime.filter import (filter_fasta, filter_fastq,
                          get_seqs_to_keep_lookup_from_fasta_file,
                          get_seqs_to_keep_lookup_from_fasta_file,
                          sample_ids_from_metadata_description,
                          get_seqs_to_keep_lookup_from_biom)
from qiime.parse import parse_mapping_file
from os.path import join
from cogent.parse.fasta import MinimalFastaParser

def get_seqs_to_keep_lookup_from_prefix(fasta_f,prefix):
    seqs_to_keep = [seq_id
                    for seq_id, seq in MinimalFastaParser(fasta_f)
                    if seq_id.startswith(prefix)]
    return {}.fromkeys(seqs_to_keep)

# define input files
input_fasta_fp='/home/wwwuser//user_data/studies/study_939/processed_data_ECUAVIDA_stage1a_/split_libraries/seqs.fna'
input_mapping_file='/home/wwwuser//user_data/studies/study_939/processed_data_ECUAVIDA_stage1a_/ECUAVIDA_stage1a__split_libraries_mapping_file.txt'
output_dir='/home/wwwuser//user_data/studies/study_939/processed_data_ECUAVIDA_stage1a_/split_libraries/per_sample_fastq/'

#input_fasta_fp='/home/wwwuser/global_gut_illumina_split_lib_seqs.fna'
#input_mapping_file='/home/wwwuser/global_gut_illumina_mapping.txt'
#output_dir='/home/wwwuser/global_gut_per_sample_fastas'

# parse mapping file
map_data, map_header, map_comments = parse_mapping_file(open(input_mapping_file,'U'))
negate=False

# get a list of all possible sample_ids
sample_ids=zip(*map_data)[0]
output_fps={}
# iterate over the sample_ids and generate a fasta file for each sample
for s_id in sample_ids:
    output_fps[str(s_id)]=open(join(output_dir,'%s.fasta' % (str(s_id))),'w')

for seq_id, seq in MinimalFastaParser(open(input_fasta_fp)):
    samp_id='_'.join(seq_id.split()[0].split('_')[:-1])
    output_fps[str(samp_id)].write('>%s\n%s\n' % (seq_id,seq))

for s_id in sample_ids:
    output_fps[str(s_id)].close()
# END

