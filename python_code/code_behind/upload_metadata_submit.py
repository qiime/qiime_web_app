
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
# Checker functions
################################
def validateSampleFile(mdtable, study_id):
    errors = []

    # Check for duplicate sample names:    
    names = []
    dupes = []
    
    sample_values = mdtable.getColumn('sample_name').values
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
        
    return errors

def validatePrepFile(mdtable):
    errors = []
    
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
                
    return errors
    
def multiFileValidation(sample_mdtable, prep_mdtable):
    errors = []
    orphans = []
    samples_with_no_prep = []
    bad_project_names = []

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
def validateFileContents(study_id, portal_type, sess, form, req):
    """
    Process the uploaded archive. If valid, write files out to the filesystem
    and validate the contents of each.
    """
    
    # A nested FieldStorage instance holds the file
    fileitem = form['file']
    
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

            # Check to see if columns are valid in this file
            mdtable = MetadataTable(outfile_filename, study_id)
            table_errors, bad_columns = mdtable.validateColumnNames()
            if len(table_errors) > 0:
                for e in table_errors:
                    errors.append(e)
                    
            # Perform specific validations
            if 'sample_template' in outfile_filename:
                sample_mdtable = mdtable
                logErrors(errors, validateSampleFile(mdtable, study_id))
            elif 'prep_template' in outfile_filename:
                prep_mdtable = mdtable
                logErrors(errors, validatePrepFile(mdtable))
                
        # Perform multi-file validations
        if portal_type != 'emp':
            logErrors(errors, multiFileValidation(sample_mdtable, prep_mdtable))

        # If the zip does not have exactly two templates, raise an error
        if portal_type == 'emp':
            pass
        elif len(templates) != 2:
            errors.append('A valid sample and prep template must be in the archive.')
            
        # Make sure we have one of each template type
        if not sample_template_found:
            errors.append('Sample template was not found.')
        if portal_type =='emp':
            pass
        elif not prep_template_found:
            errors.append('Prep template was not found.')

        # If there were errors, report them and stop processing. Note that writing to the req 
        # object is the signal for the JumpLoader to flag and error
        if errors:
            req.write('<h3>The following errors were found:</h3><ul>')
            for e in errors:    
                req.write('<li style="color:#FF0000">%s</li>\n' % e)
            req.write('</ul>')
                            
        # Delete the old files
        files = os.listdir(dir_path)
        for file_name in files:
            if file_name.endswith('.xls') or file_name.endswith('.zip'):
                if os.path.basename(file_name) not in templates:
                    os.remove(os.path.join(dir_path, file_name))
                    
        # Assuming all went well, return the list of templates
        return templates
