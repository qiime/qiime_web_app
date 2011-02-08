__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from cogent.parse.fasta import *
from data_access_connections import data_access_factory
from enums import DataAccessType

def export_db_to_fasta(output_fasta_name):
    output_fasta = open(output_fasta_name, 'w')
    data_access = data_access_factory(DataAccessType.qiime_production)
    
    # Get all studies from the database
    results = data_access.getUserStudyNames(12161, 1)
    for study_id, study_name in results:
        print '------------------------ Exporting data from study ID: %s' % study_id
        export_fasta_from_study(study_id, output_fasta)

def export_fasta_from_study(study_id, output_fasta):
    # If name passed is a string, open the file. Otherwise ignore as the file
    # has already been opened by the parent
    file_opened_here = False
    if isinstance(output_fasta, str):
        output_fasta = open(output_fasta, 'w')
        file_opened_here = True
    
    # Get our copy of data access
    data_access = data_access_factory(DataAccessType.qiime_production)
    
    # Get all samples for this study
    sample_ids = data_access.getSampleIDsFromStudy(study_id)
    export_fasta_from_samples(study_id, sample_ids, output_fasta)
    
    # Close the file if opened in this function
    if file_opened_here:
        output_fasta.close()
        
def export_fasta_from_samples(study_id, sample_ids, output_fasta):
    # If name passed is a string, open the file. Otherwise ignore as the file
    # has already been opened by the parent
    file_opened_here = False
    if isinstance(output_fasta, str):
        output_fasta = open(output_fasta, 'w')
        file_opened_here = True
    
    # Get our copy of data_access
    data_access = data_access_factory(DataAccessType.qiime_production)

    for sample_id in sample_ids:
        seqs = data_access.getSequencesFromSample(study_id, sample_id)
        print '------------------------------ Seqs for sample ID: %s' % str(sample_id)
        for seq in seqs:
            output_fasta.write('>%s\n%s\n' % (seq, seqs[seq]))
            print seq

    # Close the file if opened in this function
    if file_opened_here:
        output_fasta.close()
    
