#!/usr/bin/env python
# File created on 10 Sep 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME Web App"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.colors import natsort
from data_access_connections import data_access_factory
from enums import ServerConfig
data_access = data_access_factory(ServerConfig.data_access_type)
from enums import FieldGrouping
from numpy import zeros
from qiime.format import format_matrix,format_otu_table

def public_cols_to_dict(public_columns):
    # create a dictionary containing all public column fields
    unique_public_columns={}
    unique_studies=[]
    for i,j in enumerate(public_columns):
        if public_columns[i][1].strip('"').startswith('EXTRA_PREP') or public_columns[i][1].strip('"').startswith('EXTRA_SAMPLE'):
            continue
        else:
            col_key=public_columns[i][1].strip('"')+'####SEP####'+public_columns[i][0]
            if unique_public_columns.has_key(col_key):
                unique_public_columns[col_key].append(public_columns[i][2])
            else:
                unique_public_columns[col_key]=[]
                unique_public_columns[col_key].append(public_columns[i][2])

        if public_columns[i][2] not in unique_studies:
            unique_studies.append(str(public_columns[i][2]))
    
    return unique_public_columns,unique_studies

def get_unique_package_column_values(package_cols):
    #This function filters out hidden fields from the returned package columns
    columns=[]
    for i in range(len(package_cols)):
        if package_cols[i][1]<>'H':
            columns.append(package_cols[i][0].upper())
    
    return columns
        
def unique_cols_to_select_box_str(public_columns):
    unique_public_columns,unique_studies=public_cols_to_dict(public_columns)
    
    # get submission fields
    #sra_submission_field_list = map(lambda x:x.upper(),(zip(*data_access.getPackageColumns(FieldGrouping.sra_submission_level))[0]))
    # get study fields
    study_field_list = get_unique_package_column_values(data_access.getPackageColumns(FieldGrouping.study_level))
    # get SRA study fields
    sra_study_field_list = get_unique_package_column_values(data_access.getPackageColumns(FieldGrouping.sra_study_level))
    #vget the prep fields
    prep_field_list = get_unique_package_column_values(data_access.getPackageColumns(FieldGrouping.prep_level))
    # get the SRA sample fields
    sra_sample_field_list = get_unique_package_column_values(data_access.getPackageColumns(FieldGrouping.sra_sample_level))
    # get the required sample fields along with the package-specific fields
    sample_field_list = get_unique_package_column_values(data_access.getPackageColumns(FieldGrouping.sample_level))
    # get the SRA experiment fields
    sra_experiment_field_list = get_unique_package_column_values(data_access.getPackageColumns(FieldGrouping.sra_experiment_level))
    
    study_lists=study_field_list+sra_study_field_list
    sample_lists=sample_field_list+sra_sample_field_list
    prep_lists=prep_field_list+sra_experiment_field_list
    
    select_box=[]
    new_study_str='S'.join(unique_studies)
    
    # write out the public column values as a select box
    for col in unique_public_columns:
        table_name,col_name=col.split('####SEP####')
        studies_to_use=str(unique_public_columns[col]).strip('[]').split(',')
        study_string=[]
        
        # remove the Public fields
        if str(col_name) not in ['PUBLIC']:
            
            '''
            if col_name in sra_submission_field_list:
                select_box.append('<option id="'+'SRASuFL#ENDGRP#'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'"</option>\n")
            '''
            if table_name.startswith('EXTRA_'):
                select_box.append('<option id="'+'CUSTOM#ENDGRP#'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'">'+str(col_name)+"</option>\n")
            else:
                if col_name in study_lists:
                    select_box.append('<option id="'+'STUDY#ENDGRP#'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'">'+str(col_name)+"</option>\n")
                elif col_name in sample_lists:
                    select_box.append('<option id="'+'SAMPLE#ENDGRP#'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'">'+str(col_name)+"</option>\n")
                elif col_name in prep_lists:
                    select_box.append('<option id="'+'PREP#ENDGRP#'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'">'+str(col_name)+"</option>\n")
                else:
                    select_box.append('<option id="'+'ADD#ENDGRP#'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'">'+str(col_name)+"</option>\n")
    return '\n'.join(select_box)

def print_metadata_info_and_values_table(query_results,show_values,table,col,
                                         studies,col_values):
    
    info_table=[]
    # print the results from the above searches
    # print the column name
    info_table.append('<tr><td><em>Column Name:</em></td><td '+ \
                    'style="color:black;text-decoration:none">' + \
                    str(col)+'</td>')

    if show_values=="1":
        # print the height of the table, which is based on if no results are 
        # returned in regards to the column information
        if query_results==[]:
            info_table.append('<td rowspan=3>')
        else:
            info_table.append('<td rowspan=3>')

        # print the column values in a select box
        table_col_id=str(table) + '####SEP####' + col + '####STUDIES####' + studies
        info_table.append('<b>Select Values</b><br>')
        info_table.append('<select onchange="window.location.href=this.options[this.selectedIndex].value;reset_select(this);">')
        info_table.append('<option value="javascript:">')
        info_table.append('<option value="javascript:select_all_col_values(\'%s\');">All' % (table_col_id))
        info_table.append('<option value="javascript:select_none_col_values(\'%s\');">None' % (table_col_id))
        info_table.append('<option value="Javascript:select_invert_col_values(\'%s\');">Invert' % (table_col_id))
        info_table.append('</select>')
        info_table.append('<select style="width:300px;" id="%s" multiple onchange="saveSelection(this.id)">' % (table_col_id))
        for row in col_values:
            info_table.append('<option id="%s" value="%s" onmouseover="return overlib(\'%s\',WIDTH, 300);" onmouseout="return nd();">%s</option>' % (row,row,row,row))

        # close the select box
        info_table.append('</select>')
    info_table.append('</tr>')

    # print the table name
    #info_table.append('<tr><td><em>Table Name:</em></td><td '+ \
    #                'style="color:black;text-decoration:none">' + \
    #                table+'</td></tr>')

    # print the Data information
    if query_results==[]:
        info_table.append('<tr><td colspan=2 '+ \
                        'style="color:black;text-decoration:none">' + \
                        'This is a study-specific column defined by the user, ' +\
                        'field-specific information is not available.</td></tr>')
    else:
        info_table.append('<tr><td><em>Data Type:</em></td><td '+ \
                        'style="color:black;text-decoration:none">' + \
                        str(query_results[0][0])+'</td></tr>')
        #info_table.append('<tr><td><em>Description or Value:</em></td><td ' + \
        #                'style="color:black;text-decoration:none">' + \
        #                str(query_results[0][1])+'</td></tr>')
        info_table.append('<tr><td><em>Definition:</em></td><td ' + \
                        'style="color:black;text-decoration:none">' + \
                        str(query_results[0][2])+'</td></tr>')
    return ''.join(info_table)
    
def get_selected_column_values(controlled_col,col,table,user_id,studies):
    # if the column is not controlled, then we must look in the database
    # for the public values provided in that column
    studies_to_retrieve=studies.split('S')
    
    study_sql_array=[]
    for i in studies_to_retrieve:
        study_sql_array.append("st.study_id=%s" % (str(i)))
    study_sql_cmd=' or '.join(study_sql_array)
    
    if not controlled_col:
        
        # Get the user details
        user_details = data_access.getUserDetails(user_id)
        if not user_details:
            raise ValueError('No details found for this user')
        is_admin = user_details['is_admin']

        # Handle the different table names, since the inner joins depend on which
        # table is being traversed
        if is_admin:
            if str(table)=='STUDY':
                statement='select distinct st."%s" from "%s" st where (%s) and st.metadata_complete=\'y\'' % (col,table,study_sql_cmd)
            elif str(table)=='SAMPLE':
                statement='select distinct t."%s" from "%s" t inner join study st on t.study_id=st.study_id where (%s) and st.metadata_complete=\'y\'' % (col,table,study_sql_cmd)
            elif str(table)=='SEQUENCE_PREP':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id where (%s) and st.metadata_complete=\'y\'' % (col,table,study_sql_cmd)
            elif str(table)=='HOST_ASSOC_VERTIBRATE' or table=='HOST_ASSOC_PLANT' or table=='HOST_SAMPLE' or table=='HUMAN_ASSOCIATED':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id where (%s) and st.metadata_complete=\'y\'' % (str(col),str(table),study_sql_cmd)
            elif str(table)=='HOST':
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.host_id=h.host_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id where (%s) and st.metadata_complete=\'y\'' % (str(col),str(table),study_sql_cmd)
            else:
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id where (%s) and st.metadata_complete=\'y\'' % (col,table,study_sql_cmd)
        else:
            if str(table)=='STUDY':
                statement='select distinct st."%s" from "%s" st inner join user_study us on st.study_id=us.study_id where (st."STUDY_PUBLIC" = \'y\' or us.web_app_user_id=%s) and (%s) and st.metadata_complete=\'y\'' % (col,table,user_id,study_sql_cmd)
            elif str(table)=='SAMPLE':
                statement='select distinct t."%s" from "%s" t inner join study st on t.study_id=st.study_id inner join user_study us on st.study_id=us.study_id where (t."PUBLIC" = \'y\' or us.web_app_user_id=%s) and (%s) and st.metadata_complete=\'y\'' % (col,table,user_id,study_sql_cmd)
            elif str(table)=='SEQUENCE_PREP':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and (%s) and st.metadata_complete=\'y\'' % (col,table,user_id,study_sql_cmd)
            elif str(table)=='HOST_ASSOC_VERTIBRATE' or table=='HOST_ASSOC_PLANT' or table=='HOST_SAMPLE' or table=='HUMAN_ASSOCIATED':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and (%s) and st.metadata_complete=\'y\'' % (str(col),str(table),user_id,study_sql_cmd)
            elif str(table)=='HOST':
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.host_id=h.host_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and (%s) and st.metadata_complete=\'y\'' % (str(col),str(table),user_id,study_sql_cmd)
            else:
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and (%s) and st.metadata_complete=\'y\'' % (col,table,user_id,study_sql_cmd)
            
        # Run the statement
        con = data_access.getMetadataDatabaseConnection()
        cur = con.cursor()
        #req.write(str(statement)+'<br><br>')
        results = cur.execute(statement)
        #raise ValueError, statement
        #put the column values into a dictionary so we can run natural sort on the list
        col_values={}
        for i in results:
            if i[0] <> None:
                col_values[str(i[0])]=str(i[0])

    else:
        # get the controlled terms
        results=data_access.getValidControlledVocabTerms(col)
        #put the column values into a dictionary so we can run natural sort on the list
        col_values={}
        for i in results:
            if i[0] <> None:
                col_values[str(i[1])]=str(i[1])

    # sort the column values
    col_values=natsort(col_values)
    
    return col_values
    
#
def get_selected_column_values_old(controlled_col,col,table,user_id):
    # if the column is not controlled, then we must look in the database
    # for the public values provided in that column
    if not controlled_col:
        
        # Get the user details
        user_details = data_access.getUserDetails(user_id)
        if not user_details:
            raise ValueError('No details found for this user')
        is_admin = user_details['is_admin']

        # Handle the different table names, since the inner joins depend on which
        # table is being traversed
        if is_admin:
            if str(table)=='STUDY':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.study_id=s.study_id inner join study st on s.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (col,table)
            elif str(table)=='SAMPLE':
                statement='select distinct t."%s" from "%s" t inner join study st on t.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (col,table)
            elif str(table)=='SEQUENCE_PREP':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (col,table)
            elif str(table)=='HOST_ASSOC_VERTIBRATE' or table=='HOST_ASSOC_PLANT' or table=='HOST_SAMPLE' or table=='HUMAN_ASSOCIATED':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (str(col),str(table))
            elif str(table)=='HOST':
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.host_id=h.host_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (str(col),str(table))
            else:
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (col,table)
        else:
            if str(table)=='STUDY':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.study_id=s.study_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (col,table,user_id)
            elif str(table)=='SAMPLE':
                statement='select distinct t."%s" from "%s" t inner join study st on t.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (t."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (col,table,user_id)
            elif str(table)=='SEQUENCE_PREP':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (col,table,user_id)
            elif str(table)=='HOST_ASSOC_VERTIBRATE' or table=='HOST_ASSOC_PLANT' or table=='HOST_SAMPLE' or table=='HUMAN_ASSOCIATED':
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (str(col),str(table),user_id)
            elif str(table)=='HOST':
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.host_id=h.host_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (str(col),str(table),user_id)
            else:
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (col,table,user_id)
            
        # Run the statement
        con = data_access.getMetadataDatabaseConnection()
        cur = con.cursor()
        #req.write(str(statement)+'<br><br>')
        results = cur.execute(statement)
        #raise ValueError, statement
        #put the column values into a dictionary so we can run natural sort on the list
        col_values={}
        for i in results:
            if i[0] <> None:
                col_values[str(i[0])]=str(i[0])

    else:
        # get the controlled terms
        results=data_access.getValidControlledVocabTerms(col)
        #put the column values into a dictionary so we can run natural sort on the list
        col_values={}
        for i in results:
            if i[0] <> None:
                col_values[str(i[1])]=str(i[1])

    # sort the column values
    col_values=natsort(col_values)
    
    return col_values

def get_table_col_values_from_form(form):
    ''' get the form values from select_metadata/index.psp '''
    table_col_value={}
    unique_cols=[]
    for form_key in form:
        split_form_key=form_key.split('####STUDIES####')
        if len(split_form_key)>1:
            if type(form[form_key])==type([]):
                for vals in form[form_key]:
                    if table_col_value.has_key(form_key):
                        if vals<>'####ALL####':
                            unique_cols.append(form_key)
                            table_col_value[form_key]=str(vals)
                    else:
                        table_col_value[form_key]=str(vals)
            else:
                table_col_value[form_key]=str(form[form_key])
    return table_col_value
    

def get_otu_table(data_access, table_col_value,user_id,meta_id,tax_name):
    ''' This function is similar to what is written in the 
        generate_mapping_and_otu_table.py script, however; it does not need 
        all the extra columns and does not need to write files
    '''
    
    unique_cols=[]
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
    
        # Required fields which much show up first. Skip as they are already
        # in the statement
        if column in ['SAMPLE_NAME', 'BARCODE', 'LINKER', 'PRIMER', 
                      'EXPERIMENT_TITLE','DESCRIPTION','RUN_PREFIX']:
            continue

        # Add the table to our list if not already there and not one of the
        # required tables
        if '"'+tab+'"' not in tables and '"'+tab+'"' not in ['"STUDY"',
                                                '"SAMPLE"', '"SEQUENCE_PREP"']:
            tables.append('"'+tab+'"')

        # Finally, add to our column list
        database_map[column] = '"'+tab+'"'

        # End for

    unique_study_ids=list(set(study_id_array))
    
    statement += '"SEQUENCE_PREP".experiment_title as Description \n'
    
    if is_admin:
        statement = '\
        select distinct \n' + statement + ' \n\
        from "STUDY" '
    else:
        statement = '\
        select distinct \n' + statement + ' \n\
        from "STUDY" inner join user_study us on "STUDY".study_id=us.study_id'

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

    # Deal with the rest of the tables. They should all be assocaiated by
    # sample id.
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
        statement += ' where (%s) and ("SAMPLE"."PUBLIC"=\'y\' or us.web_app_user_id=%s)' % \
                                        (' or '.join(study_statement),user_id)

    # add where statements based on selected metadata
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
            
                #put the column values into a dictionary so we can run natural
                # sort on the list
                for i in vocab_terms:
                    if i[1]==str(clipped_col_value):
                        clipped_col_value=str(i[0])
                        break
               
            if clipped_col_value<>'####ALL####' and \
                                            clipped_col_value.upper()<>'NONE':
                same_col_addition_statements.append(\
                            '"'+tab+'"."'+column+'"=\''+clipped_col_value+'\'')
        if same_col_addition_statements<>[]:
            additional_where_statements.append('(%s)' % \
                                    (' or '.join(same_col_addition_statements)))
    if additional_where_statements<>[]:
        statement += ' and (%s) ' % (' and '.join(additional_where_statements)) 

    # connect to metadata database
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()

    # get results
    results = cur.execute(statement)
    
    # get a list of sample_names for getting OTU table
    samples_list=[]
    for row in results:
        if str(row[0]) not in samples_list: 
            samples_list.append(str(row[0]))
       
    # iterate over samples and get otu counts
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    query=[]
    sample_counts={}
    otus=[]
    for i,sample_name1 in enumerate(samples_list):
        sample_counts[sample_name1]={}
        user_data=data_access.getOTUTable(True,sample_name1,'UCLUST_REF',97,
                                          'GREENGENES_REFERENCE',97)
        for row in user_data:
            if row[0] not in otus:
                otus.append(str(row[0]))
            if sample_counts[sample_name1].has_key(str(row[0])):
                raise ValueError, 'Duplicate prokmsa ids!' 
            sample_counts[sample_name1][str(row[0])]=row[1]

    otu_table=zeros((len(otus),len(samples_list)),dtype=int)
    
    # generate otu table
    for i,sample in enumerate(samples_list):
        for j, otu in enumerate(otus):
            if sample_counts.has_key(sample):
                if sample_counts[sample].has_key(otu):
                    otu_table[j][i]=sample_counts[sample][otu]
             
    # format otu table and return
    otu_lines=format_otu_table(samples_list,otus,otu_table)

    return otu_lines