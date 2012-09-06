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


class MD5Wrap(object):
    def __init__(self, file_list):
        self.file_list = file_list
        self._current_idx = 0
        self._n_files = len(file_list)
        self.open_f = open(file_list[0])

    def read(self, num_bytes):
        """Reads num bytes from a file, moves to next file if EOF"""
        
        bytes = self.open_f.read(num_bytes)
        if not bytes:
            self._current_idx += 1

            # if there are no more files, just return bytes like normal read
            if self._current_idx >= self._n_files:
                pass # bytes will just fall through to end return
            else:
                self.open_f.close()
                self.open_f = open(self.file_list[self._current_idx])
                bytes = self.open_f.read(num_bytes)
        return bytes

