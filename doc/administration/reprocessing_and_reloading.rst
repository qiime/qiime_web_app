.. _reprocessing_and_reloading:

==============================================
Reprocessing and Reloading Studies into DB
==============================================

Here we will describe the steps involved in reprocessing and reloading a study into the DB. This is **NOT** an ideal situation, since studies should be loaded once and not require reprocessing and reloading, but in the event it is necessary, here is what you will need to do. **PLEASE BE CAREFUL** when running any of the commands described here. It is much better to double and triple-check the command to make sure it is correct, than it is to reload data you screwed up.

First you should determine if the study is broken or requires reprocesing and reloading by referring to :doc:`determine_if_study_invalid`.

Deleting Metadata and Sequences from DB
-----------------------------------------
In the scenario where the study is not salvageable and must be reprocessed, you will want to follow the steps below to properly remove all traces of the bad data.

Delete Metadata For Study
***************************
As a precaution, I would perform an "svn update" on the QIIME-webdev repository to verify that the metadata is up-to-date. Once this is verified, I would perform a delete of the metadata from the DB, just to be safe that there are not any lingering samples, such as described in :ref:`add_remove_samples`. To remove the metadata associated to a particular study, you should connect to the QIIME_METADATA tablespace and run the SQL below (where the 0 corresponds to the study_id of choice and the 1 is the option to remove the sample/prep information).

::

    exec qiime_assets.study_delete(0,1);
    commit;

From the Study Page, you should notice that the blue checkmark is now an orange x. If you don't see that, then you may want to refresh the page. If this does not properly work, then you should ask Doug for assistance instead of trying any brute-force approaches.

If the data is properly deleted you can re-upload the latest version of the metadata from the QIIME-webdev repository.

    
Delete Torque Poller Jobs for Study
*************************************
Since some studies may have numerous runs associated to it, you may not want to click on the "(admin option: clear job)" link several times. Instead you can run the following SQL statement from the SFF tablespace, where the study id is 0:

::
    
    delete from torque_job where study_id=0;
    commit;
    
This command will remove all torque jobs related to the given study and should be reflected on the Study Page.

Delete Sequence and OTU-Table Data for Study
************************************************
When deleting sequence and OTU data from the DB, it can take anywhere from a few minutes to several hours, so expect delays. Prior to performing a deletion of this data, I tend to check `Oracle Enterprise Manager (EM) <https://thebeast.colorado.edu:1158/em/>`_ along with the queue, since it takes much longer to delete a study when the DB is under heavy load or if sequence data is being loaded into the DB simultaneously. Usually if the queue is low on jobs and the load on EM is under 2.00, then I think it is an ideal situation for deleting a study. Once those checks are done, there are three ways for deleting the sequence and OTU data from the DB. The reason for this depends quite a bit on the size of the study along with the issue of a study being loaded twice into the DB.

    #. The easiest and most common way for deleting the sequence and OTU data from the DB is by running the following SQL from the SFF tablespace where the study id is 0 for this case:

        ::

            variable error_flag NUMBER;
            execute delete_all_analysis_results(0,:error_flag);
            print error_flag;
            commit;
    
        If this fails for any reason, then you may want to try this second method, which requires a bit more effort. 
    
    #. Go to the SFF tablespace and type the following SQL (i.e. study id is 101):
        
        ::
    
            select * from analysis where study_id=101;
        
        This will return a table like the following:
    
        =========== ========== ==================== ================== ============== ======== ======
        ANALYSIS_ID SEQ_RUN_ID SPLIT_LIBRARY_RUN_ID OTU_PICKING_RUN_ID OTU_RUN_SET_ID STUDY_ID NOTES
        =========== ========== ==================== ================== ============== ======== ======
        1189        597        1017                 701                701            101      (null)
        1170        596        998                  683                683            101      (null)
        =========== ========== ==================== ================== ============== ======== ======
    
        I suggest copying and pasting this table into Excel, so when you start deleting, you can remember what data you had originally. Now that you have the table, you can run the following command, where you delete based on the analysis id's, instead of collation of all runs when using the study id. For this example the analysis ids to use are 1189 and 1170, but for each row you will need to repeat this command while updating the analysis id each time:
    
        ::
    
            variable error_flag NUMBER;
            execute delete_test_analysis(1189,:error_flag);
            print error_flag;
            commit;
        
        Then you need to run it again for the second analysis row:
    
        ::
    
            variable error_flag NUMBER;
            execute delete_test_analysis(1170,:error_flag);
            print error_flag;
            commit;
        
    #. This last method is primarily for the case where a study gets loaded into the DB more than once by accident. It should be considered the last resort and requires the most effort. As we did in the previous method, we need to get the rows from the analysis table (i.e. study id is 101):
    
        ::

            select * from analysis where study_id=101;
    
        This will return a table like the following:

        =========== ========== ==================== ================== ============== ======== ======
        ANALYSIS_ID SEQ_RUN_ID SPLIT_LIBRARY_RUN_ID OTU_PICKING_RUN_ID OTU_RUN_SET_ID STUDY_ID NOTES
        =========== ========== ==================== ================== ============== ======== ======
        1189        597        1017                 701                701            101      (null)
        1170        596        998                  683                683            101      (null)
        =========== ========== ==================== ================== ============== ======== ======
        
        Now that you have the rows, I strongly encourage you to copy them into Excel, since we will be deleting rows from each table iteratively. For this particular study, you would need to run this SQL twice since there are multiple rows. You will need to put the appropriate ids for each delete statement and it may make sense to perform a commit between each delete statement:
        
        ::
        
            delete from otu_picking_failures where otu_picking_run_id = 701;
            delete from otu_picking_run where otu_picking_run_id = 701;
            delete from otu_run_set where otu_run_set_id = 701;
            delete from otu_table where otu_run_set_id = 701;
            delete from split_library_read_map where split_library_run_id = 1017;
            delete from analysis where analysis_id = 1189;
            delete from split_library_run where split_library_run_id = 1017;
            commit;
            
    
Now that the sequence and OTU data has been deleted for the study, you will need to verify that the data was removed. For the study above, you should run the following command to verify that there are "no rows selected":

::

     select * from analysis where study_id=101;

This will either return "no rows selected" or an empty table like this:

=========== ========== ==================== ================== ============== ======== ======
ANALYSIS_ID SEQ_RUN_ID SPLIT_LIBRARY_RUN_ID OTU_PICKING_RUN_ID OTU_RUN_SET_ID STUDY_ID NOTES
=========== ========== ==================== ================== ============== ======== ======
=========== ========== ==================== ================== ============== ======== ======

Now that the study has been deleted from the DB, I would reload the data according to the procedure described in :doc:`processing_and_loading`.
