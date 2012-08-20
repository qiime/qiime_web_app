.. _check_fasta:

Check FASTA
--------------
The processing protocal permits the user to upload FASTA-formatted files (with the extension of ".fna" or ".fasta"). Normally, users submitting FASTA files do not have access to the raw data from their study, such as the case where a sequencing center only sends them demultiplexed data. Another case is where a user performs their own filtering of the data (i.e. human-screening, quality filtering, assembly of the sequences, etc.), which normally happens for metagenomic sequences, but is not limited to metagenomic sequences. In the case that a user uploads a FASTA file, you need to make sure that the PLATFORM is **FASTA**. I suggest adding another column called "sequencing_technology", so the user can define the original sequencing method (e.g. FLX, Titanium, etc.).

Common Problems
^^^^^^^^^^^^^^^^^
The most common problems encountered with FASTA files has to do with the formatting of the supplied files. The DB is expecting a sequence file formatted similar to the output of `split_libraries.py <http://qiime.org/documentation/file_formats.html#demultiplexed-sequences>`_.

Expected
**********
Here is an example of a normal post-split-libraries FASTA-formatted file:

::

   >PC.634_1 FLP3FBN01ELBSX orig_bc=ACAGAGTCGGCT new_bc=ACAGAGTCGGCT bc_diffs=0
   CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTTACCCTCTCAGGCCGGCTACGCATCATCGCCTTGGTGGGCCGTT
   >PC.634_2 FLP3FBN01EG8AX orig_bc=ACAGAGTCGGCT new_bc=ACAGAGTCGGCT bc_diffs=0
   TTGGACCGTGTCTCAGTTCCAATGTGGGGGCCTTCCTCTCAGAACCCCTATCCATCGAAGGCTTGGTGGGCCGTTA
   >PC.354_3 FLP3FBN01EEWKD orig_bc=AGCACGAGCCTA new_bc=AGCACGAGCCTA bc_diffs=0
   TTGGGCCGTGTCTCAGTCCCAATGTGGCCGATCAGTCTCTTAACTCGGCTATGCATCATTGCCTTGGTAAGCCGTT
   >PC.481_4 FLP3FBN01DEHK3 orig_bc=ACCAGCGACTAG new_bc=ACCAGCGACTAG bc_diffs=0
   CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTCAACCTCTCAGTCCGGCTACTGATCGTCGACTTGGTGAGCCGTT

Problem
***********
If the end-user did not use QIIME for demultiplexing, they may supply their own per sample files, which contain the SampleID (e.g.,  :file:`USinfTw1.2.HumScreened.fna`) where the contents of the file may look like the following. It should be noted that this file will not be processed correctly using the DB and usually throws a **Key Error** since the Sequence Names do not match SampleIDs within the DB:

::

   >GQTMT4O02FR567
   ATACCCGATCTTGTCCAGGCCCGCCTTGATTTCTTCCCATTCATTGCGCTTGGGGTTCAGTGCAACGACCAGTTCTTTTG
   TTACCGGCCCCCATCAGCAAGCTGGCGCACAGCCTCCAAAGGCAGGTCTGCTGGGTAAAACCACTTTCCATACTTCACAT
   AGGTCTGTGGATTGCCATCAATCGTGGTGAGCAGATCCTTGGATGCATCCTCGCCGTCCATGGGATTGCAGTTCCAGGTG
   GTGCCATCTTCCGTCCAGACGCAGAAGGTGCTTTTCATCTTTTTGACTTCACGGCTGCCCATGAGTTTTTGCAAAGCAGG
   GGGCATCCCATCTGTCAGGTCTTCGATACGGGGAAGTTTTGCCTCCAGTCGTAGAGTTCAGAATCCACGCCGTTAATCAC
   ACAGCCTTCGGGCGCGAATAGGACAATCATACTCTGGTCGCTACCATCGGTGGCAAAGAATGACCTCTTG
   >GQTMT4O02F70CD
   CTTCCCATTCATTGCGCTTGGGGTTCAGTGCAACGACCAGTTCTTTTGTTACCGGCCCCCATCAGCAAGCTGGCGCACAG
   CCTCCAAAGGCAGGTCTGCTGGGTAAAACCACTTTCCATACTTCACATAGGTCTGTGGATTGCCATCAATCGTGGTGAGC
   AGATCCTTGGATGCATCCTCGCCGTCCATGGGATTGCAGTTCCAGGTGGTGCCATCTTCCGTCCAGACGCAGAAGGTGCT
   TTTCATCTTTTTGACTTCACGGCTGCCCATGAGTTTTTGCAAAGCAGGGGGCATCCCATCTGTCAGGTCTTCGATACGGG
   GAAGTTTTGCCTCCCAGTCGTAGAGTTCAGAATCCACGCCGTTAATCACACA

Solution 1
**************
When coming across this scenario for the first time, your best solution is to email the person uploading the files and ask them to properly format their FASTA files, so the DB can process them correctly. You can point them to the following location for formatting details `Demultiplexed Sequence Formats <http://qiime.org/documentation/file_formats.html#demultiplexed-sequences>`_. If this is too difficult for the end-user, then you may need write a script for properly formatting the data, such as the example in :ref:`check_fasta_sol_2`. Sometimes you will find that it is easier to do this for the end-user than spending lots of time discussing how they should properly format their data.

.. _check_fasta_sol_2:

Solution 2
**************
For this particular case, you may need to write a script that uses the filename as the Sequence Name and then you should also have an iterator to distinguish each sequence.

Here is an code-sample used for one of the cases that I have run into, where the Sequence Names are not properly formatted within the FASTA file. For this particular case, you should notice that there is a sequence file for each sample in the study. First, I move all the uploaded FASTA files into another directory :file:`orig_fa_files`. The filenames (e.g. :file:`USinfTw1.2.HumScreened.fna`) should contain the SampleIDs (i.e., USinfTw1.2) and sometimes has extra information which needs to be filtered off (i.e., HumScreened.fna) when writing the Sequence Names. Make sure that the original filenames are maintained since the RUN_PREFIX will need to be changed if you modify filenames. This particular script was run within **Yatsunenko_global_gut_metagenome** folder :file:`/home/wwwuser/user_data/studies/study_621`:

::

    # import python libraries
    from os import listdir
    from cogent.parse.fasta import MinimalFastaParser
    from os.path import splitext,split,join
    
    # define location of uploaded fasta files
    original_fasta_dir = './orig_fa_files'
    for i in listdir(original_fasta_dir):
        # get filename
        fname,fext=splitext(i)
        
        # parse sequence file
        old_fna=MinimalFastaParser(open(join(original_fasta_dir,i),'U'))
        
        # open a new file for writing in cwd
        new_fname=open(fname+'.fna','w')
        
        # define iterator
        num=0
        for seq_name,old_seq in old_fna:
            # get the SampleID
            sample_name='.'.join(fname.split('.')[:-1])
            
            # write new FASTA-formatted file with SampleIDs
            new_fname.write('>%s\n%s\n' % (sample_name+'_'+str(num),old_seq))
            
            # iterate
            num=num+1
            
        # close new file 
        new_fname.close()


The result should look as follows:

::

    >USinfTw1.2_0
    ATACCCGATCTTGTCCAGGCCCGCCTTGATTTCTTCCCATTCATTGCGCTTGGGGTTCAGTGCAACGACCAGTTCTTTTG
    TTACCGGCCCCCATCAGCAAGCTGGCGCACAGCCTCCAAAGGCAGGTCTGCTGGGTAAAACCACTTTCCATACTTCACAT
    AGGTCTGTGGATTGCCATCAATCGTGGTGAGCAGATCCTTGGATGCATCCTCGCCGTCCATGGGATTGCAGTTCCAGGTG
    GTGCCATCTTCCGTCCAGACGCAGAAGGTGCTTTTCATCTTTTTGACTTCACGGCTGCCCATGAGTTTTTGCAAAGCAGG
    GGGCATCCCATCTGTCAGGTCTTCGATACGGGGAAGTTTTGCCTCCAGTCGTAGAGTTCAGAATCCACGCCGTTAATCAC
    ACAGCCTTCGGGCGCGAATAGGACAATCATACTCTGGTCGCTACCATCGGTGGCAAAGAATGACCTCTTG
    >USinfTw1.2_1
    CTTCCCATTCATTGCGCTTGGGGTTCAGTGCAACGACCAGTTCTTTTGTTACCGGCCCCCATCAGCAAGCTGGCGCACAG
    CCTCCAAAGGCAGGTCTGCTGGGTAAAACCACTTTCCATACTTCACATAGGTCTGTGGATTGCCATCAATCGTGGTGAGC
    AGATCCTTGGATGCATCCTCGCCGTCCATGGGATTGCAGTTCCAGGTGGTGCCATCTTCCGTCCAGACGCAGAAGGTGCT
    TTTCATCTTTTTGACTTCACGGCTGCCCATGAGTTTTTGCAAAGCAGGGGGCATCCCATCTGTCAGGTCTTCGATACGGG
    GAAGTTTTGCCTCCCAGTCGTAGAGTTCAGAATCCACGCCGTTAATCACACA

