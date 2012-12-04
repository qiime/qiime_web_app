from os import listdir

from cogent.parse.fasta import MinimalFastaParser
from os.path import splitext,split,join

for i in listdir('./old_fnas'):
    fname,fext=splitext(i)
    old_fna=MinimalFastaParser(open(join('./old_fnas',i),'U'))
    new_fname=open(fname+'.fna','w')
    num=0
    for seq_name,old_seq in old_fna:
        new_fname.write('>%s\n%s\n' % (fname+'_'+str(num),old_seq))
        num=num+1
    new_fname.close()


