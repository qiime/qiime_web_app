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
from enums import ServerConfig

def export_full_db_to_fasta(output_fasta_name, distinct_list):
    """
    Exports the entire sequence collection to fasta
    
    This function exports the entire database to fasta format. It does not care
    about public/private nor does it depend on any linkages to other metadata.
    """
    output_fasta = open(output_fasta_name, 'w')
    data_access = data_access_factory(ServerConfig.data_access_type)
    
    seqs = data_access.getSequencesFullDatabase()
    md5s = []
    for seq in seqs:
        sequence_name, sequence_string, md5_checksum = seq[0], seq[1], seq[2]
        
        if distinct_list:
            if md5_checksum not in md5s:
                md5s.append(md5_checksum)
                output_fasta.write('>%s\n%s\n' % (sequence_name, sequence_string))
                print 'Exporting sequence: %s' % sequence_name
            else:
                print 'Duplicate checksum found for sequence name: %s. Skipping...' % sequence_name
        else:
            #output_fasta.write('>%s\n%s\n' % (sequence_name, sequence_string))
            print 'Exporting sequence: %s' % sequence_name
        

def export_db_to_fasta(output_fasta_name):
    """
    Exports sequences to fasta that have corresponding metadata
    
    This function exports all sequences to fasta which have corresponding metadata
    in the metadata schema. It will skip the rest. It DOES export private samples.
    """
    output_fasta = open(output_fasta_name, 'w')
    data_access = data_access_factory(ServerConfig.data_access_type)
    
    # Get all studies from the database
    results = data_access.getUserStudyNames(12161, 1,'qiime')
    
    for study_id, study_name,t,s in results:
        print '------------------------ Exporting data from study ID: %s' % study_id
        print study_name
        print '\n\n'
        export_fasta_from_study(study_id, output_fasta)

def export_fasta_from_study(study_id, output_fasta):
    # If name passed is a string, open the file. Otherwise ignore as the file
    # has already been opened by the parent
    file_opened_here = False
    if isinstance(output_fasta, str):
        output_fasta = open(output_fasta, 'w')
        file_opened_here = True
    
    # Get our copy of data access
    data_access = data_access_factory(ServerConfig.data_access_type)
    
    # Get all samples for this study
    sample_ids = data_access.getSampleIDsFromStudy(study_id)
    for sample_id in sample_ids:
        export_fasta_from_sample(study_id, sample_id, output_fasta)
    
    # Close the file if opened in this function
    if file_opened_here:
        output_fasta.close()
        
def export_fasta_from_sample(study_id, sample_id, output_fasta):
    # If name passed is a string, open the file. Otherwise ignore as the file
    # has already been opened by the parent
    file_opened_here = False
    if isinstance(output_fasta, str):
        output_fasta = open(output_fasta, 'w')
        file_opened_here = True
    
    # Get our copy of data_access
    data_access = data_access_factory(ServerConfig.data_access_type)
    seqs = data_access.getSequencesFromSample(study_id, sample_id)
    #print '------------------------------ Seqs for sample ID: %s' % str(sample_id)
    for seq in seqs:
        output_fasta.write('>%s\n%s\n' % (seq, seqs[seq]))
        #print seq

    # Close the file if opened in this function
    if file_opened_here:
        output_fasta.close()
    
