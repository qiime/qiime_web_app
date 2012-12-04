from cogent.parse.fasta import MinimalFastaParser
from os.path import join,split,splitext
from os import listdir,system

"""
#studies=[101]
studies=[77, 94, 101, 103, 104, 130, 213, 214, 232, 314, 316, 317, 349, 391, \
         393, 395, 397, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, \
         460, 461, 462, 486, 492, 494, 495, 496, 509, 524, 539, 550, 619, 625, \
         626, 721, 722, 734, 742, 796, 797, 802, 803, 814, 816, 819, 850, 854, \
         909, 926, 928, 929, 933, 939, 964, 966, 967, 968, 969, 992, 1005, \
         1006, 1010, 1011, 1020, 1026, 1034, 1035, 1069, 1070, 1090]
"""
studies=[77, 94, 101, 103, 104, 130, 213, 214, 232, 314, 316, 317, 349, 391, 393, 395, 397, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 486, 492, 494, 495, 496, 509, 524, 539, 550, 619, 625, 626, 721, 722, 734, 742, 776, 796, 797, 802, 803, 808, 814, 816, 819, 850, 854, 909, 926, 928, 929, 933, 939, 959, 964, 966, 967, 968, 969, 992, 1002, 1005, 1006, 1010, 1011, 1020, 1026, 1031, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1066, 1069, 1070, 1090, 1192, 1194, 1195, 1199, 1200]

input_dir='/home/wwwuser/user_data/studies/'


output_seqs=open('db_otu_failure_seqs_5_9_2012.fna','w')
for study in studies:
    study_input_dir=join(input_dir,'study_%s' % (str(study)))
    processed_folders=listdir(study_input_dir)
    for processed_folder in processed_folders:
        if processed_folder.startswith('processed'):
            #print '%s\t%s' % (study,processed_folder)
            failed_seq_map=join(study_input_dir,processed_folder,\
                        'gg_97_otus','all_failures.txt')
            failed_seqs=join(study_input_dir,\
                        processed_folder,'gg_97_otus','all_failures_seqs.fna')
            split_lib_seqs=join(study_input_dir,\
                        processed_folder,'split_libraries','seqs.fna')
            
            try:
                cmd="python2.7 /home/wwwuser/software/Qiime_svn/scripts/filter_fasta.py -f %s -o %s -s %s" % \
                        (split_lib_seqs,failed_seqs,failed_seq_map)
            
                system(cmd)
            
                seqs=MinimalFastaParser(open(failed_seqs,'U'))
                for seq_name,seq in seqs:
                    output_seqs.write('>%s\n%s\n' % (str(seq_name),str(seq)))
            except:
                pass

output_seqs.close()
