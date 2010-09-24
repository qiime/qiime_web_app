#!/usr/bin/env python
# encoding: utf-8
"""
FieldGrouping.py

Created by Doug Wendel on 2010-09-24.
An "enum" for listing out the various field groupings rathern than referring
to them by an index.
"""

class FieldGrouping:
    sra_submission_level = -8
    sra_study_level = -7
    sra_sample_level = -5
    sra_experiment_level = -6
    study_level = -3
    sample_level = -2
    prep_level = -1
