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


def connect_to_db(admin,adpasswd):
    '''Connect to the Oracle Database'''

    adpasswd=hashlib.md5(adpasswd).hexdigest().upper()
    #For the password, we only take values 0:30, since database can only
    #hold up to 30 characters for a password
    
    db = cx_Oracle.connect(admin, adpasswd[0:30], 'microbiome1.colorado.edu:1521/demo1')

    return db

def authenticate_user(db, user, passwd):
    '''If the user supplied username is valid, returns the users id'''

    #convert the user-supplied password to md5 encryption, so it can be
    #compared against the passwords in the database
    login_password=hashlib.md5(passwd).hexdigest().upper()
    login_user=user

    #Get the user id and first name of the person who logged in
    select_param="user_id,FIRST_NAME"
    from_param="qiime_user"
    where_param="qiime_user.username='%s' AND qiime_user.password='%s'" \
                    % (login_user,login_password)

    user_info=select_from_where_db(db,select_param,from_param,where_param)

    return user_info

def select_from_where_db(db,select_params,from_params,where_params):
    '''Using the SQL statement: SELECT ... FROM ... WHERE ..., this extracts the 
       data from the Database'''
    
    #Define database cursor object
    cursor = db.cursor()
    
    #Get data from the database.
    sql_query2="SELECT %s FROM %s WHERE %s" % (select_params,from_params, \
                                               where_params)
 
    cursor.execute(sql_query2)
    results=cursor.fetchall()
    
    return results
    
def select_from_db(db,select_params,from_params):
    '''Using the SQL statement: SELECT ... FROM ... WHERE ..., this extracts the 
       data from the Database'''

    #Define database cursor object
    cursor = db.cursor()

    #Get data from the database.
    sql_query2="SELECT %s FROM %s" % (select_params,from_params)
                          
    cursor.execute(sql_query2)
    results=cursor.fetchall()

    return results