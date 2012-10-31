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
from qiime.convert_fastaqual_fastq import convert_fastq
from os.path import join, exists
from os import remove
from shutil import copyfile
import gzip
import gc

class SequenceFileWriterFactory(object):
    """ Factory for generating/returning sequence file references
    
    Depending on the type of file (sff/fastq/fasta), different methods are used to generate or
    return seqeunce file information. Based on the original source type, the strategies are:
    
    SFF: We now generate per-library fastq files in split_libraries. These files are gzipped and
    a reference is returned to the caller. If the file is already gzipped, no work is perfomred
    and a file reference is returned.
    
    FASTQ: *In progress* These files are treated exactly as SFF source files above.
    
    FASTA: *In progress* For files in which we have no originall quality information, per-library
    fasta files are generated, gzipped, and a reference is returned to the caller.
    """
    def __init__(self, logger):
        """ Initial setup
        """
        self.data_access = data_access_factory(ServerConfig.data_access_type)
        self.logger = logger
        
    def __del__(self):
        """ Destructor
        
        Sets data_access to None to guarantee GC finds it. Have had issues in the past;
        this seems to help prevent dangling connections.
        """
        if self.data_access:
            self.data_access = None
            gc.collect()
            
    def get_sequence_writer(self, study_id, sample_id, row_number, root_dir):
        """ Creates/returns a reference to the gzipped per-library sequence file.
        
        Based on sequence file type, return the proper type of writer.
        """
        # Based on sample_id, row_id, look up platform in database
        query = 'select platform from sequence_prep where sample_id = {0} and row_number = {1}'.format(str(sample_id), str(row_number))
        platform = self.data_access.dynamicMetadataSelect(query).fetchone()[0].lower()
        
        # Data in database is messy - until we create a controlled vocabulary these sets
        # will be used to determine the type of source data
        sff = set(['tit', 'titanium', 'flx', '454', '454 flx'])
        fastq = set(['illumina', 'illumina gaiix'])
        fasta = set(['fasta'])
        
        if platform in sff:
            # Note that even though we start with SFF files, we're actually writing out a fastq file for export
            return SffSequenceWriter(self.data_access, study_id, sample_id, row_number, 'sff', root_dir, 'fastq', self.logger)
        elif platform in fastq:
            return FastqSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fastq', root_dir, 'fastq', self.logger)
        elif platform in fasta:
            return FastaSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fasta', root_dir, 'fasta', self.logger)
        else:
            # If no type could be determined, throw exception to inform caller a serious issues has occurred
            raise ValueError('Could not determine sequence file writer type based on platform: "%s"' % platform)

# The base class for all other sequence file writers
class BaseSequenceWriter(object):
    """ Base "abstract" class for all writer types
    
    This base class implements some common functionality for subclasses.
    """
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger):
        self.data_access = data_access
        self.study_id = study_id
        self.sample_id = sample_id
        self.row_number = row_number
        self.writer_type = writer_type
        self.root_dir = root_dir
        self.file_extension = file_extension
        self.logger = logger

    def compress_file(self, source_path, gz_path):
        self.logger.log_entry('Non-zipped file exists. Creating gzipped file...')
        f_in = open(source_path, 'rb')
        f_out = gzip.open(gz_path, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        self.logger.log_entry('Gzip archive successfully created.')
        self.logger.log_entry('Full file name is "{0}"'.format(source_path))
        self.logger.log_entry('gzip file name is "{0}"'.format(gz_path))
        
    def write(self, debug = True):
        """ 
        Creates or locates the appropriate sequence file, gzips it if necessary, returns file reference
        """

        self.logger.log_entry('Writing sequence file for study_id {0}, sample_id {1}, row_number {2}'.format(str(self.study_id), str(self.sample_id), str(self.row_number)))

        # Get the sample_name + sequence_prep_id from the sample_id
        query = """
select  s.sample_name, s.sample_name || '.' || sp.sequence_prep_id as sample_and_prep, sp.run_prefix
from    sample s 
        inner join sequence_prep sp 
        on s.sample_id = sp.sample_id 
where   s.study_id = {0}
        and sp.sample_id = {1}
        and sp.row_number = {2}
        """.format(str(self.study_id), str(self.sample_id), str(self.row_number))

        self.logger.log_entry('Running query: {0}'.format(query))
        results = self.data_access.dynamicMetadataSelect(query).fetchone()
        self.logger.log_entry('Query results: {0}'.format(str(results)))

        sample_name = results[0]
        sample_and_prep = results[1]
        run_prefix = results[2]

        self.logger.log_entry('sample_name is "{0}"'.format(sample_name))
        self.logger.log_entry('sample_and_prep is "{0}"'.format(sample_and_prep))
        self.logger.log_entry('run_prefix is "{0}"'.format(run_prefix))

        # Let's see if we can find the sequence files. SFF and FASTQ studies processed recently
        # should have per-library fastq files in the per_sample_fastq folder. FASTA studies
        # do not share this convention. In this case, we look for the FASTA files in the root directory.
        # In addition to the base filenames, they may or may not be gzipped. If the gzipped file and 
        # checksum file already exists, we just return the .gz filename and checksum. If not, we gzip,
        # generate a checksum, and then return.
        
        # The list of possible sequence file paths
        possible_file_paths = []
        # Per-library FASTQ with seqs_ prefix
        possible_file_paths.append(join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/per_sample_fastq/seqs_{2}.{3}'.format(str(self.study_id), run_prefix, sample_and_prep, self.file_extension)))
        # Per-library FASTQ with no prefix
        possible_file_paths.append(join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/per_sample_fastq/{2}.{3}'.format(str(self.study_id), run_prefix, sample_and_prep, self.file_extension)))

        # Try to find one of these files...
        found = None
        for path in possible_file_paths:
            gz_path = path + '.gz'

            # Look for the .gz file first
            if exists(gz_path):
                self.logger.log_entry('gzipped file exists. Returning name only.')
                self.logger.log_entry('gzip file name is "{0}"'.format(gz_path))
                found = gz_path
                break
            elif exists(path):
                # Attempt to compress file
                self.compress_file(path, gz_path)
                if exists(gz_path):
                    found = gz_path
                break
        
        # If none of the possibilities exist in the filesystem we must abort
        if not found:
            raise IOError('Sequence file does not exist: {0}. Skipping.'.format(str(possible_file_paths)))

        # Otherwise, we found a real file (and maybe even gzipped it too)! Return that path to the caller.
        return found
        
class FastaSequenceWriter(BaseSequenceWriter):
    """ Writes per-library fasta files
    
    This subclass creates per-library fasta files, gzips them, and returns file reference to caller
    """
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger):
        super(FastaSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger)
    
    def write(self, debug = True):
        """ 
        Creates or locates the appropriate sequence file, gzips it if necessary, returns file reference
        """

        self.logger.log_entry('Writing FNA sequence file for study_id {0}, sample_id {1}, row_number {2}'.format(str(self.study_id), str(self.sample_id), str(self.row_number)))

        # Get the sample_name + sequence_prep_id from the sample_id
        query = """
select  s.sample_name, s.sample_name || '.' || sp.sequence_prep_id as sample_and_prep, sp.run_prefix
from    sample s 
        inner join sequence_prep sp 
        on s.sample_id = sp.sample_id 
where   s.study_id = {0}
        and sp.sample_id = {1}
        and sp.row_number = {2}
        """.format(str(self.study_id), str(self.sample_id), str(self.row_number))

        self.logger.log_entry('Running query: {0}'.format(query))
        results = self.data_access.dynamicMetadataSelect(query).fetchone()
        self.logger.log_entry('Query results: {0}'.format(str(results)))

        sample_name = results[0]
        sample_and_prep = results[1]
        run_prefix = results[2]

        self.logger.log_entry('sample_name is "{0}"'.format(sample_name))
        self.logger.log_entry('sample_and_prep is "{0}"'.format(sample_and_prep))
        self.logger.log_entry('run_prefix is "{0}"'.format(run_prefix))

        # Various possible paths...
        gz_fna_path = join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/{2}.gz'.format(str(self.study_id), sample_name, sample_and_prep))
        fna_path = join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/seqs.fna'.format(str(self.study_id), sample_name))
        
        gz_run_prefix_path = join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/{2}.gz'.format(str(self.study_id), run_prefix, sample_and_prep))
        run_prefix_path = join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/seqs.fna'.format(str(self.study_id), run_prefix))

        # Check for the gzipped possibilities first
        found = None
        if exists(gz_fna_path):
            self.logger.log_entry('gzipped sample-based file exists. Returning name only.')
            self.logger.log_entry('gzip file name is "{0}"'.format(gz_fna_path))
            found = gz_fna_path
        elif exists(gz_run_prefix_path):
            self.logger.log_entry('gzipped run_prefix-based file exists. Returning name only.')
            self.logger.log_entry('gzip file name is "{0}"'.format(gz_run_prefix_path))
            found = gz_run_prefix_path
        elif exists(fna_path):
            # Attempt to compress file
            self.compress_file(fna_path, gz_fna_path)
            if exists(gz_fna_path):
                found = gz_fna_path
        elif exists(run_prefix_path):
            # Attempt to compress file
            self.compress_file(run_prefix_path, gz_run_prefix_path)
            if exists(gz_run_prefix_path):
                found = gz_run_prefix_path

        # If none of the possibilities exist in the filesystem we must abort
        if not found:
            raise IOError('Sequence file does not exist: {0}. Skipping.'.format(str(fna_path)))

        # Otherwise, we found a real file (and maybe even gzipped it too)! Return that path to the caller.
        return found    
                
class SffSequenceWriter(BaseSequenceWriter):
    """ Returns per-library gzipped fastq references for SFF data
    
    This subclass locates, gzips, and returns per-library sequence data to the caller. The per-library
    fastq files are generated from original SFF files during split_library runs.
    """
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger):
        super(SffSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger)
                
class FastqSequenceWriter(BaseSequenceWriter):
    """ Returns per-library gzipped fastq files
    
    This subclass locates, gzips, and returns references to per-library fastq files to the caller. 
    """
    def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger):
        super(FastqSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension, logger)


