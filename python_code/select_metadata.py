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
from enums import DataAccessType
data_access = data_access_factory(DataAccessType.qiime_production)
from enums import FieldGrouping

def public_cols_to_dict(public_columns):
    # create a dictionary containing all public column fields
    unique_public_columns={}
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
    
    return unique_public_columns

def get_unique_package_column_values(package_cols):
    #This function filters out hidden fields from the returned package columns
    columns=[]
    for i in range(len(package_cols)):
        if package_cols[i][1]<>'H':
            columns.append(package_cols[i][0].upper())
    
    return columns
        
def unique_cols_to_select_box_str(public_columns):
    unique_public_columns=public_cols_to_dict(public_columns)
    
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
    # write out the public column values as a select box
    for col in unique_public_columns:
        table_name,col_name=col.split('####SEP####')
        studies_to_use=str(unique_public_columns[col]).strip('[]').split(',')
        study_string=[]
        for i in studies_to_use:
            study_string.append(str(i.strip()))
            new_study_str='S'.join(study_string)
        
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
            info_table.append('<td rowspan=5>')

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
    info_table.append('<tr><td><em>Table Name:</em></td><td '+ \
                    'style="color:black;text-decoration:none">' + \
                    table+'</td></tr>')

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
        info_table.append('<tr><td><em>Description or Value:</em></td><td ' + \
                        'style="color:black;text-decoration:none">' + \
                        str(query_results[0][1])+'</td></tr>')
        info_table.append('<tr><td><em>Definition:</em></td><td ' + \
                        'style="color:black;text-decoration:none">' + \
                        str(query_results[0][2])+'</td></tr>')
    return ''.join(info_table)
    
def get_selected_column_values(controlled_col,col,table,user_id):
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
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.sample_id=h.sample_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join sff.analysis an on st.study_id=an.study_id where st.metadata_complete=\'y\'' % (str(col),str(table))
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
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.sample_id=h.sample_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (str(col),str(table),user_id)
            elif str(table)=='HOST':
                statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.host_id=h.host_id inner join "SAMPLE" s on h.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (str(col),str(table),user_id)
            else:
                statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id inner join study st on s.study_id=st.study_id inner join user_study us on st.study_id=us.study_id inner join sff.analysis an on st.study_id=an.study_id where (s."PUBLIC" = \'y\' or us.web_app_user_id=%s) and st.metadata_complete=\'y\'' % (col,table,user_id)
            
        # Run the statement
        con = data_access.getMetadataDatabaseConnection()
        cur = con.cursor()
        #req.write(str(statement)+'<br><br>')
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
        if form_key<>'fname_prefix' and form_key<>'taxonomy' and form_key<>'beta_metric' and form_key<>'rarefied_at':
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