
"""
Functions for page of same name
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from data_access_connections import data_access_factory
from enums import ServerConfig
import os

def submitJob(study_id, user_id, param_file, mapping_file, sequencing_platform, sff_files, process_only,submit_to_test_db,data_access):
    # Set up the parameters
    params = []
    params.append('Mapping=%s' % mapping_file)
    params.append('ParamFile=%s' % param_file)
    params.append('SFF=%s' % ','.join(sff_files))
    params.append('StudyID=%s' % str(study_id))
    params.append('SeqPlatform=%s' % str(sequencing_platform).upper())
    params.append('ProcessOnly=%s' % str(process_only))
    params.append('SubmitToTestDB=%s' % str(submit_to_test_db))
    job_input = '!!'.join(params)

    # Submit the job
    job_id = data_access.createTorqueJob('ProcessSFFHandler', job_input, user_id, study_id)
    # Make sure a legit job_id was created. If not, inform the user there was a problem
    if job_id < 0:
        raise Exception('There was an error creating the job. Please contact the system administrator.')

#
def submitQiimeJob(study_id, user_id, job_type, job_input, data_access):
    # Submit the job
    job_id = data_access.createTorqueJob(job_type, job_input, user_id, study_id)
    
    # Make sure a legit job_id was created. If not, inform the user there was a problem
    if job_id < 0:
        raise Exception('There was an error creating the job. Please contact the system administrator.')
    
    return job_id

def writeMappingFiles(study_id, data_access, mapping_file_dir):
    # Get a list of result sets, one per run_prefix found in the stuyd
    mapping_file_header, result_sets = data_access.getSplitLibrariesMappingFileData(study_id)
    
    # Clear the old split libraries mapping files
    data_access.clearSplitLibrariesMappingFiles(study_id)
    
    # For each result set returned, create a mapping file
    for run_prefix in result_sets:
        # Unpack the result set
        results = result_sets[run_prefix]
        
        # Create new mapping file in filesystem
        if not os.path.exists(mapping_file_dir):
            os.makedirs(mapping_file_dir)

        # Create the new mapping file for this run_prefix
        mapping_file = file(os.path.join(mapping_file_dir, '%s__split_libraries_mapping_file.txt' % run_prefix), 'w')

        # Write the header row
        mapping_file.write(mapping_file_header + '\n')

        # Write out out the rows for this file
        for row in results:
            # Can't use something like '\t'.join(row) because not all items in list
            # are string values, hence the explicit loop structure here.
            to_write = ''
            for column in row:
                val = str(column)
                if val == 'None':
                    val = ''
                to_write += val + '\t'
                
            # Write the row minus the last tab
            mapping_file.write(to_write[0:len(to_write)-1] + '\n')

        mapping_file.close()

        # Add to the database list
        data_access.addMappingFile(study_id, mapping_file.name)
        
    # Finally, return a list of all created mapping files
    mapping_files = data_access.getMappingFiles(study_id)
    return mapping_files

def submitJobsToQiime(study_id, user_id, mapping_file_dir,process_only,submit_to_test_db):
    # Instantiate one copy of data access for this process
    data_access = data_access_factory(ServerConfig.data_access_type)
    
    # Get the SFF files associated to this study
    sff_files = data_access.getSFFFiles(study_id)
    
    # Get the SFF files associated to this study
    sequencing_platform = data_access.getStudyPlatform(study_id)
    
    # Generate the mapping files
    mapping_files = writeMappingFiles(study_id, data_access, mapping_file_dir)
    
    # Figure out which mapping file pairs with each SFF file
    file_map = {}
    for mapping_file in mapping_files:
        # Skip the mapping file if it's not of the correct naming format
        if len(mapping_file.split('__')) != 2:
            continue

        run_prefix = os.path.basename(mapping_file).split('__')[0]
        matching_sff_files = []
        
        # Find the proper params file
        barcode_length = data_access.checkRunPrefixBarcodeLengths(study_id, run_prefix)
        param_file = '/home/wwwuser/projects/Qiime/qiime_web_app/python_code/parameter_files/%s__custom_parameters_uclust_ref_gg97.txt' % str(barcode_length)
        
        for sff_file in sff_files:
            sff_file_basename = os.path.splitext(os.path.basename(sff_file))[0].upper()
            # If the run_prefix matches the SFF file name exactly, assume only
            # one SFF for this run
            if run_prefix.upper() == os.path.splitext(sff_file_basename)[0].upper():
                matching_sff_files.append(sff_file)
                file_map[mapping_file] = matching_sff_files
                continue
                
            # If the run_prefix is contained in the file name, find all that match
            # and submit them together with the current mapping file
            elif run_prefix.upper() in sff_file_basename:
                # If it's the first item for this mapping file name, assign the list
                if not file_map.get(mapping_file):
                    file_map[mapping_file] = matching_sff_files
                file_map[mapping_file].append(sff_file)
            # If we get here, there are extra SFF files with no matching mapping file. 
            # For now, do nothing... may need to add some handling code at a later date.
            else:
                pass
    
    # Submit jobs to the queue
    for mapping_file in file_map:
        submitJob(study_id, user_id, param_file, mapping_file, sequencing_platform, file_map[mapping_file],process_only,submit_to_test_db, data_access)
