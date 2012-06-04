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
from os import remove
from shutil import copyfile
import gzip
import gc

class sequence_file_writer_factory(object):
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
	def __init__(self):
		""" Initial setup
		"""
		self.data_access = data_access_factory(ServerConfig.data_access_type)
		
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
			return SffSequenceWriter(self.data_access, study_id, sample_id, row_number, 'sff', root_dir, 'fastq')
		elif platform in fastq:
			return FastqSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fastq', root_dir, 'fastq')
		elif platform in fasta:
			return FastaSequenceWriter(self.data_access, study_id, sample_id, row_number, 'fasta', root_dir, 'fasta')
		else:
			# If no type could be determined, throw exception to inform caller a serious issues has occurred
			raise ValueError('Could not determine sequence file writer type based on platform: "%s"' % platform)

# The base class for all other sequence file writers
class BaseSequenceWriter(object):
	""" Base "abstract" class for all writer types
	
	This base class implements some common functionality for subclasses.
	"""
	def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
		self.data_access = data_access
		self.study_id = study_id
		self.sample_id = sample_id
		self.row_number = row_number
		self.writer_type = writer_type
		self.root_dir = root_dir
		self.file_extension = file_extension
		
	def write(self, debug = True):
		""" 
		Creates or locates the appropriate sequence file, gzips it if necessary, returns file reference
		"""

		if debug:
			print 'Writing sequence file for study_id {0}, sample_id {1}, row_number {2}'.format(str(self.study_id), str(self.sample_id), str(self.row_number))

		# Get the sample_name + sequence_prep_id from the sample_id
		query = """
select	s.sample_name || '.' || sp.sequence_prep_id, sp.run_prefix
from	sample s 
		inner join sequence_prep sp 
		on s.sample_id = sp.sample_id 
where	s.study_id = {0}
		and sp.sample_id = {1}
		and sp.row_number = {2}
		""".format(str(self.study_id), str(self.sample_id), str(self.row_number))

		if debug:
			print 'Running query: {0}'.format(query)

		results = self.data_access.dynamicMetadataSelect(query).fetchone()

		if debug: 
			print 'Query results: {0}'.format(str(results))

		sample_name = results[0]
		run_prefix = results[1]

		if debug:
			print 'Sample name is "{0}"'.format(sample_name)
			print 'Run prefix is "{0}"'.format(run_prefix)

		# Set the full file path and gzip file path
		full_file_name = join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/per_sample_fastq/seqs_{2}.fastq'.format(str(self.study_id), run_prefix, sample_name))
		if not exists(full_file_name):
			# Try removing the seqs_ prefix and see if it exists...
			full_file_name = join(self.root_dir, 'study_{0}/processed_data_{1}_/split_libraries/per_sample_fastq/{2}.fastq'.format(str(self.study_id), run_prefix, sample_name))
		if not exists(full_file_name):
			# If the file cannot be read or found, throw an exception.
			raise IOError('Sequence file does not exist: {0}. Skipping.'.format(full_file_name))
			
		gz_file_name = full_file_name + '.gz'
		
		if debug:
			print 'Full file name is "{0}"'.format(full_file_name)
			print 'gzip file name is "{0}"'.format(gz_file_name)
		
		# Shortcut - if the file exists, just return it. Don't refresh the archive.
		if exists(gz_file_name):
			if debug:
				print 'gzipped file exists. Returning name only.'
			return gz_file_name
			
		# If FASTA, create the sequence file from the database
		if self.writer_type == 'fasta' and not exists(full_file_name):
			if debug:
				print 'File does not exist, writing FASTA file {0} from database...'.format(full_file_name)
				
			# Export the file from database
			export_fasta_from_sample(self.study_id, self.sample_id, full_file_name)
			
			if debug:
				print 'File {0} exported from database successfully.'.format(full_file_name)

		# Create the gzip archive if file base file exists
		if full_file_name != None and full_file_name != '' and exists(full_file_name):

			# Otherwise, create a gzip archive of the seqs file
			if debug:
				print 'Creating gzip archive...'

			f_in = open(full_file_name, 'rb')
			f_out = gzip.open(gz_file_name, 'wb')
			f_out.writelines(f_in)
			f_out.close()
			f_in.close()

			# Remove the original file to save space
			#remove(full_file_name)

			return gz_file_name
		else:
			# If the file cannot be read or found, throw an exception.
			raise IOError('Sequence file does not exist: {0}. Skipping.'.format(full_file_name))

class FastaSequenceWriter(BaseSequenceWriter):
	""" Writes per-library fasta files
	
	This subclass creates per-library fasta files, gzips them, and returns file reference to caller
	"""
	def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
		super(FastaSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension)
				
class SffSequenceWriter(BaseSequenceWriter):
	""" Returns per-library gzipped fastq references for SFF data
	
	This subclass locates, gzips, and returns per-library sequence data to the caller. The per-library
	fastq files are generated from original SFF files during split_library runs.
	"""
	def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
		super(SffSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension)
				
class FastqSequenceWriter(BaseSequenceWriter):
	""" Returns per-library gzipped fastq files
	
	This subclass locates, gzips, and returns references to per-library fastq files to the caller. 
	"""
	def __init__(self, data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension):
		super(FastqSequenceWriter, self).__init__(data_access, study_id, sample_id, row_number, writer_type, root_dir, file_extension)


