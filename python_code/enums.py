#!/usr/bin/env python
# encoding: utf-8
"""
FieldGrouping.py

Created by Doug Wendel on 2010-09-24.
An "enum" for listing out the various field groupings rathern than referring
to them by an index.
"""
import os

class FieldGrouping:
    sra_submission_level = -8
    sra_study_level = -7
    sra_experiment_level = -5
    sra_sample_level = -6
    study_level = -3
    sample_level = -2
    prep_level = -1

class DataAccessType:
    qiime_production = 1
    qiime_test = 2
    
class ServerConfig:
    
    config_fp='/home/wwwdevuser/qiime_web.conf'
    
    filefp=open(config_fp).read().split('\n')
    config_options={}
    for line in filefp:
        if line != '':
            key,val=line.strip().split('=')
            config_options[key]=val
        
    data_access_type = eval(config_options['data_access_type'])
    home = config_options['home']

