
"""
Centralized database access for the American Gut web portal
"""

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Doug Wendel"]
__email__ = "wendel@colorado.edu"
__status__ = "Production"

import cx_Oracle
from crypt import crypt
from threading import Lock
from time import sleep
import csv

class AGDataAccess(object):
    """
    Data Access implementation for all the American Gut web portal
    """
    
    def __init__(self, connections):
        self._metadataDatabaseConnection = None
        self._ontologyDatabaseConnection = None
        self._SFFDatabaseConnection = None
        
        # Set up the connections
        if not connections:
            raise ValueError('connections is None. Cannot instantiate QiimeDataAccess')
            
        self.getMetadataDatabaseConnection = connections.getMetadataDatabaseConnection
        self.getOntologyDatabaseConnection = connections.getOntologyDatabaseConnection
        self.getSFFDatabaseConnection = connections.getSFFDatabaseConnection
        
    #####################################
    # Helper Functions
    #####################################
    
    def testDatabase(self):
        """Attempt to connect to the database
        
        Attempt a database connection. Will throw an exception if it fails. Returns
        "True" if successful.
        """
        con = self.getMetadataDatabaseConnection()
        if con:
            return True
        
    def dynamicMetadataSelect(self, query_string):
        # Make sure no tomfoolery is afoot
        query_string_parts = set(query_string.lower().split())
        verboten = set(['insert', 'update', 'delete'])
        intersection = query_string_parts.intersection(verboten)
        if len(intersection) > 0:
            raise Exception('Only select statements are allowed. Your query: %s' % query_string)
        
        con = self.getMetadataDatabaseConnection()
        return con.cursor().execute(query_string)

    def dynamicMetadataUpdate(self, query_string):
        """ """
        query_string_parts = set(query_string.lower().split())
        verboten = set(['select', 'insert', 'delete'])
        intersection = query_string_parts.intersection(verboten)
        if len(intersection) > 0:
            raise Exception('Only select statements are allowed. Your query: %s' % query_string)
        con = self.getMetadataDatabaseConnection()
        con.cursor().execute(query_string)
        con.cursor().execute('commit')

    #####################################
    # Users
    #####################################

    def authenticateWebAppUser(self, username, password):
        """ Attempts to validate authenticate the supplied username/password
        
        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        #crypt_pass = crypt(password, username)
        con = self.getMetadataDatabaseConnection()
        user_data = con.cursor()
        con.cursor().callproc('ag_authenticate_user', [username, password, user_data])
        row = user_data.fetchone()
        if row:
            user_data = {'web_app_user_id':str(row[0]), 'email':row[1], 'name':row[2], \
                'address':row[3], 'city':row[4], 'state':row[5], 'zip':row[6], \
                'country':row[7]}
            return user_data
        else:
            return False

    def addAGHumanParticipant(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_add_participant', [ag_login_id, participant_name])

    def addAGSingle(self, ag_login_id, participant_name, field_name, field_value, table_name):
        con = self.getMetadataDatabaseConnection()
        sql = "update {0} set {1} = '{2}' where ag_login_id = '{3}' and participant_name = '{4}'".format(table_name, \
            field_name, field_value, ag_login_id, participant_name)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def deleteAGParticipant(self, ag_login_id, participant_name, table_name):
        con = self.getMetadataDatabaseConnection()
        sql = "delete {0} where ag_login_id = '{1}' and participant_name = '{2}'".format(table_name, ag_login_id, participant_name)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def insertAGMultiple(self, ag_login_id, participant_name, field_name, field_value):
        con = self.getMetadataDatabaseConnection()
        sql = "insert into ag_survey_multiples (ag_login_id, participant_name, item_name, item_value) values ('{0}', \
            '{1}', '{2}', '{3}')".format(ag_login_id, participant_name, field_name, field_value)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def deleteAGMultiple(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        sql = "delete ag_survey_multiples where ag_login_id = '{0}' and participant_name = '{1}'".format(ag_login_id, participant_name)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def removeAGHumanParticipant(self, ag_login_id, participant_name):
        # Clear the general values data
        self.deleteAGGeneralValues(ag_login_id, participant_name)

        # Clear the multiple values table
        self.deleteAGMultiple(ag_login_id, participant_name)

        # Clear the participant row
        self.deleteAGParticipant(ag_login_id, participant_name, 'ag_human_survey')

    def addAGGeneralValue(self, ag_login_id, participant_name, field_name, field_value):
        con = self.getMetadataDatabaseConnection()
        sql = "insert into ag_survey_answer (ag_login_id, participant_name, question, answer) values ('{0}', '{1}', \
            '{2}', '{3}')".format(ag_login_id, participant_name, field_name, field_value)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def deleteAGGeneralValues(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        sql = "delete ag_survey_answer where ag_login_id = '{0}' and participant_name = '{1}'".format(ag_login_id, participant_name)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def logParticipantSample(self, barcode, sample_site, sample_date, hours, minutes, meridian, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_log_participant_sample', [barcode, sample_site, sample_date, hours, minutes, meridian, participant_name])

    def getParticipantSamples(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        barcodes = []
        con.cursor().callproc('ag_get_participant_samples', [ag_login_id, participant_name, results])
        for row in results:
            data = {'barcode':row[0], 'site_sampled':row[1], 'sample_date':row[2], \
                'hour':row[3], 'minute':row[4], 'meridian':row[5]}
            barcodes.append(data)

        return barcodes

    def getAvailableBarcodes(self, ag_login_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        available_barcodes = []
        con.cursor().callproc('ag_available_barcodes', [ag_login_id, results])
        for row in results:
            available_barcodes.append(row[0])

        return available_barcodes

    def verifyKit(self, supplied_kit_id):
        """Set the KIT_VERIFIED for the supplied_kit_id to 'y'"""
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_verify_kit_status', [supplied_kit_id])
