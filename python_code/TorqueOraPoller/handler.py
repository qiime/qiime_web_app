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

PYTHON_BIN="/usr/bin/python2.6"
QIIME_WEBAPP_BASE = "/home/wwwuser/projects/Qiime/qiime_web_app/python_code/scripts"
QIIME_PROCESS_SFF = QIIME_WEBAPP_BASE + "/process_sff_through_split_lib.py"
QIIME_PICK_OTU = QIIME_WEBAPP_BASE + "/chain_pick_otus.py"
QIIME_SUBMIT_SFF_METADATA_TO_DB = QIIME_WEBAPP_BASE  + "/submit_sff_through_metadata_to_db.py"
QIIME_SUBMIT_OTU_MAPPING_TO_DB = QIIME_WEBAPP_BASE  + "/submit_otu_mapping_to_db.py"
QIIME_MAKE_MAPPING_OTU_TABLE = QIIME_WEBAPP_BASE + "/make_mapping_file_and_otu_table.py"
QIIME_MAKE_MAPPING_PCOA_PLOT = QIIME_WEBAPP_BASE + "/make_mapping_file_and_pcoa_plots.py"

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
    _base_cmd = ' '.join([PYTHON_BIN, QIIME_PROCESS_SFF, "-i %(SFF)s -m %(Mapping)s -p %(ParamFile)s -s %(StudyID)s -f"])
    _base_args = {'SFF':None, 'Mapping':None, 'ParamFile':None, 'StudyID':None}
    _next_job_handler = ''

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

class makeMappingAndOTUFiles(JobHandler):
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

class makeMappingFileandPCoAPlots(JobHandler):
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

def load_sff_and_metadata(input, output):
    """Wraps the QIIME-webapp submission of sff and metadata to db script"""
    str_fmt = "%s %s/submit_sff_and_metadata_to_db.py -i %s -s 0"
    cmd_str = str_fmt % (PYTHON_BIN, QIIME_WEBAPP_BASE, input)



