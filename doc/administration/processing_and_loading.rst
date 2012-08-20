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





