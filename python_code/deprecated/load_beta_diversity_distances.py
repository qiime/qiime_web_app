#!/usr/bin/env python
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

import time 
from subprocess import Popen, PIPE, STDOUT
from qiime.parse import parse_distmat
from cogent.util.misc import app_path
from cogent.app.util import ApplicationNotFoundError
import re
from random import choice
from datetime import datetime
from time import strftime
from os.path import *
from qiime.parse import fields_to_dict
from qiime.util import (compute_seqs_per_library_stats, 
                        get_qiime_scripts_dir,
                        create_dir)
from wrap_files_for_md5 import MD5Wrap
from load_tab_file import input_set_generator, flowfile_inputset_generator, \
                            fasta_to_tab_delim


  
def load_bdiv_distances(data_access,bdiv_fpath):
    '''
       This function takes the fasta filenames and using that path, determines
       the location of the split-library and picked-otu files.  Once file
       locations have been determined, it moves the files to the DB machine
       and load the files into the DB.
    '''
    samples, distmtx=parse_distmat(open(bdiv_fpath,'U'))
    
    input_fname, input_ext = splitext(split(bdiv_fpath)[-1])
    file_split_name=input_fname.split('_')
    metric_used='_'.join(file_split_name[0:2])
    rarefied=file_split_name[-1].strip('even')
    data_to_load=[]
    sample_1_and_2=[]
    for i,samp1 in enumerate(samples):
        for j,samp2 in enumerate(samples[:i+1]):
            data_to_load.append('\t'.join(list((samples[i],samples[j],str(distmtx[i,j]),metric_used,str(rarefied)))))
            
    
    ''' 
    The output values and types for each value are as follows:
    0: sample id 1 (text)
    1: sample id 2 (text)
    2: distance (number)
    3: metric (text)  
    4: rarefied at (integer)
    '''
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    types = ['s','s', 'bf', 's', 'i']

    iterator=0
    for res in input_set_generator(data_to_load, cur, types,5000):
        print 'running %i' % (iterator)
        iterator=iterator+1
        valid = data_access.loadBetaDivDistances(True, res)
        if not valid:
            raise ValueError, 'Error: Unable to load beta-diversity file into database!'

    print 'Finished loading beta_diversity distances!' 
