#!/usr/bin/env python
# encoding: utf-8
"""
denormalizer.py

Created by Doug Wendel on 2010-04-08.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os


def main(study_metadata, sample_metadata, prep_metadata, output):
    # Open the new file for writing
    output_file = None
    try:
        output_file = open(output, 'w')
    except:
        print 'Could not open the output file for writing.'
        return
        
    # Start reading through 

if __name__ == '__main__':
    from sys import argv
    # Do some error checking here
    study_metadata = argv[1]
    sample_metadata = argv[2]
    prep_metadata = argv[3]
    output = argv[4]
    
    try:
        study_metadata_file = open(study_metadata)
        sample_metadata_file = open(sample_metadata)
        prep_metadata_file = open(prep_metadata)
        main(study_metadata_file, sample_metadata_file, prep_metadata_file)
    except:
        print 'Could not find one more more of the specified files.\n\n'
        print 'Usage: python denormalizer.py study.xls sample.xls prep.xls output.xls'
    finally:
        if study_metadata_file
            study_metadata_file.close()
        if sample_metadata_file
            sample_metadata_file.close()
        if prep_metadata_file
            prep_metadata_file.close()
    
    
    
