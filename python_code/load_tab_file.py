#!/usr/bin/env python
# File created on 27 Jul 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME-webdev"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"


from cogent.util.misc import unzip
from cx_Oracle import NUMBER, STRING

type_lookup_oracle = {'i':NUMBER,'f':NUMBER,'s':STRING}
type_lookup_mock = {'i':int,'f':float,'s':str}
def unzip_and_cast_to_cxoracle_types(data, cursor, types):
    """Unzips data and casts each field to the corresponding oracle type

    data - a list or tuple of lists or tuples

    types - a list of 'i', 's', 'f' for int, string or float
    """
    type_lookup = type_lookup_oracle

    res = []
    for t,f in zip(types, unzip(data)):
        if t == 'i':
            tmp = map(int, f)
        elif t == 'f':
            tmp = map(float, f)
        elif t == 's':
            tmp = f
        res.append(cursor.arrayvar(type_lookup[t], tmp))
    return res 

def input_set_generator(data, cursor, types, buffer_size=10000):
    """yields data parsed into oracle types in buffer_size rows at a time"""
    buffer = []
    for line in data:
        if line.startswith('#'):
            continue

        buffer.append(line.strip().split('\t'))
        if len(buffer) >= buffer_size:
            res = unzip_and_cast_to_cxoracle_types(buffer, cursor, types)
            buffer = []
            yield res

    if buffer:
        res = unzip_and_cast_to_cxoracle_types(buffer, cursor, types)
        yield res