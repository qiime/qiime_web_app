.. _check_sff:


Valid SFF and Common Problems
---------------------------------
The processing protocol permits the user to upload SFF files which are generated using Roche's 454 sequencer, however there are 2 chemistries that can be used (either FLX or Titanium). It should be noted that an SFF file is a binary file and **not** a text file, so the files cannot be concatenated. The processing protocol will automatically trim all Titanium SFF files to FLX length. Please be aware that will always happen and if the end-users want to submit their data to a public repository without trimming, we have to do some hacking, which is never a good solution.

Expected
*************
The expected file is a binary file. If you want to check the file for validity, you can run the following command:

:: 

     sffinfo -m GBSTGKY02.sff 
     
This will write out the manifest for the SFF file, which should look something like the following:

:: 

    <manifest>
    <run>
        <run_type>454</run_type>
        <accession_prefix>GBSTGKY02</accession_prefix>
        <run_name>R_2010_02_04_11_42_10_FLX09080420_adminrig_Ley-1-amplicon_Rose-2_2-4-2010</run_name>
        <analysis_name>D_2010_02_07_16_34_48_datarig3_signalProcessingAmplicons</analysis_name>
        <path>/data/R_2010_02_04_11_42_10_FLX09080420_adminrig_Ley-1-amplicon_Rose-2_2-4-2010/D_2010_02_07_16_34_48_datarig3_signalProcessingAmplicons/</path>
      </run>
      <qualityScoreVersion>1.1.03</qualityScoreVersion>
    </manifest>

.. note::
    
    NOTE: If the user wants to merge SFFs, first make sure they are using the same chemistry, then run a command like the following:

:: 

    sfffile sff1.sff sff2.sff
    
This will produce a file named :file:`454Reads.sff`, which can be renamed and used for processing.

Problems
***********
SFF file processing tends to lead to most problems from the perspective of the administrator. The most common problems that arise are: 1) The PLATFORM field in the metadata lists the wrong chemistry, 2) Incorrect Linker/Primers listed in LINKER and PRIMER fields of metadata, 3) Per-sample SFF files supplied

Problem 1 - Platform Incorrectly Defined
******************************************
The problem end-users may have is knowing whether they should put FLX or Titanium as the PLATFORM value and by default they just put one in if they don't know.

Solution
*********
This is a very common problem and the reason for it most of the time is that when a user sequences their data with Titanium chemistry it is often referred to as "FLX with Titanium chemistry", so they put FLX in the field. Another reason may be they don't know the correct chemistry used. I should note that if a user wants their full-length sequences uploaded to the DB, they may put FLX, therefore the trimming is bypassed during the processing protocol. I would not recommend this solution, since the point of the DB is to compare their data with other studies in the DB and it is well-known that the quality of the full-length Titanium reads tend to drop-off after the FLX length. As an administrator, you can check the chemistry of each SFF file by running the following command:

::

    sffinfo GBSTGKY02.sff | head | grep "# of Flows"
    
As a result, you should either see the number 400 (FLX) or 800 (Titanium). Depending on the number of flows, you should verify that the PLATFORM field in the metadata corresponds. To check the metadata field, it is usually easiest to perform an "svn update" and open the prep_template.txt file for the study of interest.


Problem 2 - Incorrect Linker/Primer Defined
***********************************************
Normally you will not catch this error until you actually try processing the study, since you will come across an error similar to the following:

::

    ValueError: Couldn't create OTU table. Is your OTU map empty? Original error message: max() arg is an empty sequence
    
Basically, this error is complaining that none of the sequence successfully hit against the Greengenes 97% sequences. 

Solution
*********
If you look at the :file:`split_library_log.txt` file under the file:`/home/wwwuser/user_data/studies/study_#/processed_*/split_libraries/` directory you will most likely see very few or no sequences made it through split-libraries. If this is the case you will need to verify that the correct linker and primers were supplied. To do this you should first "cd" into the processed directory for the study, then you want to grab a barcode used in that run of the study, as follows:

:: 

    head -n 2 GBSTGKY02__split_libraries_mapping_file.txt
    
This should give you the header and first sample of the mapping file.

::
    
    #SampleID	BarcodeSequence	LinkerPrimerSequence	Description	
    244.141635	ATACTATTGCGC	CATGCTGCCTCCCGTAGGAGT	Succession of microbial consortia in the developing infant gut microbiome	GBSTGKY02
    
Now that you can grab the barcode for the first sample, we want to use that barcode for grepping the input FASTA file for split-libraries as follows:

::

    grep "^ATACTATTGCGC" GBSTGKY02.fna | head
    
This will produce a result similar to this:

::

    [--BARCODE---]{----LINKERPRIMER-----}
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCATCGATAACCGAAATTCTTTAATAATCAAACCATGCGGTCTGATTATACCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCATCGATAACCGAAATTCTTTAATAATAAGACCATGCGGTCTGATTATACCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCATCGATAACCGAAATTCTTTAATAATCAAACCATGCGGTCTGATTATACCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGCCGATCACCCTCTCAGGTCGGCTACTGATCGTCGCCTTGGTAAGCCGTTACCTTACCAACTAGCTAATCAGACGCGGGTCCATCCTGTACTGGCTCACCTTTGATATTCAAGAGATGCCTCTCAAATATATTATCCCGTATTAGCATACCTTTCGGTATGTTATCCGTGTGTACAGGGTAGGTTACCCACGCGTTACTCACCCG
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCATCGATAACCGAAATTCTTTAATAATCAAACCATGCGGTCTGATTATACCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCAACGATAACCGAAATTCTTTAATAATAAGACCATGCGGTCTGATTATACTATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCAT
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}CTGGGCCGTGTCTCAGTCCCAATGTGGCCGTTCATCCTCTCAGACCGGCTACTGATCATCGCCTTGGTGGGCCGTTACCCCTCCAACTAGCTAATCAGACGCAATCCCCTCCTTCAGTGATAGCTTATAAATAGAGGCCACCTTTCATCCATCCTCGATGCCGAGATTGGATCGTATGCGGTATTAGCAGTCGTTTCCAACTGTTGTCCCCCT
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCATCGATAACCGAAATTCTTTAATAACAAGACCATGCGGTCTAATTATACCATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCAT
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGGCCGTGTCTCAGTCCCAATGTGGCCGATCACCCTCTCAGGTCGGCTATGCATCGTGGCCTTGGTGAGCCGTTACCTCACCAACTAGCTAATGCACCGCGGGTCCATCCATCAGCGACACCCGAAAGCGCCTTTCAAATCAAAACCATGCGGTTTTGATTGTTATACGGTATTAGCACCTGTTTCCAAGTGTTATCCCCTTCTGATGGGCAGGTTACCCACGTG
    [ATACTATTGCGC]{CATGCTGCCTCCCGTAGGAGT}TTGGACCGTGTCTCAGTTCCAATGTGGGGGACCTTCCTCTCAGAACCCCTATCCATCGAAGGTTTGGTGAGCCGTTACCTCACCAACTGCCTAATGGAACGCATCCCCATCGATAACCGAAATTCTTTAATAATAAGACCATGCGGTCTGATTATACTATCGGGTATTAATCTTTCTTTCGAAAGGCTATCCCCGAGTTATCGGCAGGTTGGATACGTGTTACTCACCCGTGCGCCGGTCGCCA

For clarity, I have added brackets "[]" to denote the barcode for each sequence and the part that follows the barcode will always be either the LinkerPrimer sequence or just the Primer sequence, denoted with curly-braces "{}". For this particular example, the Linker is "CA" and the Primer is "TGCTGCCTCCCGTAGGAGT". Now, we can check that against what is in the mapping file where we pulled the barcode from.

The exact primers used for each study can vary, however; there are common ones we come across very often.

====== ====== ======================== =====================================================
Region Linker Primer                   Example Studies Using LinkerPrimer Sequence
====== ====== ======================== =====================================================
V1-2   CA     TGCTGCCTCCCGTAGGAGT      *Original FLX Linker/Primer for all our old studies*
V1-2          TGCTGCCTCCCGTAGGAGT      *Gordon Lab Titanium*
V1-3          ATTACCGCGGCTGCTGG        *HMP*
V3-4   CC     GGACTACHVGGGTWTCTAAT     *Gordon Lab Illumina*
V3-4          GGACTACHVGGGTWTCTAAT     *Gordon Lab Illumina*
V3-4          GTGCCAGCMGCCGCGGTAA      *Default now for all our studies including EMP*
V3-5          CCGTCAATTCMTTTRAGT       *HMP*
====== ====== ======================== =====================================================

Problem 3 - Per-Sample SFF Files
***********************************************
The DB can handle per-sample SFF files without any issues, but sometimes the format of the per-sample SFF files are different than normal SFFs. For example, any study following the HMP protocol or SFFs downloaded from SRA tend to be the problematic files. The difference is that in these per-sample SFFs, the barcode is converted from uppercase to lowercase, therefore the normal functionality of process_sff.py will trim off the barcode prior to running split_libraries.py, which means no sequences will match the barcode from the mapping file.

Solution
**********

So far, this has only been an issue for Titanium, which means the protocol is currently under the convert_to_flx functionality. The solution to this problem is that we need to process the SFF without trimming the barcode and/or linkerprimer, using the "--no-trim" option of process_sff.py. Following process_sff.py, we use the clean_fasta.py script in PrimerProspector to convert all bases to uppercase and to trim off tailing N's. Now that we have cleaned up the sequences, we can pass it to split_libraries.py without any issues. There are 2 things the administrator needs to do to have this protocol called. 

Normally you will not catch this error until you actually try processing the study, since you will come across an error similar to the following:

::

    ValueError: Couldn't create OTU table. Is your OTU map empty? Original error message: max() arg is an empty sequence

To check for this, I suggest you run a command similar to the following and determine if the barcode is lowercase:

::

    sffinfo SRR045494.sff | grep "^Bases" | head -n 4
    
This should produce some output like the following, where the first 4 nucleotides are the key sequence "tcag" in lowercase followed by uppercase NT's (barcode and linkerprimer) and ending with lowercase NT's (low-quality):

::

    Bases:	tcagAGCTATCCACGCATGCTGCCTCCCTGNTGCNNNNNCANNGCTncnncngcgcncngncgtgctgngcttccncatgcatcagcgcgaccntcgatccnctcagttttcacactgcttcatggcgaagctgtgcgcttatgcggtattgcacctatttcaaggtgttatcccccagtatcggcaaggttttcccagcgttaactcaaccccg
    Bases:	tcagAGCTATCCACGACATGCTGCCTCCCTGNTGCNNNNNCANNGCAncntcnctcactcggctatgcatcgtcgccttggtaagccattaccttaccaactagctaatgcaccgcgggtccatcctttagcgacagctttcgccgccttttaagcaatgccatgcagctatgtgtanccggtattgcacctgtttccaaagtggtatccccagactttgggcaggttcccag
    Bases:	tcagATTATCGTGCACCATGCTGCCTCCCGTAGGAGTCTGGGCCGTGTCTCAGTCCCATGTGGCCGGTCNCCCNCCTCAggcgggcgtacgcatcgtcgccttcggttgggccgttacccgccaactacgctaactagcgccaatagccatccgtcctaccngttgctttggagtcacttttaacttaacggttcaccatgcagtgtccgtacctatgcgtcttagctagtcttttaccattcgtttanaccccgtgtctccggcaggttactnggttacc
    Bases:	tcagAGCTATCCACGACATGCTGCCTCCCGTAGGAGTCTGGGCCGTATCTCAGTCCCAATGTGGCCGGTCGGTCTCTCAACCCGGCTACCCGTCGTAAGCTTGGTGGGCCGTTACCCCGCCAACTACCTGATGGGCCGCGACCCCATCCCTTACCGTAAAGGCTTTCCCAACCTCTTCATGCGAAGAGACTGGAGTATTCGGTATTAGCACGGCTTTCGCCGAGTTATCCCGAAGTAAGGGGCAGGTTGGTCACGTGTTACTCACCCGTTCGCCACTTTATATCCGGCCGAAACCGGTTTAA

However; if the barcode and linkerprimer is lowercase the result will look more similar to the following, where you can see the "tcag" in lowercase along with several other lowercase NT's following that sequence:

::

    Bases:	tcagacacggacccgtcaattcctttgagtTTCAACCTTGCGGCCGTACTCCCCAGGTGGAATACTTATTGTGTTAACTCCGGCACGGAGGGGTCAGTCCCCCACACCTAGTATTCATCGTTTACGGCGTGGACTACCAGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCGCCTCAGCGTCAGTTAATGTCCAGCAAGCCGCCTTCGCCACTGGTGTTCCTCCTAATATCTACGCATTTTCACCGCTACACTAGGAATTCCGCTTGCCTCTccatcactcaagggagatagtntannnnnnatagtagtagtagtacgtacgtacgtactactactactactactactactctcgtcgtccgtccgtaccgtaccgtaccgtacctaccgtaccgtaccgtaaccgtaacgtacgtaccgtaccgtaccgtaccgtaccgtaccgtaccgtacgtacgtcgtcgtcgtcgtacgtacgtacggtacgtacgttacgttacgtacgtacgtacgtacgtacgtaccgtaccgtaccgtaccgtaccgtacgtacgtacgtaacgtaacgtaacgtaacgtaacgtaaccgtacgtactactacgtacgtcgcgcg
    Bases:	tcagacacggacccgtcaattcctttgagtTTCAACCTTGCGGCCGTACTCCCCAGGCGGGGTACGTTATTGCGTTAACTCCGGCACAGAAGGGGTCGAATCCTCCAACACCTAGTAATCATCGTTTACGGTGTGGACTACCAGGGTATCTAATCCTGTTTGTCTACCCACACTTTCGAGCCTCAGCGTCAGTTGGTGCCCAGTAGGCCGCCTTCGCCACTGGTGTTCCTCCCGATATCTACGCATTCCAccgctacaccgggaattccgcctacctctgcactactcaaagaaaaactaagttttgaaagcagtttatgggttgagcccatagatttctacttccaacttgtcttcccgcctgcgctccctttacacccagtaattccggacaacgcttgtgaccttacgttttaccgcggctgctggcacgtagttagccgtcacttccttgttgggtaccgtcattatccttccccaaacaaacaggagtttacaatccgaagaccttctttcctccacgcggcgtcgctgcatcacggggtttcccccattgtgcaattattcccccactgctgcctccccgtaggctgag
    Bases:	tcagacacggacccgtcaattcatttgagtTTCAACCTTGCGGTCGTACTCCCCAGGTGGATTACTTATTGTGTTAACTGCGGCACTGAAGGGGTCAATCCTCCAACACCTAGTAATCATCGTTTACGGTGTGGACTACCAGGGTATCTAATCCTGTTTGCTACCCACACTTTCGAGCCTCAGCGTCAGTTGGTGCCCAGTAGGCCGCCTTCGCCACTGGTGTTCCTCCCGATATCTACGCATTCCACCGCTACACCGGGAATTCCGCCTACCTCTGCACTACTCAAGAAAAACAGTTTTGAAAGCAGTTTATGGGTTGAGCCCATAGATTTCACTTCCAACTTGTCTTCCCGCCTGCGCTCCCTTTACACCCAGTAATTCCGGACAACGCTTGTGACCTACGTTTTACCGCGGCTGCTGGCACGTAGTTAGCCGGGGCGTTCTTAGTCAGGTACCGTCATTATCTTCCCTGCTGATAGAGCTTTACATACCGAAATACTTCTTCGCTCACGCGACGTCGCTGCATCAGGGTTTCCCCCATTCGTGCAATATTCCCCACTgc
    Bases:	tcagacacggacccgtcaattcctttaagtTTCAACCTTGCGGTCGTACTCCCCAGGTGGATTACTTATTGTGTTAACTGCGGCACTGAAGGGGTCAATCCTCCAACACCTAGTAATCATCGTTTACAGTGTGGACTACCAGGGTATCTAATCCTGTTTGCTACCCACACTTTCGAGCCTCAGCGTCAGTTGGTGCCCAGTAGGCCGCCTTCGCCACTGGTGTTCCTCCCGATATCTACGCATTCCACGCTACACCGGGAATTCCGCCTACCTCTGCACTACTCAAGAAAAACAGTTTTGAAAGCAGTTCATGGGTTGAGCCCATGGATTTCACTTCCAACTTGTCTTCCCGCCTGCGCTCCCTTTACACCCAGTAATTCCGGACAACGCTTGTGACCTACGTTTTACCGCGGCTGCTGGCACGTAGTTAGCCGTCACTTCCTTGTTGAGTACCGTCATTATCTTCCTCAACAACAGGAGTTTACAATCCGAAGACCTTCTTCCTCCACGCGGCGTCGCTGCATCAGGGTTTCCCCCATTCGTGCAATATTccccactgctgccc


First, you should talk with the metadata team and have them append "tcag" to the beginning of each barcode in the prep_template.txt. The reason for this is due to the key sequence "tcag" not being trimmed using this protocol. 

.. note::
    
    NOTE: This is sort of a hack and is not really the ideal solution, but as long as the original barcode is not length 8 (hamming) or 12 (golay), then the error-correction will not behave any differently upon adding the "tcag" to the beginning of each barcode.

Second you will need open the python library file :file:`/home/wwwuser/projects/Qiime/qiime_web_app/python_code/run_process_sff_through_split_lib.py` and go to the line similar to the one below and append the study id that needs to use this protocol:

::

    if study_id in ['496','968','969','1069','1002','1066','1194','1195','1457','1458','1460','1536']:
    
.. note:: 

    NOTE: I understand this is not the best solution, but it works and since we are moving away from SFF files, I would not recommend spending too much time trying to optimize this functionality, unless necessary.