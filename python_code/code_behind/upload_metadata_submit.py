
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

import os
import zipfile
from subprocess import PIPE,Popen
from metadata_table import MetadataTable
from data_access_connections import data_access_factory
from enums import ServerConfig
data_access = data_access_factory(ServerConfig.data_access_type)

################################
# Helper Functions
################################
        
def is_binary(filename):
    """
    Determinees if a file is binary or text
    
    Adapted from: http://www.velocityreviews.com/forums/t320964-determine-file-type-binary-or-text.html
    """
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    finally:
        fin.close()

    return False

################################
# Checker functions
################################

def validateSampleFile(mdtable, study_id, web_app_user_id):
    errors = []

    # Check for duplicate sample names:    
    names = []
    dupes = []
    samples_missing = False
    
    # If the sample_name is missing, exit immediately
    try:
        sample_values = mdtable.getColumn('sample_name').values
    except Exception, e:
        errors.append('Error: "sample_name" must exist in your sample template.')
        return errors, samples_missing
    
    for name_valid_pair in sample_values:
        # The values are actually a tuple of the value and whether or not it validated
        name = name_valid_pair[0]
        if name in names:
            if name not in dupes:
                dupes.append(name)
        else:
            names.append(name)
            
    for name in dupes:
        errors.append('Sample names must be unique in the sample file: "%s"' % name)

    # If metadata was previously uploaded, make sure all samples in database
    # are still represented in the sample file
    study_info = data_access.getStudyInfo(study_id, web_app_user_id)
    if study_info['metadata_complete'] == 'y':
        file_sample_names = zip(*sample_values)[0]
        all_samples_present = data_access.verifySampleNames(study_id, file_sample_names)
        if not all_samples_present:
            samples_missing = True
        
    return errors, samples_missing

def validatePrepFile(mdtable, req, study_id):
    errors = []
    key_fields_changed = False
    
    # If any key fields are missing, exit immediately
    try:
        mdtable.getColumn('linker')
        mdtable.getColumn('primer')
        mdtable.getColumn('barcode')
        mdtable.getColumn('run_prefix')
        mdtable.getColumn('platform')
        mdtable.getColumn('sample_name')
    except Exception, e:
        errors.append('"linker", "primer", "barcode", "run_prefix", "platform", and "sample_name" must exist in your prep template.')
        return errors, key_fields_changed
    
    # Combo of run_prefix and barcode must be unique
    run_prefixes = []
    barcodes = []
    pairs = []
    dupes = []
    
    run_prefix_values = mdtable.getColumn('RUN_PREFIX').values
    barcode_values = mdtable.getColumn('BARCODE').values
        
    for i, v in enumerate(run_prefix_values):
        # Values come in tuples of value/valid
        run_prefix = run_prefix_values[i][0]
        barcode = barcode_values[i][0]
        
        pair = 'prefix: "%s", barcode: "%s"' % (run_prefix, barcode)
        if pair in pairs:
            if pair not in dupes:
                dupes.append(pair)
        else:
            pairs.append(pair)
        
    for dupe in dupes:
        errors.append('Pairs of BARCODE and RUN_PREFIX must be unique with the prep file: %s' % dupe)
    
    # Verify that the key fields we require have not been modified:
    # sample_name (already verified in validateSampleFile), linker, primer, barcode, run_prefix, platform
    
    # Extract fields from mdtable
    file_sample_names = zip(*mdtable.getColumn('sample_name').values)[0]
    file_linkers = zip(*mdtable.getColumn('linker').values)[0]
    file_primers = zip(*mdtable.getColumn('primer').values)[0]
    file_barcodes = zip(*mdtable.getColumn('barcode').values)[0]
    file_run_prefixes = zip(*mdtable.getColumn('run_prefix').values)[0]
    file_platforms = zip(*mdtable.getColumn('platform').values)[0]

    # Get data from database:
    # s.sample_name, sp.linker, sp.primer, sp.barcode, sp.run_prefix, sp.platform
    # ordered by sample_name
    database_fields = data_access.getImmutableDatabaseFields(study_id)
    
    # Compare. If they do not match, we must ask the user to reload all metadata or abort
    i = 0
    for file_sample_name in file_sample_names:
        for sample_name, linker, primer, barcode, run_prefix, platform in database_fields:
            if file_sample_name == sample_name:
                if file_linkers[i] != linker or file_primers[i] != primer or file_barcodes[i] != barcode or file_run_prefixes[1] != run_prefix or file_platforms[i] != platform:
                    key_fields_changed = True
        i += 1
    
    return errors, key_fields_changed
    
def multiFileValidation(sample_mdtable, prep_mdtable):
    errors = []
    orphans = []
    samples_with_no_prep = []
    bad_project_names = []
    
    # If any key fields are missing, exit immediately
    try:
        sample_mdtable.getColumn('sample_name')
        prep_mdtable.getColumn('sample_name')
    except Exception, e:
        errors.append('Cross-file validation failed due to missing "sample_name" field.')
        return errors

    # Make sure no sample_name entries exist in prep template that do not also exist in sample file
    sample_sample_values = sample_mdtable.getColumn('sample_name').values
    prep_sample_values = prep_mdtable.getColumn('sample_name').values
    
    for i, v in enumerate(prep_sample_values):
        if v not in sample_sample_values:
            if v[0] not in orphans:
                orphans.append(v[0])
                
    for orphan in orphans:
        errors.append('Sample value "%s" appears in prep template but is not listed in the sample file.' % orphan)
    
    # Make sure all samples in sample file are represented in the prep file
    for i, v in enumerate(sample_sample_values):
        if v not in prep_sample_values:
            if v[0] not in samples_with_no_prep:
                samples_with_no_prep.append(v[0])
                
    for sample in samples_with_no_prep:
        errors.append('Sample "%s" in sample file has no matching entry in the prep template.' % sample)
        
    return errors
    
def logErrors(master_list, new_list):
    if not new_list:
        return
        
    if master_list == None:
        raise ValueError('Master exception list is None.')
        
    for error in new_list:
        master_list.append(error)

################################
# The main attraction 
################################
def validateFileContents(study_id, portal_type, sess, form, req, web_app_user_id):
    """
    Process the uploaded archive. If valid, write files out to the filesystem
    and validate the contents of each.
    """
    
    # A nested FieldStorage instance holds the file
    fileitem = form['file']
    
    # Sample validation variables
    samples_missing = False
    
    # Test if the file was uploaded
    if fileitem.filename:
        # strip leading path from file name to avoid directory traversal attacks
        fname = form['output_fname']+fileitem.filename.strip().replace(" ","")
        dir_path = os.path.join(os.path.dirname(req.filename), form['output_dir'])

        # write the zipped file on the server
        zippedf = open(os.path.join(dir_path, fname), 'wb')
        zippedf.write(fileitem.file.read())
        zippedf.close()
    
        # create a zipfile object
        t = zipfile.ZipFile(os.path.join(dir_path, fname),'r')
        
        # Do some error checking of the archive's contents
        errors = []
        templates = []
        
        sample_template_found = False
        prep_template_found = False
        
        sample_mdtable = None
        prep_mdtable = None
        
        for fullname in t.namelist():
            # Ignore directories
            if fullname.endswith('/'):
                continue

            filename = os.path.basename(fullname).lower()
            # Ignore files that start with '.' - seem to be an artifact of the built-in
            # Mac file compression option within the Finder
            if filename.startswith('.'):
                continue

            # Make sure ends with .xls or .txt
            if filename.endswith('.xls') or filename.endswith('.txt'):
                pass
            else:
                continue

            # Validate that it's one of the two expected templates
            if 'sample_template' in filename:
                sample_template_found = True
            elif 'prep_template' in filename:
                prep_template_found = True
            else:
                continue

            # Add the file to the list of templates
            templates.append(filename)
                            
            # Looks like we're good, write it out to the filesystem
            outfile_filename = os.path.join(dir_path, filename)
            try:
                outfile = open(outfile_filename, 'w')
                outfile.write(t.read(fullname))
                outfile.flush()
                outfile.close()
            except IOError as e:
                errors.append("""Could not open file "%s". The error was: %s""" % (filename, e))
                continue
                
            # Check to see if it's a binary file
            if is_binary(outfile_filename):
                errors.append('The file "%s" is not a tab-delimited text file. Please resave this file in this format and try again.' % filename)
                continue
                
            # Check to see if columns are valid in this file
            mdtable = MetadataTable(outfile_filename, study_id)
            table_errors, bad_columns = mdtable.validateColumnNames()
            if len(table_errors) > 0:
                for e in table_errors:
                    errors.append(e)
            
            # Make sure there's at least one row of data in the file
            i = 0
            with open(outfile_filename, 'rU') as f:
                for line in f:
                    i += 1
            if i < 2:
                errors.append('The file "%s" contains no data.' % filename)
                continue

            # Perform specific validations
            if 'sample_template' in outfile_filename:
                sample_mdtable = mdtable
                sample_errors, samples_missing = validateSampleFile(mdtable, study_id, web_app_user_id)
                logErrors(errors, sample_errors)
            elif 'prep_template' in outfile_filename:
                prep_mdtable = mdtable
                prep_errors, key_fields_changed = validatePrepFile(mdtable, req, study_id)
                logErrors(errors, prep_errors)

        # Make sure we have one of each template type
        if not sample_template_found:
            errors.append('Sample template was not found.')
            
        if portal_type =='emp':
            pass
        elif not prep_template_found:
            errors.append('Prep template was not found.')
                
        # Perform multi-file validations
        if portal_type != 'emp' and sample_mdtable and prep_mdtable:
            logErrors(errors, multiFileValidation(sample_mdtable, prep_mdtable))

        # If the zip does not have exactly two templates, raise an error
        if portal_type == 'emp':
            pass
        elif len(templates) != 2:
            errors.append('A valid sample and prep template must be in the archive.')
            
        # If there were errors, report them and stop processing. Note that writing to the req 
        # object is the signal for the JumpLoader to flag and error
        if errors:
            req.write('<h3>The following errors were found:</h3><ul>')
            for e in errors:    
                req.write('<li style="color:#FF0000">%s</li>\n' % e)
            req.write('</ul>')
            
            return None
        else:
            # Handle sample database validation issues
            if samples_missing:
                # Do not change this string. It's checked for on the respose page.
                req.write('missing samples')
                return None
            
            # Handle immutable field issues
            if key_fields_changed:
                # Do not change this string. It's checked for on the respose page.
                req.write('immutable fields changed')
                return None
                                        
            # Delete the old files
            files = os.listdir(dir_path)
            for file_name in files:
                if file_name.endswith('.xls') or file_name.endswith('.zip'):
                    if os.path.basename(file_name) not in templates:
                        os.remove(os.path.join(dir_path, file_name))

            # Assuming all went well, return the list of templates
            return templates
            

