#!/usr/bin/env python

from sys import argv
from cogent.util.misc import unzip
import cx_Oracle

def unzip_and_cast_to_cxoracle_types(data, cursor):
    ids,acc,dec,coreset,seq,checksum = unzip(data)
    ids = cursor.arrayvar(cx_Oracle.STRING, ids)
    acc = cursor.arrayvar(cx_Oracle.STRING, acc)
    dec = cursor.arrayvar(cx_Oracle.STRING, dec)
    coreset = cursor.arrayvar(cx_Oracle.NUMBER, map(int, coreset))
    seq = cursor.arrayvar(cx_Oracle.STRING, seq)
    checksum = cursor.arrayvar(cx_Oracle.FIXED_CHAR, checksum)
    return ids,acc,dec,coreset,seq,checksum

def input_set_generator(data, cursor):
    buffer = []
    redundant_buffer = []
    buffer_hashes = set([])
    for line in data:
        if line.startswith('#'):
            continue
        fields = line.strip().split('\t')
        if fields[-1] in buffer_hashes:
            redundant_buffer.append(fields)
        else:
            buffer_hashes.add(fields[-1])
            buffer.append(fields)
        if len(buffer) > 500:
            res = unzip_and_cast_to_cxoracle_types(buffer, cursor) 
            buffer = []
            buffer_hashes = set([])
            yield res

            if redundant_buffer:
                res = unzip_and_cast_to_cxoracle_types(redundant_buffer,cursor) 
                redundant_buffer = []
                yield res


    if buffer:
        res = unzip_and_cast_to_cxoracle_types(buffer, cursor) 
        yield res
    if redundant_buffer:
        res = unzip_and_cast_to_cxoracle_types(redundant_buffer, cursor) 
        yield res

def main():
    lines = open(argv[1])
    con = cx_Oracle.connect(user='SFF',
                            password='SFF454SFF',
                            dsn='webdev.microbio.me:1521/dbdev')
    cur = con.cursor()
    ref_set_id = 7 #cur.var(cx_Oracle.NUMBER, 7)
    for input_set in input_set_generator(lines, cur):
        ids,acc,dec,coreset,seq,checksum = input_set
        print 'would execute'
        cur.callproc('load_gg_seq_data_package.array_insert',[ref_set_id, ids, acc, dec, coreset,seq, checksum])

if __name__ == '__main__':
    main()
