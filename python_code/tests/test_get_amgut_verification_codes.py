#!/usr/bin/env python

from get_amgut_verification_codes import collapse_names
from cogent.util.unit_test import TestCase, main

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdoandt@colorado.edu"
__status__ = "Development"

class VerificationTests(TestCase):
    def setUp(self):
        pass

    def test_collapse_names(self):
        """properly collapse names"""
        recs = [('a','b@c.com','123','v222'),
                ('b','whatever','235','v2235'),
                ('a','b@c.com','333','v344'),
                ('c','b@c.com','2315','v667')]

        exp = {1:[['b','whatever','235','v2235'],
                  ['c','b@c.com','2315','v667']],
               2:[['a','b@c.com','123', '333', 'v222', 'v344']]}
        
        obs = collapse_names(recs)
        self.assertEqual(sorted(obs.keys()), sorted(exp.keys()))
        for k in obs:
            self.assertEqual(sorted(obs[k]), sorted(exp[k]))

if __name__ == '__main__':
    main()

