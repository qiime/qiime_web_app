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

def validateRunPrefix(study_id):
    '''
    Check every run prefix has a sequence file. It is case insensitive.
    '''
    data_access = data_access_factory(ServerConfig.data_access_type)
    run_prefixes = data_access.getRunPrefixes(study_id)
    if run_prefixes:
        for run_prefix in run_prefixes:
            found_flag = False
            run_prefix = run_prefix.upper()
            for filename in data_access.getSFFFiles(study_id):
                filename = os.path.basename(filename).upper()
                if filename.startswith(run_prefix):
                    found_flag = True
                    break
            if found_flag:
                return (True, "Run prefixes are validated successfully.")
            else:
                return (False, "The run prefix %s does not have a valid sequence file." % run_prefix)
    else:
        return (False, "The run prefix is not found for study %s" % study_id)
