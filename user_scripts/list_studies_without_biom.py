from cogent.parse.fasta import MinimalFastaParser
from os.path import abspath,join,split,splitext,exists
from os import listdir,system

studies=[77, 94, 101, 103, 104, 130, 213, 214, 232, 314, 316, 317, 349, 391, 393, 395, 397, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 486, 492, 494, 495, 496, 509, 524, 539, 550, 619, 625, 626, 721, 722, 734, 742, 776, 796, 797, 802, 803, 808, 814, 816, 819, 850, 854, 909, 926, 928, 929, 933, 939, 959, 964, 966, 967, 968, 969, 992, 1002, 1005, 1006, 1010, 1011, 1020, 1026, 1030, 1031, 1033, 1034, 1035, 1036, 1037, 1038, 1043, 1046, 1066, 1069, 1070, 1090, 1192, 1194, 1195, 1198, 1199, 1200, 1335, 1345, 1364, 1436]
#studies=[77,101]
input_dir='/home/wwwuser/user_data/studies/'

for study in studies:
    study_input_dir=join(input_dir,'study_%s' % (str(study)))
    processed_folders=listdir(study_input_dir)
    for processed_folder in processed_folders:
        if processed_folder.startswith('processed'):
            #print processed_folder
            gg_biom_fp=join(study_input_dir,processed_folder,'gg_97_otus','exact_uclust_ref_otu_table.biom')
            
            if not exists(gg_biom_fp):
                print "No BIOM: %s\t%s\n" % (study,processed_folder)
            #
            gg_otu_table_fp=join(study_input_dir,processed_folder,'gg_97_otus','exact_uclust_ref_otu_table.txt')
            #print gg_otu_table_fp
            if not exists(gg_otu_table_fp):
                print "No TXT: %s\t%s\n" % (study,processed_folder)