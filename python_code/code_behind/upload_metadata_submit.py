
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

def validateFileContents(study_id, sess, form, req):
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
        study_template_found = False
        sample_template_found = False
        prep_template_found = False
        
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

            # Validate that it's one of the three expected templates
            if 'study_template' in filename:
                study_template_found = True
            elif 'sample_template' in filename:
                sample_template_found = True
            elif 'prep_template' in filename:
                prep_template_found = True
            else:
                continue

            # Add the file to the list of templates
            templates.append(filename)
                            
            # Looks like we're good, write it out to the filesystem
            try:
                outfile = open(os.path.join(dir_path, filename), 'w')
                outfile.write(t.read(fullname))
                outfile.flush()
                outfile.close()
            except IOError as e:
                errors.append("""Could not open file "%s". The error was: %s""" % (filename, e))
                continue

            # Check to see if columns are valid in this file
            mdtable = MetadataTable(os.path.join(dir_path, filename), study_id)
            table_errors = mdtable.validateColumnNames()
            if len(table_errors) > 0:
                for error in table_errors:
                    errors.append(error)

        # If the zip does not have exactly three templates, raise an error
        if len(templates) != 3:
            errors.append('Error: A valid study, sample, and prep template must be in the archive.')
            
        # Make sure we have one of each template type
        if not study_template_found:
            errors.append('Error: Study tempalte was not found.')
        if not sample_template_found:
            errors.append('Error: Sample template was not found.')
        if not prep_template_found:
            errors.append('Error: Prep template was not found.')

        # If there were errors, report them and stop processing. Note that writing to the req 
        # object is the signal for the JumpLoader to flag and error
        if errors:
            for error in errors:
                req.write('<h3>The following errors were found:</h3><ul>')
                req.write('<li style="color:#FF0000">%s</li>\n' % error)
                req.write('</ul>')
                return None
                            
        # Delete the old files
        files = os.listdir(dir_path)
        for file_name in files:
            if file_name.endswith('.xls') or file_name.endswith('.zip'):
                if os.path.basename(file_name) not in templates:
                    os.remove(os.path.join(dir_path, file_name))
                    
        # Assuming all went well, return the list of templates
        return templates
