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
