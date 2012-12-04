from cogent.util.misc import safe_md5
from os import listdir,system
from os.path import join
outf=open('/home/wwwuser/global_gut_per_sample_fastas/yatsunenko_global_gut_md5.txt','w')

home_dir='/home/wwwuser/global_gut_per_sample_fastas/'
for file in listdir(home_dir):
    if file.endswith('.fasta'):
        system('md5sum %s' % (join(home_dir,file)))


