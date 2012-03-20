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
from sequence_file_writer import sequence_file_writer_factory
import hashlib
from ftplib import FTP
#from data_access_connections import data_access_factory
#from enums import ServerConfig

class LiveEBISRARestServices(BaseRestServices):
    def __init__(self, study_id, web_app_user_id, root_dir):
        super(LiveEBISRARestServices, self).__init__(study_id, web_app_user_id)
        self.key = ''
        self.hostname = ''
        self.study_url = '/service/%s/study' % self.key
        self.sample_url = '/service/%s/sample' % self.key
        self.library_url = '/service/%s/preparation' % self.key
        self.sequence_url = '/service/%s/reads' % self.key
        self.root_dir = root_dir
        self.file_list = {}
        self.errors = []
        
        # File paths
        self.submission_file_path = '/tmp/ebi_sra_submission_metadata_%s.xml' % self.study_id
        self.study_file_path = '/tmp/ebi_sra_study_metadata_%s.xml' % self.study_id
        self.sample_file_path = '/tmp/ebi_sra_sample_metadata_%s.xml' % self.study_id
        self.experiment_file_path = '/tmp/ebi_sra_experiment_metadata_%s.xml' % self.study_id
        self.run_file_path = '/tmp/ebi_sra_run_metadata_%s.xml' % self.study_id
        
        # EBI FTP info
        self.ftp_url = 'ftp.sra.ebi.ac.uk'
        self.ftp_user = 'era-drop-215'
        self.ftp_pass = 'J7XoQJ8I'
        
        # Open the FTP connection, leave open for efficiency
        self.ftp = FTP(self.ftp_url, self.ftp_user, self.ftp_pass)

    def __del__(self):
        # Close the FTP connection
        self.ftp.quit()
        
    def send_ftp_data(self, file_path):
        f = open(file_path, 'rb')
        self.ftp.storbinary('STOR {0}'.format(basename(file_path)), f)
        f.close()

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
        
    def submit_files(self, debug = False):
        """ Sends all files to EBI via FTP
        """
        
        # Send the XML files
        xml_file_list = []
        xml_file_list.append(self.study_file_path)
        xml_file_list.append(self.submission_file_path)
        xml_file_list.append(self.sample_file_path)
        xml_file_list.append(self.experiment_file_path)
        xml_file_list.append(self.run_file_path)
        
        for f in xml_file_list:
            if debug:
                print 'Sending XML file "{0}"'.format(f)
            send_ftp_data(f)        
        
        # Send the sequence files
        for f in self.file_list:
            if debug:
                print 'Sending sequence file "{0}"'.format(f)
            send_ftp_data(f)
                
    def generate_metadata_files(self, debug = False):
        """
        Submits data to EBI SRA via REST services.

        This function takes the input options from the user and generates a url
        and request header for submitting to the EBI SRA system. 
        """
        
        # A short name for the data helper
        helper = self.rest_data_helper
        
        # Set up a list of invalid values
        invalid_values = set(['', ' ', None, 'None'])
        
        # Sequence writer factory - used for generating sequence file writers based on type of data
        writer_factory = sequence_file_writer_factory()
        
        # Get the study information
        study_info = helper.get_study_info()
    
        ######################################################
        #### Study XML
        ######################################################

        print '------------------> STUDY <------------------'
        
        # Get the study info
        study_file = open(self.study_file_path, 'w')

        study_alias = 'qiime_study_{0}'.format(str(self.study_id))
        study_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        study_file.write('<STUDY_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.study.xsd">\n')
        study_file.write('    <STUDY alias="{0}" center_name="CCME">\n'.format(study_alias))
        study_file.write('        <DESCRIPTOR>\n')
        study_file.write('            <STUDY_TITLE>{0}</STUDY_TITLE>\n'.format(study_info['study_title']))
        study_file.write('            <STUDY_TYPE existing_study_type="{0}"/>\n'.format(study_info['investigation_type']))
        study_file.write('            <STUDY_ABSTRACT>{0}</STUDY_ABSTRACT>\n'.format(self.clean_whitespace(study_info['study_abstract'])))
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
        
        print '------------------> SAMPLE AND PREP <------------------'
        
        samples = study_info['samples']
        
        # Reference to the sample file
        sample_file = open(self.sample_file_path, 'w')
        sample_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sample_file.write('<SAMPLE_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.sample.xsd">\n')
        
        # Reference to the experiment file
        experiment_file = open(self.experiment_file_path, 'w')
        experiment_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        experiment_file.write('<EXPERIMENT_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.experiment.xsd">\n')
        
        # Reference to the run file
        run_file = open(self.run_file_path, 'w')
        run_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        run_file.write('<RUN_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.run.xsd">\n')

        # For every sample, get the details and write them to the sample file
        for sample_dict in samples:
            sample_alias = 'qiime_study_{0}:{1}'.format(str(self.study_id), sample_dict['sample_name'])
            sample_file.write('    <SAMPLE alias="{0}" center_name="CCME"> \n'.format(sample_alias))
            sample_file.write('        <TITLE>{0}</TITLE>\n'.format(sample_dict['sample_name']))
            sample_file.write('        <SAMPLE_NAME>\n')
            if 'taxon_id' in sample_dict:
                taxon_id = sample_dict['taxon_id']
            else:
                taxon_id = 'unknown'
            sample_file.write('            <TAXON_ID>{0}</TAXON_ID>\n'.format(taxon_id))
            sample_file.write('        </SAMPLE_NAME>\n')
            if 'taxon_id' in sample_dict:
                description = sample_dict['description']
            else:
                description = 'unknown'
            sample_file.write('        <DESCRIPTION>{0}</DESCRIPTION>\n'.format(description))
            sample_file.write('        <SAMPLE_ATTRIBUTES>\n')

            for sample_key in sample_dict:
                if sample_key == 'preps':
                    prep_list = sample_dict[sample_key]
                    for prep_dict in prep_list:
                        # Extract a few values because they're frequently used
                        study_id = str(self.study_id)
                        sample_id = str(sample_dict['sample_id'])
                        row_number = str(prep_dict['row_number'])
                        
                        experiment_alias = 'qiime_experiment_{0}:{1}:{2}'.format(study_id, sample_id, row_number)
                        experiment_file.write('   <EXPERIMENT alias="{0}" center_name="CCME">\n'.format(experiment_alias))
                        experiment_file.write('       <TITLE>{0}</TITLE>\n'.format(experiment_alias))
                        experiment_file.write('       <STUDY_REF refname="{0}"/>\n'.format(study_alias))
                        experiment_file.write('       <DESIGN>\n')
                        experiment_file.write('           <DESIGN_DESCRIPTION>{0}</DESIGN_DESCRIPTION>\n'.format(prep_dict['experiment_design_description']))
                        experiment_file.write('           <SAMPLE_DESCRIPTOR refname="{0}"/>\n'.format(sample_alias))
                        experiment_file.write('           <LIBRARY_DESCRIPTOR>\n')
                        experiment_file.write('               <LIBRARY_NAME>{0}</LIBRARY_NAME>\n'.format(sample_dict['sample_name'] + ':' + row_number))
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
                        
                        
                        
                        
                        ##############################
                        ##################
                        ########## NEED TO PUT IN PROPER PLATFORM HERE
                        
                        
                        
                        
                        
                        
                        experiment_file.write('           <ILLUMINA>\n')
                        experiment_file.write('               <INSTRUMENT_MODEL>unspecified</INSTRUMENT_MODEL>\n')
                        experiment_file.write('           </ILLUMINA>\n')
                        experiment_file.write('       </PLATFORM>\n')
                        experiment_file.write('   </EXPERIMENT>\n')
                        experiment_file.write('   <EXPERIMENT_ATTRIBUTES>\n')
                        for prep_key in prep_dict:                        
                            experiment_file.write('       <EXPERIMENT_ATTRIBUTE>\n')
                            experiment_file.write('           <TAG>{0}</TAG>\n'.format(prep_key))
                            experiment_file.write('           <VALUE>{0}</VALUE>\n'.format(prep_dict[prep_key]))
                            experiment_file.write('       </EXPERIMENT_ATTRIBUTE>\n')
                        experiment_file.write('   </EXPERIMENT_ATTRIBUTES>\n')

                        # Create or reference sequence file
                        # Can be fastq, sff, or fasta, depending on what files we have available
                        file_writer = writer_factory.get_sequence_writer(self.study_id, sample_id, row_number, self.root_dir)
                        print 'Writer type is {0}'.format(file_writer.writer_type)
                        file_path = ''
                        file_identifier = ''
                        try:
                            file_path = file_writer.write()
                            file_identifier = '{0}:{1}:{2}'.format(self.study_id, sample_id, row_number)
                            self.file_list[file_identifier] = file_path
                        except Exception, e:
                            error = 'Exception caught while attempting to obtain file_path: "{0}". '.format(str(e))
                            error += 'file_path: "{0}", file_identifier: "{1}" '.format(str(file_path), str(file_identifier))
                            error += 'file_writer: {0} '.format(str(file_writer))
                            self.errors.append(error)
                            continue
                        
                        
                        ######################################
                        ############################
                        ############## NEED TO REPLACE RUN ALIAS AND RUN DATE
                        
                        
                        
                        
                        
                        # The run file references
                        run_file.write('    <RUN alias="july_09_488m_A_ECH2009_run" run_date="2010-10-11T00:00:00">\n')
                        run_file.write('        <EXPERIMENT_REF refname="{0}"/>\n'.format(experiment_alias))
                        run_file.write('        <DATA_BLOCK>\n')
                        run_file.write('            <FILES>\n')
                        run_file.write('                <FILE filename="{0}" filetype="{1}"/>\n'.format(basename(file_path), file_writer.file_extension))
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
        
        ######################################################
        #### Submission XML
        ######################################################
    
        print '------------------> SUBMISSION <------------------'
    
        submission_file = open(self.submission_file_path, 'w')
        submission_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        submission_file.write('<SUBMISSION_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.submission.xsd">\n')
        submission_file.write('<SUBMISSION alias="qiime_submission_{0}" center_name="CCME">\n'.format(str(self.study_id)))
        submission_file.write('<ACTIONS>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="{0}" schema="study"/>\n'.format(basename(self.study_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="{0}" schema="sample"/>\n'.format(basename(self.sample_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="{0}" schema="experiment"/>\n'.format(basename(self.experiment_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <ADD source="{0}" schema="run"/>\n'.format(basename(self.run_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('</ACTIONS>\n')

        # Sequence files here?
        submission_file.write('<FILES>\n')
        
        # Checksum for file. Done in chunks to prevent memory overflow for large files
        block_size = 8192
        for seqs_file in self.file_list:
            file_name = basename(self.file_list[seqs_file])
            open_file = open(self.file_list[seqs_file])
            md5 = hashlib.md5()
            while True:
                data = open_file.read(block_size)
                if not data:
                    break
                md5.update(data)
            checksum = md5.hexdigest()
            open_file.close()
            
            
            submission_file.write('    <FILE checksum="{0}" filename="{1}" checksum_method="MD5"/>\n'.format(checksum, file_name))    
        submission_file.write('</FILES>\n')
        
        submission_file.write('</SUBMISSION>\n')
        submission_file.write('</SUBMISSION_SET>\n')    

        print 'File List:'
        for f in self.file_list:
            print '{0} - {1}'.format(str(f), str(self.file_list[f]))
        
        if len(self.errors) > 0:
            print 'ERRORS FOUND:'
            for error in self.errors:
                print 'Error: {0}'.format(error)
