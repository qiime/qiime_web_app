"""
Functions to validate submission after qsub and before running the job
"""
__author__ = "Zhenjiang (Zech) Xu"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Zhenjiang (Zech) Xu"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Zhenjiang (Zech) Xu"]
__email__ = "zhenjiang.xu@colorado.edu"
__status__ = "Development"

import os
from enums import ServerConfig
from data_access_connections import data_access_factory


def validateFileExistence(study_id, study_dir):
    '''
    check the existence of sequence files in the filesystem 
    for each sequence filename in the database.
    '''
    data_access = data_access_factory(ServerConfig.data_access_type)
    absence_list = []
    for filename in data_access.getSFFFiles(study_id):
        filename  = os.path.basename(filename)
        file_list = os.listdir(study_dir)
        if not filename in file_list:
            absence_list.append(filename)
    return absence_list

def validateRunPrefix(study_id):
    '''
    Check every run prefix has a sequence file. It is case insensitive.
    '''
    data_access = data_access_factory(ServerConfig.data_access_type)
    run_prefixes = data_access.getRunPrefixes(study_id)
    error_list = []
    if run_prefixes:
        # if the list is not empty
        for run_prefix in run_prefixes:
            error_found = True
            run_prefix = run_prefix.upper()
            for filename in data_access.getSFFFiles(study_id):
                filename = os.path.basename(filename).upper()
                if filename.startswith(run_prefix):
                    error_found = False
                    break
            if error_found:
                error_list.append(run_prefix)
        return error_list
    else:
        return False
