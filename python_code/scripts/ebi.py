#!/usr/bin/env python

from logging import logger

import click

from data_access_connections import data_access_factory
from enums import ServerConfig

# check sequence files
#     check md5s (actually correctly)
# generate metadata files
# send sequence files
# send metadata

@click.command()
@click.option('--study-id', required=True, type=int)
@click.option('--sequence-file', required=True, type=click.File('r'))
@click.option('--mapping-file', required=True, type=click.File('r'))
@click.option('--validate-md5/--no-validate-md5', required=False)
def validate_sample(study_id, sequence_file, mapping_file, validate_md5):
    pass

@click.command()
@click.option('--study-id', required=True, type=int)
@click.option('--sequence-file', required=True, type=click.File('r'))
@click.option('--mapping-file', required=True, type=click.File('r'))
@click.option('--validate-md5/--no-validate-md5', required=False)
def validate_and_submit_sample(study_id, sequence_file, mapping_file, validate_md5):
    pass

@click.command()
@click.option('--study-id', required=True, type=int)
@click.option('--sequence-file', required=True, type=click.File('r'))
@click.option('--mapping-file', required=True, type=click.File('r'))
@click.option('--validate-md5/--no-validate-md5', required=False)
def update_sample(study_id, sequence_file, mapping_file, validate_md5):
    pass
