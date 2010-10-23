__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Jesse Stombaugh","Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

from data_access_connections import data_access_factory
from enums import DataAccessType
from os import system,path
import os
from qiime.merge_mapping_files import merge_mapping_files, write_mapping_file
from qiime.make_otu_table import make_otu_table
from load_tab_file import input_set_generator
from select_metadata import get_table_col_values_from_form

def write_mapping_and_otu_table(data_access,table_col_value,fs_fp,web_fp,taxonomy_class, file_name_prefix,user_id):
    unique_cols=[]
    # Create the mapping file based on sample and field selections

    # get the directory location for the files to write
    otu_table_file_dir=path.join(fs_fp,'otu_table_files')
    mapping_file_dir=path.join(fs_fp,'mapping_files')
    zip_file_dir=path.join(fs_fp,'zip_files')

    otu_table_file_dir_db=path.join(web_fp,'otu_table_files')
    mapping_file_dir_db=path.join(web_fp,'mapping_files')
    zip_file_dir_db=path.join(web_fp,'zip_files')

    map_files=[]
    
    #recorded_fields = data_access.getMetadataFields(study_id)
    database_map = {}
    tables = []

    # Start building the statement for writing out the mapping file
    # THIS ORDER MUST REMAIN THE SAME SINCE CHANGES WILL AFFECT LATER FUNCTION
    statement = '"SAMPLE".sample_name||\'.\'||"SEQUENCE_PREP".run_prefix as SampleID, \n'
    statement += '"SEQUENCE_PREP".barcode, \n'
    statement += 'concat("SEQUENCE_PREP".linker, "SEQUENCE_PREP".primer) as LinkerPrimerSequence, \n'
    statement += '"SAMPLE".study_id, \n'
    statement += '"SEQUENCE_PREP".run_prefix as RUN_PREFIX, \n'
    statement += '"SEQUENCE_PREP".experiment_title as Description, \n'

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
        if column in ['SAMPLE_NAME', 'BARCODE', 'LINKER', 'PRIMER', 'EXPERIMENT_TITLE']:
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

    statement = statement[0:len(statement) - 3]

    if user_id==12171:
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
    statement += '\
    left join "HOST_SAMPLE" \n\
    on "SAMPLE".sample_id = "HOST_SAMPLE".sample_id\n'

    # Deal with the rest of the tables. They should all be assocaiated by sample id.
    for table in tables:
        if 'HOST' in table or 'HUMAN' in table:
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

    if user_id==12171:
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
            additional_where_statements.append('%s' % (' or '.join(same_col_addition_statements)))
    if additional_where_statements<>[]:
        statement += ' and (%s) ' % (' and '.join(additional_where_statements)) 

    #req.write(statement)
    # Run the statement

    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()

    #req.write(str(statement)+'<br><br>')
    results = cur.execute(statement)


    # Write out proper header row, #SampleID, BarcodeSequence, LinkerPrimerSequence, Description, all others....
    mapping_file = file(os.path.join(mapping_file_dir, file_name_prefix+'_map.txt'), 'w')

    map_filepath=os.path.join(mapping_file_dir, file_name_prefix+'_map.txt')
    map_filepath_db=os.path.join(mapping_file_dir_db, file_name_prefix+'_map.txt')

    #req.write('http://localhost:5001/'+map_filepath)
    # All mapping files start with an opening hash
    mapping_file.write('#')

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

    # Write the header row
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

    mapping_file.write(to_write[0:len(to_write)-1] + '\n')

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
        mapping_file.write(to_write[0:len(to_write)-1] + '\n')

    mapping_file.close()

    # create a dictionary for getting run_prefix from run_id
    otu_map_dict={}
    sid_run_prefix_to_seq_run_id={}
    for study_id,run_prefix_value in study_id_and_run_prefix:
        seq_run_id_out=data_access.getSeqRunIdFromRunPrefix(run_prefix_value,study_id)
        sid_run_prefix_to_seq_run_id[study_id+'_'+run_prefix_value]=seq_run_id_out
    it=0
    # iterate through the list of samples and get the OTU map for each sample
    for otu_sample_name,otu_run_prefix,otu_study_id in sample_to_run_prefix:
        #req.write('<html><p>%i</p></html>'%it)
        it+=1
        otus=data_access.getOTUMap(otu_sample_name,
                    int(sid_run_prefix_to_seq_run_id[otu_study_id+'_'+otu_run_prefix]),
                    97,'UCLUST_REF','GREENGENES_REFERENCE',97)

        # based on the returned OTU Map, append sample those to an OTU dictionary
        for o in otus:
            tmp_sample_name=otu_sample_name
            if tmp_sample_name+'_'+otu_run_prefix in duplicate_samples:
                tmp_sample_name=o[1].split('_')
                tmp_sample_name[0]+='_%s' % (otu_run_prefix)
                new_otu_sample_name='_'.join(tmp_sample_name)
            else:
                new_otu_sample_name=o[1]
            
            if otu_map_dict.has_key(str(o[0])):
                otu_map_dict[str(o[0])].append(new_otu_sample_name)
            else:
                otu_map_dict[str(o[0])]=[]
                otu_map_dict[str(o[0])].append(new_otu_sample_name)
    otu_id_list=list(set(otu_map_dict.keys()))


    if taxonomy_class:
        otu_to_taxonomy={}
        for i in otu_id_list:
            otu_taxonomy=data_access.getOTUGG97Taxonomy(str(i),taxonomy_class)
            if otu_taxonomy==None:
                otu_taxonomy='NA;'
            otu_to_taxonomy[i]=otu_taxonomy
    
    else:
        otu_to_taxonomy=None
  

    # Write the OTU table
    otu_table_fpath=os.path.join(otu_table_file_dir, file_name_prefix + 
                                    '_otu_table.txt')     
    otu_table_fpath_db=os.path.join(otu_table_file_dir_db, file_name_prefix + 
                                    '_otu_table.txt')

    outfile = open(otu_table_fpath, 'w')

    outfile.write(make_otu_table(otu_map_dict, otu_to_taxonomy))
    outfile.close()


    # zip up the OTU table and Mapping file for easy download
    zip_fpath=os.path.join(zip_file_dir, file_name_prefix + '.zip')
    zip_fpath_db=os.path.join(zip_file_dir_db, file_name_prefix + '.zip')
    cmd_call='zip -jX %s %s' % (zip_fpath,map_filepath)
    system(cmd_call)
    cmd_call='zip -jX %s %s' % (zip_fpath,otu_table_fpath)
    system(cmd_call)

    #add filepaths to DB, so we know where to find the generated files
    valid=data_access.addMetaAnalysisMapOTUFiles(True, sess['meta_analysis_id'], \
                                            map_filepath_db,otu_table_fpath_db,
                                            zip_fpath_db)



