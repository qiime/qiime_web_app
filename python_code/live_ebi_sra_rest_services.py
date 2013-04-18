#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from os.path import basename, exists, join
import sys
import httplib, urllib
from base_rest_services import BaseRestServices
from sequence_file_writer import SequenceFileWriterFactory
import hashlib
from ftplib import FTP
from subprocess import Popen, PIPE, STDOUT
from os.path import split
from os import chmod
from sys import stdout
from datetime import date, timedelta

class SequenceFile(object):
    def __init__(self, file_path, file_id, checksum):
        self.file_path = file_path
        self.file_id = file_id
        self.checksum = checksum

class LiveEBISRARestServices(BaseRestServices):
    
    def __init__(self, study_id, web_app_user_id, root_dir, debug = False):
        """ Sets up initial values
        
        Sets up file paths, urls, and other necessary details for submission to the EBI SRA
        """
        super(LiveEBISRARestServices, self).__init__(study_id, web_app_user_id, debug)
        self.key = ''
        self.hostname = ''
        self.study_url = '/service/%s/study' % self.key
        self.sample_url = '/service/%s/sample' % self.key
        self.library_url = '/service/%s/preparation' % self.key
        self.sequence_url = '/service/%s/reads' % self.key
        self.root_dir = root_dir
        self.file_list = []
        self.errors = []
        
        # File paths
        self.submission_file_path = join(self.base_study_path, 'ebi_submission_metadata_{0}.xml'.format(study_id))
        self.study_file_path = join(self.base_study_path, 'ebi_study_metadata_{0}.xml'.format(study_id))
        self.sample_file_path = join(self.base_study_path, 'ebi_sample_metadata_{0}.xml'.format(study_id))
        self.experiment_file_path = join(self.base_study_path, 'ebi_experiment_metadata_{0}.xml'.format(study_id))
        self.run_file_path = join(self.base_study_path, 'ebi_run_metadata_{0}.xml'.format(study_id))
        self.curl_file_path = join(self.base_study_path, 'ebi_curl_command_{0}.sh'.format(study_id))
        
        # EBI FTP info
        self.ftp_url = 'ftp.sra.ebi.ac.uk'
        self.ftp_user = 'era-drop-215'
        self.ftp_pass = 'J7XoQJ8I'
        
        # Open the FTP connection, leave open for efficiency
        #self.ftp = FTP(self.ftp_url, self.ftp_user, self.ftp_pass)
        
        # Eventually we may want to database these entries, but here are references to EBI
        # controlled vocabularies. These can be passed to the base class method 
        # "controlled_vocab_lookup" which will attempt to find a good match for a term
        self.existing_study_type = set([ \
            'Whole Genome Sequencing', 'Metagenomics', 'Transcriptome Analysis', \
            'Resequencing', 'Epigenetics', 'Synthetic Genomics', 'Forensic or Paleo-genomics', \
            'Gene Regulation Study', 'Cancer Genomics', 'Population Genomics', 'RNASeq', 'Exome Sequencing', \
            'Pooled Clone Sequencing', 'Other'])
            
        self.instrument_model = set([ \
            'Illumina Genome Analyzer', 'Illumina Genome Analyzer II', 'Illumina Genome Analyzer IIx', \
            'Illumina HiSeq 2000', 'Illumina HiSeq 1000', 'Illumina MiSeq', 'unspecified'])
            
        self.library_strategy = set([ \
            'WGS', 'WXS', 'RNA-Seq', 'WCS', 'CLONE', 'POOLCLONE', 'AMPLICON', 'CLONEEND', 'FINISHING', \
            'ChIP-Seq', 'MNase-Seq', 'DNase-Hypersensitivity', 'Bisulfite-Seq', 'EST', 'FL-cDNA', \
            'CTS', 'MRE-Seq', 'MeDIP-Seq', 'MBD-Seq', 'OTHER'])

        self.library_source = set([ \
            'GENOMIC', 'TRANSCRIPTOMIC', 'METAGENOMIC', 'METATRANSCRIPTOMIC', 'SYNTHETIC', \
            'VIRAL RNA', 'OTHER'])
            
        self.library_selection = set([ \
            'RANDOM', 'PCR', 'RANDOM PCR', 'RT-PCR', 'HMPR', 'MF', 'CF-S', 'CF-M', 'CF-H', 'CF-T', \
            'MSLL', 'cDNA', 'ChIP', 'MNase', 'DNAse', 'Hybrid Selection', 'Reduced Representation', \
            'Restriction Digest', '5-methylcytidine antibody', 'MBD2', 'CAGE', 'RACE', 'other', 'unspecified'])

    def __del__(self):
        """ Closes the FTP connection
        """
        #self.ftp.quit()
        pass

    def generate_curl_command(self):
        curl_command = 'curl -F "SUBMISSION=@{0}" -F "STUDY=@{1}" -F "SAMPLE=@{2}" -F "RUN=@{3}" -F"EXPERIMENT=@{4}" \
            "https://www.ebi.ac.uk/ena/submit/drop-box/submit/?auth=ERA%20era-drop-215%20UquRb+8GCPOaT56b6wzR5pFeF8E%3D"'.format(\
            self.submission_file_path, self.study_file_path, self.sample_file_path, self.run_file_path, self.experiment_file_path)
            
        return curl_command

    def send_curl_data(self, curl_output_fp, curl_command_fp):
        curl_output = open(curl_output_fp, 'w')
        run_list = ['{0}'.format(curl_command_fp)]
        proc = Popen(run_list, shell=True, universal_newlines=True, stdout=PIPE)
        complete = False
        while True:
            out = proc.stdout.read(1)
            if out == '' and proc.poll() != None:
                break
            if out != '':
                curl_output.write(out)
        curl_output.close()

        # Read the output file
        curl_output = open(curl_output_fp, 'r')
        curl_result = curl_output.read()
        curl_output.close()
        
        status = ''
        if 'success="true"' in curl_result:
            status = 'VALID'
        elif 'success="false"' in curl_result:
            status = 'INVALID'
        else:
            status = 'UNKNOWN'
        
        return status, curl_result
                    
    def send_ftp_data(self, file_path, debug = False):
        """ Sends a file to the EBI "dropbox" (FTP account)
        """
        with open(file_path, 'rb') as f:
            self.logger.log_entry('FTP to {0}: \n{1}'.format(self.ftp_url, file_path))
            self.ftp.storbinary('STOR {0}'.format(basename(file_path)), f)
            
    def call_ascp_command_line(self, ascp_command, debug = False):
        # For now, stdout set to None. There is a known bug in Python that will deadlock
        # the process if enough output is generated by the child process and the outputs
        # are piped back to the parent. See http://docs.python.org/library/subprocess.html.
        
        # Log file
        log_file = 'stdout.tmp'
        subprocess_output = open(log_file, 'w')
        
        #proc = Popen(ascp_command, shell=True, universal_newlines=True, stdout=subprocess_output, stderr=STDOUT)
        proc = Popen(ascp_command, shell=True, universal_newlines=True, stdout=None, stderr=STDOUT)
        return_value = proc.wait()
        subprocess_output.close()
        
        self.logger.log_entry('Return Value Was: %s' % str(return_value))
        subprocess_output = open(log_file, 'r')
        file_contents = subprocess_output.read()
        subprocess_output.close()
        self.logger.log_entry(file_contents)        
        
        if return_value != 0:
            raise Exception(file_contents)

    def send_post_data(self, url_path, file_contents, debug = False):
        """ Sends POST data
        
        Currently unused for the EBI but will likely be activated for sending one
        or more XML files to their REST service.
        """
        success = None
        entity_id = None

        # Output the file contents if
        if len(file_contents) < 10000:
            self.logger.log_entry(file_contents)
        self.logger.log_entry('Host: %s' % self.hostname)
        self.logger.log_entry('Service URL: %s' % url_path)

        # Submit file data
        headers = {"Content-type":"text/xml", "Accept":"text/xml", "User-Agent":"qiime_website"}
        conn = httplib.HTTPConnection(self.hostname)
        conn.request(method = "POST", url = url_path, body = file_contents, headers = headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        # Output the status and response
        self.logger.log_entry(response.status, response.reason)
        self.logger.log_entry(str(data))

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

        # Send the xml data
        """
        for f in xml_file_list:
            self.logger.log_entry('Sending XML file "{0}"'.format(f))
            #self.send_ftp_data(f)
            ascp_command = 'ascp -QT -k2 -L- {0} era-drop-215@fasp.sra.ebi.ac.uk:/.'.format(f)
            self.call_ascp_command_line(ascp_command, debug)
        """

        # Send the sequence files by directory
        unique_dirs = []
        for f in self.file_list:
            basedir, filename = split(f.file_path)
            if basedir not in unique_dirs:
                unique_dirs.append(basedir)
        
        for unique_dir in unique_dirs:
            self.logger.log_entry('Sending sequence file directory "{0}"'.format(unique_dir))
            ascp_command = 'ascp -QT -k2 -L- {0}/*.gz era-drop-215@fasp.sra.ebi.ac.uk:/.'.format(unique_dir)
            self.call_ascp_command_line(ascp_command, debug = False)
            
    def parse_ebi_output(self):
        pass
                
    def generate_metadata_files(self, debug = True, action_type = 'VALIDATE'):
        """
        Submits data to EBI SRA via REST services.
        
        action_type can be VALIDATE or ADD. Add will validate and add. VALIDATE will only validate

        This function takes the input options from the user and generates a url
        and request header for submitting to the EBI SRA system. 
        """
        
        # A short name for the data helper
        helper = self.rest_data_helper
        
        # Set up a list of invalid values
        invalid_values = set(['', ' ', None, 'None'])
        
        # Sequence writer factory - used for generating sequence file writers based on type of data
        writer_factory = SequenceFileWriterFactory(self.logger)
        
        # Get the study information
        study_info = helper.get_study_info()
    
        ######################################################
        #### Study XML
        ######################################################

        self.logger.log_entry('------------------> STUDY <------------------')
        
        # Get the study info
        study_file = open(self.study_file_path, 'w')

        study_alias = 'qiime_study_{0}'.format(str(self.study_id))
        study_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        study_file.write('<STUDY_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.study.xsd">\n')
        study_file.write('    <STUDY alias="{0}" center_name="CCME-COLORADO">\n'.format(study_alias))
        study_file.write('        <DESCRIPTOR>\n')
        study_file.write('            <STUDY_TITLE>{0}</STUDY_TITLE>\n'.format(study_info['study_title']))
        
        # Determine the study type
        existing_study_type = 'Other'
        if 'investigation_type' in study_info:
            result = self.controlled_vocab_lookup(self.existing_study_type, study_info['investigation_type'])
            if result is not None:
                existing_study_type = result
        study_file.write('            <STUDY_TYPE existing_study_type="{0}"/>\n'.format(existing_study_type))
        
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
        
        self.logger.log_entry('------------------> SAMPLE AND PREP <------------------')
        
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
            sample_file.write('    <SAMPLE alias="{0}" center_name="CCME-COLORADO"> \n'.format(sample_alias))
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

                        # If there are no seqeucnes, skip this prep entry. There will be no per-sample
                        # sequence file, thus the metadata describing it is not needed
                        if prep_dict['num_sequences'] == 0:
                            self.logger.log_entry('PREP DICT ENTRY HAS NO SEQUENCES. SKIPPING ENTRY: {0}'.format(str(prep_dict)))
                            continue;

                        self.logger.log_entry('PREP DICT IS: {0}'.format(str(prep_dict)))
                        
                        # Extract a few values because they're frequently used
                        study_id = str(self.study_id)
                        sample_id = str(sample_dict['sample_id'])
                        row_number = str(prep_dict['row_number'])

                        # Create or reference sequence file writer
                        # Can be fastq, sff, or fasta, depending on what files we have available
                        file_writer = writer_factory.get_sequence_writer(self.study_id, sample_id, row_number, self.root_dir)
                        self.logger.log_entry('Writer type is {0}'.format(file_writer.writer_type))

                        platform = ''
                        
                        if file_writer.writer_type == 'sff':
                            platform = 'LS454'
                        elif file_writer.writer_type == 'fastq':
                            platform = 'ILLUMINA'
                        elif file_writer.writer_type == 'fasta':
                            platform = 'LS454'
                        else:
                            platform = 'UNKNOWN'
                        
                        # Extract a few values because they're frequently used
                        study_id = str(self.study_id)
                        sample_id = str(sample_dict['sample_id'])
                        row_number = str(prep_dict['row_number'])
                        
                        experiment_alias = 'qiime_experiment_{0}:{1}:{2}'.format(study_id, sample_id, row_number)
                        experiment_file.write('   <EXPERIMENT alias="{0}" center_name="CCME-COLORADO">\n'.format(experiment_alias))
                        experiment_file.write('       <TITLE>{0}</TITLE>\n'.format(experiment_alias))
                        experiment_file.write('       <STUDY_REF refname="{0}"/>\n'.format(study_alias))
                        experiment_file.write('       <DESIGN>\n')
                        experiment_file.write('           <DESIGN_DESCRIPTION>{0}</DESIGN_DESCRIPTION>\n'.format(prep_dict['experiment_design_description']))
                        experiment_file.write('           <SAMPLE_DESCRIPTOR refname="{0}"/>\n'.format(sample_alias))
                        experiment_file.write('           <LIBRARY_DESCRIPTOR>\n')
                        experiment_file.write('               <LIBRARY_NAME>{0}</LIBRARY_NAME>\n'.format(sample_dict['sample_name'] + ':' + row_number))

                        # Figure out the library_strategy
                        library_strategy = 'OTHER'
                        library_source = 'METAGENOMIC'
                        library_selection = 'unspecified'
                        if 'investigation_type' in study_info:
                            investigation_type = study_info['investigation_type']
                            if investigation_type == 'metagenome':
                                library_strategy = 'POOLCLONE'
                            elif investigation_type == 'mimarks-survey':
                                library_strategy = 'AMPLICON'
                                library_selection = 'PCR'
                        experiment_file.write('               <LIBRARY_STRATEGY>{0}</LIBRARY_STRATEGY>\n'.format(library_strategy))
                        experiment_file.write('               <LIBRARY_SOURCE>{0}</LIBRARY_SOURCE>\n'.format(library_source))
                        experiment_file.write('               <LIBRARY_SELECTION>PCR</LIBRARY_SELECTION>\n')

                        experiment_file.write('               <LIBRARY_LAYOUT>\n')
                        experiment_file.write('                   <SINGLE/>\n')
                        experiment_file.write('               </LIBRARY_LAYOUT>\n')
                        experiment_file.write('               <LIBRARY_CONSTRUCTION_PROTOCOL>{0}</LIBRARY_CONSTRUCTION_PROTOCOL>\n'.format(self.clean_text_value(prep_dict['library_construction_protocol'])))
                        experiment_file.write('           </LIBRARY_DESCRIPTOR>\n')
                        
                        # Spot descriptor required for LS454
                        if platform == 'LS454':
                            experiment_file.write('        <SPOT_DESCRIPTOR>\n')
                            experiment_file.write('            <SPOT_DECODE_SPEC>\n')
                            experiment_file.write('                <READ_SPEC>\n')
                            experiment_file.write('                    <READ_INDEX>0</READ_INDEX>\n')
                            experiment_file.write('                    <READ_CLASS>Application Read</READ_CLASS>\n')
                            experiment_file.write('                    <READ_TYPE>Forward</READ_TYPE>\n')
                            experiment_file.write('                    <BASE_COORD>1</BASE_COORD>\n')
                            experiment_file.write('                </READ_SPEC>\n')
                            experiment_file.write('            </SPOT_DECODE_SPEC>\n')
                            experiment_file.write('        </SPOT_DESCRIPTOR>\n')
                        
                        experiment_file.write('       </DESIGN>\n')
                        
                        experiment_file.write('       <PLATFORM>\n')
                        experiment_file.write('           <{0}>\n'.format(platform))
                        experiment_file.write('               <INSTRUMENT_MODEL>unspecified</INSTRUMENT_MODEL>\n')
                        experiment_file.write('           </{0}>\n'.format(platform))                       
                        experiment_file.write('       </PLATFORM>\n')
                                                
                        experiment_file.write('       <EXPERIMENT_ATTRIBUTES>\n')
                        for prep_key in prep_dict:                        
                            experiment_file.write('          <EXPERIMENT_ATTRIBUTE>\n')
                            experiment_file.write('             <TAG>{0}</TAG>\n'.format(prep_key))
                            clean_value = self.clean_text_value(prep_dict[prep_key])
                            experiment_file.write('             <VALUE>{0}</VALUE>\n'.format(clean_value))
                            experiment_file.write('          </EXPERIMENT_ATTRIBUTE>\n')
                        experiment_file.write('       </EXPERIMENT_ATTRIBUTES>\n')
                        
                        experiment_file.write('   </EXPERIMENT>\n')
                        
                        checksum = None
                        file_path = ''
                        file_identifier = ''
                        block_size = 8192
                        
                        try:
                            file_path = file_writer.write()
                            checksum_file_path = '{0}.checksum'.format(file_path)
                            checksum = None
                            
                            # Check to see if the md5 has already been calculated and skip if already done
                            checksum_file_path = '{0}.checksum'.format(file_path)
                            if exists(checksum_file_path):
                                with open(checksum_file_path) as f:
                                    checksum = f.read()
                            
                            # Doesn't exist so calcuate and store result in file
                            else:                                   
                                # Checksum for file. Done in chunks to prevent memory overflow for large files
                                open_file = open(file_path)
                                md5 = hashlib.md5()
                                while True:
                                    data = open_file.read(block_size)
                                    if not data:
                                        break
                                    md5.update(data)
                                checksum = md5.hexdigest()
                                open_file.close()
                                
                                # Write the checksum file
                                with open(checksum_file_path, 'w') as f:
                                    f.write(checksum)

                            file_identifier = '{0}:{1}:{2}'.format(self.study_id, sample_id, row_number)
                            self.file_list.append(SequenceFile(file_path, file_identifier, checksum))
                        except Exception, e:
                            error = 'Exception caught while attempting to obtain file_path: "{0}". '.format(str(e))
                            error += 'file_path: "{0}", file_identifier: "{1}" '.format(str(file_path), str(file_identifier))
                            error += 'file_writer: {0} '.format(str(file_writer))
                            self.errors.append(error)
                            continue
                        
                        # The run file references
                        run_file.write('    <RUN alias="{0}_run" center_name="CCME-COLORADO">\n'.format(basename(file_path)))
                        run_file.write('        <EXPERIMENT_REF refname="{0}"/>\n'.format(experiment_alias))
                        run_file.write('        <DATA_BLOCK>\n')
                        run_file.write('            <FILES>\n')
                        run_file.write('                <FILE filename="{0}" filetype="{1}" quality_scoring_system="{2}" checksum_method="MD5" checksum="{3}"/>\n'.format(basename(file_path), file_writer.file_extension, 'phred', checksum))
                        run_file.write('            </FILES>\n')
                        run_file.write('        </DATA_BLOCK>\n')
                        run_file.write('    </RUN>\n')
                                        
                else:
                    sample_file.write('            <SAMPLE_ATTRIBUTE>\n')
                    sample_file.write('                <TAG>{0}</TAG>\n'.format(str(sample_key)))
                    clean_value = self.clean_text_value(str(sample_dict[sample_key]))
                    sample_file.write('                <VALUE>{0}</VALUE>\n'.format(clean_value))
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
    
        self.logger.log_entry('------------------> SUBMISSION <------------------')
        
        # Actions are either ADD or VALIDATE. ADD validates and adds data. VALIDATE is validate only
    
        submission_file = open(self.submission_file_path, 'w')
        submission_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        submission_file.write('<SUBMISSION_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.submission.xsd">\n')
        submission_file.write('<SUBMISSION alias="qiime_submission_{0}" center_name="CCME-COLORADO">\n'.format(str(self.study_id)))
        submission_file.write('<ACTIONS>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <{0} source="{1}" schema="study"/>\n'.format(action_type, basename(self.study_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <{0} source="{1}" schema="sample"/>\n'.format(action_type, basename(self.sample_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <{0} source="{1}" schema="experiment"/>\n'.format(action_type, basename(self.experiment_file_path)))
        submission_file.write('    </ACTION>\n')
        submission_file.write('    <ACTION>\n')
        submission_file.write('        <{0} source="{1}" schema="run"/>\n'.format(action_type, basename(self.run_file_path)))
        submission_file.write('    </ACTION>\n')

        # Only add the hold attribute if we are actually adding data to EBI. I don't know this for
        # certain but it seems that having it in there during validation causes certain entities to
        # be created on their end, causing the actual ADD operaiton to fail even if data validates.
        if action_type == 'ADD':
            submission_file.write('    <ACTION>\n')
            one_year = str(date.today() + timedelta(365))
            submission_file.write('         <HOLD HoldUntilDate="{0}"/>\n'.format(one_year))
            submission_file.write('    </ACTION>\n')

        submission_file.write('</ACTIONS>\n')

        # Sequence files here?
        #submission_file.write('<FILES>\n')
        #for seqs_file in self.file_list:
        #    submission_file.write('    <FILE checksum="{0}" filename="{1}" checksum_method="MD5"/>\n'.format(seqs_file.checksum, basename(seqs_file.file_path)))
        #submission_file.write('</FILES>\n')
        
        submission_file.write('</SUBMISSION>\n')
        submission_file.write('</SUBMISSION_SET>\n')

        self.logger.log_entry('File List:')
        for f in self.file_list:
            self.logger.log_entry('{0} - {1}'.format(f.file_path, f.checksum))
            
        # Write out the curl command to a file for now
        curl_file = open(self.curl_file_path, 'w')
        curl_file.write(self.generate_curl_command())
        curl_file.close()
        
        # Fix permissions
        chmod(self.curl_file_path, 0755)
        
        if len(self.errors) > 0:
            self.logger.log_entry('ERRORS FOUND:')
            for error in self.errors:
                self.logger.log_entry('Error: {0}'.format(error))
