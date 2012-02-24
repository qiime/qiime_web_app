#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from os.path import basename
import sys
import httplib, urllib
from base_rest_services import BaseRestServices
from data_access_connections import data_access_factory
from enums import ServerConfig

class LiveEBISRARestServices(BaseRestServices):
    def __init__(self, study_id, web_app_user_id):
        super(LiveEBISRARestServices, self).__init__(study_id, web_app_user_id)
        self.key = ''
        self.hostname = ''
        self.study_url = '/service/%s/study' % self.key
        self.sample_url = '/service/%s/sample' % self.key
        self.library_url = '/service/%s/preparation' % self.key
        self.sequence_url = '/service/%s/reads' % self.key

    def send_post_data(self, url_path, file_contents, debug = False):
        success = None
        entity_id = None

        # Output the file contents if debug mode is set
        if debug:
            if len(file_contents) < 10000:
                print file_contents
            print 'Host: %s' % self.hostname
            print 'Service URL: %s' % url_path

        # Submit file data
        headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
        conn = httplib.HTTPConnection(self.hostname)
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
        
    def submit_files(self):
        """ Sends all files to EBI
        """
        
        # Read the study file
        study_file = open(study_file_path, 'r')
        file_contents = study_file.read()
        study_file.close()

        # Send the data to EBI via REST services
        success, project_id = self.send_post_data(self.study_url, file_contents, self.hostname)
        if not project_id:
            print 'Failed to add study metadata to MG-RAST. Aborting...'
            return
            
        # Send all other files in the same way.
        
    def generate_metadata_files(self, debug = False):
        """
        Submits data to EBI SRA via REST services.

        This function takes the input options from the user and generates a url
        and request header for submitting to the EBI SRA system. 
        """
        
        # A short name for the data helper
        helper = self.rest_data_helper
        
        #sequence_file_path = '/tmp/ebi_sra_sequence_metadata_%s.xml' % study_id
        #fasta_base_path = '/tmp/'

        # Set up a list of invalid values
        invalid_values = set(['', ' ', None, 'None'])
    
        ######################################################
        #### Submission XML
        ######################################################
    
        print 'SUBMISSION'
    
        # Get the study information
        study_info = helper.get_study_info()
    
        submission_file_path = '/tmp/ebi_sra_submission_metadata_%s.xml' % self.study_id
        submission_file = open(submission_file_path, 'w')
        submission_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        submission_file.write('<SUBMISSION_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        submission_file.write('xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.submission.xsd">\n')
        submission_file.write('<SUBMISSION alias="qiime_submission_{0}" center_name="CCME">\n'.format(str(self.study_id)))
        submission_file.write('<ACTIONS>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="qiime_study_{0}" schema="study"/>\n'.format(str(self.study_id)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="qiime_sample_{0}" schema="sample"/>\n'.format(str(self.study_id)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="qiime_experiment_{0}" schema="experiment"/>\n'.format(str(self.study_id)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="qiime_run_{0}" schema="run"/>\n'.format(str(self.study_id)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('</ACTIONS>\n')
        submission_file.write('</SUBMISSION>\n')
        submission_file.write('</SUBMISSION_SET>\n')    

        ######################################################
        #### Study XML
        ######################################################

        print 'STUDY'
        
        # Get the study info
        study_file_path = '/tmp/ebi_sra_study_metadata_%s.xml' % self.study_id
        study_file = open(study_file_path, 'w')

        study_alias = 'qiime_study_{0}'.format(str(self.study_id))
        study_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        study_file.write('<STUDY_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        study_file.write('    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.study.xsd">\n')
        study_file.write('    <STUDY alias="{0}"\n'.format(study_alias))
        study_file.write('        center_name="CCME">\n')
        study_file.write('        <DESCRIPTOR>\n')
        study_file.write('            <STUDY_TITLE>{0}</STUDY_TITLE>\n'.format(study_info['study_title']))
        study_file.write('            <STUDY_TYPE existing_study_type="{0}"/>\n'.format(study_info['investigation_type']))
        study_file.write('            <STUDY_ABSTRACT>{0}</STUDY_ABSTRACT>\n'.format(study_info['study_abstract']))
        study_file.write('        </DESCRIPTOR>\n')
        study_file.write('        <STUDY_ATTRIBUTES>\n')
    
        # Write out the remaining study fields
        for item in study_info:
            
            # Skip the samples
            if item == 'samples':
                continue
                
            study_file.write('            <STUDY_ATTRIBUTE>\n')
            study_file.write('                <TAG>{0}</TAG>\n'.format(item))
            study_file.write('                <VALUE>{0}</VALUE>\n'.format(study_info[item]))
            study_file.write('            </STUDY_ATTRIBUTE>\n')
        
        study_file.write('        </STUDY_ATTRIBUTES>\n')
        study_file.write('    </STUDY>\n')
        study_file.write('</STUDY_SET>\n')
    
        study_file.close()
        
        ######################################################
        #### Sample XML
        ######################################################
        
        print 'SAMPLE AND PREP'
        
        samples = study_info['samples']
        
        # Reference to the sample file
        sample_file_path = '/tmp/ebi_sra_sample_metadata_%s.xml' % self.study_id
        sample_file = open(sample_file_path, 'w')
        sample_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sample_file.write('<SAMPLE_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        sample_file.write('    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.sample.xsd">\n')
        
        # Reference to the experiment file
        experiment_file_path = '/tmp/ebi_sra_experiment_metadata_%s.xml' % self.study_id
        experiment_file = open(experiment_file_path, 'w')
        experiment_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        experiment_file.write('<EXPERIMENT_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        experiment_file.write('    xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.experiment.xsd">\n')
        
        # Reference to the run file
        run_file_path = '/tmp/ebi_sra_run_metadata_%s.xml' % self.study_id
        run_file = open(run_file_path, 'w')
        run_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        run_file.write('<RUN_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        run_file.write('xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.run.xsd">\n')

        # For every sample, get the details and write them to the sample file
        for sample_dict in samples:
            sample_alias = 'qiime_study_{0}:{1}'.format(str(self.study_id), sample_dict['sample_name'])
            sample_file.write('    <SAMPLE alias="{0}" center_name="CCME"> \n'.format(sample_alias))
            sample_file.write('        <TITLE>{0}</TITLE>\n'.format(sample_dict['sample_name']))
            sample_file.write('        <SAMPLE_NAME>\n')
            sample_file.write('            <TAXON_ID>{0}</TAXON_ID>\n'.format(sample_dict['taxon_id']))
            sample_file.write('        </SAMPLE_NAME>\n')
            sample_file.write('        <DESCRIPTION>{0}</DESCRIPTION>\n'.format(sample_dict['description']))
            sample_file.write('        <SAMPLE_ATTRIBUTES>\n')

            for sample_key in sample_dict:
                if sample_key == 'preps':
                    prep_list = sample_dict[sample_key]
                    for prep_dict in prep_list:
                        experiment_alias = 'qiime_experiment_{0}:{1}:{2}'.format(str(self.study_id), str(sample_dict['sample_id']), str(prep_dict['row_number']))
                        experiment_file.write('   <EXPERIMENT alias="{0}" center_name="CCME">\n'.format(experiment_alias))
                        experiment_file.write('       <TITLE>{0}</TITLE>\n'.format(experiment_alias))
                        experiment_file.write('       <STUDY_REF refname="{0}"/>\n'.format(study_alias))
                        experiment_file.write('       <DESIGN>\n')
                        experiment_file.write('           <DESIGN_DESCRIPTION>{0}</DESIGN_DESCRIPTION>\n'.format(prep_dict['experiment_design_description']))
                        experiment_file.write('           <SAMPLE_DESCRIPTOR refname="{0}"/>\n'.format(sample_alias))
                        experiment_file.write('           <LIBRARY_DESCRIPTOR>\n')
                        experiment_file.write('               <LIBRARY_NAME>{0}</LIBRARY_NAME>\n'.format(sample_dict['sample_name'] + ':' + str(prep_dict['row_number'])))
                        experiment_file.write('               <LIBRARY_STRATEGY>OTHER</LIBRARY_STRATEGY>\n')
                        experiment_file.write('               <LIBRARY_SOURCE>OTHER</LIBRARY_SOURCE>\n')
                        experiment_file.write('               <LIBRARY_SELECTION>unspecified</LIBRARY_SELECTION>\n')
                        experiment_file.write('               <LIBRARY_LAYOUT>\n')
                        experiment_file.write('                   <SINGLE/>\n')
                        experiment_file.write('               </LIBRARY_LAYOUT>\n')
                        experiment_file.write('               <LIBRARY_CONSTRUCTION_PROTOCOL>{0}</LIBRARY_CONSTRUCTION_PROTOCOL>\n'.format(prep_dict['library_construction_protocol']))
                        experiment_file.write('           </LIBRARY_DESCRIPTOR>\n')
                        experiment_file.write('       </DESIGN>\n')
                        experiment_file.write('       <PLATFORM>\n')
                        experiment_file.write('           <ILLUMINA>\n')
                        experiment_file.write('               <INSTRUMENT_MODEL>unspecified</INSTRUMENT_MODEL>\n')
                        experiment_file.write('           </ILLUMINA>\n')
                        experiment_file.write('       </PLATFORM>\n')
                        experiment_file.write('   </EXPERIMENT>\n')
                        for prep_key in prep_dict:                        
                            experiment_file.write('   <EXPERIMENT_ATTRIBUTES>\n')
                            experiment_file.write('       <EXPERIMENT_ATTRIBUTE>\n')
                            experiment_file.write('           <TAG>{0}</TAG>\n'.format(prep_key))
                            experiment_file.write('           <VALUE>{0}</VALUE>\n'.format(prep_dict[prep_key]))
                            experiment_file.write('       </EXPERIMENT_ATTRIBUTE>\n')
                            experiment_file.write('   </EXPERIMENT_ATTRIBUTES>\n')
                        
                        #################
                        ##################
                        # GENERATE SAMPLE FILE HERE
                        
                        # The run file references
                        run_file.write('    <RUN alias="july_09_488m_A_ECH2009_run" run_date="2010-10-11T00:00:00">\n')
                        run_file.write('        <EXPERIMENT_REF refname="{0}"/>\n'.format(experiment_alias))
                        run_file.write('        <DATA_BLOCK>\n')
                        run_file.write('            <FILES>\n')
                        run_file.write('                <FILE filename="{0}" filetype="sff"/>\n'.format(basename(run_file_path)))
                        run_file.write('            </FILES>\n')
                        run_file.write('        </DATA_BLOCK>\n')
                        run_file.write('    </RUN>\n')
                                        
                else:
                    sample_file.write('            <SAMPLE_ATTRIBUTE>\n')
                    sample_file.write('                <TAG>{0}</TAG>\n'.format(str(sample_key)))
                    sample_file.write('                <VALUE>{0}</VALUE>\n'.format(str(sample_dict[sample_key])))
                    sample_file.write('            </SAMPLE_ATTRIBUTE>\n')
            
            sample_file.write('        </SAMPLE_ATTRIBUTES>\n')
            sample_file.write('    </SAMPLE>\n')
        
        # Close the sample file    
        sample_file.write('</SAMPLE_SET>\n')
        sample_file.close()
        
        # Close the prep file
        experiment_file.write('</EXPERIMENT_SET>\n')
        experiment_file.close()
        
        # Close the run file
        run_file.write('</RUN_SET>')
        run_file.close()
        
        
        
        
