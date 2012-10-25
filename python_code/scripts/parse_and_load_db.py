#!/usr/bin/env python

from sys import argv
from cogent.util.misc import unzip
from optparse import OptionParser, make_option
from cx_Oracle import connect, NUMBER, STRING, FIXED_CHAR

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Production"

options = [make_option('--input',dest='input',default=None,type='string',\
              help="Input tab delimited file"),
           make_option('--types',dest='types',default=None,type='string',\
              help="Comma separated types for each col. Use i, f, or s for int, float, or str"),
           make_option('--test',dest='test',action='store_true', default=False,
              help="Test for sanity, implies verbose"),
           make_option('--verbose',dest='verbose',action='store_true',default=False,
              help="To be or not to be...verbose"),
           make_option('--stored-proc',dest='stored_proc',default=None, type='string',
              help="Stored procedure to call"),
           make_option('--dsn',dest='dsn',default=None,type='string',
              help="DSN to connect to"),
           make_option('--username',dest='username',default=None,type='string',
              help="DB username"),
           make_option('--password',dest='password',default=None,type='string',
              help="DB password"),
           make_option('--buffer-size', dest='buffer_size',default=10000,
               type='int',help="Parsing buffer size")]

type_lookup_oracle = {'i':NUMBER,'f':NUMBER,'s':STRING,'fc':FIXED_CHAR}
type_lookup_mock = {'i':int,'f':float,'s':str}
def unzip_and_cast_to_cxoracle_types(data, cursor, types):
    """Unzips data and casts each field to the corresponding oracle type

    data - a list or tuple of lists or tuples

    types - a list of 'i', 's', 'f' for int, string or float
    """
    if isinstance(cursor, MockConnection):
        type_lookup = type_lookup_mock
    else:
        type_lookup = type_lookup_oracle

    res = []
    for t,f in zip(types, unzip(data)):
        if t == 'i':
            tmp = map(int, f)
        elif t == 'f':
            tmp = map(float, f)
        elif t == 's':
            tmp = f
        else:
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

class MockConnection(object):
    def __init__(self):
        pass
    def connect(self, *args, **kwargs):
        return self
    def cursor(self):
        return self
    def arrayvar(self, cast_type, data):
        return map(cast_type, data)
    def commit(self):
        return self
    def close(self):
        return self
    def callproc(self, *args):
        pass
def main(args_in=argv):
    parser = OptionParser(option_list=options)
    opts, args = parser.parse_args(args=args_in)
    lines = open(opts.input)
    types = opts.types.split(',')
    stored_proc = opts.stored_proc
    buffer_size = opts.buffer_size
    test = opts.test
    verbose = opts.verbose

    if test:
        verbose = True
    
    if opts.verbose:
        print "Attempting connection..."

    if test:
        con = MockConnection()
    else:
        try:
            con = connect(user=opts.username,
                                password=opts.password,
                                dsn=opts.dsn)
        except:
            print "Unable to connect!"
            raise SystemExit

    if verbose:
        print "Connection succeeded..."
    
    set_count = 1
    cur = con.cursor()
    for input_set in input_set_generator(lines, cur, types, buffer_size):
        if verbose:
            print "Sending off set count %d..." % set_count
        cur.callproc(stored_proc, input_set)
        set_count += 1

    if verbose:
        print "Committing..."
    con.commit()

    if verbose:
        print "Closing db connection..."
    con.close()
    
if __name__ == '__main__':
    main()
