#!/usr/bin/env python
# File created on 27 Jul 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "QIIME-webdev"
__credits__ = ["Jesse Stombaugh","Daniel McDonald", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"


from cogent.util.misc import unzip
from cx_Oracle import NUMBER, STRING, DATETIME, CLOB
from numpy import average
from cogent.parse.flowgram_parser import lazy_parse_sff_handle
from datetime import datetime

type_lookup_oracle = {'i':NUMBER,'f':NUMBER,'s':STRING, 'd':DATETIME, 'c':CLOB}
def unzip_and_cast_to_cxoracle_types(data, cursor, types, \
        type_lookup=type_lookup_oracle):
    """Unzips data and casts each field to the corresponding oracle type

    data - a list or tuple of lists or tuples

    types - a list of 'i', 's', 'f' for int, string or float
    """
    res = []
    for t,f in zip(types, unzip(data)):
        if t == 'i':
            tmp = map(int, f)
        elif t == 'f':
            tmp = map(float, f)
        # yes, this method is absolutely fucking ugly right now
        elif t == 'c':
            clob = cursor.var(CLOB)
            all_strings = '@'.join(f)
            all_strings_splits = [i+1 for i,s in enumerate(all_strings) if s == '@']
            all_strings_splits.append(len(all_strings))
            clob.setvalue(0,all_strings)
            res.append(clob)
            res.append(cursor.arrayvar(type_lookup['i'], all_strings_splits))
            continue
        else:
            tmp = f
        res.append(cursor.arrayvar(type_lookup[t], tmp))
    return res 

def input_set_generator(data, cursor, types, buffer_size=10000, 
        type_lookup=type_lookup_oracle, delim='\t'):
    """yields data parsed into oracle types in buffer_size rows at a time"""
    buffer = []
    for line in data:
        if line.startswith('#'):
            continue

        buffer.append(line.strip().split(delim))
        if len(buffer) >= buffer_size:
            res = unzip_and_cast_to_cxoracle_types(buffer, cursor, types, type_lookup)
            buffer = []
            yield res

    if buffer:
        res = unzip_and_cast_to_cxoracle_types(buffer, cursor, types, type_lookup)
        yield res

def fasta_to_tab_delim(data):
    """Yields FASTA files in tab delim format

    Will strip off comments. For instance, the following file

    >foo bar
    attatatatggcca
    ...

    will result in a record:

    foo\tattatatatggcca
    """
    to_yield = []
    seq_string = ''
    for line in data:
        if line.startswith('>'):
            if seq_string:
                to_yield.append(seq_string)
                seq_string = ''
                yield '\t'.join(to_yield)
                to_yield = []

            items = line[1:].split(' ')
            id_ = items[0]

            if '=' in items[1]:
                length_ = items[1].split('=')[1]
            else:
                length_ = 'N/A'

            id_ = line[1:].split()[0]
            to_yield.append(id_)
            to_yield.append(length_)
        else:
            seq_string += line.strip()
            #to_yield.append(line)
            #yield '\t'.join(to_yield)
            #to_yield = []
    if to_yield and seq_string:
        to_yield.append(seq_string)
        yield '\t'.join(to_yield)

truncate_flow_value_f = lambda x: "%0.2f" % x
def unzip_flow(flow, seq_run_id, file_md5):
    """Returns tuple of the fields we care about"""
    res = [seq_run_id]

    res.append(getattr(flow,'Name'))
    res.append(getattr(flow,'Bases'))
    res.append(int(getattr(flow, '# of Bases')))
    res.append(getattr(flow,'Run Name', file_md5))

    run_date_raw = getattr(flow, 'Run Prefix')
    datetime_raw = map(int, run_date_raw.split('_')[1:-1])
    run_date = datetime(*datetime_raw)

    res.append(run_date)
    res.append(int(getattr(flow,'Region #')))

    xy_location = getattr(flow, 'XY Location')
    x,y = xy_location.split('_')

    res.append(int(x))
    res.append(int(y))
    res.append('\t'.join(map(truncate_flow_value_f,flow.flowgram)))
    res.append(getattr(flow,'Flow Indexes'))
    res.append(int(getattr(flow,'Clip Qual Left')))
    res.append(int(getattr(flow,'Clip Qual Right')))
    res.append(int(getattr(flow,'Clip Adap Left')))
    res.append(int(getattr(flow,'Clip Adap Right')))
   
    qual = getattr(flow, 'Quality Scores')
    qual_values = map(int,qual.split('\t'))
    
    res.append(min(qual_values))
    res.append(max(qual_values))
    res.append(average(qual_values))
    res.append(qual)

    return res

def flowfile_inputset_generator(data, cursor, seq_run_id, file_md5, \
        buffer_size=1000, type_lookup=type_lookup_oracle):
    """Yields buffer_size tuples of flowgram data
    
    data : 
    """
    table_types = ['i', # SEQ_RUN_ID
                   's', # READ_ID
                   's', # READ_SEQUENCE
                   'i', # READ_SEQUENCE_LENGTH
                   's', # RUN_NAME
                   'd', # RUN_DATE
                   'i', # REGION
                   'i', # X_LOCATION
                   'i', # Y_LOCATION
                   'c', # FLOWGRAM_STRING
                   'c', # FLOW_INDEX_STRING
                   'i', # CLIP_QUAL_LEFT
                   'i', # CLIP_QUAL_RIGHT
                   'i', # CLIP_ADAP_LEFT
                   'i', # CLIP_ADAP_RIGHT
                   'i', # QUAL_MIN
                   'i', # QUAL_MAX
                   'f', # QUAL_AVG
                   'c'] # QUAL_STRING

    flow_generator, header = lazy_parse_sff_handle(data)

    buffer = []
    buffer_count = 0

    for flow in flow_generator:
        flow_data = unzip_flow(flow, seq_run_id, file_md5)
        
        buffer.append(flow_data)
        buffer_count += 1    

        if buffer_count >= buffer_size:
            res = unzip_and_cast_to_cxoracle_types(buffer, cursor, table_types, \
                                                   type_lookup)
            buffer = []
            buffer_count = 0
            yield res

    if buffer_count:
        res = unzip_and_cast_to_cxoracle_types(buffer, cursor, table_types, \
                                               type_lookup)
        buffer = []
        buffer_count = 0
        yield res
