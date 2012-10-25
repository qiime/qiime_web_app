#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

from wrap_files_for_md5 import MD5Wrap
from cogent.util.unit_test import TestCase, main

class MD5Tests(TestCase):
    def setUp(self):
        pass
    def test_init(self):
        """ test_init: """
        
        foo = MD5Wrap([__file__,'b','c'])
        self.assertEqual(foo.file_list, [__file__,'b','c'])
        self.assertEqual(foo._current_idx, 0)
        self.assertEqual(foo._n_files, 3)
        self.assertFalse(foo.open_f.closed)
    def test_read(self):
        """ test_read: """
        
        foo = MD5Wrap([__file__,'b','c'])
        exp = '#!/usr/bin/env python'
        obs = foo.read(21)
        self.assertEqual(obs,exp)

if __name__ == '__main__':
    main()
