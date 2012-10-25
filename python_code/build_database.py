#!/usr/bin/env python
# encoding: utf-8
"""
build_database.py

Created by Doug Wendel on 2010-03-30.
"""
__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Development"

import os
from data_access_connections import data_access_factory
from enums import ServerConfig

def buildDatabase():
    try:
        # Clear existing database
        con = data_access_factory(ServerConfig.data_access_type).getTestDatabaseConnection()        
        sqlCommand = 'alter session set ddl_lock_timeout=2'
        con.cursor().execute(sqlCommand)
        sqlCommand = 'select \'DROP \'|| object_type || \' \"\' || object_name || \'\"\' || DECODE(OBJECT_TYPE,\'TABLE\',\' CASCADE CONSTRAINTS\',\'\') from user_objects'
        stmt_list = con.cursor().execute(sqlCommand)        
        rows = stmt_list.fetchall()
        
        for row in rows:
            print 'running statement: ' + row[0]
            try:
                con.cursor().execute(row[0])
            except Exception, e:
                print e

        # Create schema and populate
        commandLine = '$ORACLE_HOME/sqlplus qiime_test/\"odyssey$\"@microbiome1.colorado.edu/microbe @\'../../database/scripts/create_schema.sql\''
        result = os.system(commandLine).read()
        print result
        
        # Install types package
        #commandLine = '$ORACLE_HOME/sqlplus qiime_test/\"odyssey$\"@microbiome1.colorado.edu/microbe @\'../../database/packages/types.sql\''
        #print commandLine
        #result = os.system(commandLine).read()
        #print result
        
        # Install procedures    
        #commandLine = '$ORACLE_HOME/sqlplus qiime_test/\"odyssey$\"@microbiome1.colorado.edu/microbe @\'../../database/procedures/get_column_dictionary.sql\''
        #result = os.system(commandLine).read()
        #print result
        
    except Exception, e:
        print e
    finally:
        if con != None:
            con.close()

if __name__ == '__main__':
    buildDatabase()

