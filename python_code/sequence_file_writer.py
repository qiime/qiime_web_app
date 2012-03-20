#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

# Imports
from data_access_connections import data_access_factory
from enums import ServerConfig
from sample_export import *
from qiime.convert_fastaqual_to_fastq import convert_fastq
from os.path import join, exists
from shutil import copyfile

class sequence_file_writer_factory(object):
    def __init__(self):
        self.data_access = data_access_factory(ServerConfig.data_access_type)
        
    def __del__(self):
        if self.data_access:
            self.data_access == None
            
    def get_sequence_writer(self, study_id, sample_id, row_number, root_dir):
        # Based on sample_id, row_id, look up platform in database
        query = 'select platform from sequence_prep where sample_id = {0} and row_number = {1}'.format(str(sample_id), str(row_number))
        #print query
        platform = self.data_access.dynamicMetadataSelect(query).fetchone()[0].lower()
        
        sff = set(['tit', 'titanium', 'flx', '454', '454 flx'])
        fastq = set(['illumina', 'illumina gaiix'])
        fasta = set(['fasta'])
        
        if platform in sff:
            # Note that even though we start with SFF files, we're actually writing out a fastq file for export
            return SffSequenceWriter(self.data_access, study_id, sample_id, row_number, 'sff', root_dir, '.fastq')
        elif platform in fastq:
            return FastqSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fastq', root_dir, '.fastq')
        elif platform in fasta:
            return FastaSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fasta', root_dir, '.fasta')
        else:
            raise ValueError('Could not determine sequence file writer type based on platform: "%s"' % platform)
            return None

# The base class for all other sequence file writers
class BaseSequenceWriter(object):
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
        self.data_access = data_access
        self.study_id = study_id
        self.sample_id = sample_id
        self.row_number = row_number
        self.writer_type = writer_type
        self.root_dir = root_dir
        self.file_extension = file_extension
        
    def write(self):
        raise NotImplementedError('Base class has no implementation')

# Fasta sequence file writer
class FastaSequenceWriter(BaseSequenceWriter):
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
        super(FastaSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension)
        
    def write(self):
        print 'Writing FASTA sequence file for study_id {0}, sample_id {1}, row_number {2}'.format(str(self.study_id), str(self.sample_id), str(self.row_number))
        file_path = '/tmp/qiime_experiment_{0}:{1}:{2}_sequences'.format(self.study_id, self.sample_id, self.row_number)
        export_fasta_from_sample(self.study_id, self.sample_id, file_path)
        if exists(file_path):
            return file_path
        else:
            raise Exception('FASTA file was not created: {0}. Skipping.'.format(file_path))
                
# Fasta sequence file writer
class SffSequenceWriter(BaseSequenceWriter):
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
        super(SffSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension)
        
    def write(self):
        """ 
        The SFF writer doesn't atually have to do any work in creating the sequence file. 
        Split libraries has been reconfigured to produce the correct files. This function 
        therefore is responsible for makeing sure the file actually exists and copying it to
        the proper location with the right file name for later upload
        """
        
        #print 'Writing SFF sequence file for study_id {0}, sample_id {1}, row_number {2}'.format(str(self.study_id), str(self.sample_id), str(self.row_number))
        
        # Get the sample_name + sequence_prep_id from the sample_id
        query = """
select  s.sample_name || '.' || sp.sequence_prep_id 
from    sample s 
        inner join sequence_prep sp 
        on s.sample_id = sp.sample_id 
where   s.study_id = 367
        and sp.sample_id = {0}
        and sp.row_number = {1}
        """.format(str(self.sample_id), str(self.row_number))
        
        sample_name = self.data_access.dynamicMetadataSelect(query).fetchone()[0]
        #print 'Sample name is "{0}"'.format(sample_name)
        
        # File should already exist - go find it
        full_file_name = join(self.root_dir, 'study_{0}/processed_data_Fasting_subset_/split_libraries/per_sample_fastq/seqs_{1}.fastq'.format(str(self.study_id), sample_name))
        # print 'Full file name is "{0}"'.format(full_file_name)
        if full_file_name != None and full_file_name != '':
            return full_file_name
        else:
            raise Exception('SFF file does not exist: {0}. Skipping.'.format(full_file_name))        
                
# Fasta sequence file writer
class FastqSequenceWriter(BaseSequenceWriter):
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
        super(FastqSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension)
        
    def write(self):
        print 'Writing FASTQ sequence file for study_id {0}, sample_id {1}, row_number {2}'.format(str(self.study_id), str(self.sample_id), str(self.row_number))
        # export_fasta_from_sample(self.study_id, self.sample_id, file_path)
        # filter fastq file and


