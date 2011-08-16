#!/usr/bin/env python

from cogent.util.unit_test import TestCase, main
from rapid_dedup_naive import get_duplicate_ids_from_seqs

__author__ = "Daniel McDonald"
__copyright__ = "QIIME Web App"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "daniel.mcdonald@colorado.edu"
__status__ = "Development"

class DedupTests(TestCase):
    def setUp(self):
        self.seqs = """>a
AATTGGCC
>b
AATTAATT
>c
AATTAA
>d
AATTAA
>e
TTAA
>f
TTAA
>g
AATTAA
""".splitlines()

    def test_get_duplicate_ids_from_seqs(self):
        """Returns {label:(md5sum(seq), seq)} and {label:[dup_labels]}"""
        dup = {'bfa6af6c781dccc1453e2a52074de5c7':['a'],
               '3ba25f3d2a0e7848a1cb61addc167abd':['b'],
               'fa84df08d446c40b89e86235913c65b5':['c','d','g'],
               'ecccb7340fe2a704f233bbf07df6c0f3':['e','f']}
        seqs = {'bfa6af6c781dccc1453e2a52074de5c7':'AATTGGCC',
                '3ba25f3d2a0e7848a1cb61addc167abd':'AATTAATT',
                'fa84df08d446c40b89e86235913c65b5':'AATTAA',
                'ecccb7340fe2a704f233bbf07df6c0f3':'TTAA'}
        obs_dup, obs_seqs = get_duplicate_ids_from_seqs(self.seqs)
        
        self.assertEqual(obs_dup, dup)
        self.assertEqual(obs_seqs, seqs)
        

if __name__ == '__main__':
    main()
