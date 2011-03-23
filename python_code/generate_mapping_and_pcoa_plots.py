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
from enums import DataAccessType
from cogent.app.util import get_tmp_filename
from os import system,path,makedirs
import os
from random import choice
from numpy import zeros
from time import strftime,clock,time
from qiime.merge_mapping_files import merge_mapping_files, write_mapping_file
from qiime.make_otu_table import make_otu_table
from qiime.parse import parse_mapping_file,parse_qiime_parameters

from load_tab_file import input_set_generator
from select_metadata import get_table_col_values_from_form
from qiime.format import format_matrix,format_otu_table
from run_process_sff_through_split_lib import web_app_call_commands_serially
from qiime.workflow import print_commands,\
                           print_to_stdout, no_status_updates,generate_log_fp,\
                           get_params_str, WorkflowError,WorkflowLogger
from qiime.util import get_qiime_scripts_dir,create_dir,load_qiime_config
from cogent.util.misc import get_random_directory_name


qiime_config = load_qiime_config()
            
def write_mapping_and_pcoa_plots(data_access, table_col_value, fs_fp, web_fp, file_name_prefix,user_id,meta_id,beta_metric,rarefied_at):
    total1 = time()
    unique_cols=[]
    # Create the mapping file based on sample and field selections
    # get the directory location for the files to write
    otu_table_file_dir=path.join(fs_fp,'otu_table_files')
    mapping_file_dir=path.join(fs_fp,'mapping_files')
    zip_file_dir=path.join(fs_fp,'zip_files')
    pcoa_file_dir_loc=path.join(fs_fp,'pcoa_files')

    otu_table_file_dir_db=path.join(web_fp,'otu_table_files')
    mapping_file_dir_db=path.join(web_fp,'mapping_files')
    zip_file_dir_db=path.join(web_fp,'zip_files')
    pcoa_file_dir_loc_db=path.join(web_fp,'pcoa_files')    
                
    alphabet = "ABCDEFGHIJKLMNOPQRSTUZWXYZ"
    alphabet += alphabet.lower()
    alphabet += "01234567890"
    random_dir_name=''.join([choice(alphabet) for i in range(10)])
    unique_name=strftime("%Y_%m_%d_%H_%M_%S")+random_dir_name
    plot_unique_name=beta_metric+'_plots_'+unique_name
    pcoa_file_dir=os.path.join(pcoa_file_dir_loc,plot_unique_name)
    pcoa_file_dir_db=os.path.join(pcoa_file_dir_loc_db,plot_unique_name)
    
    create_dir(pcoa_file_dir)
    
    map_files=[]
    
    t1 = time()
    
    #recorded_fields = data_access.getMetadataFields(study_id)
    database_map = {}
    tables = []
    
    # Get the user details
    user_details = data_access.getUserDetails(user_id)
    if not user_details:
        raise ValueError('No details found for this user')
    is_admin = user_details['is_admin']

    # Start building the statement for writing out the mapping file
    # THIS ORDER MUST REMAIN THE SAME SINCE CHANGES WILL AFFECT LATER FUNCTION
    statement = '"SAMPLE".sample_name||\'.\'||"SEQUENCE_PREP".sequence_prep_id as SampleID, \n'
    statement += '"SEQUENCE_PREP".barcode, \n'
    statement += 'concat("SEQUENCE_PREP".linker, "SEQUENCE_PREP".primer) as LinkerPrimerSequence, \n'
    statement += '"SAMPLE".study_id, \n'
    statement += '"SEQUENCE_PREP".run_prefix as RUN_PREFIX, \n'


    study_id_array=[]
    # Break out the recorded fields and store as dict: field name and table name
    # field[0] = field_name, field[1] = table_name

    for i in table_col_value:
        tab_col_studies=i.split('####SEP####')
        tab=tab_col_studies[0]
    
        col_studies=tab_col_studies[1].split('####STUDIES####')
    
        column=col_studies[0]
        studies=col_studies[1].split('S')
        for study_id in studies:
            study_id_array.append(study_id)
    
        # Required fields which much show up first. Skip as they are already in the statement
        if column in ['SAMPLE_NAME', 'BARCODE', 'LINKER', 'PRIMER', 'EXPERIMENT_TITLE','DESCRIPTION','RUN_PREFIX']:
            continue

        # Add to select list
        statement += '"'+tab + '"."' + column + '", \n'
   
        # Add the table to our list if not already there and not one of the required tables
        if '"'+tab+'"' not in tables and '"'+tab+'"' not in ['"STUDY"', '"SAMPLE"', '"SEQUENCE_PREP"']:
            tables.append('"'+tab+'"')

        # Finally, add to our column list
        database_map[column] = '"'+tab+'"'

        # End for

    unique_study_ids=list(set(study_id_array))
    
    statement += '"SEQUENCE_PREP".experiment_title as Description \n'
    
    if is_admin:
        statement = '\
        select distinct \n' + statement + ' \n\
        from "STUDY" '######inner join sff.analysis anal on "STUDY".study_id=anal.study_id'
    else:
        statement = '\
        select distinct \n' + statement + ' \n\
        from "STUDY" inner join user_study us on "STUDY".study_id=us.study_id'######inner join sff.analysis anal on "STUDY".study_id=anal.study_id'

    statement += ' \n\
    inner join "SAMPLE" \n\
    on "STUDY".study_id = "SAMPLE".study_id \n '

    statement += ' \
    inner join "SEQUENCE_PREP" \n\
    on "SAMPLE".sample_id = "SEQUENCE_PREP".sample_id \n '

    # Handle Common fields table
    if '"COMMON_FIELDS"' in tables:
        tables.remove('"COMMON_FIELDS"')
        statement += '\
    left join "COMMON_FIELDS" \n\
    on "SAMPLE".sample_id = "COMMON_FIELDS".sample_id \n'

    # Handle host tables
    if '"HOST_SAMPLE"' in tables:
        tables.remove('"HOST_SAMPLE"')
        statement += '\
        left join "HOST_SAMPLE" \n\
        on "SAMPLE".sample_id = "HOST_SAMPLE".sample_id\n'

    # Deal with the rest of the tables. They should all be assocaiated by sample id.
    for table in tables:
        if table=='"HOST"':
            statement += '\
            left join ' + table + '\n\
            on "HOST_SAMPLE".host_id = ' + table + '.host_id\n '
        else:
            statement += '\
            left join ' + table + '\n\
            on "SAMPLE".sample_id = ' + table + '.sample_id\n '

    # add the study ids to the statement
    study_statement=[]
    for study_id in unique_study_ids:
        study_statement.append('"STUDY".study_id = ' + study_id)

    if is_admin:
        statement += ' where (%s)' % (' or '.join(study_statement))
    else:
        statement += ' where (%s) and ("SAMPLE"."PUBLIC"=\'y\' or us.web_app_user_id=%s)' % (' or '.join(study_statement),user_id)
    
    additional_where_statements=[]
    for i in table_col_value:
        tab_col_studies=i.split('####SEP####')
        tab=tab_col_studies[0]
        col_studies=tab_col_studies[1].split('####STUDIES####')
        column=col_studies[0]
    
        selected_col_values=table_col_value[i].split('\',\'')
        controlled_col=data_access.checkIfColumnControlledVocab(str(column))
        if controlled_col:
            vocab_terms=data_access.getValidControlledVocabTerms(str(column))
        same_col_addition_statements=[]

        for col_value in selected_col_values:
            col_value=col_value.strip('\'')

            clipped_col_value=str(col_value.strip("'"))
            if controlled_col:
            
                #put the column values into a dictionary so we can run natural sort on the list
                for i in vocab_terms:
                    if i[1]==str(clipped_col_value):
                        clipped_col_value=str(i[0])
                        break
                   
            if clipped_col_value<>'####ALL####' and clipped_col_value.upper()<>'NONE':
                same_col_addition_statements.append('"'+tab+'"."'+column+'"=\''+clipped_col_value+'\'')
        if same_col_addition_statements<>[]:
            additional_where_statements.append('(%s)' % (' or '.join(same_col_addition_statements)))
    if additional_where_statements<>[]:
        statement += ' and (%s) ' % (' and '.join(additional_where_statements)) 

    #req.write(statement)
    # Run the statement

    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    print statement
    #req.write(str(statement)+'<br><br>')
    results = cur.execute(statement)


    # Write out proper header row, #SampleID, BarcodeSequence, LinkerPrimerSequence, Description, all others....
    tmp_mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix+'_map_tmp.txt'), 'w')
    map_filepath=os.path.join(mapping_file_dir, file_name_prefix+'_map.txt')
    map_filepath_db=os.path.join(mapping_file_dir_db, file_name_prefix+'_map.txt')

    # All mapping files start with an opening hash
    tmp_mapping_file.write('#')

    # determine if a column is a controlled vaocabulary columnn
    controlled_vocab_columns={}
    for i,column in enumerate(cur.description):
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
    for column in cur.description:
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
        tmp_mapping_file.write(to_write[0:len(to_write)-1] + '\n')

    tmp_mapping_file.close()

    open_tmp_mapping_file=open(os.path.join(mapping_file_dir, file_name_prefix+'_map_tmp.txt')).readlines()
    mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix+'_map.txt'), 'w')
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
    
    
    query=[]
    for i,sample_name1 in enumerate(samples_list):
        for j,sample_name2 in enumerate(samples_list[:i+1]):
            query.append('\t'.join([sample_name1,sample_name2,'999999999999',beta_metric,str(rarefied_at)]))
    
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    types = ['s','s', 'bf', 's', 'i']

    iterator=0
    listofall={}
    print query
    data_rows_lookup={}
    for i in samples_list:
        data_rows_lookup[i]={}
    for res in input_set_generator(query, cur, types,10000):
        
        print 'running %i' % (iterator)
        iterator=iterator+1
        valid = data_access.getBetaDivDistancesArray(True, res)
        if valid != []:
            for i,samp1 in enumerate(valid[0]):
                data_rows_lookup[samp1][valid[1][i]]=valid[2][i]
        

    '''
    data_rows_lookup={}
    for i in samples_list:
        data_rows_lookup[i]={}
    
    for i,sample_name1 in enumerate(samples_list):
        for j,sample_name2 in enumerate(samples_list[:i+1]):
            data_found=data_access.getBetaDivDistances(True,sample_name1,sample_name2,
                                                     beta_metric,rarefied_at)
            data_rows_lookup[sample_name1][sample_name2]=data_found
            
    '''
    distances=[]
    sample_labels=[]
    for i in samples_list:
        row_data=[]
        for j in samples_list:
            if (data_rows_lookup[i].has_key(j) and data_rows_lookup[i][j]!=None):
                row_data.append(data_rows_lookup[i][j])
                if i not in sample_labels:
                    sample_labels.append(i)
            elif (data_rows_lookup[j].has_key(i) and data_rows_lookup[j][i]!=None):
                row_data.append(data_rows_lookup[j][i])
                if i not in sample_labels:
                    sample_labels.append(i)
                    

        if row_data !=[]:
            distances.append(row_data)     

    #sample_labels.append(sample_name1)
    #distances.append(data_row)
    
    distance_matrix=format_matrix(distances,sample_labels,sample_labels)
    #print distance_matrix
    dist_fpath=os.path.join(pcoa_file_dir, file_name_prefix+'_%s.txt' % beta_metric)
    dist_fpath_db=os.path.join(pcoa_file_dir_db, file_name_prefix+'_%s.txt' % beta_metric)
    distance_mat_file = file(dist_fpath, 'w')
    distance_mat_file.write(distance_matrix)
    distance_mat_file.close()
    
    t2 = time()
    print 'Making distance mtx file: %s' % (t2 - t1)
    t1=time()
    prefs_fp_db,pc_fp_db,discrete_3d_dir_db,continuous_3d_dir_db,\
           prefs_fp,pc_fp,discrete_3d_dir,continuous_3d_dir=\
        run_principal_coords_through_3d_plots(dist_fpath,map_filepath,\
                        pcoa_file_dir,beta_metric,pcoa_file_dir_db)
    
    t2 = time()
    print 'pcoa plotting: %s' % (t2-t1)
    
    pc_filename=pc_fp_db.split('/')[-1]
    discrete_3d_fpath_db=os.path.join(discrete_3d_dir_db,pc_filename+'_3D.html')
    continuous_3d_fpath_db=os.path.join(continuous_3d_dir_db,pc_filename+'_3D.html')

    t1 = time()
    # zip up the OTU table and Mapping file for easy download
    zip_fpath=os.path.join(zip_file_dir, file_name_prefix + '_' + unique_name + '.zip')
    zip_fpath_db=os.path.join(zip_file_dir_db, file_name_prefix + '_' + unique_name+ '.zip')
    
    cmd_call='cd %s; zip %s %s' % (mapping_file_dir,zip_fpath,map_filepath.split('/')[-1])
    system(cmd_call)
    #cmd_call='zip -Xj  %s %s' % (zip_fpath,dist_fpath)
    #system(cmd_call)
    #cmd_call='zip -Xj  %s %s' % (zip_fpath,prefs_fp)
    #ystem(cmd_call)
    #cmd_call='zip -Xj  %s %s' % (zip_fpath,pc_fp)
    #system(cmd_call)
    #cmd_call='zip -r %s %s' % (zip_fpath,discrete_3d_dir)
    #system(cmd_call)
    cmd_call='cd %s; zip -r %s %s' % (pcoa_file_dir_loc,zip_fpath,pcoa_file_dir.split('/')[-1])
    system(cmd_call)
    
    t2 = time()
    print 'Zipping files: %s' % (t2 - t1)
    
    #add filepaths to DB, so we know where to find the generated files
    valid=data_access.addMappingPCoAFiles(True, meta_id, \
                                            map_filepath_db,dist_fpath_db,
                                            prefs_fp_db,
                                            pc_fp_db,
                                            discrete_3d_fpath_db,
                                            continuous_3d_fpath_db,
                                            zip_fpath_db)
    total2 = time()
    print 'total time: %s' % (total2-total1)
    
    
def run_principal_coords_through_3d_plots(dist_fpath,mapping_fp,output_dir,beta_diversity_metric,pcoa_file_dir_db):  
    """ Run the data preparation steps of Qiime 
    
        The steps performed by this function are:
         2) Peform a principal coordinates analysis on the result of
          Step 1;
         3) Generate a 3D prefs file for optimized coloring of continuous
          variables;
         4) Generate a 3D plot for all mapping fields with colors
          optimized for continuous data;
         5) Generate a 3D plot for all mapping fields with colors
          optimized for discrete data.
    
    """  
    # Prepare some variables for the later steps

    commands = []
    python_exe_fp = qiime_config['python_exe_fp']
    script_dir = get_qiime_scripts_dir()
    params=parse_qiime_parameters(open('/home/wwwuser/user_data/custom_parameters_uclust_ref_gg97.txt'))
    logger = WorkflowLogger(generate_log_fp(output_dir),
                            params=params,
                            qiime_config=qiime_config)
    
    mapping_file_header = parse_mapping_file(open(mapping_fp,'U'))[1]
    mapping_fields = ','.join(mapping_file_header)
    
    # Build the 3d prefs file generator command
    prefs_fp = get_tmp_filename(output_dir, suffix=".pref").strip()
    prefs_fp_db=os.path.join(pcoa_file_dir_db,os.path.split(prefs_fp)[-1])
    prefs_cmd = \
     '%s %s/make_prefs_file.py -m %s -o %s' %\
     (python_exe_fp, script_dir, mapping_fp, prefs_fp)
    commands.append([('Build prefs file', prefs_cmd)])
       
    # Prep the principal coordinates command
    
    pc_fp = '%s_pc.txt' % (os.path.splitext(dist_fpath)[0])
    pc_fp_db=os.path.join(pcoa_file_dir_db,os.path.split(pc_fp)[-1])
    
    try:
        params_str = get_params_str(params['principal_coordinates'])
    except KeyError:
        params_str = ''
    # Build the principal coordinates command
    pc_cmd = '%s %s/principal_coordinates.py -i %s -o %s' %\
     (python_exe_fp, script_dir, dist_fpath, pc_fp)
    commands.append(\
     [('Principal coordinates (%s)' % beta_diversity_metric, pc_cmd)])

    # Prep the continuous-coloring 3d plots command
    continuous_3d_dir = '%s/%s_3d_continuous/' %\
     (output_dir, beta_diversity_metric)
    continuous_3d_dir_db = '%s/%s_3d_continuous/' %\
     (pcoa_file_dir_db, beta_diversity_metric)
    try:
        makedirs(continuous_3d_dir)
    except OSError:
        pass
    try:
        params_str = get_params_str(params['make_3d_plots'])
    except KeyError:
        params_str = ''
    # Build the continuous-coloring 3d plots command
    continuous_3d_command = \
     '%s %s/make_3d_plots.py -p %s -i %s -o %s -m %s' %\
      (python_exe_fp, script_dir, prefs_fp, pc_fp, continuous_3d_dir,\
       mapping_fp)

    # Prep the discrete-coloring 3d plots command
    discrete_3d_dir = '%s/%s_3d_discrete/' %\
     (output_dir, beta_diversity_metric)
    discrete_3d_dir_db = '%s/%s_3d_discrete/' %\
     (pcoa_file_dir_db, beta_diversity_metric)
    '''
    try:
        makedirs(discrete_3d_dir)
    except OSError:
        pass
    try:
        params_str = get_params_str(params['make_3d_plots'])
    except KeyError:
        params_str = ''
    # Build the discrete-coloring 3d plots command
    discrete_3d_command = \
     '%s %s/make_3d_plots.py -b "%s" -i %s -o %s -m %s' %\
      (python_exe_fp, script_dir, mapping_fields, pc_fp, discrete_3d_dir,\
       mapping_fp)

    commands.append([\
      ('Make 3D plots (continuous coloring, %s)' %\
        beta_diversity_metric,continuous_3d_command),\
      ('Make 3D plots (discrete coloring, %s)' %\
        beta_diversity_metric,discrete_3d_command,)])
    '''
    commands.append([\
      ('Make 3D plots (continuous coloring, %s)' %\
        beta_diversity_metric,continuous_3d_command)])

    # Call the command handler on the list of commands
    web_app_call_commands_serially(commands, print_to_stdout, logger)

    return prefs_fp_db,pc_fp_db,discrete_3d_dir_db,continuous_3d_dir_db,\
           prefs_fp,pc_fp,discrete_3d_dir,continuous_3d_dir 

    
