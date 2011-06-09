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
from numpy import average
from cogent.parse.flowgram_parser import lazy_parse_sff_handle
from datetime import datetime
from hashlib import md5

try:
    from cx_Oracle import NUMBER, STRING, DATETIME, CLOB,FIXED_CHAR,NATIVE_FLOAT
    type_lookup_oracle = {'i':NUMBER,'f':NUMBER,'s':STRING, 'd':DATETIME, 'c':CLOB,'fc':FIXED_CHAR,'bf':NATIVE_FLOAT}
except ImportError:
    print "Cannot import cx_Oracle"
    type_lookup_oracle = {}
    pass
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
        elif t == 'f'  or t == 'bf' :
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

def fasta_to_tab_delim(data, seq_run_id,split_library_run_id):
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
                to_yield.append(str(len(seq_string)))
                to_yield.append(md5(seq_string).hexdigest())
                to_yield.append(seq_string)
                yield '\t'.join(to_yield)
                seq_string = ''
                to_yield = []

            items = line[1:].split(' ')
            sample_id = items[0]
            read_id = items[1]
            orig_bc = ''
            new_bc = ''
            bc_diffs = '0'
            
            if len(items) > 2 and '=' in items[2]:
                orig_bc = items[2].split('=')[1]
                            
            if len(items) > 3 and '=' in items[3]:
                new_bc = items[3].split('=')[1]
            
            if len(items) > 4 and '=' in items[4]:
                bc_diffs = items[4].split('=')[1]
                
            to_yield.append(str(split_library_run_id))
            to_yield.append(str(seq_run_id))
            to_yield.append(sample_id)

            barcode_read_group_tag = sample_id.rfind('_')
            if barcode_read_group_tag > 0:
                barcode_read_group_tag = sample_id[0:sample_id.rfind('_')]
            else:
                barcode_read_group_tag = sample_id
            to_yield.append(barcode_read_group_tag)

            to_yield.append(read_id)
            to_yield.append(orig_bc)
            to_yield.append(new_bc)
            to_yield.append(bc_diffs)
        else:
            seq_string += line.strip()
    
    if to_yield and seq_string:
        to_yield.append(str(len(seq_string)))
        to_yield.append(md5(seq_string).hexdigest())
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
