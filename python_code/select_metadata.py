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
from qiime_data_access import *
data_access = QiimeDataAccess()

def public_cols_to_dict(public_columns):
    # create a dictionary containing all public column fields
    unique_public_columns={}
    for i,j in enumerate(public_columns):
        col_key=public_columns[i][1].strip('"')+'####SEP####'+public_columns[i][0]
        if unique_public_columns.has_key(col_key):
            unique_public_columns[col_key].append(public_columns[i][2])
        else:
            unique_public_columns[col_key]=[]
            unique_public_columns[col_key].append(public_columns[i][2])
    
    return unique_public_columns
    
def unique_cols_to_select_box_str(public_columns):
    unique_public_columns=public_cols_to_dict(public_columns)
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
            select_box.append('<option id="'+str(col)+'" value="'+str(col)+'####STUDIES####'+new_study_str+'" onclick="showResult(\'metadata_left_col\',this.id,this.value)">'+str(col_name)+"</option>\n")
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
        info_table.append('<select id="%s" multiple style="width:300px;" onchange="saveSelection(this.id)">' % (table_col_id))

        for row in col_values:
            info_table.append('<option id="%s" value="%s">%s</option>' % (row,row,row))

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
    
def get_selected_column_values(controlled_col,col,table):
    # if the column is not controlled, then we must look in the database
    # for the public values provided in that column
    if not controlled_col:

        # Handle the different table names, since the inner joins depend on which
        # table is being traversed
        if str(table)=='STUDY':
            statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.study_id=s.study_id where s."PUBLIC"=\'y\'' % (col,table)
        elif str(table)=='SAMPLE':
            statement='select distinct t."%s" from "%s" t where t."PUBLIC"=\'y\'' % (col,table)
        elif str(table)=='SEQUENCE_PREP':
            statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id where s."PUBLIC"=\'y\'' % (col,table)
        elif str(table)=='HOST_ASSOC_VERTIBRATE' or table=='HOST_ASSOC_PLANT' or table=='HOST':
            statement='select distinct t."%s" from "%s" t inner join "HOST_SAMPLE" h on t.host_id=h.host_id inner join "SAMPLE" s on h.sample_id=s.sample_id where s."PUBLIC"=\'y\'' % (str(col),str(table))
        else:
            statement='select distinct t."%s" from "%s" t inner join "SAMPLE" s on t.sample_id=s.sample_id where s."PUBLIC"=\'y\'' % (col,table)

        # Run the statement
        con = data_access.getDatabaseConnection()
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
    