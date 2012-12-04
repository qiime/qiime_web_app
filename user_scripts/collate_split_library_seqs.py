from cogent.parse.fasta import MinimalFastaParser
from os.path import join,split,splitext
from os import listdir

#studies=[449,968]
#studies=[393,619,455,742,625,1011,967,964,459,316,462,213,450,457,734,77,854,968,494,966,452,397,492,814,626,395,992,1006,461,94,314,496,509,495,349,1070,449,453,456,550,232,797,721,486,451,214,101,130,929,909,1010,850,926,1090,454,460,104,458,819,928,969,1014,722,621,1005,317,103,391,524,803,802,816,539,1026]
#studies=[850]
input_dir='/home/wwwuser/user_data/studies/'

studies=[77, 94, 101, 103, 104, 130, 213, 214, 232, 314, 316, 317, 349, 391, 393, 395, 397, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 486, 492, 494, 495, 496, 509, 524, 539, 550, 619, 625, 626, 721, 722, 734, 742, 776, 796, 797, 802, 803, 808, 814, 816, 819, 850, 854, 909, 926, 928, 929, 933, 939, 959, 964, 966, 967, 968, 969, 992, 1002, 1005, 1006, 1010, 1011, 1020, 1026, 1031, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1066, 1069, 1070, 1090, 1192, 1194, 1195, 1199, 1200]

output_seqs=open('full_db_split_lib_seqs_5_9_2012.fna','w')
for study in studies:
    study_input_dir=join(input_dir,'study_%s' % (str(study)))
    processed_folders=listdir(study_input_dir)
    for processed_folder in processed_folders:
        if processed_folder.startswith('processed'):
            #print '%s\t%s' % (study,processed_folder)
            split_lib_seqs=join(study_input_dir,processed_folder,'split_libraries','seqs.fna')
            seqs=MinimalFastaParser(open( split_lib_seqs,'U'))
            for seq_name,seq in seqs:
                output_seqs.write('>%s\n%s\n' % (str(seq_name),str(seq)))

output_seqs.close()


