from os import listdir

from cogent.parse.fasta import MinimalFastaParser
from os.path import splitext,split,join



#old_fna=MinimalFastaParser(open('/home/wwwuser/user_data/studies/study_1005/seqs.fna','U'))

old_fna=MinimalFastaParser(open('/home/wwwuser/gn_454_rc_lte500bases.fasta','U'))
new_fname=open('gn_seqs.fna','w')
num=0
for seq_name,old_seq in old_fna:
    seq_name_split=seq_name.split()
    print '.'.join(seq_name_split[0].split('_')[0].split('-'))
    new_seq_name='.'.join(seq_name_split[0].split('_')[0].split('-'))+ '_' + seq_name_split[0].split('_')[1]
    #new_seq_name='.'.join(seq_name_split[0].split('_')[1:-1])
    #print new_seq_name
    new_fname.write('>%s\n%s\n' % (new_seq_name + ' ' +' '.join(seq_name_split[1:]),old_seq))
    #num=num+1
new_fname.close()


