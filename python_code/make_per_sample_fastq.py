#!/usr/bin/env python

from collections import defaultdict
from os.path import join, exists
from os import mkdir
from gzip import open as gz_open

import click
from skbio.parse.sequences.fastq import parse_fastq
from skbio.format.sequences.fastq import format_fastq_record

def split_helper(input_fastq, output_directory, sequence_buffer_size=1000,
                 gzip=True):
    """Splits a demultiplexed FASTQ file into per-sample FASTQ files

    Parameters
    ----------
    input_fastq : file
        The input demultiplexed FASTQ file.
    output_directory : str
        Path to the output directory. It will be created if it does not already
        exist.
    sequence_buffer_size : int
        The number of sequences to hold in memory for each sample before
        writing them to disk.
    gzip : bool, optional
        If ``True``, then the generated FASTQ files will be gzipped

    Notes
    -----
    The sequence identifiers in `input_fastq` should be of the form output by
    QIIME's demultiplexing scripts; namely, they should be:
    ``SampleID_SequenceNumber And Additional Notes if Applicable``
    """
    if not exists(output_directory):
        mkdir(output_directory)

    per_sample_seqs = defaultdict(list)
    per_sample_counts = defaultdict(int)
    unique_filepaths = set()
    for defline, seq, qual in parse_fastq(input_fastq,
                                          enforce_qual_range=False):
        label = defline.split()[0]
        sample_name, sequence_number = label.rsplit('_', 1)

        per_sample_seqs[sample_name].append((defline, seq, qual))
        per_sample_counts[sample_name] += 1

        if per_sample_counts[sample_name] > sequence_buffer_size:
            output_filepath = join(output_directory, sample_name+'.fastq')
            unique_filepaths.add(output_filepath)
            with open(output_filepath, 'a') \
                    as outfile:
                outfile.write(
                    format_fastq_record(*per_sample_seqs[sample_name]))

            per_sample_seqs[sample_name] = []
            per_sample_counts[sample_name] = 0
    
    for sample_name, entries in per_sample_seqs.iteritems():
        if not entries:
            continue

        output_filepath = join(output_directory, sample_name+'.fastq')
        unique_filepaths.add(output_filepath)
        with open(output_filepath, 'a') \
                as outfile:
            outfile.write(
                format_fastq_record(*per_sample_seqs[sample_name]))

    if gzip:
        pass

@click.group()
def cli():
    pass

@cli.command()
@click.option('--input-fastq', required=True, type=click.File('r'))
@click.option('--sequence-buffer-size', default=1000)
@click.option('--output-directory', required=True, type=str)
@click.option('--gzip/--no-gzip', default=True)
def split(input_fastq, output_directory, sequence_buffer_size,
          gzip):
    split_helper(input_fastq, output_directory, sequence_buffer_size,
                 gzip)

if __name__ == '__main__':
    cli()
