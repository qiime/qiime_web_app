#!/usr/bin/env python

from cogent.util.unit_test import TestCase, main
from handler import JobExistsError, JobNotExistsError, JobHandler, \
        PollerTestHandlerOkay, ProcessSFFHandler

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@@colorado.edu"
__status__ = "Pre-release"

class JobHandlerTests(TestCase):
    def setUp(self):
        pass

    def test_init(self):
        """test base vars"""
        self.assertEqual(JobHandler._base_cmd, '')
        self.assertEqual(JobHandler._base_args, {})
        self.assertEqual(JobHandler._input_delimiter, '!!')

class PollerTestHandlerOkayTests(TestCase):
    """Tests for tests...
    
    These tests exercise the base class
    """
    def setUp(self):
        self.foo = PollerTestHandlerOkay('job1','')

    def test_init(self):
        """Makes sure shibby is setup"""
        self.assertEqual(self.foo._base_cmd, 'sleep 10; hostname')
        self.assertEqual(self.foo._base_args, {})
        self.assertEqual(self.foo.InputArgs, {})
        self.assertEqual(self.foo.OracleJobName, 'job1')

    def test_str(self):
        """test __str__"""
        exp = "OracleJobName:job1\tInputArgs:{}\tTorqueJobId:None\tState:None\tNotes:"
        obs = str(self.foo)
        self.assertEqual(obs,exp)

    def test_call(self):
        """Returns cmd"""
        self.assertEqual(self.foo(), 'sleep 10; hostname')

    def test_checkJobOutput(self):
        """Makes sure we err as expected"""
        self.assertFalse(self.foo.checkJobOutput([],[]))
        self.assertRaises(AssertionError, self.foo.checkJobOutput, [],['asd'])

    def test_getJobNotes(self):
        """job has no notes"""
        self.assertEqual(self.foo.getJobNotes(),'')

    def test_setTorqueJobId(self):
        """should set/raise approproately"""
        self.foo.setTorqueJobId('asd')
        self.assertEqual(self.foo.getTorqueJobId(), 'asd')
        self.assertRaises(JobExistsError, self.foo.setTorqueJobId, 'bar')

    def test_getTorqueJobId(self):
        """Should get the job id"""
        self.foo.setTorqueJobId('asd')
        self.assertEqual(self.foo.getTorqueJobId(), 'asd')

    def test_getJobState(self):
        """Should get the job state"""
        self.assertRaises(JobNotExistsError, self.foo.getJobState)
        self.foo.setTorqueJobId('asd')
        self.assertEqual(self.foo.getJobState(), 'NEW')

    def test_removeTorqueJobId(self):
        """should unset the job id"""
        self.assertRaises(JobNotExistsError, self.foo.removeTorqueJobId)
        self.foo.setTorqueJobId('asd')
        self.assertEqual(self.foo.getTorqueJobId(), 'asd')
        self.foo.removeTorqueJobId()
        self.assertRaises(JobNotExistsError, self.foo.getTorqueJobId)

    def test_updateJobState(self):
        """should update job state"""
        self.assertRaises(JobNotExistsError, self.foo.updateJobState, 'asd')
        self.foo.setTorqueJobId('asd')
        self.assertEqual(self.foo.getJobState(), 'NEW')

class ProcessSFFTests(TestCase):
    def setUp(self):
        self.job = ProcessSFFHandler('jobname', 'SFF=10!!Mapping=5!!Output=2')

    def test_init(self):
        """Make sure shibby is inited correctly"""
        self.assertEqual(self.job.InputArgs, {'SFF':'10',
                                              'Mapping':'5',
                                              'Output':'2'})
        self.assertEqual(self.job.OracleJobName, 'jobname')

    def test_checkJobOutput(self):
        self.assertFalse(self.job.checkJobOutput([],[]))
        self.assertTrue(self.job.checkJobOutput([],['1','2']))
        self.assertEqual(self.job.getJobNotes(),'1\n2')
if __name__ == '__main__':
    main()

