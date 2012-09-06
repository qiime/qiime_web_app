#!/usr/bin/env python
# File created on 10 Sep 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME-DB Project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.colors import natsort
from enums import ServerConfig
from enums import FieldGrouping
from numpy import zeros
from qiime.format import format_matrix,format_otu_table

def public_cols_to_dict(public_columns):
    """ create a dictionary containing all public column fields """
    
    unique_public_columns={}
    unique_studies=[]
    for i,j in enumerate(public_columns):
        # pull out any extra_ table listings
        if public_columns[i][1].strip('"').startswith('EXTRA_PREP') or \
                    public_columns[i][1].strip('"').startswith('EXTRA_SAMPLE'):
            continue
        else:
            # split on separator and append to dictionary
            col_key=public_columns[i][1].strip('"') + '####SEP####' + \
                                                            public_columns[i][0]
            if unique_public_columns.has_key(col_key):
                unique_public_columns[col_key].append(public_columns[i][2])
            else:
                unique_public_columns[col_key]=[]
                unique_public_columns[col_key].append(public_columns[i][2])

        if str(public_columns[i][2]) not in unique_studies:
            unique_studies.append(str(public_columns[i][2]))
    
    return unique_public_columns,unique_studies

def get_unique_package_column_values(package_cols):
    """ This function filters out hidden fields from the returned package 
columns"""

    columns=[]
    for i in range(len(package_cols)):
        if package_cols[i][1]<>'H':
            columns.append(package_cols[i][0].upper())
    
    return columns
        
def unique_cols_to_select_box_str(public_columns,data_access):
    unique_public_columns,unique_studies=public_cols_to_dict(public_columns)
    """Convert unique columns into a select-box string"""
    
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
    
    study_lists=study_field_list + sra_study_field_list
    sample_lists=sample_field_list + sra_sample_field_list
    prep_lists=prep_field_list + sra_experiment_field_list
    
    select_box=[]
    new_study_str='S'.join(unique_studies)
    
    javascript_str='available_cols=new Array();\n'
    # write out the public column values as a select box
    for col in unique_public_columns:
        table_name,col_name=col.split('####SEP####')
        studies_to_use=str(unique_public_columns[col]).strip('[]').split(',')
        study_string=[]
        # remove the Public fields
        if str(col_name) not in ['PUBLIC']:
            # build a javascript array
            javascript_str+='available_cols["'+str(col)+'"]=new Array();\n'
            
            # append values to the javascript array
            if len(unique_public_columns[col])==len(unique_studies):
                if table_name.startswith('EXTRA_'):
                    javascript_str+='available_cols["'+str(col)+'"]=["common_study","CUSTOM#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                else:
                    if col_name in study_lists:
                        javascript_str+='available_cols["'+str(col)+'"]=["common_study","STUDY#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                    elif col_name in sample_lists:
                        javascript_str+='available_cols["'+str(col)+'"]=["common_study","SAMPLE#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                    elif col_name in prep_lists:
                        javascript_str+='available_cols["'+str(col)+'"]=["common_study","PREP#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                    else:
                        javascript_str+='available_cols["'+str(col)+'"]=["common_study","ADD#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
            else:
                if table_name.startswith('EXTRA_'):
                    javascript_str+='available_cols["'+str(col)+'"]=["unique_study","CUSTOM#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                else:
                    if col_name in study_lists:
                        javascript_str+='available_cols["'+str(col)+'"]=["unique_study","STUDY#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                    elif col_name in sample_lists:
                        javascript_str+='available_cols["'+str(col)+'"]=["unique_study","SAMPLE#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                    elif col_name in prep_lists:
                        javascript_str+='available_cols["'+str(col)+'"]=["unique_study","PREP#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'
                    else:
                        javascript_str+='available_cols["'+str(col)+'"]=["unique_study","ADD#ENDGRP#'+str(col)+'","'+str(col)+'####STUDIES####'+new_study_str+'","'+str(col_name)+'"]\n'

    return javascript_str #'\n'.join(select_box)

def print_metadata_info_and_values_table(query_results,show_values,table,col,
                                         studies,col_values):
    """ print information pertaining to selected metadata """

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
        info_table.append('<select onchange="window.location.href=this.options[this.selectedIndex].value;reset_select(this);saveSelection(\'%s\')">' % (table_col_id))
        info_table.append('<option value="javascript:">')
        info_table.append('<option value="javascript:select_all_col_values(\'%s\');">All' % (table_col_id))
        info_table.append('<option value="javascript:select_none_col_values(\'%s\');">None' % (table_col_id))
        info_table.append('<option value="Javascript:select_invert_col_values(\'%s\');">Invert' % (table_col_id))
        info_table.append('</select>')
        info_table.append('<select style="width:300px;" id="%s" multiple onchange="saveSelection(this.id)">' % (table_col_id))
        for row in col_values:
            info_table.append('<option id="%s" value="%s" onmouseover="return overlib(\'%s\',WIDTH, 300);" onmouseout="return nd();">%s</option>' % (row,row,row,row))

        # close the select box
        info_table.append('</select></td>')
    info_table.append('</tr>')

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
        info_table.append('<tr><td><em>Definition:</em></td><td ' + \
                        'style="color:black;text-decoration:none">' + \
                        str(query_results[0][2])+'</td></tr>')
                        
    return ''.join(info_table)
    
def get_selected_column_values(controlled_col, col, table, user_id, studies,
                               data_access):
    """ if the column is not controlled, then we must look in the database 
for the public values provided in that column"""

    # get a list of study ids
    studies_to_retrieve=studies.split('S')
    study_sql_array=[]
    for i in studies_to_retrieve:
        study_sql_array.append("st.study_id=%s" % (str(i)))
    study_sql_cmd=' or '.join(study_sql_array)
    
    # determine if a controlled-vocab field
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
        results = cur.execute(statement)

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
        results = cur.execute(statement)

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
    