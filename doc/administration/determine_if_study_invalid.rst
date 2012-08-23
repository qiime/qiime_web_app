.. _determine_if_study_invalid:

=====================================================
Determine If Study Needs Reprocessed and Reloaded
=====================================================
There are a few reasons why a study may need to be reprocessed and reloaded, such as 1) a change to key-fields in the :file:`prep_template.txt`, 2) the data is inaccurate or 3) the end-user wants to add/remove samples from their study

.. _change_to_keyfields:

Change to Key-Fields in :file:`prep_template.txt`
-------------------------------------------------
The most common method is that a user changes some of the key-fields (sample_name, barcode, linker, primer, platform and run_prefix) in the :file:`prep_template.txt` and upon re-uploading of the metadata they get a pop-up window that looks like the following:

.. image:: ../images/metadata_upload_reprocess_popup.png
   :align: center
   
If the end-user clicks the "OK" button, it means that all of the previous metadata associated with this study will be deleted, including the unique accessions which is the link of each sample to the SFF tablespace.

For some of these cases the adminstrator may be able to salvage the broken study, so please refer to :ref:`salvage_study`.

Inaccurate Data
----------------
Occasionally, you may be in the situation where the end-user gives you incorrect values one or more of the following fields in the uploaded :file:`prep_template.txt`: sample_names, barcodes, linker, primers, platform or run_prefix. Upon processing, the study may process and give reasonable seqs/sample counts, which is one of the checks performed prior to loading, the study may get loaded and appear to be correct, when in fact they gave you incorrect data to start with, so inaccurate data gets loaded. Normally, you will not notice this situation without assistance from the end-user uploading the data. It is recommended that you send the :file:`split_library_log.txt` file and a full-mapping file prior to loading a dataset, so the end-user can compare your results with theirs. This has been a semi-successful solution to resolve this situation where inaccurate data gets loaded into the DB.

.. _add_remove_samples:

Addition/Removal of Samples from a Study
-----------------------------------------
There are certain situations, where an end-user may want to add/remove a sample from their study. Normally, they should get the pop-up described in :ref:`change_to_keyfields`, since the key-fields will most likely change. In the case of removing a sample, the end-user may not get a pop-up message, but this does not mean the sample will be deleted from either the QIIME_METADATA or SFF tablespaces. In the case of adding a sample, they should most likely get a pop-up window and the study will need to be reprocessed and reloaded.

.. _salvage_study:

Salvaging a Broken Study
--------------------------
The first step that an administrator should take, is to determine if the study was broken due to :ref:`change_to_keyfields`, where the processed data is actually valid and the only problem is a broken link between the metadata and sequence data. An example of this would occur if there was a change to the linker or primer for an Illumina dataset, which doesn't use those fields for processing, therefore the processed data may be okay. This issue would cause the sequence_prep_id's for the study to change, but all the sample_names, run_prefix, etc. could remain the same. Make sure that none of the other key fields change and only the linker or primer were changed. As long as there is a one-to-one relationship between the :file:`sample_template.txt` and :file:`prep_template.txt`, meaning that **no sample** in the sample_template has more than one :file:`prep_template.txt` row, you can run an SQL statement similar to the following under the QIIME_METADATA tablespace, where we are updating all the sequence_prep_ids in the QIIME_METADATA tablespace using the original sequence_prep_id's used for processing from the SFF tablespace. To use this SQL you will need to put the study ids you want to fix in the study_ids list:

::

    #
    from data_access_connections import data_access_factory
    from enums import ServerConfig

    data_access = data_access_factory(ServerConfig.data_access_type)
    con = data_access.getMetadataDatabaseConnection()
    study_ids = []

    query_string = """
    select  distinct s.study_id 
    from    study s 
            inner join sample sa 
            on s.study_id = sa.study_id 
            inner join sequence_prep sp 
            on sa.sample_id = sp.sample_id 
    where   exists
            (
                select  1
                from    sequence_prep sp2
                where   sp2.num_sequences is null
                        and sp2.sequence_prep_id = sp.sequence_prep_id
            )
    order by study_id
    """

    results = data_access.dynamicMetadataSelect(query_string)
    print '---------------------- Studies List ----------------------'
    for row in results:
        study_id = row[0]
        print 'study_id: {0}'.format(str(study_id))
        study_ids.append(row[0])

    query_string = """
    select  substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) as sequence_prep_id, 
            count(substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1)) as cnt 
    from    sff.split_library_read_map slrm 
            inner join sff.analysis a 
            on slrm.split_library_run_id = a.split_library_run_id 
            inner join qiime_metadata.sequence_prep sp 
            on sp.sequence_prep_id = substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) 
    where   a.study_id = {0} 
            and sp.num_sequences is null
    group by substr(slrm.sample_name, instr(slrm.sample_name, '.', -1) + 1) 
    """

    print '---------------------- Seqs per Prep ID ----------------------'
    for study_id in study_ids:
        seq_prep_counts = []
        run_string = query_string.format(study_id)
        #print run_string
        results = data_access.dynamicMetadataSelect(query_string.format(study_id))
        for sequence_prep_id, seq_count in results:
            seq_prep_counts.append((sequence_prep_id, seq_count))

            query_string_2 = """
            update  sequence_prep 
            set     num_sequences = {0} 
            where   sequence_prep_id = {1} 
            """

            for sequence_prep_id, seq_count in seq_prep_counts:
                run_string = query_string_2.format(seq_count, sequence_prep_id)
                #print run_string
                con.cursor().execute(run_string)
                con.cursor().execute('commit')

    # end


In the case where the same sample was sequenced using different preparations, you will need to reprocess and reload the entire study. The reason for this is that it is not possible to identify which sequences belong to one sample preparation versus the other sample preparation, since barcodes, linker/primers are removed from the sequences prior to loading into the SFF tablespace. The sequence_name only points to the sample_name and sequence_prep_id, so if the sample_name is not unique, any change to the sequence_prep_id will result in mass confusion.
