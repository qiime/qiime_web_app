.. _essential_files:

===========
Input Files
===========

What Files Do I Need?
---------------------

1. FASTA file(s) (.fna or .fasta)
2. Basepair list (.txt) - Optional
3. Feature List (.txt) - Optional


File Format Details
-------------------

These are general guidelines that apply to multiple files:

1. Files should have proper file type suffix: E.g. '.fna' or '.fasta' for FASTA files, '.txt' for basepair and feature lists
2. Do not use spaces in the filename. Use underscores or MixedCase instead. For example: :file:`some RNA.fna` is not allowed, should be :file:`some_RNA.fna` or :file:`SomeRNA.fna`

FASTA File (.fna or .fasta)
^^^^^^^^^^^^^^^^^
The following shows 6 lines from a FASTA file.  The two lines contain the secondary structure mask, where the sequence name must be "#=GC SS_cons" or else some functionality of Boulder ALE may not work properly. 
::

    >#=GC SS_cons
    ..(((((((..((((...........)))).(((((.......))))).....(((((.......))))))))))))....
    >1N77_C
    --GGCCCCAUCGUCUAGC--GGUU-AGGACGCGGCCCUCUCAAGGCCGAAA-CGGGGGUUCGAUUCCCCCUGGGGUCACCA
    >Aquifex_aeolicus|GE0001391.GluUUC
    GCCCCCGUCGUCUAG--CCUGGCCUAGGACGCCGGCCUUUCACGCCGGAAA-CGCGGGUUCAAAUCCCGCCGGGGGUGCCA
    

Basepair List (.txt) - Optional
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The basepair list is a tab-delimited list of nucleotide positions (NT1 and NT2 in first two columns) followed by the basepair family, which is based on the Leontis-Westhof basepair classification.  Users can download a list of basepairs for their favorite PDB structure from the FR3D website `FR3D website <http://rna.bgsu.edu/FR3D/>`_

::

    0	70	cWW
    1	69	cWW
    2	68	cWW
    3	67	cWW
    4	66	cWW
    5	65	cWW
    6	64	cWW
    7	13	tWH
    7	20	tsS

Feature List (.txt) - Optional
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The feature list is a list of features that the user wants to map onto the alignment.  This will allow the user to color and collapse (vertically) regions of the alignment based on the feature. The feature list is a tab-delimited list where the columns are as follows: 

1) Reference Sequence 
2) Level of Description (set to 1) 
3) Region (broad definition i.e. stem or loop)
4) Region (narrow definition i.e. D_loop, T_stem, etc.)
5) Nucleotide range. If involves two stretches of nts, use a colon ":" delimiter.

::

    1N_77   1   stem    Acceptor_stem   0-6:64-70
    1N_77   1   stem    D_stem          9-12:21-24
    1N_77   1   loop    D_loop          13-20
    1N_77   1   stem    Anti-Codon_stem 25-30:38-43
    1N_77   1   loop    Anti-Codon_loop 31-37
    1N_77   1   loop    Variable_loop   44-46
    1N_77   1   stem    T_stem          47-51:59-63
    1N_77   1   loop    T_loop          52-58
    1N_77   1   loop    CCA_tail        72-74