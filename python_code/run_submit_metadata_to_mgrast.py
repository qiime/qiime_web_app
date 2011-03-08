#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

import httplib, urllib
from data_access_connections import data_access_factory
from enums import DataAccessType
from sample_export import export_fasta_from_sample

def submit_metadata_for_study(key, study_id):
    """This function takes the input options from the user and generates a url
    and request header for submitting to the MG-RAST cgi script"""

    # Get a copy of data access
    data_access = data_access_factory(DataAccessType.qiime_production)

    # Some vars
    # host = 'dunkirk.mcs.anl.gov'
    # host = 'test.metagenomics.anl.gov'
    host = 'www.metagenomics.anl.gov'
    
    #study_cgi_path = '/~wilke/service/%s/study' % key
    #sample_cgi_path = '/~wilke/service/%s/sample' % key
    #prep_cgi_path = '/~wilke/service/%s/preparation' % key
    #sequence_cgi_path = '/~wilke/service/%s/reads' % key
    
    study_cgi_path = '/service/%s/study' % key
    sample_cgi_path = '/service/%s/sample' % key
    prep_cgi_path = '/service/%s/preparation' % key
    sequence_cgi_path = '/service/%s/reads' % key
    
    study_file_path = '/tmp/mgrast_study_metadata_%s.xml' % study_id
    sample_file_path = '/tmp/mgrast_sample_metadata_%s.xml' % study_id
    prep_file_path = '/tmp/mgrast_prep_metadata_%s.xml' % study_id
    sequence_file_path = '/tmp/mgrast_sequence_metadata_%s.xml' % study_id
    fasta_base_path = '/tmp/'

    ######################################################
    #### Study Submission
    ######################################################

    print 'STUDY'

    # Get the study info and put it into xml format for MG-RAST
    study_file = open(study_file_path, 'w')
    study_info = data_access.getStudyInfo(study_id)
    
    study_file.write('<study>\n')
    study_file.write("    <study_id namespace='qiime'>%s</study_id>\n" % study_id)
    study_file.write('    <study_name>%s</study_name>\n' % study_info['project_name'])
    study_file.write('    <submission_system>qiime</submission_system>\n')
    study_file.write('    <metadata>\n')
    
    # Don't want to write these to MG-RAST
    del study_info['mapping_file_complete']
    del study_info['can_delete']
    del study_info['project_id']
    
    for item in study_info:
        study_file.write('        <{0}>{1}</{0}>\n'.format(item, study_info[item]))
    
    study_file.write('    </metadata>\n')
    study_file.write('</study>\n')
    study_file.close()

    # Read the study file
    study_file = open(study_file_path, 'r')
    file_contents = study_file.read()
    study_file.close()

    #print file_contents

    # Submit the study file data
    headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
    conn = httplib.HTTPConnection(host)
    conn.request(method="POST", url=study_cgi_path, body=file_contents, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Get the MG-RAST project_id
    if '<success>0</success>' in data:
        print 'Failed to add metadata to MG-RAST'
        print response.status, response.reason
        print str(data)
        #return
    
    # Find the MG-RAST project id for this newly created study
    if '<project_id>' in data:
        project_id = data[data.find('<project_id>')+len('<project_id>'):data.find('</project_id>')]
    else:
        print 'Setting temporary project_id to 1'
        project_id = 1
        
    print 'MG-RAST project_id: %s' % project_id

    ######################################################
    #### Sample Submission
    ######################################################

    # Get the column for this study and bin them into sample and prep lists
    study_columns = data_access.getStudyActualColumns(study_id)

    # Find the samples for this study
    samples = data_access.getSampleList(study_id)

    # For every sample, get the details and write them to the sample file
    for sample_id in samples:
        print 'SAMPLE'
        
        # Assign the sample name for later use
        sample_name = samples[sample_id]
        
        # Open the sample file for writing
        sample_file = open(sample_file_path, 'w')
        
        # Write the sample information to the sample file
        sample_file.write('<data_block>\n')
        sample_file.write('    <sample>\n')
        sample_file.write("        <study_id namespace='qiime'>%s</study_id>\n" % study_id)
        sample_file.write('        <project_id>%s</project_id>\n' % project_id)
        sample_file.write("        <sample_id namespace='qiime'>%s</sample_id>\n" % sample_id)
        sample_file.write('        <sample_name>%s</sample_name>\n' % sample_name)
        sample_file.write('        <metadata>\n')

        # For each column for this sample, write the value to the sample file
        for column_name in study_columns:
            table_name = data_access.findMetadataTable(column_name, study_id)
            table_category = data_access.getTableCategory(table_name)
            
            # Skip the prep and study columns
            if table_category in ['prep', 'study']:
                continue
                
            #print table_name, column_name, sample_id
            column_value = data_access.getSampleColumnValue(sample_id, table_name, column_name)
            sample_file.write('            <{0}>{1}</{0}>\n'.format(column_name, column_value))
            
        sample_file.write('        </metadata>\n')
        sample_file.write('    </sample>\n')
        sample_file.write('</data_block>\n')
        
        #Close the file and re-open for reading
        sample_file.close()
        sample_file = open(sample_file_path, 'r')
        file_contents = sample_file.read()
        sample_file.close()
        
        #print file_contents

        # Send the file to MG-RAST
        headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
        conn = httplib.HTTPConnection(host)
        conn.request(method="POST", url=sample_cgi_path, body=file_contents, headers=headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print str(data)
        conn.close()
        
        # Find the MG-RAST project id for this newly created study
        mgrast_sample_id = ''
        if '<sample_id>' in data:
            mgrast_sample_id = data[data.find('<sample_id>')+len('<sample_id>'):data.find('</sample_id>')]
        else:
            print 'No MG-RAST sample_id found'
            project_id = 1
    
        print 'MG-RAST sample_id: %s' % mgrast_sample_id

        ######################################################
        #### Sequence Prep Submission
        ######################################################

        for sample_id, row_number in data_access.getPrepList(sample_id):
            print 'PREP'
            # Open the prep file for writing
            prep_file = open(prep_file_path, 'w')

            prep_file.write('<data_block>\n')
            prep_file.write('    <sample_prep>\n')
            prep_file.write('        <study_id>%s</study_id>\n' % study_id)
            prep_file.write('        <project_id>%s</project_id>\n' % project_id)
            prep_file.write("        <sample_id namespace='qiime'>%s</sample_id>\n" % sample_id)
            prep_file.write("        <sample_id namespace='mgrast'>%s</sample_id>\n" % mgrast_sample_id)
            prep_file.write('        <sample_name>%s</sample_name>\n' % sample_name)
            prep_file.write('        <row_number>%s</row_number>\n' % row_number)
            prep_file.write('        <metadata>\n')

            # For each column for this sample, write the value to the sample file
            for column_name in study_columns:
                table_name = data_access.findMetadataTable(column_name, study_id)
                table_category = data_access.getTableCategory(table_name)
            
                # Skip the prep and study columns
                if table_category != 'prep':
                    continue
                    
                column_value = data_access.getPrepColumnValue(sample_id, row_number, table_name, column_name)
                prep_file.write('            <{0}>{1}</{0}>\n'.format(column_name, column_value))
            
            prep_file.write('        </metadata>\n')
            prep_file.write('    </sample_prep>\n')
            prep_file.write('</data_block>\n')
        
            #Close the file and re-open for reading
            prep_file.close()
            prep_file = open(prep_file_path, 'r')
            file_contents = prep_file.read()
            prep_file.close()
        
            #print file_contents

            # Send the file to MG-RAST
            headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
            conn = httplib.HTTPConnection(host)
            conn.request(method="POST", url=prep_cgi_path, body=file_contents, headers=headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()
            print str(data)
            conn.close()

            ######################################################
            #### Fasta Submission
            ######################################################

            print 'FASTA'

            # Open the prep file for writing
            sequence_file = open(sequence_file_path, 'w')

            sequence_file.write('<data_file>\n')
            sequence_file.write('     <study_id>%s</study_id>\n' % study_id)
            sequence_file.write('     <project_id>%s</project_id>\n' % project_id)
            sequence_file.write("     <sample_id namespace='qiime'>%s</sample_id>\n" % sample_id)
            sequence_file.write("     <sample_id namespace='mgrast'>%s</sample_id>\n" % mgrast_sample_id)
            sequence_file.write('     <row_number>%s</row_number>\n' % row_number)
            sequence_file.write("     <sequences type='16s'>\n")

            # For each column for this sample, write the value to the sample file
            output_fasta_path = fasta_base_path + 'sequences_%s_%s.fasta' % (sample_id, row_number)
            export_fasta_from_sample(study_id, sample_id, output_fasta_path)
            sequence_file.write(open(output_fasta_path, 'r').read())
            
            sequence_file.write('     </sequences>\n')
            sequence_file.write('</data_file>\n')
        
            #Close the file and re-open for reading
            sequence_file.close()
            sequence_file = open(sequence_file_path, 'r')
            file_contents = sequence_file.read()
            sequence_file.close()
        
            #print file_contents

            # Send the file to MG-RAST
            headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
            conn = httplib.HTTPConnection(host)
            conn.request(method="POST", url=sequence_cgi_path, body=file_contents, headers=headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()
            print str(data)
            conn.close()

