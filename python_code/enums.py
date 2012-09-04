#!/usr/bin/env python
# File created on 19 Apr 2011
from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2012, The QIIME-webdev project"
__credits__ = [" Doug Wendel","Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
"""
FieldGrouping.py

Created by Doug Wendel on 2010-09-24.
An "enum" for listing out the various field groupings rathern than referring
to them by an index.
"""
import os
import getpass

class FieldGrouping:
    """ this is the metadata field groupings
    """

    emp_level = -11
    mims_prep = -10
    mimarks_prep = -9
    sra_submission_level = -8
    sra_study_level = -7
    sra_experiment_level = -5
    sra_sample_level = -6
    study_level = -3
    sample_level = -2
    prep_level = -1

class DataAccessType:
    """ this is the two types of data access connections
    """
    
    qiime_production = 1
    qiime_test = 2
    
class ServerConfig:
    """ this is the cluster's server configuration to determine if it is a 
        production or development server
    """
    
    # define the filepath to the server configuration
    config_fp='/home/%s/qiime_web.conf' % getpass.getuser()
    
    # convert text file into dictionary
    filefp=open(config_fp).read().split('\n')
    config_options={}
    for line in filefp:
        if line != '':
            key,val=line.strip().split('=')
            config_options[key]=val
    
    # using eval is not a good thing to do
    data_access_type = eval(config_options['data_access_type'])
    home = config_options['home']

