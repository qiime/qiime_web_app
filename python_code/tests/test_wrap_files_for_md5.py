#!/usr/bin/env python

from wrap_files_for_md5 import MD5Wrap
from cogent.util.unit_test import TestCase, main

class MD5Tests(TestCase):
    def setUp(self):
        pass
    def test_init(self):
        foo = MD5Wrap([__file__,'b','c'])
        self.assertEqual(foo.file_list, [__file__,'b','c'])
        self.assertEqual(foo._current_idx, 0)
        self.assertEqual(foo._n_files, 3)
        self.assertFalse(foo.open_f.closed)
    def test_read(self):
        foo = MD5Wrap([__file__,'b','c'])
        exp = '#!/usr/bin/env python'
        obs = foo.read(21)
        self.assertEqual(obs,exp)

if __name__ == '__main__':
    main()
