#!/usr/bin/env python
'''
__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2009, the Qiime Project"
__credits__ = ["Jesse Stombaugh"] #remember to add yourself
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Prototype"

Author: Jesse Stombaugh (jesse.stombaugh@colorado.edu)
Status: Prototype

'''
#from oracle_connect import user_pswd
#(user,passwd)=user_pswd()
import cx_Oracle
import hashlib
from time import strftime
from oracle_db import connect_to_db,authenticate_user
from cogent.util.unit_test import TestCase, main

class TopLevelTests(TestCase):
    """Tests of top-level functions"""

    def setUp(self):
        """define some top-level data"""
        self.user='Rob Knight'
        self.passwd='Barbeque'
        self.admin='qiime_production'
        self.adpasswd='odyssey$'
        self.user1='Rob Knight'
        self.passwd1='Barbeque'
        self.user2='test1'
        self.passwd2='Barbeque'
        self.user3='Rob Knight'
        self.passwd3='test2'

    def test_connect_to_db(self):
    
        obs=connect_to_db(self.admin,self.adpasswd);

        exp="<cx_Oracle.Connection to qiime_production@microbiome1.colorado.edu:1521/demo1>"
        #self.assertEqual(obs,exp)
        
    def test_authenticate_user(self):
        #Determine if the user supplied a username
            db=connect_to_db(self.admin,self.adpasswd);
            #convert the user-supplied password to md5 encryption, so it can be
            #compared against the passwords in the database
            obs1=authenticate_user(db,self.user1,self.passwd1)
            exp1=[(7,'Rob')]
            obs2=authenticate_user(db,self.user2,self.passwd2)
            exp2=[]
            obs3=authenticate_user(db,self.user3,self.passwd3)
            exp3=[]

            self.assertEqual(obs1,exp1)
            self.assertEqual(obs2,exp2)
            self.assertEqual(obs3,exp3)


#run tests if called from command line
if __name__ == "__main__":
    main()