#!/usr/bin/env python
# File created on 06 Jun 2012
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2012, The QIIME-DB Project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

from cogent.parse.fasta import MinimalFastaParser
from os import listdir,remove,system
from os.path import join,split,splitext,exists,getsize
from numpy import mean
import gzip
import operator
from write_mapping_file import write_mapping_file as write_db_mapping_files
from qiime.merge_mapping_files import merge_mapping_files, write_mapping_file
import zipfile
from biom.parse import parse_biom_table
from qiime.format import format_biom_table

def write_full_mapping_file(study, study_input_dir,zip_fname,files_to_remove,
                            output_dir):
    
    ### Generate a merged mapping file
    # write per_run mapping files and then return the prefixes
    run_prefixes=write_db_mapping_files(study,True,study_input_dir,False)
    
    # define the full mapping file
    mapping_fname='study_%s_mapping_file.txt' % (str(study))
    final_mapping_fp=join(output_dir,mapping_fname)
    # add to list of files to remove
    files_to_remove.append(final_mapping_fp)
    
    # iterate over run_prefixes and create a list of files that need to be
    # merged
    mapping_files_to_merge=[]
    for i in run_prefixes:
        mapping_fp=join(study_input_dir,'study_%s_run_%s_mapping.txt' % \
                                        (str(study),str(i)))
        # add to list of files to remove
        files_to_remove.append(mapping_fp)
        mapping_files_to_merge.append(open(mapping_fp,'U'))
    
    # merge the mapping files and return tabular data
    mapping_data = merge_mapping_files(mapping_files_to_merge,\
                                       no_data_value='no_data')
    # write the full mapping file
    write_mapping_file(mapping_data,final_mapping_fp)
    
    # zip the full mapping file
    #cmd_call='cd %s; tar czvf %s %s' % (study_input_dir,zip_fname,mapping_fname)
    #system(cmd_call)
    
    return files_to_remove
    
def generate_full_split_lib_seqs(study, study_input_dir, zip_fname,
                                 files_to_remove,output_dir):
    ### Generate the full split-library sequence file
    # define sequence output file
    seq_fname='study_%s_split_library_seqs.fna.gz' % (str(study))
    output_seq_fp=join(output_dir,seq_fname)
    # add to list of files to remove
    files_to_remove.append(output_seq_fp)
    
    output_seqs=gzip.open(output_seq_fp,'w')
    iterator=0
    
    # get a list of all files in study_dir
    processed_folders=listdir(study_input_dir)
    samples={}
    biom_files=[]
    for processed_folder in processed_folders:
        # determine if the file startswith the word "processed"
        if processed_folder.startswith('processed'):
            # define split-lib seq fp
            split_lib_seqs=join(study_input_dir,processed_folder,
                                'split_libraries','seqs.fna')
            # open split-lib seq fp
            seqs=MinimalFastaParser(open(split_lib_seqs,'U'))
            # iterate over sequences
            for seq_name,seq in seqs:
                # update sequence numbers since they may cause issues across
                # multiple split-lib runs
                full_seq_name_list=seq_name.split()
                seq_name_prefix='_'.join(full_seq_name_list[0].split('_')[:-1])
                
                # get per sample sequence counts
                if seq_name_prefix in samples:
                    samples[seq_name_prefix]=samples[seq_name_prefix]+1
                else:
                    samples[seq_name_prefix]=1
                
                # update the sequence name, but retain barcode info
                updated_seq_name=seq_name_prefix + '_' + str(iterator) + \
                                 ' ' + ' '.join(full_seq_name_list[1:])
                
                # write the sequence out in FASTA format
                output_seqs.write('>%s\n%s\n' % (str(updated_seq_name),
                                                 str(seq)))
                iterator=iterator+1
            
            # get list of biom files
            gg_biom_fp=join(study_input_dir,processed_folder,
                            'gg_97_otus','exact_uclust_ref_otu_table.biom')
            if exists(gg_biom_fp) and getsize(gg_biom_fp)>0:
                biom_files.append(gg_biom_fp)
                
    output_seqs.close()
    
    # zip the full split-library sequence file
    #cmd_call='cd %s; tar rzvf %s %s' % (study_input_dir,zip_fname,seq_fname)
    #system(cmd_call)
    
    return files_to_remove, biom_files, samples
    
def generate_split_lib_log(study, study_input_dir, zip_fname, files_to_remove,\
                           samples,output_dir):
    #
    ### Generate log information for split-library sequences
    # define log fp
    log_fname='study_%s_split_library_log.txt' % (str(study))
    log_fp=join(output_dir,log_fname)
    # add to list of files to remove
    files_to_remove.append(log_fp)
    
    # write the seq min/max/mean and number of samples
    log_file=open(log_fp,'w')
    log_file.write('Num Samples\t%s\n' % (str(len(samples))))
    log_file.write('Sample ct min/max/mean: %s / %s / %s\n' % \
                (str(min(samples.values())), str(max(samples.values())), \
                 str(mean(samples.values()))))
                 
    # sort the sample_ids and write them to log-file
    sorted_samples=sorted(samples.iteritems(), key=operator.itemgetter(1))
    log_file.write('Sample\tSequence Count\n')
    for sample in sorted_samples:
        log_file.write('%s\t%s\n' % (str(sample[0]), \
                                     str(sample[1])))
    # write total number of sequences
    log_file.write('\nTotal number seqs written\t%s\n' % \
                                            (str(sum(samples.values()))))
    log_file.close()
    
    # zip the full split-library log file
    #cmd_call='cd %s; tar rzvf %s %s' % (study_input_dir,zip_fname,log_fname)
    #system(cmd_call)
    
    return files_to_remove
    
def generate_full_otu_table(study, study_input_dir, zip_fname, files_to_remove,
                            biom_files,output_dir):
    ### Merge OTU tables
    master = parse_biom_table(open(biom_files[0],'U'))
    # only merge if there is more than 1 biom file
    if len(biom_files) > 1:
        for input_fp in biom_files[1:]:
            master = master.merge(parse_biom_table(open(input_fp,'U')))
        
    # write full biom-table
    full_biom_table_fname='study_%s_closed_reference_otu_table.biom' % \
                                                              (str(study))
    full_biom_table_fp=join(output_dir,full_biom_table_fname)
    # add to list of files to remove
    files_to_remove.append(full_biom_table_fp)
    
    biom_f = open(join(full_biom_table_fp),'w')
    biom_f.write(format_biom_table(master))
    biom_f.close()
    
    # zip the full biom-table file
    #cmd_call='cd %s; tar rzvf %s %s' % (study_input_dir,zip_fname,
    #                               full_biom_table_fname)
    #system(cmd_call)
    
    return files_to_remove
    
def scp_files_to_thebeast(study,zip_fp,zip_fname,public):
    ### Move the zipped file to thebeast ftp site
    if public:
        # use scp to copy file
        system("scp %s thebeast.colorado.edu:/qiimedb_studies/public/" % (zip_fp))
        
        # define the public url
        url='ftp://thebeast.colorado.edu/pub/QIIME_DB_Public_Studies/%s' % (zip_fname)
        
        # get QIIME-DB connection
        try:
            from data_access_connections import data_access_factory
            from enums import ServerConfig
            import cx_Oracle
            data_access = data_access_factory(ServerConfig.data_access_type)
        except ImportError:
            print "NOT IMPORTING QIIMEDATAACCESS"
            pass

        con=data_access.getMetadataDatabaseConnection()
        cur=con.cursor()
        
        # verify path hasn't been inserted in db already
        statement='select file_path from study_files ' + \
                  'where file_path=\'%s\'and study_id=%s and file_type=\'SPLIT_LIB_SEQS_MAPPING\'' % \
                  (url,str(study))
        results=cur.execute(statement)

        results_exist=False
        for i in results:
            results_exist=True

        # if url not in DB, then insert it
        if not results_exist:
            data_access.addSeqFile (str(study),url,'SPLIT_LIB_SEQS_MAPPING')
        
    else:
        # for private data, we will also scp it to thebeast
        system("scp %s thebeast.colorado.edu:/qiimedb_studies/private/" % (zip_fp))
    
#
def generate_full_split_lib_qual(study, study_input_dir, zip_fname,
                                 files_to_remove,output_dir):
    ### Generate the full split-library sequence file
    # define sequence output file
    seq_fname='study_%s_split_library_seqs.qual.gz' % (str(study))
    output_seq_fp=join(output_dir,seq_fname)
    # add to list of files to remove
    files_to_remove.append(output_seq_fp)
    
    output_seqs=gzip.open(output_seq_fp,'w')
    iterator=0
    
    # get a list of all files in study_dir
    processed_folders=listdir(study_input_dir)
    samples={}
    biom_files=[]
    for processed_folder in processed_folders:
        # determine if the file startswith the word "processed"
        if processed_folder.startswith('processed'):
            # define split-lib seq fp
            split_lib_seqs=join(study_input_dir,processed_folder,
                                'split_libraries_per_sample','seqs.qual')
            # open split-lib seq fp
            seqs=MinimalFastaParser(open(split_lib_seqs,'U'))
            # iterate over sequences
            for seq_name,seq in seqs:
                # update sequence numbers since they may cause issues across
                # multiple split-lib runs
                full_seq_name_list=seq_name.split()
                seq_name_prefix='_'.join(full_seq_name_list[0].split('_')[:-1])
                
                # get per sample sequence counts
                if seq_name_prefix in samples:
                    samples[seq_name_prefix]=samples[seq_name_prefix]+1
                else:
                    samples[seq_name_prefix]=1
                
                # update the sequence name, but retain barcode info
                updated_seq_name=seq_name_prefix + '_' + str(iterator) + \
                                 ' ' + ' '.join(full_seq_name_list[1:])
                
                # write the sequence out in FASTA format
                output_seqs.write('>%s\n%s\n' % (str(updated_seq_name),
                                                 str(seq)))
                iterator=iterator+1
            
            # get list of biom files
            gg_biom_fp=join(study_input_dir,processed_folder,
                            'gg_97_otus','exact_uclust_ref_otu_table.biom')
            if exists(gg_biom_fp) and getsize(gg_biom_fp)>0:
                biom_files.append(gg_biom_fp)
                
    output_seqs.close()
    
    # zip the full split-library sequence file
    #cmd_call='cd %s; tar rzvf %s %s' % (study_input_dir,zip_fname,seq_fname)
    #system(cmd_call)
    
    return files_to_remove, biom_files, samples
#
#
def generate_full_split_lib_fastq(study, study_input_dir, zip_fname,
                                 files_to_remove,output_dir):
    ### Generate the full split-library sequence file
    # define sequence output file
    seq_fname='study_%s_split_library_seqs.fastq.gz' % (str(study))
    fna_fname='study_%s_split_library_seqs.fna.gz' % (str(study))
    output_seq_fp=join(output_dir,seq_fname)
    output_fna_fp=join(output_dir,fna_fname)
    # add to list of files to remove
    files_to_remove.append(output_seq_fp)
    files_to_remove.append(output_fna_fp)
    
    output_seqs=gzip.open(output_seq_fp,'w')
    output_fna=gzip.open(output_fna_fp,'w')
    iterator=0
    
    # get a list of all files in study_dir
    processed_folders=listdir(study_input_dir)
    samples={}
    biom_files=[]
    for processed_folder in processed_folders:
        # determine if the file startswith the word "processed"
        if processed_folder.startswith('processed'):
            # define split-lib seq fp
            split_lib_seqs=join(study_input_dir,processed_folder,
                                'split_libraries','seqs.fna')
            
            #
            split_lib_qual=join(study_input_dir,processed_folder,
                                'split_libraries','seqs.qual')
            # open sequence files
            seqs=MinimalFastaParser(open(split_lib_seqs,'U'))
            qual_sequences=MinimalFastaParser(open(split_lib_qual,'U'))
        
            # open split-lib seq fp
            seqs=MinimalFastaParser(open(split_lib_seqs,'U'))
            # iterate over sequences
            for seq_name,seq in seqs:
                # update sequence numbers since they may cause issues across
                # multiple split-lib runs
                qual_seq_name,qual_seq=qual_sequences.next()
                if seq_name==qual_seq_name:
                    
                    full_seq_name_list=seq_name.split()
                    seq_name_prefix='_'.join(full_seq_name_list[0].split('_')[:-1])
                
                    # get per sample sequence counts
                    if seq_name_prefix in samples:
                        samples[seq_name_prefix]=samples[seq_name_prefix]+1
                    else:
                        samples[seq_name_prefix]=1
                
                    # update the sequence name, but retain barcode info
                    updated_seq_name=seq_name_prefix + '_' + str(iterator) + \
                                     ' ' + ' '.join(full_seq_name_list[1:])
                
                    # write the sequence out in FASTA format
                    output_seqs.write('@%s\n%s\n+\n%s\n' % \
                            (str(updated_seq_name), str(seq), str(qual_seq)))
                    # write the sequence out in FASTA format
                    output_fna.write('>%s\n%s\n' % (str(updated_seq_name),
                                                     str(seq)))
                    iterator=iterator+1
                else:
                    print seq_name
            
            # get list of biom files
            gg_biom_fp=join(study_input_dir,processed_folder,
                            'gg_97_otus','exact_uclust_ref_otu_table.biom')
                            
            if exists(gg_biom_fp) and getsize(gg_biom_fp)>0:
                biom_files.append(gg_biom_fp)
                
    output_seqs.close()
    output_fna.close()
    
    # zip the full split-library sequence file
    #cmd_call='cd %s; tar rzvf %s %s' % (study_input_dir,zip_fname,seq_fname)
    #cmd_call='cd %s; tar rzvf %s %s' % (study_input_dir,zip_fname,fna_fname)
    #system(cmd_call)
    
    return files_to_remove, biom_files, samples