.. _processing_and_loading:

========================================
Processing and Loading Studies into DB
========================================

Here we will describe the steps involved in processing and loading a study into the DB. 


Processing a Study
---------------------
Prior to processing any study in the DB, you should always check the following:

#. Make sure the Sequence files and Metadata have been uploaded (based on blue checkmarks).
    #. Check the sequence files uploaded (using show/hide sequence files) and check their validity.
        * :doc:`check_fasta`
        * :doc:`check_sff`
        * :doc:`check_fastq`
    #. Check the samples associate to the sequence files (using show/hide samples)
        #. Check the Sample Name and make sure no samples contain spaces or invalid characters (e.g. "-", "_", "$", "#", ",", etc.).
        #. Check that the Run Prefix is actually a prefix that matches the sequence files uploaded and make sure that the file extension (e.g. ".sff", ".fna", ".fastq") is **removed**.
#. If all the checks above are okay, then click on the "Submit job to Qiime (Process Only)" link.
#. You should notice that the job will be submitted and it should progress through the following job-types (NEW -> QUEUED -> RUNNING -> COMPLETED_OKAY).

.. _load_study:

Loading a Study
-------------------
Prior to loading a study into the DB you should always check the following:

#. Go to the Study Page for the study and verify that all the processing jobs have completed and display the message "COMPLETED_OKAY". 
    * If you notice any "COMPLETED_ERROR" messages, I suggest you first make sure that the input files were valid:
        * :doc:`check_fasta`
        * :doc:`check_sff`
        * :doc:`check_fastq`
#. Check the :file:`split_library_log.txt` to verify the study was demultiplexed as expected:

    :: 
        
        cat /home/wwwuser/user_data/studies/study_808/processed_data_s_4_1_sequences_/split_libraries/split_library_log.txt 
    
    A normal :file:`split_library_log.txt` file looks similar to the following: 

    ::

        Input file paths
        Mapping filepath: /home/wwwuser/user_data/studies/study_808/processed_data_s_4_1_sequences_/s_4_1_sequences__split_libraries_mapping_file.txt (md5: a9bf8d5aa384f6cad86388ba6f3c2773)
        Sequence read filepath: /home/wwwuser/user_data/studies/study_808/s_4_1_sequences.fastq (md5: 3a99101c100d839bb4da1d9d32404705)
        Barcode read filepath: /home/wwwuser/user_data/studies/study_808/s_4_1_sequences_barcodes.fastq (md5: 766fcd097ad95162db9b7c52a943b4f7)

        Quality filter results
        Total number of input sequences: 97649265
        Barcode not in mapping file: 87692490
        Read too short after quality truncation: 146969
        Count of N characters exceeds limit: 2378
        Illumina quality digit = 0: 0
        Barcode errors exceed max: 7332527

        Result summary (after quality filtering)
        Median sequence length: 100.00
        UT.15.42.414610	388010
        AK.19.15a.414612	335027
        AK.19.12a.414616	204798
        AK.19.18a.414617	201786
        UT.15.44.414611	198691
        UT.15.45.414619	184685
        UT.15.42.414609	165700
        AK.19.12a.414608	162975
        FL.3.13a.414620	154372
        HI.20.11a.414621	138472
        FL.3.14a.414607	123269
        FL.3.16a.414618	115233
        HI.20.11a.414613	101091
        HI.20.18a.414615	719
        HI.20.15a.414614	73
        ---
    
    .. note::
    
        Note: the sequence/sample counts vary quite a bit for each study and for each technology used. For instance, with FLX/Titanium you should normally see anywhere from 100-10,000 seqs/sample, however for Illumina you could see as much as 100-3,000,000 seqs/sample depending on the study. It should also be noted that depending on the sample type you may see high/low counts depending on the type of the sample. Normally we can amplify gut samples very well, however; some environments amplify poorly and you may need to take that into account. When looking at a study, you may need to take into account that they supplied per-sample sequence files (e.g., HMP), where some of the sequence files did not make it through the split-libraries quality filtering, so those samples produced a "COMPLETED_ERROR" but in that case it was an allowable exclusion, since the majority of the samples had a high number of sequences.
    
    An example of a bad :file:`split_library_log.txt` file should look similar to the following:

    ::

        Number raw input seqs	1339

        Length outside bounds of 200 and 1000	0
        Num ambiguous bases exceeds limit of 6	0
        Missing Qual Score	0
        Mean qual score below minimum of 25	1
        Max homopolymer run exceeds limit of 6	0
        Num mismatches in primer exceeds limit of 0: 1190

        Sequence length details for all sequences passing quality filters:
        Raw len min/max/avg	238.0/293.0/271.2
        Wrote len min/max/avg	205.0/260.0/238.2

        Barcodes corrected/not	0/0
        Uncorrected barcodes will not be written to the output fasta file.
        Corrected barcodes will be written with the appropriate barcode category.
        Corrected but unassigned sequences will not be written unless --retain_unassigned_reads is enabled.

        Total valid barcodes that are not in mapping file	0
        Sequences associated with valid barcodes that are not in the mapping file will not be written.

        Barcodes in mapping file
        Num Samples	1
        Sample ct min/max/mean: 148 / 148 / 148.00
        Sample	Sequence Count	Barcode
        PC.636	148	ACGGTGAGTGTC
        PC.593	0	AGCAGCACTTGT
        PC.354	0	AGCACGAGCCTA
        PC.635	0	ACCGCAGAGTCA
        PC.481	0	ACCAGCGACTAG
        PC.634	0	ACAGAGTCGGCT
        PC.356	0	ACAGACCACTCA
        PC.607	0	AACTGTGCGTAC
        PC.355	0	AACTCGTCGATG

        Total number seqs written	148
    
    For this particular case, you will notice almost all the samples do not have any sequences. This would call me to question whether the barcodes and/or linkerprimer are possibly wrong. If the result you find out that the barcodes and linkerprimer are actually correct, then you can proceed, but I would check the following pages prior to accepting this as valid:

        * :doc:`check_fasta`
        * :doc:`check_sff`
        * :doc:`check_fastq`

.. _perlibstats_check:

#. If the :file:`split_library_log.txt` file looks good (i.e. most samples have > 100 seqs/sample), then you will need to check that file against the OTU-Table produced via the closed-reference OTU-picking protocol. To do this we can run a command similar to the following:

    ::

        per_library_stats.py -i /home/wwwuser/user_data/studies/study_808/processed_data_s_4_1_sequences_/gg_97_otus/exact_uclust_ref_otu_table.biom 
    
    
    A normal output should look like the following:
    
    ::
    
        Num samples: 15
        Num otus: 6624
        Num observations (sequences): 1739869.0
        Table density (fraction of non-zero values): 17.5108

        Seqs/sample summary:
         Min: 43.0
         Max: 258834.0
         Median: 114754.0
         Mean: 115991.266667
         Std. dev.: 66803.5033767
         Median Absolute Deviation: 25415.0
         Default even sampling depth in
          core_qiime_analyses.py (just a suggestion): 68323.0

        Seqs/sample detail:
         HI.20.15a.414614: 43.0
         HI.20.18a.414615: 494.0
         HI.20.11a.414613: 68323.0
         FL.3.16a.414618: 86185.0
         FL.3.14a.414607: 95617.0
         HI.20.11a.414621: 96402.0
         FL.3.13a.414620: 109370.0
         UT.15.42.414609: 114754.0
         AK.19.12a.414608: 120340.0
         UT.15.45.414619: 129212.0
         AK.19.18a.414617: 139806.0
         UT.15.44.414611: 140169.0
         AK.19.12a.414616: 148925.0
         AK.19.15a.414612: 231395.0
         UT.15.42.414610: 258834.0
        
    Using this output you can compare it to the output produced when running "cat" on the :file:`split_library_log.txt` file. You will notice that the seqs/sample are less in the :file:`per_library_stats.py` output. 
    
    .. note::
    
        The data in this output only accounts for the sequences that successfully hit the 97% Greengenes sequences. Normally, these number are anywhere from 50%-100% the same as the seqs/sample in the :file:`split_library_log.txt` file. This tends to depend on the environment of the sample, since Greengenes has better coverage of certain environments.

#. Now that you have verified the :file:`split_library_log.txt` file and :file:`per_library_stats.py` output, you can load the Study into the DB. There are 2 options for loading the data:
    #. You can click on the "(admin option: submit job)" link on the Study Page.
    #. You can submit the job via SQL from the SFF tablespace using a command similar to the following:
    
        ::
    
            update torque_job set job_state_id=-1 where job_type_id=12 and study_id=0 and job_state_id=-2;
            commit;
            
#. If the loading goes smoothly you will notice there will be twice as many loading jobs as there are processing jobs and they should all have the message "COMPLETED_OKAY". The reason for twice as many entries is due to the splitting of OTU-Table loading from sequence loading. The sequence loading is much slower than the OTU-Table loading, so we plan to have a separate slow-seq queue for that job.

    .. note::

        As long as the :file:`split_library_log.txt` file and :file:`per_library_stats.py` output are sane, I have not run into any issues loading, except for the case where the filesystem went down. This is a fairly robust protocol.
    
Validate Loaded Study
---------------------------------
Once a Study has been processed and loaded into the DB, it is always good to validate that the study was properly loaded. Here are the steps that should be done:

#. Go to the Meta-Analysis Portal on the QIIME website and select "Perform Meta-Analysis"
#. From the Drop-down below "Select Studies" select "Contains seqs".
#. Now from the filtered Study list, select the study you just loaded.
#. Move all columns of the metadata from "Available Metadata Fields" to "Selected Metadata Fields"
#. Click the "Continue" button on the bottom of the page.
#. On the Parameters page, check the following boxes:
    * Taxonomy Summmary
    * Beta-Diversity 
        * 3D PCoA Plots
    * In case the study is large, you may want to set "Select Processing Method" to "Parallel" and only run "unweighted_unifrac", which can be found under "Metrics to use" in the "Optional Parameters" of beta-diversity.py
#. Click on the "Submit" button at the bottom of the page.
#. Wait for all the results to be produced and verify there is data in the OTU-Table and mapping file. You can also compare the OTU-Table to the :file:`per_library_stats.py` output from :ref:`load_study`.
#. You should take a look at the Taxa-Summaries to verify the sample count and verify that all samples are not comprised of *only* 1 or 2 taxa. 
#. When opening the beta-diversity plots you should see clustering of samples and in the case that the study is published, you may want to compare against the paper. You should also verify the number of samples present.

