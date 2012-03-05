__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Jesse Stombaugh","Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

from subprocess import Popen, PIPE, STDOUT
from data_access_connections import data_access_factory
from enums import ServerConfig
from cogent.app.util import get_tmp_filename
from os import system,path,makedirs
import os
from random import choice
from numpy import zeros
from time import strftime,clock,time
from qiime.merge_mapping_files import merge_mapping_files, write_mapping_file
from qiime.make_otu_table import make_otu_table
from qiime.parse import parse_mapping_file,parse_qiime_parameters
from datetime import datetime
from time import strftime
from load_tab_file import input_set_generator
from select_metadata import get_table_col_values_from_form
from qiime.format import format_matrix,format_otu_table
from run_process_sff_through_split_lib import web_app_call_commands_serially
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,generate_log_fp,\
                           get_params_str, WorkflowError,WorkflowLogger
from qiime.util import get_qiime_scripts_dir,create_dir,load_qiime_config
from cogent.util.misc import get_random_directory_name
from submit_job_to_qiime import submitQiimeJob
import socket
from generate_mapping_and_otu_table import get_mapping_data
qiime_config = load_qiime_config()
script_dir = get_qiime_scripts_dir()

def write_mapping(data_access, table_col_value, fs_fp, web_fp, 
                                file_name_prefix,user_id,meta_id,params_path,
                                rarefied_at,otutable_rarefied_at,
                                jobs_to_start,tax_name,tree_fp):
                                
    tmp_prefix=get_tmp_filename('',suffix='').strip()

    total1 = time()
    unique_cols=[]
    # Create the mapping file based on sample and field selections
    # get the directory location for the files to write
    otu_table_file_dir=path.join(fs_fp,'otu_table_files')
    mapping_file_dir=path.join(fs_fp,'mapping_files')
    zip_file_dir=path.join(fs_fp,'zip_files')
    #pcoa_file_dir_loc=path.join(fs_fp,'pcoa_files')

    otu_table_file_dir_db=path.join(web_fp,'otu_table_files')
    mapping_file_dir_db=path.join(web_fp,'mapping_files')
    zip_file_dir_db=path.join(web_fp,'zip_files')
    pcoa_file_dir_loc_db=path.join(web_fp,'pcoa_files')    
                
    alphabet = "ABCDEFGHIJKLMNOPQRSTUZWXYZ"
    alphabet += alphabet.lower()
    alphabet += "01234567890"
    random_dir_name=''.join([choice(alphabet) for i in range(10)])
    unique_name=strftime("%Y_%m_%d_%H_%M_%S")+random_dir_name
    #plot_unique_name=beta_metric+'_plots_'+unique_name
    #pcoa_file_dir=os.path.join(pcoa_file_dir_loc,plot_unique_name)
    #pcoa_file_dir_db=os.path.join(pcoa_file_dir_loc_db,plot_unique_name)
    #create_dir(pcoa_file_dir)
    map_files=[]
    
    t1 = time()
    
    # Get the user details
    user_details = data_access.getUserDetails(user_id)
    if not user_details:
        raise ValueError('No details found for this user')
    is_admin = user_details['is_admin']

    # get mapping results
    results,cur_description=get_mapping_data(data_access, is_admin, table_col_value, user_id)
   
    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig
        import cx_Oracle
        data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass

    # Write out proper header row, #SampleID, BarcodeSequence, LinkerPrimerSequence, Description, all others....
    tmp_mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix+'_map_tmp.txt'), 'w')
    map_filepath=os.path.join(mapping_file_dir, file_name_prefix+'_'+tmp_prefix+'_map.txt')
    map_filepath_db=os.path.join(mapping_file_dir_db, file_name_prefix+'_'+tmp_prefix+'_map.txt')

    # All mapping files start with an opening hash
    tmp_mapping_file.write('#')

    # determine if a column is a controlled vaocabulary columnn
    controlled_vocab_columns={}
    for i,column in enumerate(cur_description):
        if column in ['SAMPLE_NAME', 'BARCODE', 'LINKER', 'PRIMER', \
                      'EXPERIMENT_TITLE']:
            pass
        else:
            valid_controlled_vocab=\
                        data_access.checkIfColumnControlledVocab(column[0])
            if valid_controlled_vocab:
                controlled_vocab_columns[str(column[0])]=i

    # create a dictionary storing the controlled columns and their values
    controlled_vocab_lookup={}
    for column in controlled_vocab_columns:
        vocab_id_to_valid_term=data_access.getValidControlledVocabTerms(column)
        controlled_vocab_lookup[controlled_vocab_columns[column]]=dict(vocab_id_to_valid_term)


    to_write = ''
    for column in cur_description:
        if column[0]=='SAMPLEID':
            to_write+='SampleID\t'
        elif column[0]=='BARCODE':
            to_write+='BarcodeSequence\t'
        elif column[0]=='DESCRIPTION':
            to_write+='Description\t'
        elif column[0]=='LINKERPRIMERSEQUENCE':
            to_write+='LinkerPrimerSequence\t'
        else:
            to_write += column[0] + '\t'

    tmp_mapping_file.write(to_write[0:len(to_write)-1] + '\n')

    sample_to_run_prefix=[]
    study_id_and_run_prefix=[]
    samples_list=[]
    map_file_write=[]
    duplicate_samples=[]
    samples_list=[]

    for row in results:
        # Can't use something like '\t'.join(row) because not all items in list
        # are string values, hence the explicit loop structure here.
        to_write = ''
        sample_to_run_prefix.append(list((str(row[0]),str(row[4]),str(row[3]))))
    
        if list((str(row[3]),str(row[4]))) not in study_id_and_run_prefix:
            study_id_and_run_prefix.append(list((str(row[3]),str(row[4]))))
        
        if str(row[0]) in samples_list:
            # Order of row goes as follows: SampleID, BarcodeSequence,
            # LinkerPrimerSequence,Run_Prefix, then Description is at the end
            row=list(row)
            row[0]=row[0]+'_'+str(row[4])
            row=tuple(row)
            duplicate_samples.append(str(row[0]))
        else:    
            samples_list.append(str(row[0]))
    
        for i,column in enumerate(row):
            if controlled_vocab_lookup.has_key(i):
                val = str(column)
                if val == 'None':
                    new_val = ''
                else:
                    new_val=controlled_vocab_lookup[i][int(val)]
                to_write += new_val + '\t'
            else:
                val = str(column)
                if val == 'None':
                    val = ''
                to_write += val + '\t'
        # Write the row minus the last tab
        tmp_mapping_file.write(to_write[0:len(to_write)] + '\n')

    tmp_mapping_file.close()
    open_tmp_mapping_file=open(os.path.join(mapping_file_dir, file_name_prefix+'_map_tmp.txt')).readlines()
    mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix+'_'+tmp_prefix+'_map.txt'), 'w')
    mapping_lines = []
    all_headers = {}
    result = []
    
    # iterate over mapping files, parsing each
    data, current_headers, current_comments = \
       parse_mapping_file(open_tmp_mapping_file,strip_quotes=False)
    all_headers.update(dict.fromkeys(current_headers))
    for d in data:
        current_values = {}
        for i,v in enumerate(d):
            if v !='':
                current_values[current_headers[i]] = v
        mapping_lines.append(current_values)
    
    # remove and place the fields whose order is important
    del all_headers['SampleID']
    del all_headers['BarcodeSequence']
    del all_headers['LinkerPrimerSequence']
    del all_headers['Description']
    all_headers = ['SampleID','BarcodeSequence','LinkerPrimerSequence'] \
     + list(all_headers) + ['Description']
    
    # generate the mapping file lines containing all fields
    result.append('#' + '\t'.join(all_headers))
    for mapping_line in mapping_lines:
        result.append('\t'.join(\
         [mapping_line.get(h,'NA') for h in all_headers if h!='']))
    
    #test=merge_mapping_files([merged_file])
    mapping_file.write('\n'.join(result))
    mapping_file.close()
    
    t2 = time()
    print 'Making map file: %s' % (t2 - t1)
    
    t1 = time()
    

    # zip up the OTU table and Mapping file for easy download
    zip_fpath=os.path.join(zip_file_dir, file_name_prefix + '_' + tmp_prefix + '_map.zip')
    zip_fpath_db=os.path.join(zip_file_dir_db, file_name_prefix + '_' + tmp_prefix+ '_map.zip')
    
    cmd_call='cd %s; zip %s %s' % (mapping_file_dir,zip_fpath,map_filepath.split('/')[-1])
    system(cmd_call)
    params_fpath=params_path.split('/')
    cmd_call='cd %s; zip %s %s' % ('/'.join(params_fpath[:-1]),zip_fpath,params_fpath[-1])
    system(cmd_call)
    
    
    #get the date to put in the db
    run_date=datetime.now().strftime("%d/%m/%Y/%H/%M/%S")
    
    valid=data_access.addMetaAnalysisFiles(True,int(meta_id),map_filepath_db,'OTUTABLE',run_date,'MAPPING')
    if not valid:
        raise ValueError, 'There was an issue uploading the filepaths to the DB!'

            
    #add the zip file to the DB
    valid=data_access.addMetaAnalysisFiles(True,int(meta_id),zip_fpath_db,'OTUTABLE',run_date,'ZIP')
    if not valid:
        raise ValueError, 'There was an issue uploading the filepaths to the DB!'
        
