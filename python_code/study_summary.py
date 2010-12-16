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
        

def print_study_info_and_values_table(query_results):
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
    sffs=list(set(zip(*query_results)[5]))
    seq_run_ids=list(set(zip(*query_results)[6]))
    numreads=set(zip(*query_results)[7])
    
    
    samples={}
    read_counts=[]

    for i,sff in enumerate(sffs):
        
        results=data_access.getQiimeSffReadCounts(seq_run_ids[i])
        for row in results:
            read_counts.append(row[0])
            
        results=data_access.getQiimeSffSamples(study_id,seq_run_ids[i])
        samples[seq_run_ids[i]]=[]
        for row in results:
            samples[seq_run_ids[i]].append(row[0])
    
    sff_sample_count={}
    for i,sff in enumerate(sffs):
        sff_sample_count[sff]=[]
        for j in samples[seq_run_ids[i]]:
            results=0
            query_results=data_access.getQiimeSffSamplesCount(j)
            sff_sample_count[sff].append(list((j,query_results[1])))
    
    for i in project_names:
        info_table.append('<h3>'+str(i)+'</h3>')
    info_table.append('<table><tr><th><u>Study Information</u></th><td></tr>')
    for i in study_ids:
        info_table.append('<tr><th>Study ID:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
    for i in project_names:
        info_table.append('<tr><th>Project Name:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
    for i in study_titles:
        info_table.append('<tr><th>Study Title:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
    for i in study_abstracts:
        info_table.append('<tr><th>Study Abstract:</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                str(i)+'</td></tr>')
    for i in pmids:
        if i != None:
            info_table.append('<tr><th>Pubmed ID (pmid):</th><td '+ \
                'style="color:black;text-decoration:none">' + \
                '<a href=http://www.ncbi.nlm.nih.gov/pubmed?term='+\
                str(i)+'[uid] target="_blank">'+str(i)+'</a></td></tr>')
        else: 
            info_table.append('<tr><th>Pubmed ID (pmid):</th><td> '+ \
                'This paper does not currently have a pmid!</td></tr>')
    info_table.append('</table><br>')
    
    for i,sff in enumerate(sffs):
        info_table.append('<table><tr><th><u>SFF(s) Information</u></th><td></td></tr>')
        info_table.append('<tr><th>SFF Filename:</th><td>' + \
                str(sff)+'</td></tr>')
        info_table.append('<tr><th>Number of Reads:</th><td>' + \
                str(read_counts[i])+'</td></tr>')
        info_table.append('<tr><th>Number of Samples:</th><td>' + \
                str(len(samples[seq_run_ids[i]]))+'</td></tr>')
        info_table.append('<tr><th>Split-Library Sequences:</th><td>' + \
                str(sum(zip(*sff_sample_count[sff])[1]))+'</td></tr>')
        info_table.append('<tr><th><a id=\'sym_'+str(i) + \
                '\' onclick=\"show_hide_samples(\'div_'+str(i) + \
                '\',this.id);\" style=\"color:blue;\">&#x25BA;</a>&nbsp;Samples</th><td><td></tr>')
        info_table.append('</table>')
        info_table.append('<div id="div_'+str(i)+ \
                '" style="display:none;"><table border="1px" style="font-size:smaller;">')
        info_table.append('<tr"><th>SampleID</th><th>Sequences/Sample</th></tr>')

        sff_sample_count[sff].sort(key=lambda x:x[1],reverse=True)
        for j in sff_sample_count[sff]:
            info_table.append('<tr><td>'+str(j[0])+'</td><td>'+str(j[1])+'</td></tr>')
        
        info_table.append('</table></div><br>')

    info_table.append('<table><tr><th>Total Number of Reads:</th><td>' + \
                str(sum(read_counts))+'</td></tr></table>')
                
    return ''.join(info_table)
    
