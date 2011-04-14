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
from enums import ServerConfig
from sample_export import export_fasta_from_sample
import os
import stat

def resolve_host(url_path):
    data = ''
    #host = 'metagenomics.anl.gov'
    host = dunkirk.mcs.anl.gov/~wilke

    try:
        print 'Attempting DNS connection to: %s' % host
        conn = httplib.HTTPConnection(host)
        headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
        conn.request(method = "POST", url = url_path, body = "connect test", headers = headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print 'data is: %s ' % data
        
        # Make sure a 404 was not returned
        if '404' not in data and data != '':
            print 'DNS attempt successful.'
            return host
        else:
            print 'DNS attempt unsuccessful. Data return was: %s' % data
            host = '140.221.76.10'

    except Exception, e:
        print str(e)
        host = '140.221.76.10'
    
    try:
        print 'Attempting IP connection to: %s' % host
        conn = httplib.HTTPConnection(host)
        headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
        conn.request(method = "POST", url = url_path, body = "connect test", headers = headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print 'data is: %s ' % data

        # Make sure a 404 was not returned
        if '404' not in data and data != '':
            print 'IP attempt successful.'
            return host
        else:
            print 'IP attempt unsuccessful. Aborting.'
    except Exception, e:
        print str(e)
        print 'Resolving host %s failed. Aborting...' % host
        
    return None

def clean_value_for_mgrast(value):
    value = str(value).replace('<', '__lessthan__')
    value = str(value).replace('>', '__greaterthan__')
    value = str(value).replace('$', '__dollarsign__')
    return value

def send_data_to_mgrast(url_path, file_contents, host, debug):
    success = None
    entity_id = None
        
    # Output the file contents if debug mode is set
    if debug:
        print file_contents
        print 'Host: %s' % host
        print 'Service URL: %s' % url_path
    
    # Submit file data
    headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
    conn = httplib.HTTPConnection(host)
    conn.request(method = "POST", url = url_path, body = file_contents, headers = headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    
    # Output the status and response if debug mode is set
    if debug:
        print response.status, response.reason
        print str(data)

    # Check for success
    if '<success>0</success>' in data:
        success = False
    elif '<success>1</success>' in data:
        success = True
    
    # Look for a returned identifier in the data
    if '<project_id>' in data:
        entity_id = data[data.find('<project_id>')+len('<project_id>'):data.find('</project_id>')]
    elif '<sample_id>' in data:
        entity_id = data[data.find('<sample_id>')+len('<sample_id>'):data.find('</sample_id>')]

    return success, entity_id

def submit_metadata_for_study(key, study_id, web_app_user_id, debug = False):
    """This function takes the input options from the user and generates a url
    and request header for submitting to the MG-RAST cgi script"""

    # Get a copy of data access
    data_access = data_access_factory(ServerConfig.data_access_type)

    study_cgi_path = '/service/%s/study' % key
    sample_cgi_path = '/service/%s/sample' % key
    prep_cgi_path = '/service/%s/preparation' % key
    sequence_cgi_path = '/service/%s/reads' % key
    
    study_file_path = '/tmp/mgrast_study_metadata_%s.xml' % study_id
    sample_file_path = '/tmp/mgrast_sample_metadata_%s.xml' % study_id
    prep_file_path = '/tmp/mgrast_prep_metadata_%s.xml' % study_id
    sequence_file_path = '/tmp/mgrast_sequence_metadata_%s.xml' % study_id
    fasta_base_path = '/tmp/'
    
    # Attempt to reslve the MG-RAST host
    # host = '140.221.76.10'
    #host = resolve_host(study_cgi_path)
    host = 'metagenomics.anl.gov'
    if host is None:
        print 'Could not resolve host. Aborting.'
        return

    ######################################################
    #### Study Submission
    ######################################################

    print 'STUDY'

    # Get the study info and put it into xml format for MG-RAST
    study_file = open(study_file_path, 'w')
    study_info = data_access.getStudyInfo(study_id, web_app_user_id)
    
    study_file.write('<study>\n')
    study_file.write("    <study_id namespace='qiime'>%s</study_id>\n" % study_id)
    study_file.write('    <study_name>%s</study_name>\n' % study_info['project_name'])
    study_file.write('    <submission_system>qiime</submission_system>\n')
    study_file.write('    <metadata>\n')
    
    # Don't want to write these to MG-RAST
    del study_info['mapping_file_complete']
    del study_info['can_delete']
    del study_info['project_id']
    del study_info['lab_person_contact']
    del study_info['emp_person']
    del study_info['has_extracted_data']
    del study_info['number_samples_promised']
    del study_info['spatial_series']
    del study_info['first_contact']
    del study_info['has_physical_specimen']
    del study_info['avg_emp_score']
    del study_info['user_emp_score']
    del study_info['lab_person']
    del study_info['principal_investigator']
    del study_info['principal_investigator_contact']
    del study_info['most_recent_contact']
    
    for item in study_info:
        value = study_info[item]
        study_file.write('        <{0}>{1}</{0}>\n'.format(item, clean_value_for_mgrast(value)))
    
    study_file.write('    </metadata>\n')
    study_file.write('</study>\n')
    study_file.close()

    # Read the study file
    study_file = open(study_file_path, 'r')
    file_contents = study_file.read()
    study_file.close()
        
    # Send the data to MG-RAST via REST services
    success, project_id = send_data_to_mgrast(study_cgi_path, file_contents, host, debug)
    if not project_id:
        print 'Failed to add study metadata to MG-RAST. Aborting...'
        return

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
            sample_file.write('            <{0}>{1}</{0}>\n'.format(column_name, 
                clean_value_for_mgrast(column_value)))
                        
        sample_file.write('        </metadata>\n')
        sample_file.write('    </sample>\n')
        sample_file.write('</data_block>\n')
        
        #Close the file and re-open for reading
        sample_file.close()
        sample_file = open(sample_file_path, 'r')
        file_contents = sample_file.read()
        sample_file.close()

        # Send the data to MG-RAST via REST services
        success, mgrast_sample_id = send_data_to_mgrast(sample_cgi_path, file_contents, host, debug)
        if not success or not mgrast_sample_id:
            print 'Failed to add sample metadata to MG-RAST for sample_id %s: %s. Skipping sample and its dependencies...'\
                % (sample_id, sample_name)
            continue

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
                prep_file.write('            <{0}>{1}</{0}>\n'.format(column_name,
                    clean_value_for_mgrast(column_value)))
            
            prep_file.write('        </metadata>\n')
            prep_file.write('    </sample_prep>\n')
            prep_file.write('</data_block>\n')
        
            #Close the file and re-open for reading
            prep_file.close()
            prep_file = open(prep_file_path, 'r')
            file_contents = prep_file.read()
            prep_file.close()
        
            # Send the data to MG-RAST via REST services
            success, entity_id = send_data_to_mgrast(prep_cgi_path, file_contents, host, debug)
            if not success:
                print 'Failed to add prep metadata to MG-RAST for sample_id %s. Skipping sample and its dependencies...' % sample_id
                continue

            ######################################################
            #### Fasta Submission
            ######################################################

            print 'FASTA'
            
            output_fasta_path = fasta_base_path + 'sequences_%s_%s.fasta' % (sample_id, row_number)
            export_fasta_from_sample(study_id, sample_id, output_fasta_path)
            file_size = os.stat(output_fasta_path)[stat.ST_SIZE]
            
            # If there are no sequences then skip
            if file_size > 0:
                continue

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
            f = open(output_fasta_path, 'r')
            sequence_file.write(f.read())
            f.close()
            
            sequence_file.write('     </sequences>\n')
            sequence_file.write('</data_file>\n')
        
            #Close the file and re-open for reading
            sequence_file.close()
            sequence_file = open(sequence_file_path, 'r')
            file_contents = sequence_file.read()
            sequence_file.close()
            
            # Send the data to MG-RAST via REST services
            success, entity_id = send_data_to_mgrast(prep_cgi_path, file_contents, host, debug)
            if not success:
                print 'Failed to add sequence data to MG-RAST for sample_id %s, row_number %s.'\
                    % (sample_id, row_number)


