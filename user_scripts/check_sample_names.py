#/usr/bin/env python

from re import findall
from inspect import getfile, currentframe
file_name = getfile(currentframe())

if __name__ == '__main__':
    """The best way to use this script (assuming you're copying and pasting
    from the QIIME DB website) is to do python -i {file_name}

    and then from within the interpreter paste the sample names into a
    variable, splitlines, and then pass that variable to the function
    erroneous_sample_names.

    example:

        python -i {file_name}
        >>> l = '''Cassowary.24664.624238   n   None    Metcalf_16sV4_DecompMaterialV4_71712_NoIndex_L007_R1_001    Coming soon...
        ... ExBk6.2.5X.624219   n   None    Metcalf_16sV4_DecompMaterialV4_71712_NoIndex_L007_R1_001    Coming soon...
        ... Extr.neg.MX.624213  n   None    Metcalf_16sV4_DecompMaterialV4_71712_NoIndex_L007_R1_001    Coming soon...'''
        >>> l = l.splitlines()
        >>> erroneous_sample_names(l)
        False
        >>>

    """.format(file_name=file_name)

def erroneous_sample_names(samples, sample_id_column=0, expected_num_cols=5):
    """Validates a set of sample names.

    Takes a list of samples and validates the sample id's (ensures they have
    only alphanumeric characters and periods).

    Returns False if no offending sample names are present, or L if at least
    one invalid entry is found, where L is a list of offending indices in the
    input list.
    """
    # keeps track of which samples failed
    fails = []

    # enumerate the samples so we can keep track of which ID's caused errors
    for i, sample in enumerate(samples):
        cols = sample.split('\t')

        # there should be 5 columns, unless something changes (just the
        # required columns); if not, fail
        if len(cols) != expected_num_cols:
            fails.append(i)
            continue

        # isolate the sample_id to check it for improper characters
        sample_id = cols[sample_id_column]

        # use this regular expression to search for characters that are
        # NOT alphanumeric or a period
        result = findall('[^a-zA-Z0-9\.]', sample_id)

        # if any are found, fail
        if result:
            fails.append(i)
            continue

    # if there are any fails, return them
    # otherwise return False
    if fails:
        return fails
    else:
        return False
