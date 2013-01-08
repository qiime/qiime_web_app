from string import strip

def MinimalConvertedFastqFastaParser(infile):
    """ Internal function for yielding 2 lines of file at a time 

    This parser handles the case in which split_libraries has already
    produced a FASTA formatted file from illumina data. Quality scores
    in files produced this way can begin with the normally reserved 
    character of ">". This parser simply reads pairs of rows and assumes
    that the first is the label and second is the sequence.
    """
    count = 0
    for line in infile:
        strip(line)
        # First row of pair is always the label
        if count == 0:
            label = line[1:].strip()
            count += 1
        elif count == 1:
            seq = line.strip()
            count = 0
            yield label, seq