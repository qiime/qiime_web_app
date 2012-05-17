#!/usr/bin/env python
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

import time 
from subprocess import Popen, PIPE, STDOUT
from qiime.parse import parse_mapping_file,parse_classic_otu_table
from cogent.util.misc import app_path
from cogent.app.util import ApplicationNotFoundError
from cogent.parse.fastq import MinimalFastqParser
from os import system,popen
from glob import glob
import re
from random import choice
from datetime import datetime
from time import strftime
from qiime.workflow import WorkflowLogger
from os.path import *
from qiime.parse import fields_to_dict
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,generate_log_fp,\
                           get_params_str, WorkflowError
from qiime.util import (compute_seqs_per_library_stats, get_top_fastq_two_lines,
                        get_qiime_scripts_dir,qiime_system_call,
                        create_dir)
from wrap_files_for_md5 import MD5Wrap
from load_tab_file import input_set_generator, flowfile_inputset_generator, \
                            fasta_to_tab_delim
from cogent.parse.flowgram_parser import get_header_info
from hashlib import md5
from cogent.util.misc import safe_md5

  
def submit_sff_and_split_lib(data_access,fasta_files,metadata_study_id):
    '''
       This function takes the fasta filenames and using that path, determines
       the location of the split-library and picked-otu files.  Once file
       locations have been determined, it moves the files to the DB machine
       and load the files into the DB.
    '''
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    #print 'Rebuilding PK_SPLIT_LIBRARY_READ_MAP...'
    #cur.execute('alter index "SFF"."PK_SPLIT_LIBRARY_READ_MAP" rebuild ')
    #cur = con.cursor()
    study_id_exists=data_access.checkIfStudyIdExists(metadata_study_id)
    print "Study ID exists: " + str(study_id_exists)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUZWXYZ"
    alphabet += alphabet.lower()
    alphabet += "01234567890"
    random_fname=''.join([choice(alphabet) for i in range(10)])
    tmp_filename ='_'+random_fname+'_'+strftime("%Y_%m_%d_%H_%M_%S")
    fasta_filenames=fasta_files.split(',')
    seq_run_id=0  
    analysis_id=0    
    split_lib_input_checksums=[]
    fasta_qual_files=[]
    
    #valid = data_access.disableTableConstraints()
    print "Disabled table constraints"

    #split the fasta filenames and determine filepaths
    for fasta_fname in fasta_filenames:
        input_fname, input_ext = splitext(split(fasta_fname)[-1])
        input_basename, input_ext = splitext(fasta_fname)
        input_dir = split(input_basename)[:-1][0]
        
        if re.search('0\d$', input_fname)==None or re.search('0\d$', input_fname).group()==None:
            sff_basename=input_fname
        else:
            sff_basename=input_fname[:-2]

        if re.search('0\d_FLX$', sff_basename)==None or re.search('0\d_FLX$', sff_basename).group()==None:
            sff_basename=sff_basename
        else:
            sff_basename=sff_basename[:-6]

            
        print 'sff_basename: %s' % sff_basename

        analysis_notes=split(input_basename)[0]
        
        #using the fasta basename, define qual and flow files
        qual_fname=join(input_basename+'.qual')
        flow_fname=join(input_basename+'.txt')
        fasta_qual_files.append(fasta_fname)
        fasta_qual_files.append(qual_fname)
        
        #Run the Oracle process_sff_files load package
        ## Get the location and name of the SFF file, get it's MD5. .SFF is one 
        # directory up from the other files
        rev = dirname(fasta_fname)[::-1]
        
        sffs_in_processed_folder = glob(join(input_dir, '*_FLX.sff'))

        if len(sffs_in_processed_folder) == 0:
            sff_file_dir = split(input_dir)[0]
        else:
            sff_file_dir=input_dir
            
        sff_file = join(sff_file_dir, input_fname + '.sff')
        #sff_file = input_basename+'.sff'
        
        sff_md5 = safe_md5(open(sff_file)).hexdigest()
        
        print 'MD5 is: %s' % str(sff_md5)

        if analysis_id==0:
            analysis_id=data_access.createAnalysis(metadata_study_id)
        
        sff_exists=data_access.checkIfSFFExists(sff_md5)
        print 'sff in database? %s' % str(sff_exists)
        
        #if True:
        if not sff_exists:
            print 'flow_fname: %s' % flow_fname
            sff_header=get_header_info(open(flow_fname))
            
            if sff_header['# of Flows']=='400':
                instrument_code='GS FLX'
            elif sff_header['# of Flows']=='168':
                instrument_code='GS2-'
            elif sff_header['# of Flows']=='800':
                instrument_code='Titanium'
            else:
                instrument_code='UNKNOWN'
            print 'Instrument Code: %s' % instrument_code
            if seq_run_id==0:
                seq_run_id=data_access.createSequencingRun(True,instrument_code,
                                            sff_header['Version'],seq_run_id)
                valid=data_access.addSFFFileInfo(True,sff_basename,
                                             sff_header['# of Reads'],
                                             sff_header['Header Length'],
                                             sff_header['Key Length'],
                                             sff_header['# of Flows'],
                                             sff_header['Flowgram Code'],
                                             sff_header['Flow Chars'],
                                             sff_header['Key Sequence'],
                                             sff_md5,seq_run_id)
            else:
                valid=data_access.addSFFFileInfo(True,sff_basename,
                                             sff_header['# of Reads'],
                                             sff_header['Header Length'],
                                             sff_header['Key Length'],
                                             sff_header['# of Flows'],
                                             sff_header['Flowgram Code'],
                                             sff_header['Flow Chars'],
                                             sff_header['Key Sequence'],
                                             sff_md5,seq_run_id)

        else:
            seq_run_id=data_access.getSeqRunIDUsingMD5(sff_md5)
    
    print 'sequence_run_id is: %s' % str(seq_run_id)
            
    print fasta_qual_files
    split_lib_input_md5sum=safe_md5(MD5Wrap(fasta_qual_files)).hexdigest()
    print split_lib_input_md5sum
    print 'Finished loading the processed SFF data!'
    print 'Run ID: %s' % seq_run_id
    print 'Analysis ID: %s' % analysis_id
    
    valid=data_access.updateAnalysisWithSeqRunID(True,analysis_id,seq_run_id)
    if not valid:
        raise ValueError, 'Error: Unable to append SEQ_RUN_ID into ANALYSIS table!'

    return analysis_id,input_dir,seq_run_id,split_lib_input_md5sum

def load_split_lib_sequences(data_access,input_dir,analysis_id, seq_run_id,
                             split_lib_input_md5sum):

    #define the split library file paths using the original fasta input 
    #directory
    split_lib_seqs = join(input_dir, 'split_libraries', 'seqs.fna')
    split_lib_hist = join(input_dir, 'split_libraries', 'histograms.txt')
    split_lib_log = join(input_dir, 'split_libraries', 'split_library_log.txt')
    
    # this needs to be a try/except since FASTA files does not have these files
    try:
        split_hist_str = open(split_lib_hist).read()
        split_log_str = open(split_lib_log).read()
    except IOError:
        split_hist_str=None
        split_log_str=None
    
    #read in the workflow log file and determine timestamp and svn version of
    #Qiime used for the analysis
    svn_version = '1418' # This is temporarily defined, however will use script to dtermine this value
    qiime_revision=get_qiime_svn_version()
    run_date=datetime.now().strftime("%d/%m/%Y/%H/%M/%S")
    print run_date
    full_log_fp = glob(join(input_dir, 'log*.txt'))[0]
    full_log_str = open(full_log_fp, 'U').read()
    log_str = open(full_log_fp, 'U').readlines()
    
    split_lib_cmd="Split-libraries was not run due to this being a FASTA-file"
    pick_otus_cmd=''
    #from the workflow log file get the split-library and pick-otus cmds
    for substr in log_str:
        if 'split_libraries_fastq.py' in substr:
            split_lib_cmd=substr
        elif 'parallel_pick_otus_uclust_ref.py' in substr:
            pick_otus_cmd=substr
        elif 'split_libraries.py' in substr:
            split_lib_cmd=substr
        elif 'pick_otus.py' in substr:
            pick_otus_cmd=substr

    #Insert the split-library log information in the DB
    valid,split_library_run_id=data_access.loadSplitLibInfo(True,analysis_id,\
                                     run_date, split_lib_cmd,\
                                     svn_version, split_log_str, \
                                     split_hist_str, split_lib_input_md5sum)
                                     
    print "Split-Lib ID: %s" % split_library_run_id
    if not valid:
        raise ValueError,'Error: Unable to load split-library info to database server!'
    
    print "Finished loading the split-library log information!"

    #process and load_fna_data
    
    print "starting new fna load"
    start = time.time()

    ''' 
    The output values and types for each value are as follows:
    0: sequence run id (integer)
    1: sample id (text)
    2: barcode read group tag (text)
    3: read id (text)    
    4: original barcode (text)
    5: new barcode (text)
    6: number of barcode diffs (integer)
    7: sequence length (integer)
    8: sequence md5 hash (text)
    9: sequence string (text)
    '''

    types = ['i','i', 's', 's', 's', 's', 's', 'i', 'i', 'fc', 's']
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    #print 'Rebuilding PK_SPLIT_LIBRARY_READ_MAP...'
    #cur.execute('alter index "SFF"."PK_SPLIT_LIBRARY_READ_MAP" rebuild ')
    #cur = con.cursor()
    open_fasta = open(split_lib_seqs)
    iterator=0
    
    for res in input_set_generator(fasta_to_tab_delim(open_fasta, seq_run_id,\
                                    split_library_run_id), cur, types,\
                                    buffer_size=500):
        #print str(res)
        print 'running %i' % (iterator)
        iterator=iterator+1
        valid = data_access.loadFNAFile(True, res)
        if not valid:
            raise ValueError, 'Error: Unable to load FNA file into database!'

    open_fasta.close()

    end = time.time()
    print 'Total processor time elapsed: %s' % str(end - start)
    
    print 'Finished loading split_library FNA file.'
    
    try:
        ### MOVING THIS INTO SEQUENCE LOADING SINCE RELIES ON SPLIT_LIBRARY_READ_MAP
        # try/except necessary since some datasets are metagenomes, 
        # which do not have OTU failures
    
        # Get otu_picking_run_id
        con = data_access.getSFFDatabaseConnection()
        cur = con.cursor()
        statement='select otu_picking_run_id from analysis where analysis_id=%s' % (str(analysis_id))
        results = cur.execute(statement)
        for i in results:
            otu_picking_run_id=i[0]
    
        pick_otus_failures = join(input_dir, 'gg_97_otus', 'all_failures.txt')

        lines = open(pick_otus_failures,'U')
        otu_failures = []
        for line in lines:
            otu_failures.append('%s\t%s'% (line.strip('\n'),str(otu_picking_run_id)))
        types=['s','i']
        con=data_access.getSFFDatabaseConnection()
        cur = con.cursor()
        set_count = 1

        for input_set in input_set_generator(otu_failures, cur, types, buffer_size=10000):
            valid = data_access.loadOTUFailuresAll(True, input_set)
            if not valid:
                raise ValueError, 'Error: Unable to load OTU failures data into database!'
            print "loading OTU failure set: %s" % set_count
            set_count += 1

        print 'Successfully loaded the OTU failures into the database!'
    except:
        print "Unable to load OTU failures!"
    print 'End of function'
    
    return split_library_run_id
    
def load_otu_mapping(data_access, input_dir, analysis_id):
    # For OTU Tables
    #read in the workflow log file and determine timestamp and svn version of
    #Qiime used for the analysis
    pOTUs_threshold = '97'
    ref_set_threshold = '97'
    pOTUs_method='UCLUST_REF'
    reference_set_name='GREENGENES_REFERENCE'
    otus_log_str = open(join(input_dir, 'gg_97_otus', 'log.txt')).read()
    log_str = open(join(input_dir, 'gg_97_otus', 'log.txt')).readlines()
    
    #from the workflow log file get the pick-otus cmd
    for substr in log_str:
        if 'parallel_pick_otus_uclust_ref.py' in substr:
            pick_otus_cmd=substr
        elif 'pick_otus.py' in substr:
            pick_otus_cmd=substr
    
    otu_run_set_id = 0
    svn_version = '1418' # This is temporarily defined, however will use script to dtermine this value
    qiime_revision=get_qiime_svn_version()
    run_date=datetime.now().strftime("%d/%m/%Y/%H/%M/%S")    
    pick_otus_map = join(input_dir, 'gg_97_otus', 'exact_uclust_ref_otus.txt')
    #split_lib_seqs = join(input_dir, 'leftover.fasta')
    split_lib_seqs = join(input_dir, 'split_libraries', 'seqs.fna')
    split_lib_seqs_md5=safe_md5(open(split_lib_seqs)).hexdigest()
    
    #Insert the otu-picking log information in the DB
    print 'calling loadAllOTUInfo with analysis_id %s' % str(analysis_id)
    valid,new_otu_run_set_id,otu_picking_run_id=data_access.loadAllOTUInfo(True,
                                  otu_run_set_id, run_date,
                                  pOTUs_method, pOTUs_threshold,
                                  svn_version, pick_otus_cmd, otus_log_str,
                                  split_lib_seqs_md5,reference_set_name,
                                  ref_set_threshold, analysis_id)
    if not valid:
        raise ValueError, 'Error: Unable to load OTU run data into database!'
    else:
        print "Finished registering OTU run!"
    
    otu_map=[]
    otu_to_seqid = fields_to_dict(open(pick_otus_map, 'U'))
    for otu in otu_to_seqid:
        for sample in otu_to_seqid[otu]:
            otu_map.append('%s\t%s\t%s\t%s' % (otu,sample,new_otu_run_set_id, 
                                               reference_set_name))
    print 'Finished setting otu_map.'
    
    types = ['s','s','i','s']
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    #print 'Starting PK_SPLIT_LIBRARY_READ_MAP index rebuild...'
    #cur.execute('alter index "SFF"."PK_SPLIT_LIBRARY_READ_MAP" rebuild ')
    print 'Fisnished rebuilding index PK_SPLIT_LIBRARY_READ_MAP.'
    cur = con.cursor()
    set_count = 1
    
    print 'Loading OTU Table into the database!'
    pick_otus_table = join(input_dir, 'gg_97_otus','exact_uclust_ref_otu_table.txt')
    otu_table_lines=open(pick_otus_table).readlines()
    sample_ids, otu_ids, otu_table, lineages = parse_classic_otu_table(otu_table_lines)
    # convert OTU table to tab-delimited list
    otu_table_load=[]
    for i,otu in enumerate(otu_ids):
        for j,sample in enumerate(sample_ids):
            if otu_table[i][j]>0:
                otu_table_load.append("%s\t%s\t%s\t%s" % \
                                (otu,sample,new_otu_run_set_id,otu_table[i][j]))

    # get DB connection
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    
    # load otu table into DB
    data_types=['s','s','i','f']   
    set_count = 0      
    for input_set in input_set_generator(otu_table_load, cur,data_types,\
                                         buffer_size=1000):
        valid=data_access.loadOTUTable(True,input_set)
        if not valid:
            raise ValueError, 'Error: Unable to load OTU table!'
        print "loading OTU Table: %s" % set_count
        set_count += 1
    
    print 'Successfully loaded the OTU Table into the database!'
    print 'End of function' 

    
def cp_files(filepath,location):
    """Transfers files to another server."""
    check_cp()
    cmd_call='cp %s %s' % (filepath,location)
    print 'cp command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call

def zip_files(filepath1,filepath2,directory,location):
    """Transfers files to another server."""
    check_zip()
    
    cmd_call='cd %s | zip -jX split_library_input.zip %s' % (directory,filepath1)
    print 'zip command is: %s' % cmd_call
    system(cmd_call)
    cmd_call='cd %s | zip -jX split_library_input.zip %s' % (directory,filepath2)
    print 'zip command is: %s' % cmd_call
    system(cmd_call)
    return cmd_call

def get_qiime_svn_version():
    """Transfers files to another server."""
    qiime_dir=get_qiime_scripts_dir()
    cmd_call='svn info %s | egrep "Revision: "' % (qiime_dir)
    #print 'svn command is: %s' % cmd_call
    output = popen('svn info %s | egrep "Revision: "' % (qiime_dir)).read()
    revision=output.replace("Revision: ","")

    return revision

def check_cat():
    """Raise error if cat is not in $PATH """
    if not app_path('cat'):
        raise ApplicationNotFoundError,\
        "cat is not in $PATH. Is it installed? Have you added it to $PATH?"\
        
def check_cp():
    """Raise error if cp is not in $PATH """
    if not app_path('cp'):
        raise ApplicationNotFoundError,\
        "cp is not in $PATH. Is it installed? Have you added it to $PATH?"\

def check_zip():
    """Raise error if zip is not in $PATH """
    if not app_path('zip'):
        raise ApplicationNotFoundError,\
        "zip is not in $PATH. Is it installed? Have you added it to $PATH?"\

#

def submit_illumina_and_split_lib(data_access,fastq_files,metadata_study_id,
                                  input_dir):
     
    '''
        This function takes the fasta filenames and using that path, determines
        the location of the split-library and picked-otu files.  Once file
        locations have been determined, it moves the files to the DB machine
        and load the files into the DB.
    '''
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    #print 'Rebuilding PK_SPLIT_LIBRARY_READ_MAP...'
    #cur.execute('alter index "SFF"."PK_SPLIT_LIBRARY_READ_MAP" rebuild ')
    #cur = con.cursor()
    study_id_exists=data_access.checkIfStudyIdExists(metadata_study_id)
    print "Study ID exists: " + str(study_id_exists)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUZWXYZ"
    alphabet += alphabet.lower()
    alphabet += "01234567890"
    random_fname=''.join([choice(alphabet) for i in range(10)])
    tmp_filename ='_'+random_fname+'_'+strftime("%Y_%m_%d_%H_%M_%S")
    fastq_filenames=fastq_files.split(',')
    seq_run_id=0  
    analysis_id=0    
    split_lib_input_checksums=[]
    #fasta_qual_files=[]

    #valid = data_access.disableTableConstraints()
    print "Disabled table constraints"

    #split the fasta filenames and determine filepaths
    for fastq_fname in fastq_filenames:
        input_fname, input_ext = splitext(split(fastq_fname)[-1])
        input_basename, input_ext = splitext(fastq_fname)
        
        analysis_notes=split(input_basename)[0]
        
        fastq_md5 = safe_md5(open(fastq_fname)).hexdigest()

        print 'MD5 is: %s' % str(fastq_md5)

        if analysis_id==0:
            analysis_id=data_access.createAnalysis(metadata_study_id)
         
        fastq_exists=data_access.checkIfSFFExists(fastq_md5)
        print 'fastq in database? %s' % str(fastq_exists)
        
        if not fastq_exists:
            if seq_run_id==0:
                seq_run_id=data_access.createSequencingRun(True,'ILLUMINA',
                                                           None,seq_run_id)
            
            count_seqs_cmd="grep ^@ %s | wc -l" % (fastq_fname)
            o,e,r = qiime_system_call(count_seqs_cmd)
            seq_counts = o.strip()
            
            fastq_fname_open=open(fastq_fname)
            first_seq_fastq=get_top_fastq_two_lines(fastq_fname_open)
            header_length=len(first_seq_fastq[1])
            num_flows=len(first_seq_fastq[1])
            
            valid=data_access.addSFFFileInfo(True,input_fname,
                                          seq_counts,
                                          header_length,
                                          None,
                                          num_flows,
                                          None,
                                          None,
                                          None,
                                          fastq_md5,seq_run_id)
        else:
            seq_run_id=data_access.getSeqRunIDUsingMD5(fastq_md5)
             
    print 'sequence_run_id is: %s' % str(seq_run_id)
    
    #print fasta_qual_files
    split_lib_input_md5sum=safe_md5(MD5Wrap(fastq_filenames)).hexdigest()
    print split_lib_input_md5sum
    print 'Finished loading the processed ILLUMINA data!'
    print 'Run ID: %s' % seq_run_id
    print 'Analysis ID: %s' % analysis_id

    valid=data_access.updateAnalysisWithSeqRunID(True,analysis_id,seq_run_id)
    if not valid:
        raise ValueError, 'Error: Unable to append SEQ_RUN_ID into ANALYSIS table!'

    return analysis_id,input_dir,seq_run_id,split_lib_input_md5sum
    
#
#
def submit_fasta_and_split_lib(data_access,fasta_files,metadata_study_id,
                                  input_dir):
     
    '''
        This function takes the fasta filenames and using that path, determines
        the location of the split-library and picked-otu files.  Once file
        locations have been determined, it moves the files to the DB machine
        and load the files into the DB.
    '''
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()

    study_id_exists=data_access.checkIfStudyIdExists(metadata_study_id)
    print "Study ID exists: " + str(study_id_exists)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUZWXYZ"
    alphabet += alphabet.lower()
    alphabet += "01234567890"
    random_fname=''.join([choice(alphabet) for i in range(10)])
    tmp_filename ='_'+random_fname+'_'+strftime("%Y_%m_%d_%H_%M_%S")
    fasta_filenames=fasta_files.split(',')
    seq_run_id=0  
    analysis_id=0    
    split_lib_input_checksums=[]
    #fasta_qual_files=[]

    #valid = data_access.disableTableConstraints()
    print "Disabled table constraints"

    #split the fasta filenames and determine filepaths
    for fasta_fname in fasta_filenames:
        input_fname, input_ext = splitext(split(fasta_fname)[-1])
        input_basename, input_ext = splitext(fasta_fname)
        
        analysis_notes=split(input_basename)[0]
        
        fasta_md5 = safe_md5(open(fasta_fname)).hexdigest()

        print 'MD5 is: %s' % str(fasta_md5)

        if analysis_id==0:
            analysis_id=data_access.createAnalysis(metadata_study_id)
         
        fasta_exists=data_access.checkIfSFFExists(fasta_md5)
        print 'fasta in database? %s' % str(fasta_exists)
        
        if not fasta_exists:
            if seq_run_id==0:
                seq_run_id=data_access.createSequencingRun(True,'FASTA',
                                                           None,seq_run_id)
            
            count_seqs_cmd="grep '^>' %s | wc -l" % (fasta_fname)
            o,e,r = qiime_system_call(count_seqs_cmd)
            seq_counts = o.strip()
            
            valid=data_access.addSFFFileInfo(True,input_fname,
                                          seq_counts,
                                          None,
                                          None,
                                          None,
                                          None,
                                          None,
                                          None,
                                          fasta_md5,seq_run_id)
        else:
            seq_run_id=data_access.getSeqRunIDUsingMD5(fasta_md5)
             
    print 'sequence_run_id is: %s' % str(seq_run_id)
    
    #print fasta_qual_files
    split_lib_input_md5sum=safe_md5(MD5Wrap(fasta_filenames)).hexdigest()
    print split_lib_input_md5sum
    print 'Finished loading the processed FASTA data!'
    print 'Run ID: %s' % seq_run_id
    print 'Analysis ID: %s' % analysis_id

    valid=data_access.updateAnalysisWithSeqRunID(True,analysis_id,seq_run_id)
    if not valid:
        raise ValueError, 'Error: Unable to append SEQ_RUN_ID into ANALYSIS table!'
                                              
    return analysis_id,input_dir,seq_run_id,split_lib_input_md5sum