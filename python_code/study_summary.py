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
        

def print_study_info_and_values_table(query_results, data_access):
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
        info_table.append("<table><th>Download Sequence Data:</th><td style=\"color:red;\">This dataset has not yet been collated. \
            Feel free to contact us for the status of this dataset. \
            (<a href='mailto:qiimeweb@gmail.com?subject=Status of QIIME-DB Study: %s'>email</a>)</td></table>" % (str(study_id)))

    
    return ''.join(info_table)
    
def get_sample_summary_html(study_id, data_access):
    """Returns an HTML table detailing per-sample information for a study

    input:
        study_id: the study_id of the study for which information should be
                  displayed
        data_access: instance of the data access class that can retrieve the
                     information to be displayed.

    output:
        out_string: an HTML-formatted table containing per-sample information
    """
    out_string = ''

    sample_details = data_access.getSampleDetailList(study_id)
    # Determine if we should write the seq and otu counts
    write_seq_otu_cols = True
    # This is the first sequence count field in the record. If None assume data
    # does not yet exist for samples in general
    if sample_details:
        if sample_details[0][5] == None:
            write_seq_otu_cols = False
    else:
        return ('Sample descriptions are not available; '
            'There is no metadata associated with this study yet.')

    # List all samples names here
    out_string += '<table width="100%">\n'
    if write_seq_otu_cols:
        # Figure out averages 
        total_seqs = sum(map(lambda x: x[5], sample_details))
        otu_pct_assign = sum(map(lambda x: x[6], sample_details))
        # 2 steps to average
        avg_otu_pct_assign = map(lambda x: x[7], sample_details)
        avg_otu_pct_assign = round(float(sum(avg_otu_pct_assign)) / float(len(avg_otu_pct_assign)), 1)

        out_string += '''<tr>
            <th colspan="4">Downloads</th>
            <th align="left">Total Sequence Count</th>
            <th align="left">Total Number of Seqs<br/> Assigned to an OTU</th>
            <th align="left">Avg % OTU Assignment</th>
            </tr>\n'''
        out_string += '''<tr>
            <td colspan="4">
            <a href="export_sample_grid.psp?study_id={0}" target="_blank">Sample Grid</a><br/>
            <a href="export_histograms.psp?study_id={0}" target="_blank">Histograms</a>
            </td>
            <td align="left">{1}</td>
            <td align="left">{2}</td>
            <td align="left">{3}%</td>
            </tr>\n'''.format(study_id, total_seqs, otu_pct_assign, avg_otu_pct_assign)
        out_string += '<tr><td colspan="7"/></tr>\n'

        out_string += '''<th align="left">Sample Name</th>
            <th align="left">Public</th>
            <th align="left">Collection Date</th>
            <th align="left">Run Prefix</th>
            <th align="left">Sequence Count</th>
            <th align="left">Number of Seqs Assigned<br/> to an OTU</th>
            <th align="left">% OTU Assignment</th>\n'''
    else:
        out_string += '''<th align="left">Sample Name</th><th align="left">Public</th><th align="left">Collection Date</th>
            <th align="left">Run Prefix</th>\n'''

    for sample_name, sample_id, public, collection_date, run_prefix,\
        sequence_count, otu_count, otu_percent_hit in sample_details:

        if otu_count == None:
            otu_count = 0
        if otu_percent_hit == None:
            otu_percent_hit = 0
        if write_seq_otu_cols:
            out_string += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s%%</td></tr>\n' % \
                (sample_name, public, collection_date, run_prefix, sequence_count, otu_count, round(otu_percent_hit, 1))
        else:
            out_string += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % \
                (sample_name, public, collection_date, run_prefix)

    out_string += '</table>\n'

    return out_string
