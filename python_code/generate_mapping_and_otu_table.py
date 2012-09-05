__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2012, QIIME-webdev project"
__credits__ = ["Doug Wendel", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Jesse Stombaugh","Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

from data_access_connections import data_access_factory
from enums import ServerConfig
from cogent.app.util import get_tmp_filename
from numpy import inf
from os import system,path,makedirs
import os
from random import choice
from numpy import zeros
from time import strftime,clock,time
from qiime.merge_mapping_files import merge_mapping_files
from qiime.parse import parse_mapping_file,parse_qiime_parameters
from datetime import datetime
from time import strftime
from run_process_sff_through_split_lib import web_app_call_commands_serially
from qiime.workflow import print_commands,call_commands_serially,\
                           print_to_stdout, no_status_updates,generate_log_fp,\
                           get_params_str, WorkflowError,WorkflowLogger
from qiime.util import get_qiime_scripts_dir,create_dir,load_qiime_config,\
                       get_qiime_library_version
from cogent.util.misc import get_random_directory_name
from submit_job_to_qiime import submitQiimeJob
from qiime.filter import filter_samples_from_otu_table
from biom.table import SparseOTUTable, DenseOTUTable, table_factory,\
                       get_biom_format_version_string,get_biom_format_url_string
from json import dumps
from numpy import array

# get qiime config and qiime scripts directory
qiime_config = load_qiime_config()
script_dir = get_qiime_scripts_dir()

def combine_map_header_cols(combinecolorby, mapping):
    """Merge two or more mapping columns into one column"""
    
    # create an empty array the size of the mapping file
    combinedmapdata=array([''] * len(mapping), dtype='a1000')
    title=[]
    match=False
    # iterate over columns and see if the colunns are supposed to be joined
    for p in range(len(combinecolorby)):                    
        for i in range(len(mapping[0])):
            if str(combinecolorby[p]) == str(mapping[0][i]):
                match=True
                for q in range(len(mapping)):
                    
                    # merge columns
                    if combinedmapdata[q] == '':
                        combinedmapdata[q] = mapping[q][i]
                    else:
                        combinedmapdata[q] = combinedmapdata[q] + '_' + \
                                                                mapping[q][i]
                break
            else:
                match=False
        
        # no column matches found
        if not match:
            raise ValueError, 'One of the columns you tried to combine does not exist!'
        title.append(combinecolorby[p])
        
    # merge the column header names
    combinedmapdata[0]='_and_'.join(title)
    for i in range(len(combinedmapdata)):
        mapping[i].append(combinedmapdata[i])
    
    return mapping

def get_mapping_data(data_access,is_admin,table_col_value,user_id,
                     get_count=False):
    """ Get the metadata associated to the form values selected by the end-user """
    
    #recorded_fields = data_access.getMetadataFields(study_id)
    database_map = {}
    tables = []
    study_id_array=[]
    
    # Start building the statement for writing out the mapping file
    # THIS ORDER MUST REMAIN THE SAME SINCE CHANGES WILL AFFECT LATER FUNCTION
    statement = '"SAMPLE".sample_name||\'.\'||"SEQUENCE_PREP".sequence_prep_id as SampleID, \n'
    statement += '"SEQUENCE_PREP".barcode, \n'
    statement += 'concat("SEQUENCE_PREP".linker, "SEQUENCE_PREP".primer) as LinkerPrimerSequence, \n'
    statement += '"SAMPLE".study_id, \n'
    statement += '"SEQUENCE_PREP".run_prefix as RUN_PREFIX, \n'

    # Break out the recorded fields and store as dict: field name and table name
    # field[0] = field_name, field[1] = table_name

    # since the form values are using html forms, we needed to put specific 
    # separators in place. 
    for i in table_col_value:
        
        # get a list of tables and columns and studies
        tab_col_studies=i.split('####SEP####')
        
        # get a list of DB tables
        tab=tab_col_studies[0].upper()
        
        # get a list of metadata columns and study ids
        col_studies=tab_col_studies[1].split('####STUDIES####')
        
        # get a list of studies
        column=col_studies[0].upper()
        
        # get a list of studies
        studies=col_studies[1].split('S')
        for study_id in studies:
            study_id_array.append(study_id)

        # Required fields which much show up first. 
        # Skip as they are already in the statement
        if column in ['SAMPLE_NAME', 'BARCODE','DESCRIPTION','RUN_PREFIX']:
            continue

        # Add to select list
        statement += '"'+tab + '"."' + column + '", \n'

        # Add the table to our list if not already there and not one of the 
        # required tables
        if '"'+tab+'"' not in tables and '"'+tab+'"' not in ['"STUDY"', \
                                                             '"SAMPLE"', \
                                                             '"SEQUENCE_PREP"']:
            tables.append('"'+tab+'"')

        # Finally, add to our column list
        database_map[column] = '"'+tab+'"'

        # End for
    
    # append the Description column
    statement += '"SAMPLE".description as Description \n'
    unique_study_ids=list(set(study_id_array))
    
    ###this is for the website sample count
    if get_count:
        statement = 'count(1) \n'
    
    # if the user is an admin, we do not need to check permission for use of 
    # studies
    if is_admin:
        statement = '\
        select distinct \n' + statement + ' \n\
        from "STUDY" '
    else:
        statement = '\
        select distinct \n' + statement + ' \n\
        from "STUDY" inner join user_study us on "STUDY".study_id=us.study_id'

    # append SAMPLE Table
    statement += ' \n\
    inner join "SAMPLE" \n\
    on "STUDY".study_id = "SAMPLE".study_id \n '
    
    # append SEQUENCE_PREP Table
    statement += ' \
    left join "SEQUENCE_PREP" \n\
    on "SAMPLE".sample_id = "SEQUENCE_PREP".sample_id \n '

    # Handle Common fields table
    if '"COMMON_FIELDS"' in tables:
        tables.remove('"COMMON_FIELDS"')
        statement += '\
        left join "COMMON_FIELDS" \n\
        on "SAMPLE".sample_id = "COMMON_FIELDS".sample_id \n'

    # Handle host tables
    if '"HOST_SAMPLE"' in tables:
        statement += '\
        left join "HOST_SAMPLE" \n\
        on "SAMPLE".sample_id = "HOST_SAMPLE".sample_id\n'

    # Deal with the rest of the tables. They should all be associated by 
    # sample id.
    for table in tables:
        if table=='"HOST"' in tables and '"HOST_SAMPLE"' not in tables:
            statement += '\
            left join "HOST_SAMPLE" \n\
            on "SAMPLE".sample_id = "HOST_SAMPLE".sample_id\n'
            statement += '\
            left join ' + table + '\n\
            on "HOST_SAMPLE".host_id = ' + table + '.host_id\n '
        elif table=='"HOST"' and '"HOST_SAMPLE"' in tables:
            statement += '\
            left join ' + table + '\n\
            on "HOST_SAMPLE".host_id = ' + table + '.host_id\n '
        elif table.lower().startswith('"extra_prep') or \
                                    table=='"COMMON_EXTRA_PREP"':
            statement += '\
            left join ' + table + '\n\
            on "SEQUENCE_PREP".sample_id = ' + table + \
            '.sample_id and "SEQUENCE_PREP".row_number = ' + table + \
            '.row_number\n '
        elif table!='"HOST_SAMPLE"':
            statement += '\
            left join ' + table + '\n\
            on "SAMPLE".sample_id = ' + table + '.sample_id\n '

    # add the study ids to the statement
    study_statement=[]
    for study_id in unique_study_ids:
        study_statement.append('"STUDY".study_id = ' + study_id)
        
    # if admin we can use all studies, but if not, then we need to allow for
    # user-specific or public studies only
    if is_admin:
        statement += ' where (%s)' % (' or '.join(study_statement))
    else:
        statement += ' where (%s) and ("SAMPLE"."PUBLIC"=\'y\' or us.web_app_user_id=%s)' % (' or '.join(study_statement),user_id)
    
    
    # Now we iterate over the form values and determine if the user
    # selected only specific values for a given metadata category (i.e. 
    # ENVO:feces or GAZ:United States of America)
    additional_where_statements=[]
    for i in table_col_value:
        # split on table and columns and studies
        tab_col_studies=i.split('####SEP####')
        
        # get the list of tables
        tab=tab_col_studies[0]
        
        # split on column and study
        col_studies=tab_col_studies[1].split('####STUDIES####')
        
        # get a list of columns
        column=col_studies[0]
        
        # get a list of selected column values
        selected_col_values=table_col_value[i].split('\',\'')
        
        # check if controlled vocabulary
        controlled_col=data_access.checkIfColumnControlledVocab(str(column))
        if controlled_col:
            vocab_terms=data_access.getValidControlledVocabTerms(str(column))
        same_col_addition_statements=[]

        # iterate over selected values
        for col_value in selected_col_values:
            col_value=col_value.strip('\'')
            
            # strip off quotes, since SQL will get screwed up otherwise
            clipped_col_value=str(col_value.strip("'"))
            
            # check if controlled vocab
            if controlled_col:
            
                # put the column values into a dictionary so we can run natural 
                # sort on the list
                for i in vocab_terms:
                    if i[1]==str(clipped_col_value):
                        clipped_col_value=str(i[0])
                        break
            
            if clipped_col_value<>'####ALL####' and \
                                            clipped_col_value.upper()<>'NONE':
                same_col_addition_statements.append('"' + tab + '"."' + \
                                                    column + '"=\'' + \
                                                    clipped_col_value+'\'')
        if same_col_addition_statements<>[]:
            additional_where_statements.append('(%s)' % \
                                    (' or '.join(same_col_addition_statements)))
    if additional_where_statements<>[]:
        statement += ' and (%s) ' % (' and '.join(additional_where_statements)) 

    # Run the statement
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    # print statement
    
    results = cur.execute(statement)
        
    cur_description=[]
    for column in cur.description:
        cur_description.append(column)
    
    # get metadata
    result_arr=[]
    for i in results:
        result_arr.append(i)

    return result_arr,cur_description


def write_mapping_and_otu_table(data_access, table_col_value, fs_fp, web_fp, 
                                file_name_prefix,user_id,meta_id,params_path,
                                rarefied_at,otutable_rarefied_at,
                                jobs_to_start,tax_name,tree_fp):
    """ Write out the mapping file and OTU-table """
    
    tmp_prefix=get_tmp_filename('',suffix='').strip()

    total1 = time()
    unique_cols=[]
    
    # get the directory location for the files to write
    otu_table_file_dir=path.join(fs_fp,'otu_table_files')
    mapping_file_dir=path.join(fs_fp,'mapping_files')
    zip_file_dir=path.join(fs_fp,'zip_files')
    #pcoa_file_dir_loc=path.join(fs_fp,'pcoa_files')
    
    # get the url location for the files to write
    otu_table_file_dir_db=path.join(web_fp,'otu_table_files')
    mapping_file_dir_db=path.join(web_fp,'mapping_files')
    zip_file_dir_db=path.join(web_fp,'zip_files')
    pcoa_file_dir_loc_db=path.join(web_fp,'pcoa_files')
    
    # generate random directory name
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
    results,cur_description=get_mapping_data(data_access, is_admin, 
                                             table_col_value, user_id)

    # need to reconnect to data_access, since it gets closed due to con.close()
    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig
        import cx_Oracle
        data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
        
    # get filepaths for mapping files using the run-prefixes
    tmp_mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix + \
                                                        '_map_tmp.txt'), 'w')
    map_filepath=os.path.join(mapping_file_dir, file_name_prefix + '_' + \
                                                        tmp_prefix + '_map.txt')
    map_filepath_db=os.path.join(mapping_file_dir_db, file_name_prefix + '_' + \
                                                        tmp_prefix + '_map.txt')

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
        controlled_vocab_lookup[controlled_vocab_columns[column]] = \
                                                    dict(vocab_id_to_valid_term)
    
    # Write out the key field headers
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
        
        # write out controlled vocabulary values
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
    open_tmp_mapping_file=open(os.path.join(mapping_file_dir, 
                                file_name_prefix + '_map_tmp.txt')).readlines()
    mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix + \
                                        '_' + tmp_prefix + '_map.txt'), 'w')
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
    result.append(all_headers)
    for mapping_line in mapping_lines:
        result.append([mapping_line.get(h,'NA') for h in all_headers if h!=''])

    #Create an array using multiple columns from mapping file
    try:
        parameter_f = open(params_path)
    except IOError:
        raise IOError,\
         "Can't open parameters file (%s). Does it exist? Do you have read access?"\
         % params_path
    
    # determine if columns should be combined
    qiime_params=parse_qiime_parameters(parameter_f)
    try:
        combined_mapping_categories = \
                        qiime_params['combine_metadata']['columns'].split(',')
    except:
        combined_mapping_categories=''
    
    # combine metadata columns
    if combined_mapping_categories:
        for mapping_category in combined_mapping_categories:
            combinecolorby=mapping_category.strip('\'').strip('"').split('_and_')
            result=combine_map_header_cols(combinecolorby,result)
        
    # write final mapping file
    final_mapping=[]
    for i,mdata in enumerate(result):
        if i==0:
            final_mapping.append('#'+'\t'.join(mdata))
        else:
            final_mapping.append('\t'.join(mdata))
        
    #test=merge_mapping_files([merged_file])
    mapping_file.write('\n'.join(final_mapping))
    mapping_file.close()
    
    #flush result
    final_mapping=[]
    result=[]
    
    t2 = time()
    print 'Making map file: %s' % (t2 - t1)
    
    t1 = time()
    
    # write the OTU-table
    otu_table_filepath, otu_table_filepath_db, otu_table_fname = \
                    write_otu_table(data_access, 
                                    samples_list, tax_name, file_name_prefix,
                                    tmp_prefix, otu_table_file_dir,
                                    otu_table_file_dir_db)
    
    # zip up the files and add the paths to DB
    zip_fpath, zip_fpath_db = zip_and_add_filepaths(data_access, 
                          file_name_prefix, 
                          tmp_prefix, meta_id, otu_table_file_dir, 
                          mapping_file_dir, zip_file_dir, zip_file_dir_db, 
                          map_filepath, map_filepath_db, otu_table_filepath, 
                          otu_table_filepath_db, params_path)
    
    # rarefy OTU table if necessary
    if otutable_rarefied_at:
        rarefy_otu_table(data_access, otu_table_fname, otu_table_file_dir, 
                         otu_table_file_dir_db, otutable_rarefied_at, meta_id, 
                         otu_table_filepath, otu_table_filepath_db, zip_fpath)
                         
    # run any additional analysis, such as heatmap, bdiv, alpha-rare
    run_other_qiime_analysis(data_access, fs_fp, web_fp, otu_table_filepath, 
                              map_filepath, file_name_prefix, user_id, meta_id, 
                              params_path, rarefied_at, jobs_to_start, tree_fp, 
                              zip_fpath, zip_fpath_db)
    
def write_otu_table(data_access, samples_list, tax_name, file_name_prefix,
                    tmp_prefix, otu_table_file_dir, otu_table_file_dir_db):
    """ Write out the OTU-table """
    
    # Get the OTU-Ids and counts for each sample (OTU-Table)
    sample_counts={}
    otus=[]
    updated_sample_list=[]
    
    # iterate over samples and get the counts
    for i,sample_name1 in enumerate(samples_list):
       sample_counts[sample_name1]={}
       user_data=data_access.getOTUTable(True, sample_name1, 'UCLUST_REF', 97,
                                         'GREENGENES_REFERENCE',97)
       for row in user_data:
           if row[0] not in otus:
               otus.append(str(row[0]))
           if sample_counts[sample_name1].has_key(str(row[0])):
               raise ValueError, 'Duplicate prokmsa ids! - %s ' % sample_name1
           
           ## store OTU counts
           sample_counts[sample_name1][str(row[0])]=row[1]

       # create a list of only samples with OTU hits
       if sample_counts[sample_name1]!={}:
           updated_sample_list.append(sample_name1)
    
    # flush some memory
    samples_list=[]

    # prepare data for json dictionary
    dict_for_json={}
    dict_for_json['id']=None
    dict_for_json['format']=get_biom_format_version_string()
    dict_for_json['format_url']=get_biom_format_url_string()
    dict_for_json['type']="OTU table"
    dict_for_json['generated_by']="QIIME-DB %s" % get_qiime_library_version()
    dict_for_json['date']= "%s" % datetime.now().isoformat()
    dict_for_json['matrix_type']="sparse"
    dict_for_json['matrix_element_type']="int"
    dict_for_json['shape']=[len(otus),len(updated_sample_list)]
    dict_for_json['rows']=[]
    dict_for_json["data"]=[]
    dict_for_json["columns"]=[]

    # create the sparse data output
    for i,sample in enumerate(updated_sample_list):
        dict_for_json["columns"].append({"id":sample, "metadata":None})
        for j, otu in enumerate(otus):
            if sample_counts.has_key(sample):
                if sample_counts[sample].has_key(otu):
                    dict_for_json["data"].append([j, i, 
                                                  sample_counts[sample][otu]])

    # Get Taxonomy information for each observation
    taxonomy=[]
    for i in otus:
       tax_str=data_access.getGGTaxonomy(True,i,tax_name+'_tax_string')
       if not tax_str:
           dict_for_json['rows'].append({"id":"GG_OTU_1", "metadata":None})
       else:
           dict_for_json['rows'].append({"id":i, 
                                    "metadata":{'taxonomy':tax_str.split(';')}})


    json_dump= dumps(dict_for_json)
    
    # flush dict
    dict_for_json={}
    
    """
    # we are dumping json now instead 
    # create the biom object
    otu_biom=table_factory(otu_table,samples_list,otus,
                          sample_metadata=None,
                          observation_metadata=taxonomy,
                          table_id=None,
                          constructor=SparseOTUTable,
                          dtype=int)
    """
    # create OTU table filepaths
    otu_table_fname = file_name_prefix+'_'+tmp_prefix+'_otu_table.biom'
    otu_table_filepath=os.path.join(otu_table_file_dir, otu_table_fname)
    otu_table_filepath_db=os.path.join(otu_table_file_dir_db, otu_table_fname)
    
    # write OTU table
    otu_table_write=open(otu_table_filepath,'w')
    otu_table_write.write(json_dump)
    otu_table_write.close()
    
    return otu_table_filepath, otu_table_filepath_db, otu_table_fname

def zip_and_add_filepaths(data_access, file_name_prefix, tmp_prefix, meta_id,
                          otu_table_file_dir, mapping_file_dir, zip_file_dir, 
                          zip_file_dir_db, map_filepath, map_filepath_db, 
                          otu_table_filepath, otu_table_filepath_db, 
                          params_path):
    """ Zip and add filepaths to the DB """
    
    # zip up the OTU table and Mapping file for easy download
    zip_fpath=os.path.join(zip_file_dir, file_name_prefix + '_' + tmp_prefix + \
                                                    '_map_and_otu_table.zip')
    zip_fpath_db=os.path.join(zip_file_dir_db, file_name_prefix + '_' + \
                                          tmp_prefix + '_map_and_otu_table.zip')
    
    cmd_call='cd %s; zip %s %s' % (mapping_file_dir, zip_fpath, 
                                   map_filepath.split('/')[-1])
    system(cmd_call)
    cmd_call='cd %s; zip %s %s' % (otu_table_file_dir, zip_fpath, 
                                   otu_table_filepath.split('/')[-1])
    system(cmd_call)
    params_fpath=params_path.split('/')
    cmd_call='cd %s; zip %s %s' % ('/'.join(params_fpath[:-1]), zip_fpath, 
                                   params_fpath[-1])
    system(cmd_call)
    
    # get the date to put in the db
    run_date=datetime.now().strftime("%d/%m/%Y/%H/%M/%S")
    
    # Insert filepaths into the DB
    valid=data_access.addMetaAnalysisFiles(True, int(meta_id), map_filepath_db, 
                                           'OTUTABLE', run_date, 'MAPPING')
    if not valid:
        raise ValueError, 'There was an issue uploading the filepaths to the DB!'
    
    # Insert filepaths into the DB
    valid=data_access.addMetaAnalysisFiles(True, int(meta_id), 
                                           otu_table_filepath_db, 'OTUTABLE', 
                                           run_date, 'OTU_TABLE')
    if not valid:
        raise ValueError, 'There was an issue uploading the filepaths to the DB!'
    
    
    #add the zip file to the DB
    valid=data_access.addMetaAnalysisFiles(True, int(meta_id), zip_fpath_db, 
                                           'OTUTABLE', run_date, 'ZIP')
    if not valid:
        raise ValueError, 'There was an issue uploading the filepaths to the DB!'
        
    return zip_fpath, zip_fpath_db

def rarefy_otu_table(data_access, otu_table_fname, otu_table_file_dir, 
                     otu_table_file_dir_db, otutable_rarefied_at, meta_id, 
                     otu_table_filepath, otu_table_filepath_db, zip_fpath):
    """ Rarefy the OTU table is specified by user """
    
    otu_table_basename, otu_table_ext = os.path.splitext(otu_table_fname)
    
    python_exe_fp = qiime_config['python_exe_fp']
    commands=[]
    command_handler=call_commands_serially
    status_update_callback=no_status_updates
    logger = WorkflowLogger(generate_log_fp('/tmp/'),
                            params=dict(''),
                            qiime_config=qiime_config)
    
    # get the date to put in the db
    run_date=datetime.now().strftime("%d/%m/%Y/%H/%M/%S")
    
    # Sample the OTU table at even depth
    new_fname='%s_even%d%s' % (otu_table_basename, otutable_rarefied_at, 
                               otu_table_ext)
    even_sampled_otu_table_fp = os.path.join(otu_table_file_dir, new_fname)
    single_rarefaction_cmd = \
     '%s %s/single_rarefaction.py -i %s -o %s -d %d' % \
     (python_exe_fp, script_dir, otu_table_filepath,
      even_sampled_otu_table_fp, otutable_rarefied_at)
    commands.append([('Sample OTU table at %d seqs/sample' % \
                     otutable_rarefied_at, single_rarefaction_cmd)])
      
    otu_table_filepath=even_sampled_otu_table_fp
    otu_table_filepath_db=os.path.join(otu_table_file_dir_db, new_fname)
    
    # Call the command handler on the list of commands
    command_handler(commands, status_update_callback, logger)
    
    # Insert the rarefied OTU table filepath to the DB
    valid=data_access.addMetaAnalysisFiles(True, int(meta_id), 
                                           otu_table_filepath_db, 
                                           'OTUTABLE', run_date, 
                                           'OTU_TABLE')
    if not valid:
        raise ValueError, 'There was an issue uploading the filepaths to the DB!'
    
    # zip the rarefied OTU table
    cmd_call='cd %s; zip %s %s' % (otu_table_file_dir, zip_fpath, 
                                   otu_table_filepath.split('/')[-1])
    system(cmd_call)
    
    return

def run_other_qiime_analysis(data_access, fs_fp, web_fp, otu_table_filepath, 
                             map_filepath, file_name_prefix, user_id, meta_id, 
                             params_path, rarefied_at, jobs_to_start, tree_fp, 
                             zip_fpath, zip_fpath_db):

    # get the date to put in the db
    run_date=datetime.now().strftime("%d/%m/%Y/%H/%M/%S")
    
    # Prepare the params for submitting new jobs to the torque-poller
    params=[]
    params.append('fs_fp=%s' % fs_fp)
    params.append('web_fp=%s' % web_fp)
    params.append('otu_table_fp=%s' % otu_table_filepath)
    params.append('mapping_file_fp=%s' % map_filepath)
    params.append('fname_prefix=%s' % file_name_prefix)
    params.append('user_id=%s' % user_id)
    params.append('meta_id=%s' % meta_id)
    params.append('params_path=%s' % params_path)
    params.append('bdiv_rarefied_at=%s' % rarefied_at)
    params.append('jobs_to_start=%s' % jobs_to_start)
    params.append('tree_fp=%s' % tree_fp)
    params.append('run_date=%s' % run_date)
    params.append('zip_fpath=%s' % zip_fpath)
    params.append('zip_fpath_db=%s' % zip_fpath_db)
    job_input='!!'.join(params)
    
    # Determine which meta-analyses the user selected 
    analyses_to_start=jobs_to_start.split(',')
    
    # Prepare TopiaryExplorer job
    if 'showTE' in analyses_to_start:
        tree_fpath=path.abspath('%s/software/gg_otus_4feb2011/trees/gg_97_otus_4feb2011.tre' % (os.environ['HOME']))
        python_exe_fp = qiime_config['python_exe_fp']
        commands=[]
        command_handler=call_commands_serially
        status_update_callback=no_status_updates
        logger = WorkflowLogger(generate_log_fp('/tmp/'),
                               params=dict(''),
                               qiime_config=qiime_config)
        
        #define topiary explorer fpaths
        jnlp_fname=path.splitext(path.split(otu_table_filepath)[-1])[0]+'.jnlp'
        tep_fname=path.splitext(path.split(otu_table_filepath)[-1])[0] + '.tep'
        jnlp_filepath_web=path.join(web_fp, 'topiaryexplorer_files', jnlp_fname)
        jnlp_filepath_web_tep=path.join(web_fp,'topiaryexplorer_files', 
                                        tep_fname)
        
        # define the hard-link for the JNLP 
        if ServerConfig.home=='/home/wwwdevuser/':
            host_name='http://webdev.microbio.me/qiime'
        else:
            host_name='http://www.microbio.me/qiime'
            
        jnlp_filepath_web_tep_url=path.join(host_name, jnlp_filepath_web_tep)
        output_dir=os.path.join(fs_fp, 'topiaryexplorer_files')
        
        #build command
        make_tep_cmd='%s %s/make_tep.py -i %s -m %s -t %s -o %s -u %s -w' %\
        (python_exe_fp, script_dir, otu_table_filepath, map_filepath, 
         tree_fpath, output_dir, jnlp_filepath_web_tep_url)
        
        commands.append([('Make TopiaryExplorer jnlp', make_tep_cmd)])

        # Call the command handler on the list of commands
        command_handler(commands, status_update_callback, logger)
        
        #zip Topiary Explorer jnlp file
        cmd_call='cd %s; zip %s %s' % (output_dir,zip_fpath,jnlp_fname)
        system(cmd_call)
        
        #zip Topiary Explorer project file
        cmd_call='cd %s; zip %s %s' % (output_dir,zip_fpath,tep_fname)
        system(cmd_call)
        
        valid=data_access.addMetaAnalysisFiles(True, int(meta_id), 
                                               jnlp_filepath_web, 'OTUTABLE', 
                                               run_date, 'TOPIARYEXPLORER')
        if not valid:
            raise ValueError, 'There was an issue uploading the filepaths to the DB!'
            
    # Generate and Submit Beta-Diversity Job
    if 'bdiv' in analyses_to_start:
        job_type='betaDiversityThroughPlots'

        # Submit the Beta Diversity jobs
        try:
            # Attempt the submission
            submitQiimeJob(meta_id, user_id, job_type, job_input, data_access)
        
        except Exception, e:
            raise ValueError,e
    
    # Generate and Submit Heatmap Job        
    if 'heatmap' in analyses_to_start:
        job_type='makeOTUHeatmap'
        
        # Submit the Beta Diversity jobs
        try:
            # Attempt the submission
            submitQiimeJob(meta_id, user_id, job_type, job_input, data_access)
        
        except Exception, e:
            raise ValueError,e
    
    # Generate and Submit Alpha-Diversity Job
    if 'arare' in analyses_to_start:
        job_type='alphaRarefaction'
        
        # Submit the Alpha Diversity jobs
        try:
            # Attempt the submission
            submitQiimeJob(meta_id, user_id, job_type, job_input, data_access)
        
        except Exception, e:
            raise ValueError,e
        
    # # Generate and Submit Summarized-Taxonomy Job
    if 'sumtaxa' in analyses_to_start:
        job_type='summarizeTaxa'
        
        # Submit the Summarized Taxa jobs
        try:
            # Attempt the submission
            submitQiimeJob(meta_id, user_id, job_type, job_input, data_access)
        
        except Exception, e:
            raise ValueError,e

def check_job_state_id(data_access, meta_id, job_type_id):
    """ get the job_state_ids """
    
    jobs = data_access.getJobInfo(meta_id, job_type_id)
    
    return jobs[0]