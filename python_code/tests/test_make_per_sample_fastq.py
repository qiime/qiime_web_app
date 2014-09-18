#!/usr/bin/env python

from unittest import TestCase, main
from StringIO import StringIO
from tempfile import mkdtemp
from shutil import rmtree
from os.path import join, exists

from make_per_sample_fastq import split_helper

class MakePerSampleFastqTests(TestCase):
    def setUp(self):
        self.output_dir = mkdtemp()
        self.test_fastq = StringIO(test_fastq)

    def tearDown(self):
        rmtree(self.output_dir)

    def testSplit_4(self):
        split_helper(self.test_fastq, self.output_dir,
                     sequence_buffer_size=4, ascii_increment=33)
        self.assertTrue(exists(join(self.output_dir, 'S1.fastq')))
        self.assertTrue(exists(join(self.output_dir, 'S2.fastq')))
        s1_contents = open(join(self.output_dir, 'S1.fastq')).read()
        s2_contents = open(join(self.output_dir, 'S2.fastq')).read()
        self.assertEqual(s1_contents, s1_exp)
        self.assertEqual(s2_contents, s2_exp)

    def testSplit_2(self):
        split_helper(self.test_fastq, self.output_dir,
                     sequence_buffer_size=2, ascii_increment=33)
        self.assertTrue(exists(join(self.output_dir, 'S1.fastq')))
        self.assertTrue(exists(join(self.output_dir, 'S2.fastq')))
        s1_contents = open(join(self.output_dir, 'S1.fastq')).read()
        s2_contents = open(join(self.output_dir, 'S2.fastq')).read()
        self.assertEqual(s1_contents, s1_exp)
        self.assertEqual(s2_contents, s2_exp)



test_fastq = """@S1_0
ATGC
+
####
@S1_1
ATGC
+
####
@S1_2
ATGC
+
####
@S1_3
ATGC
+
####
@S2_0
ATGC
+
####
"""

s1_exp = """@S1_0
ATGC
+
####
@S1_1
ATGC
+
####
@S1_2
ATGC
+
####
@S1_3
ATGC
+
####
"""
s2_exp = """@S2_0
ATGC
+
####
"""


if __name__ == '__main__':
    main()
