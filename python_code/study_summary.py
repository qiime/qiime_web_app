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
from enums import FieldGrouping
        

def print_study_info_and_values_table(query_results,data_access):
    ''' This function write the Study summary information below the select-box'''

    info_table=[]
    
    # pull out the study_id for the selected study
    study_ids=set(zip(*query_results)[0])
    for i in study_ids:
        study_id=str(i)
    
    #pull the different fields for a given study
    project_names=set(zip(*query_results)[1])
    study_titles=set(zip(*query_results)[2])
    study_abstracts=set(zip(*query_results)[3])
    pmids=set(zip(*query_results)[4])
    
    #write out study information
    info_table.append('<table><tr><th><u>Study Information</u></th><td></tr>')
    #Write out the study_ids for each sff
    for i in study_ids:
        info_table.append('<tr><th>Study ID:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
                
    #Write out the project_names for each sff
    for i in project_names:
        info_table.append('<tr><th>Project Name:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
                
    #Write out the study_titles for each sff
    for i in study_titles:
        info_table.append('<tr><th>Study Title:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
                
    #Write out the study_abstracts for each sff
    for i in study_abstracts:
        info_table.append('<tr><th>Study Abstract:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
                
    #write out the pubmed_ids for each sff and create a link to pubmed
    for i in pmids:
        if i != None:
            info_table.append('<tr><th>Pubmed ID (pmid):</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                '<a href=http://www.ncbi.nlm.nih.gov/pubmed?term='+\
                str(i)+'[uid] target="_blank">'+str(i)+'</a></td></tr>')
        else: 
            info_table.append('<tr><th>Pubmed ID (pmid):</th><td>'+\
                '<em style="color:red;"> '+ \
                'This paper does not currently have a pmid!</em></td></tr>')
    info_table.append('</table><br>')
    
    ### get a QIIME DB connection
    try:
        from data_access_connections import data_access_factory
        from enums import ServerConfig,DataAccessType
        import cx_Oracle
        data_access = data_access_factory(ServerConfig.data_access_type)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
    
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    
    # create the select command
    for i in study_ids:
        statement="select file_path from study_files where study_id=%s and file_type=\'SPLIT_LIB_SEQS_MAPPING\'" % (str(i))
        study_id=str(i)
    
    # provide a link to the split-library data
    file_path=cur.execute(statement)
    oracle_cursor_len=0
    for path in file_path:
        oracle_cursor_len=oracle_cursor_len+1
        if path:
            info_table.append('<table><th>Download Sequence Data:</th><td><a href=%s>Sequences, Mapping and OTU Table</a></td></table>' % (path))
    
    # if no link, then allow user to email about getting data
    if oracle_cursor_len==0:
        info_table.append("<table><th>Download Sequence Data:</th><td style=\"color:red;\">Please send an email to Jesse Stombaugh to get the data (<a href='mailto:jesse.stombaugh@colorado.edu?subject=Get QIIME-DB Study: %s from thebeast'>email</a>)</table></table>" % (str(study_id)))

    
    return ''.join(info_table)
    
