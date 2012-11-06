#!/usr/bin/env python

"""Job handlers that support the QIIME-webapp poller"""

from copy import copy

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@@colorado.edu"
__status__ = "Pre-release"

import os
from enums import ServerConfig

PYTHON_BIN="%s/software/bin/python2.7" % ServerConfig.home
QIIME_WEBAPP_BASE = "%s/git/qiime_web_app/python_code/scripts" % ServerConfig.home
QIIME_PROCESS_SFF = QIIME_WEBAPP_BASE + "/process_sff_through_split_lib.py"
QIIME_LOAD_ANALYSIS_OTU_TABLE = QIIME_WEBAPP_BASE + "/submit_analysis_and_otu_table_to_db.py"
QIIME_LOAD_SPLIT_LIB_SEQS = QIIME_WEBAPP_BASE + "/submit_split_lib_seqs_to_db.py"
QIIME_EXPORT_MGRAST = QIIME_WEBAPP_BASE + "/submit_metadata_to_mgrast.py"
QIIME_EXPORT_EBISRA = QIIME_WEBAPP_BASE + "/submit_metadata_to_ebi_sra.py"
QIIME_PICK_OTU = QIIME_WEBAPP_BASE + "/chain_pick_otus.py"
#QIIME_SUBMIT_SFF_METADATA_TO_DB = QIIME_WEBAPP_BASE  + "/submit_sff_through_metadata_to_db.py"
#QIIME_SUBMIT_OTU_MAPPING_TO_DB = QIIME_WEBAPP_BASE  + "/submit_otu_mapping_to_db.py"
QIIME_MAKE_MAPPING_OTU_TABLE = QIIME_WEBAPP_BASE + "/make_mapping_file_and_otu_table.py"
QIIME_MAKE_MAPPING_FILE = QIIME_WEBAPP_BASE + "/make_mapping_file.py"
QIIME_MAKE_MAPPING_PCOA_PLOT = QIIME_WEBAPP_BASE + "/make_mapping_file_and_pcoa_plots.py"
QIIME_MAKE_MAP_OTU_TABLE_AND_SUBMIT_JOBS = QIIME_WEBAPP_BASE + "/make_mapping_file_and_otu_table.py"
QIIME_BDIV_THROUGH_PLOTS= QIIME_WEBAPP_BASE + "/bdiv_through_plots.py"
QIIME_MAKE_OTU_HEATMAP= QIIME_WEBAPP_BASE + "/make_otu_heatmap.py"
QIIME_SUMMARIZE_TAXA= QIIME_WEBAPP_BASE + "/summarize_taxonomy.py"
QIIME_ALPHA_RAREFACTION= QIIME_WEBAPP_BASE + "/alpha_rarefaction.py"


class HandlerException(Exception):
    pass
class JobExistsError(HandlerException):
    pass
class JobNotExistsError(HandlerException):
    pass
class InputError(HandlerException):
    pass

class JobHandler(object):
    """Abstract base class for job objects"""
    # _base_cmd is a to-be-formatted string of the form:
    # some_executable --arg1=default --arg2=%(arg_key_name)s ...
    _base_cmd = ''

    # _base_args is a dict containing argument key names and values of the form
    # {'arg_key_name':some_value, ...}
    _base_args = dict() 
    
    # delimiter of the key/value pairs packed into the INPUT column in the
    # TORQUE_JOBS table
    _input_delimiter = "!!"
    
    # for chaining jobs
    _next_job_handler = None

    def __init__(self, ora_job_name, input_str):
        self.OracleJobName = ora_job_name
        self.InputArgs = self._parse_input(input_str)
        self.TorqueJobId = None
        self.State = None
        self._notes = ''

    def __str__(self):
        """Stringimafy self"""
        name = 'OracleJobName:%s' % str(self.OracleJobName)
        args = 'InputArgs:%s' % str(self.InputArgs)
        pbs_id = 'TorqueJobId:%s' % str(self.TorqueJobId)
        state = 'State:%s' % str(self.State)
        notes = 'Notes:%s' % str(self._notes)
        return '\t'.join([name,args,pbs_id,state,notes])

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """Place holder for checking Torque job output
        
        Return False for no error, return True if error
        """
        raise NotImplementedError

    def getJobNotes(self):
        """Returns any notes"""
        return self._notes

    def _format_job_command(self):
        """Place holder for formatting a job command(s)"""
        return self._base_cmd % self.InputArgs

    def __call__(self):
        """Returns a formatted command"""
        return self._format_job_command()

    def _parse_input(self, input):
        """Unpackimafy the input
        
        Expects input to be a string formatted like:

        "key1=some_value!!key2=foo!!key3=bar"

        !! is the default _input_delimiter
        """
        # if job type does not take input
        if self._base_args == {} and (input == '' or input == None):
            return {}

        # parse packed input string
        try:
            args = input.split(self._input_delimiter)
        except:
            raise InputError, "Could not split input for Oracle job %s" \
                    % self.OracleJobName

        cur_args = copy(self._base_args)

        # setup input arguments dict
        for arg in args:
            try:
                key, value = arg.split('=')
            except:
                raise InputError, "Malformed input argument for Ora Job %s" \
                    % self.OracleJobName
            
            if key not in cur_args:
                raise InputError, "Invalid input argument for Ora Job %s" \
                    % self.OracleJobName
             
            cur_args[key] = value

        # verify that we have set all arguments
        if None in set(cur_args.values()):
            raise InputError, "Missing input argument for Ora Job %s" \
                % self.OracleJobName

        return cur_args

    def setTorqueJobId(self, job_id, state='NEW'):
        """Updates self with a new Torque job"""
        if self.TorqueJobId is not None:
            raise JobExistsError, "Torque Job %s already exists for Ora Job %s"\
                     % (job_id, self.OracleJobName)
        self.TorqueJobId = job_id
        self.State = state

    def getTorqueJobId(self):
        """Returns Torque job id"""
        if self.TorqueJobId is None:
            raise JobNotExistsError, "Ora Job %s doesn't have a Torque job!"\
                    % (self.OracleJobName)
        return self.TorqueJobId

    def getJobState(self):
        """Returns Torque job state"""
        if self.TorqueJobId is None:
            raise JobNotExistsError, "Ora Job %s doesn't have a Torque job!"\
                    % (self.OracleJobName)
        return self.State

    def removeTorqueJobId(self):
        """Removes a Torque job from self"""
        if self.TorqueJobId is None:
            raise JobNotExistsError, "Ora Job %s doesn't have a Torque job!"\
                    % (self.OracleJobName)
        self.TorqueJobId = None

    def updateJobState(self, state):
        """Updates Torque job state"""
        if self.TorqueJobId is None:
            raise JobNotExistsError, "Ora Job %s doesn't have a Torque job!"\
                    % (self.OracleJobName)
        self.State = state

class PollerTestHandlerOkay(JobHandler):
    """Test Handler"""
    _base_cmd = 'sleep 10; hostname'
    _base_args = {}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        assert not stderr_lines
        return False

class PollerTestHandlerErr(JobHandler):
    """Test Handler"""
    _base_cmd = 'sleep 10; hostname'
    _base_args = {}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """Make sure stderr_lines aren't empty"""
        assert stderr_lines
        self._notes = '\n'.join(stderr_lines)
        return True

# after this handler completes successfully, we have to add another job to the queue for 
# LoadSffAndMetadataHandler (Job Type of ??)
class ProcessSFFHandler(JobHandler):
    """Handler for process_sff_through_split_lib.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_PROCESS_SFF, "-i %(SFF)s -m %(Mapping)s -p %(ParamFile)s -s %(StudyID)s -d %(SubmitToTestDB)s -q %(SeqPlatform)s -r %(ProcessOnly)s -u %(UserId)s -fc"])
    _base_args = {'SFF':None, 'Mapping':None, 'ParamFile':None, 'StudyID':None,'SubmitToTestDB':None,'SeqPlatform':None,'ProcessOnly':None,'UserId':None}
    _next_job_handler = ''

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
#
# Load sequences into the DB
class LoadAnalysisOTUTableHandler(JobHandler):
    """Handler for submit_analysis_and_otu_table_to_db.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_LOAD_ANALYSIS_OTU_TABLE, \
            "-i %(ProcessedFastaFilepath)s -s %(StudyId)s -u %(UserId)s -o %(OutputDir)s -t %(TestDB)s -p %(Platform)s"])
    _base_args = {'ProcessedFastaFilepath':None, 'StudyId':None,'UserId':None,'OutputDir':None,'TestDB':None,'Platform':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False

# Load OTU table into DB
class LoadSplitLibSeqsHandler(JobHandler):
    """Handler for submit_split_lib_seqs_to_db.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_LOAD_SPLIT_LIB_SEQS, \
            "-i %(ProcessedFastaFilepath)s -s %(StudyId)s -u %(UserId)s -o %(OutputDir)s -t %(TestDB)s -a %(AnalysisId)s -r %(SeqRunId)s -m %(MDchecksum)s"])
    _base_args = {'ProcessedFastaFilepath':None, 'StudyId':None,'UserId':None,'OutputDir':None,'TestDB':None,'AnalysisId':None,'SeqRunId':None,'MDchecksum':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
            
# Command for picking OTUs
class ProcessPickOTUHandler(JobHandler):
    """Handler for pick_otus.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_PICK_OTU, "-i %(FastaFile)s -p %(ParamFile)s -o %(OutputDir)s -f"])
    _base_args = {'FastaFile':None, 'ParamFile':None, 'OutputDir':None}
    _next_job_handler = ''

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False

# Exports study metadata and sequences to MG-RAST
class ExportToMGRASTHandler(JobHandler):
    """Handler for submit_metadata_to_mgrast.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_EXPORT_MGRAST, "-s %(StudyID)s"])
    _base_args = {'StudyID':None}
    _next_job_handler = ''

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
            
# Exports study metadata and sequences to MG-RAST
class ExportToEBISRAHandler(JobHandler):
    """Handler for submit_metadata_to_mgrast.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_EXPORT_EBISRA, "-s %(StudyID)s"])
    _base_args = {'StudyID':None}
    _next_job_handler = ''

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False

'''
# Command for writing OTU mapping data to database
class LoadOTUMappingHandler(JobHandler):
    """Handler for submit_otu_mapping_to_db.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_SUBMIT_OTU_MAPPING_TO_DB, "-i %(InputDir)s"])
    _base_args = {'InputDir':None}
    _next_job_handler = ''

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False

# Command for writing OTU mapping data to test database
class TestLoadOTUMappingHandler(JobHandler):
    """Handler for submit_otu_mapping_to_db.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_SUBMIT_OTU_MAPPING_TO_DB, "-i %(InputDir)s -t %(TestDBFlag)s"])
    _base_args = {'InputDir':None, 'TestDBFlag':True}
    _next_job_handler = ''

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False


# when calling for the test database, use the -t option
class TestLoadSFFAndMetadataHandler(JobHandler):
    """Handler for submit_sff_and_metadata_to_db.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_SUBMIT_SFF_METADATA_TO_DB, \
            "-i %(ProcessedFastaFilepath)s -s %(StudyId)s -t"])
    _base_args = {'ProcessedFastaFiles':None, 'StudyId':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
'''
class makeMappingAndOTUFiles(JobHandler):
    ###OLD FXN
    """Handler for make_mapping_file_and_otu_table.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_MAKE_MAPPING_OTU_TABLE, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --query %(query)s --tax_class %(tax_class)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s"])
    _base_args = {'fs_fp':None, 'web_fp':None, 'query':None, 'tax_class':None,'fname_prefix':None,'user_id':None,'meta_id':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
#
class generateMapSubmitJobs(JobHandler):
    """Handler for bdiv_through_3d_plots.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_MAKE_MAPPING_FILE, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --query %(query)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --params %(params_path)s --bdiv_rarefied_at %(bdiv_rarefied_at)s --otutable_rarefied_at %(otutable_rarefied_at)s --jobs_to_start %(jobs_to_start)s --taxonomy %(taxonomy)s --tree_fp %(tree_fp)s" ])
    _base_args = {'fs_fp':None, 'web_fp':None, 'query':None,'fname_prefix':None,'user_id':None,'meta_id':None,'params_path':None,'bdiv_rarefied_at':None,'otutable_rarefied_at':None,'jobs_to_start':None,'taxonomy':None,'tree_fp':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False

'''                    
class LoadSFFAndMetadataHandler(JobHandler):
    """Handler for submit_sff_and_metadata_to_db.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_SUBMIT_SFF_METADATA_TO_DB, \
            "-i %(ProcessedFastaFilepath)s -s %(StudyId)s"])
    _base_args = {'ProcessedFastaFiles':None, 'StudyId':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
'''
'''
class makeMappingFileandPCoAPlots(JobHandler):
    ###OLD FXN
    """Handler for make_mapping_file_and_otu_table.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_MAKE_MAPPING_PCOA_PLOT, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --query %(query)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --beta_metric %(beta_metric)s --rarefied_at %(rarefied_at)s"])
    _base_args = {'fs_fp':None, 'web_fp':None, 'query':None,'fname_prefix':None,'user_id':None,'meta_id':None,'beta_metric':None,'rarefied_at':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
'''
class generateMapOTUTableSubmitJobs(JobHandler):
    """Handler for bdiv_through_3d_plots.py"""
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_MAKE_MAP_OTU_TABLE_AND_SUBMIT_JOBS, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --query %(query)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --params %(params_path)s --bdiv_rarefied_at %(bdiv_rarefied_at)s --otutable_rarefied_at %(otutable_rarefied_at)s --jobs_to_start %(jobs_to_start)s --taxonomy %(taxonomy)s --tree_fp %(tree_fp)s" ])
    _base_args = {'fs_fp':None, 'web_fp':None, 'query':None,'fname_prefix':None,'user_id':None,'meta_id':None,'params_path':None,'bdiv_rarefied_at':None,'otutable_rarefied_at':None,'jobs_to_start':None,'taxonomy':None,'tree_fp':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False

'''    
def load_sff_and_metadata(input, output):
    """Wraps the QIIME-webapp submission of sff and metadata to db script"""
    str_fmt = "%s %s/submit_sff_and_metadata_to_db.py -i %s -s 0"
    cmd_str = str_fmt % (PYTHON_BIN, QIIME_WEBAPP_BASE, input)
'''

class betaDiversityThroughPlots(JobHandler):
    """Handler for bdiv_through_plots.py"""

    _base_cmd = ' '.join([PYTHON_BIN, QIIME_BDIV_THROUGH_PLOTS, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --otu_table_fp %(otu_table_fp)s --mapping_file_fp %(mapping_file_fp)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --params %(params_path)s --bdiv_rarefied_at %(bdiv_rarefied_at)s --jobs_to_start %(jobs_to_start)s --tree_fp %(tree_fp)s --run_date %(run_date)s --zip_fpath %(zip_fpath)s --zip_fpath_db %(zip_fpath_db)s" ])
    _base_args = {'fs_fp':None, 'web_fp':None,'otu_table_fp':None,'mapping_file_fp':None,'fname_prefix':None,'user_id':None,'meta_id':None,'params_path':None,'bdiv_rarefied_at':None,'jobs_to_start':None,'tree_fp':None,'run_date':None,'zip_fpath':None,'zip_fpath_db':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
#
class makeOTUHeatmap(JobHandler):
    """Handler for make_otu_heatmap.py"""

    _base_cmd = ' '.join([PYTHON_BIN, QIIME_MAKE_OTU_HEATMAP, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --otu_table_fp %(otu_table_fp)s --mapping_file_fp %(mapping_file_fp)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --params %(params_path)s --bdiv_rarefied_at %(bdiv_rarefied_at)s --jobs_to_start %(jobs_to_start)s --tree_fp %(tree_fp)s --run_date %(run_date)s --zip_fpath %(zip_fpath)s --zip_fpath_db %(zip_fpath_db)s" ])
    _base_args = {'fs_fp':None, 'web_fp':None,'otu_table_fp':None,'mapping_file_fp':None,'fname_prefix':None,'user_id':None,'meta_id':None,'params_path':None,'bdiv_rarefied_at':None,'jobs_to_start':None,'tree_fp':None,'run_date':None,'zip_fpath':None,'zip_fpath_db':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
#
class alphaRarefaction(JobHandler):
    """Handler for make_otu_heatmap.py"""

    _base_cmd = ' '.join([PYTHON_BIN, QIIME_ALPHA_RAREFACTION, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --otu_table_fp %(otu_table_fp)s --mapping_file_fp %(mapping_file_fp)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --params %(params_path)s --bdiv_rarefied_at %(bdiv_rarefied_at)s --jobs_to_start %(jobs_to_start)s --tree_fp %(tree_fp)s --run_date %(run_date)s --zip_fpath %(zip_fpath)s --zip_fpath_db %(zip_fpath_db)s" ])
    _base_args = {'fs_fp':None, 'web_fp':None,'otu_table_fp':None,'mapping_file_fp':None,'fname_prefix':None,'user_id':None,'meta_id':None,'params_path':None,'bdiv_rarefied_at':None,'jobs_to_start':None,'tree_fp':None,'run_date':None,'zip_fpath':None,'zip_fpath_db':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
#
#
class summarizeTaxa(JobHandler):
    """Handler for make_otu_heatmap.py"""

    _base_cmd = ' '.join([PYTHON_BIN, QIIME_SUMMARIZE_TAXA, "--fs_fp %(fs_fp)s --web_fp %(web_fp)s --otu_table_fp %(otu_table_fp)s --mapping_file_fp %(mapping_file_fp)s --fname_prefix %(fname_prefix)s --user_id %(user_id)s --meta_id %(meta_id)s --params %(params_path)s --bdiv_rarefied_at %(bdiv_rarefied_at)s --jobs_to_start %(jobs_to_start)s --tree_fp %(tree_fp)s --run_date %(run_date)s --zip_fpath %(zip_fpath)s --zip_fpath_db %(zip_fpath_db)s" ])
    _base_args = {'fs_fp':None, 'web_fp':None,'otu_table_fp':None,'mapping_file_fp':None,'fname_prefix':None,'user_id':None,'meta_id':None,'params_path':None,'bdiv_rarefied_at':None,'jobs_to_start':None,'tree_fp':None,'run_date':None,'zip_fpath':None,'zip_fpath_db':None}

    def checkJobOutput(self, stdout_lines, stderr_lines):
        """If stderr_lines is not empty an error has occured"""
        if len(stderr_lines):
            self._notes = '\n'.join(stderr_lines)
            return True
        else:
            return False
