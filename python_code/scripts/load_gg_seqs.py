#!/usr/bin/env python

from sys import argv
from cogent.util.misc import unzip
import cx_Oracle

def unzip_and_cast_to_cxoracle_types(data, cursor):
    ids,acc,dec,coreset,seq,checksum = unzip(data)
    ids = cursor.arrayvar(cx_Oracle.NUMBER, map(int, ids))
    acc = cursor.arrayvar(cx_Oracle.STRING, acc)
    dec = cursor.arrayvar(cx_Oracle.STRING, dec)
    coreset = cursor.arrayvar(cx_Oracle.NUMBER, map(int, coreset))
    seq = cursor.arrayvar(cx_Oracle.STRING, seq)
    checksum = cursor.arrayvar(cx_Oracle.STRING, checksum)
    return ids,acc,dec,coreset,seq,checksum

def input_set_generator(data, cursor):
    buffer = []
    for line in data:
        if line.startswith('#'):
            continue
        buffer.append(line.strip().split('\t'))

        if len(buffer) > 500:
            res = unzip_and_cast_to_cxoracle_types(buffer, cursor) 
            buffer = []
            yield res

    if buffer:
        res = unzip_and_cast_to_cxoracle_types(buffer, cursor) 
        yield res

def main():
    lines = open(argv[1])
    con = cx_Oracle.connect(user='SFF',
                            password='SFF454SFF',
                            dsn='quarterbarrel.microbio.me:1521/qiimedb.microbio.me')
    cur = con.cursor()
    ref_set_id = 7 #cur.var(cx_Oracle.NUMBER, 7)
    for input_set in input_set_generator(lines, cur):
        ids,acc,dec,coreset,seq,checksum = input_set
        print 'would execute'
        cur.callproc('load_gg_seq_data_package.array_insert',[ref_set_id, ids, acc, dec, coreset,seq, checksum])

if __name__ == '__main__':
    main()
