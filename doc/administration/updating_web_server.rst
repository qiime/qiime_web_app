.. _updating_web_server:

==================================
Updating Software on Web Servers
==================================
Prior to updating **anything** on the `Production QIIME Web Server <http://www.microbio.me/qiime/>`_, you **should** install or update the software on the `Development QIIME Web Server <http://webdev.microbio.me/qiime/>`_.

Login Information
-------------------
Various test datasets that can be uploaded and tested through the website are in the QIIME-webdev reposotory under :file:`qiime_web_app/python_code/tests/support_files/qiime_test_datasets`.

Development Web Server
************************
SSH to Development Web Server:
::

    ssh [user-acct]@webdev.microbio.me

Sign in as QIIME Development User: wwwdevuser 
::

    sudo su - wwwdevuser

Production Web Server
************************
SSH to Production Web Server:
::

    ssh [user-acct]@www.microbio.me

Sign in as QIIME Production User: wwwuser 
::

    sudo su - wwwuser
    

How to Add/Update Software
----------------------------
*****Use Development Web Server First*****

Prior to running the following commands, make sure there are no jobs running in the queue, since you do not want to update software while scripts are running.

#. Stop the Poller
    ::
        
        python $HOME/projects/Qiime/qiime_web_app/python_code/TorqueOraPoller/poller.py stop
        
    By running "top" you should notice that no python jobs are running.
    
    .. note::
    
        On the Production Web Server, there is a cron job running in the background, which checks that the poller is running and sends an email if it stops for any reason. The cron job uses the poller files which are located under the :file:`/tmp/` directory and have a prefix of :file:`qiime-webapp-poller`.
        
    Here is an example shell script that can be used for checking the poller status via a cron job:
    
    ::
        
        #!/bin/bash

        # This is a cron job for checking that qiime-poller is running
        if [ -f /tmp/qiime-webapp-poller.pid ]
        then
            # get pid and verify it is running
            pid=`cat /tmp/qiime-webapp-poller.pid`
            jobinfo=`ps -f -p $pid | grep $pid`

            # check that job is running
            if [ "$jobinfo" == "" ]
            then
                if [ -f /tmp/qiime-webapp-poller.stderr ]
                then
                    tail -n 100 /tmp/qiime-webapp-poller.stderr | mail -s "QIIME poller not running" jistombaugh@gmail.com
                else
                    echo "qiime-poller output files missing from /tmp/" | mail -s "QIIME poller not running" jistombaugh@gmail.com
                fi
            fi
        else
            if [ -f /tmp/qiime-webapp-poller.stderr ]
            then
                tail -n 100 /tmp/qiime-webapp-poller.stderr | mail -s "QIIME poller not running" jistombaugh@gmail.com
            else
                echo "qiime-poller output files missing from /tmp/" | mail -s "QIIME poller not running" jistombaugh@gmail.com
            fi
        fi

#. Update or add new software onto the system.
    For instance, if you are updating QIIME, you will also want to update the BIOM and PyCogent repositories, where the repositories are located in the folder :file:`$HOME/software/`. To update these repositories you "cd" to the appropriate folder under :file:`$HOME/software/` and type the following:
    
    ::

        svn update
        
    When updating the BIOM repository, you should "cd" into the BIOM repository folder (:file:`$HOME/software/biom-format`) and run the tests: 
    
    ::
    
        python python-code/tests/all_tests.py -v
            
    When updating PyCogent, you should "cd" into the PyCogent repository folder (:file:`$HOME/software/PyCogent/` on Development and :file:`$HOME/software/PyCogent_svn/` on Production) and run the tests:
    
    ::
    
        ./run_tests
            
    When updating QIIME, you should "cd" into the QIIME repository folder (:file:`$HOME/software/Qiime/` on Development and :file:`$HOME/software/Qiime_svn/` on Production) and run the tests:
    
    ::
    
        python tests/all_tests.py -v
        
    For a quick test to verify that QIIME is properly working, you can "cd" into the :file:`qiime_tutorial` folder in the QIIME repository and type the following command:
    
    ::
    
        ./qiime_tutorial_commands_serial.sh
        
    .. note::
    
        The reason for the discrepancy in repository names on the Production Web Server is that initially it was setup to only use QIIME releases, which was abandoned due to the rapid development of QIIME and the DB.
        

#. If all the tests pass, then you can start the Poller

    ::
    
        python $HOME/projects/Qiime/qiime_web_app/python_code/TorqueOraPoller/poller.py start
    
    
Updating QIIME-webdev Repository
----------------------------------
*****Use Development Web Server First*****

If you decide to update the QIIME-webdev repository, you should perform the following steps:

#. Stop the Poller

    ::
    
        python $HOME/projects/Qiime/qiime_web_app/python_code/TorqueOraPoller/poller.py stop
        
    By running "top" you should notice that no python jobs are running.

#. Update the QIIME-webdev repository:

    ::

        svn up $HOME/projects/Qiime/

#. Restart the httpd service. To do this, you will need to be logged in as the "root" user and you can type the following command:

    ::

        service httpd restart
        
#. Start the Poller

    ::

        python $HOME/projects/Qiime/qiime_web_app/python_code/TorqueOraPoller/poller.py start

#. Test that everything is working fine.
    #. Run the Web Server tests:
    
        ::
        
            python $HOME/projects/Qiime/qiime_web_app/python_code/tests/all_tests.py -v
            
    #. Upload and try processing some test datasets located under :file:`qiime_web_app/python_code/tests/support_files/qiime_test_datasets`. I suggest trying to process the FASTA, Illumina and SFF datasets.
    #. Perform some Meta-Analyses to verify everything is behaving as expected.
    
    
    
    
    