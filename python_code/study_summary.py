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
#from data_access_connections import data_access_factory
#from enums import ServerConfig
#data_access = data_access_factory(ServerConfig.data_access_type)
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
    sffs=list(set(zip(*query_results)[5]))
    seq_run_ids=list(set(zip(*query_results)[6]))
    numreads=set(zip(*query_results)[7])
    
    
    samples={}
    read_counts=[]

    if sffs[0]:
        # iterate over the sffs in this study
        for i,sff in enumerate(sffs):
            
            # deprecation due to no longer loading into reads table
            '''
            #Get the number of reads in a given sff
            results=data_access.getQiimeSffReadCounts(seq_run_ids[i])
            for row in results:
                read_counts.append(row[0])
            '''
            #Get a list of samples for a given sff
            results=data_access.getQiimeSffSamples(study_id,seq_run_ids[i])
            samples[seq_run_ids[i]]=[]
            for row in results:
                samples[seq_run_ids[i]].append(row[0])
    
        #get a list of sample counts for a given sff
        sff_sample_count={}
        for i,sff in enumerate(sffs):
            sff_sample_count[sff]=[]
            for j in samples[seq_run_ids[i]]:
                results=0
                query_results=data_access.getQiimeSffSamplesCount(j)
                sff_sample_count[sff].append(list((j,query_results[1])))
    
    # start writing the data into an HTML table. The reason for the looping,is 
    # that we want to make sure each SFF and Sample has the same information
    
    #Write out the project names selected
    for i in project_names:
        info_table.append('<h3>'+str(i)+\
                          ' (<a href=\'./study_summary/export_metadata.psp\' '+\
                          ' target="_blank">'+\
                          'download metadata</a>)&nbsp;')
        #
        if sffs[0]:
            info_table.append('(<a href=\'./study_summary/export_sffs.psp\' '+\
                              ' target="_blank">'+\
                              'download sffs</a>)</h3>')
        else:
            info_table.append('</h3>')
    #
    
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
    
    if sffs[0]:
        #Write SFF information
        #Write out each SFF and it's associated sample information
        for i,sff in enumerate(sffs):
            info_table.append('<table><tr><th><u>SFF(s) Information</u></th>')
        
            #write out SFF name
            info_table.append('<td></td></tr><tr><th>SFF Filename:</th><td>' + \
                    str(sff)+'</td></tr>')
        
            # deprecating due to no longer loading into reads table
            '''
            #write out number of reads
            info_table.append('<tr><th>Number of Reads:</th><td>' + \
                    str(read_counts[i])+'</td></tr>')
            '''
            #write out number of samples
            info_table.append('<tr><th>Number of Samples:</th><td>' + \
                    str(len(samples[seq_run_ids[i]]))+'</td></tr>')
        
            #write out total number of split-lib seqs
            info_table.append('<tr><th>Split-Library Sequences:</th><td>' + \
                    str(sum(zip(*sff_sample_count[sff])[1]))+'</td></tr>')
        
            #write out Samples
            info_table.append('<tr><th><a id=\'sym_'+str(i) + \
                    '\' onclick=\"show_hide_samples(\'div_'+str(i) + \
                    '\',this.id);\" style=\"color:blue;\">&#x25BA;</a>&nbsp;Samples</th><td></td></tr>')
            info_table.append('</table>')
            info_table.append('<div id="div_'+str(i)+ \
                    '" style="display:none;"><table border="1px" style="font-size:smaller;">')
            info_table.append('<tr><th>SampleID</th><th>Sequences/Sample</th></tr>')
            sff_sample_count[sff].sort(key=lambda x:x[1],reverse=True)
            for j in sff_sample_count[sff]:
                info_table.append('<tr><td>'+str(j[0])+'</td><td>'+str(j[1])+'</td></tr>')
        
            info_table.append('</table></div><br>')
            
        # deprecating due to no longer loading into reads table
        '''
        # write out total number of reads across all sffs
        info_table.append('<table><tr><th>Total Number of Reads:</th><td>' + \
                    str(sum(read_counts))+'</td></tr></table>')
        '''
    else:
        info_table.append('<table><tr><th><u>SFF(s) Information</u></th></tr><tr><td style=\"color:red;\">The sequence data for this study has not been processed!</td></tr></table>')
                
    return ''.join(info_table)
    
