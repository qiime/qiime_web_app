
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
import httplib
import json
import urllib
from random import choice

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

    #####################################
    # Users
    #####################################

    def authenticateWebAppUser(self, username, password):
        """ Attempts to validate authenticate the supplied username/password
        
        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
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

    def addAGLogin(self, email, name, address, city, state, zip, country):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_insert_login', [email, name, address, city, state, zip, country])

    def updateAGLogin(self, ag_login_id, email, name, address, city, state, zip, country):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_update_login', [ag_login_id, email, name, address, city, state, zip, country])

    def getAGSurveyDetails(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_survey_details',
            [ag_login_id, participant_name, results])

        data = {}
        for row in results:
            if row[3]:
                data[row[2]] = row[3]

        return data

    def getAGLogins(self):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_logins', [results])

        # ag_login_id, email, name
        return [(row[0], row[1], row[2]) for row in results]

    def getAGKitsByLogin(self):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_kits_by_login', [results])

        # ag_login_id, email, name
        return [(row[0], row[1], row[2]) for row in results]

    def getAGBarcodes(self):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_barcodes', [results])

        return [row[0] for row in results]

    def getAGBarcodesByLogin(self, ag_login_id):
        # returned tuple consists of:
        # site_sampled, sample_date, sample_time, participant_name, environment_sampled, notes 
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_barcodes_by_login', [ag_login_id, results])
        barcodes = results.fetchall()
        """
        Tuple format is:

        al.email, akb.ag_kit_barcode_id, akb.ag_kit_id, akb.barcode, 
        akb.site_sampled, akb.environment_sampled, akb.sample_date, 
        akb.sample_time, akb.participant_name, akb.notes
        """
        return barcodes

    def getAGBarcodeDetails(self, barcode):
        # returned tuple consists of:
        # site_sampled, sample_date, sample_time, participant_name, environment_sampled, notes 
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_barcode_details', [barcode, results])
        barcode_details = results.fetchone()
        """
        Tuple format is:

        al.email, akb.ag_kit_barcode_id, akb.ag_kit_id, akb.barcode, 
        akb.site_sampled, akb.environment_sampled, akb.sample_date, 
        akb.sample_time, akb.participant_name, akb.notes
        """
        return barcode_details

    def getAGKitDetails(self, supplied_kit_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_kit_details', [supplied_kit_id, results])
        row = results.fetchone()
        kit_details = {
            'ag_kit_id': row[0],
            'supplied_kit_id': row[1],
            'kit_password': row[2],
            'swabs_per_kit': row[3],
            'kit_verification_code': row[4],
            'kit_verified': row[5],
            'verification_email_sent': row[6]
        }

        return kit_details

    def getAGCode(self, type):
        length_of_password = 8
        alpha = ''
        if type == 'alpha':
            alpha = 'abcdefghijklmnopqrstuvwxyz'
            alpha += alpha.upper()
        elif type == 'numeric':
            alpha += '0123456789'

        passwd = ''.join([choice(alpha) for i in range(length_of_password)])

        return passwd

    def getNewAGKitId(self):
        sql = "select 1 from ag_handout_kits where kit_id = '{0}' union select 1 from ag_kit where supplied_kit_id = '{0}'"
        code = None

        while True:
            # Get a code
            code = self.getAGCode('alpha')
            # Check if in DB. If clear, exit loop
            results = self.dynamicMetadataSelect(sql.format(code)).fetchall()
            if len(results) == 0:
                break

        return code

    def getNextAGBarcode(self):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_next_barcode', [results])
        next_barcode = results.fetchone()[0]
        text_barcode = '{0}'.format(str(next_barcode))
        # Pad out the barcode until it's 9 digits long
        while len(text_barcode) < 9:
            text_barcode = '0{0}'.format(text_barcode)

        return next_barcode, text_barcode

    def reassignAGBarcode(self, ag_kit_id, barcode):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_reassign_barcode', [ag_kit_id, barcode])

    def addAGKit(self, ag_login_id, kit_id, kit_password, swabs_per_kit, kit_verification_code):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_insert_kit', [ag_login_id, kit_id, kit_password, swabs_per_kit, kit_verification_code])

    def updateAGKit(self, ag_kit_id, supplied_kit_id, kit_password, swabs_per_kit, kit_verification_code):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_update_kit', [ag_kit_id, supplied_kit_id, kit_password, swabs_per_kit, kit_verification_code])

    def addAGBarcode(self, ag_kit_id, barcode):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_insert_barcode', [ag_kit_id, barcode])

    def updateAGBarcode(self, barcode, ag_kit_id, site_sampled, environment_sampled, sample_date, sample_time, participant_name, notes):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_update_barcode', [barcode, ag_kit_id, site_sampled, environment_sampled, sample_date, sample_time, participant_name, notes])

    def addAGHumanParticipant(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_add_participant', [ag_login_id, participant_name])

    def addAGAnimalParticipant(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_add_animal_participant', [ag_login_id, participant_name])

    def addAGSingle(self, ag_login_id, participant_name, field_name, field_value, table_name):
        con = self.getMetadataDatabaseConnection()
        sql = "update {0} set {1} = '{2}' where ag_login_id = '{3}' and participant_name = '{4}'".format(table_name, \
            field_name, field_value, ag_login_id, participant_name)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    def deleteAGParticipant(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_delete_participant', [ag_login_id, participant_name])

    def insertAGMultiple(self, ag_login_id, participant_name, field_name, field_value):
        con = self.getMetadataDatabaseConnection()
        sql = "insert into ag_survey_multiples (ag_login_id, participant_name, item_name, item_value) values ('{0}', \
            '{1}', '{2}', '{3}')".format(ag_login_id, participant_name, field_name, field_value)
        con.cursor().execute(sql)
        con.cursor().execute('commit')

    #def deleteAGMultiple(self, ag_login_id, participant_name):
    #    con = self.getMetadataDatabaseConnection()
    #    sql = "delete ag_survey_multiples where ag_login_id = '{0}' and participant_name = '{1}'".format(ag_login_id, participant_name)
    #    con.cursor().execute(sql)
    #    con.cursor().execute('commit')

    #def removeAGHumanParticipant(self, ag_login_id, participant_name):
        # Clear the general values data
        #self.deleteAGGeneralValues(ag_login_id, participant_name)

        # Clear the multiple values table
        #self.deleteAGMultiple(ag_login_id, participant_name)

        # Clear the participant row
        #self.deleteAGParticipant(ag_login_id, participant_name, 'ag_human_survey')

    def addAGGeneralValue(self, ag_login_id, participant_name, field_name, field_value):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_insert_survey_answer', [ag_login_id,
            participant_name, field_name, field_value])

    def deleteAGGeneralValues(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_delete_survey_answer', [ag_login_id, participant_name])

    def logParticipantSample(self, barcode, sample_site, environment_sampled, sample_date, sample_time, participant_name, notes):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_log_participant_sample', [barcode, sample_site, environment_sampled, sample_date, sample_time, participant_name, notes])

    def deleteSample(self, barcode, ag_login_id):
        """
        Strictly speaking the ag_login_id isn't needed but it makes it really hard to hack
        the function when you would need to know someone else's login id (a GUID) to 
        delete something maliciously
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_delete_sample', [barcode, ag_login_id])

    def getHumanParticipants(self, ag_login_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_human_participants', [ag_login_id, results])

        return [row[0] for row in results]

    def getAnimalParticipants(self, ag_login_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_animal_participants', [ag_login_id, results])

        return [row[0] for row in results]

    def getParticipantExceptions(self, ag_login_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_get_participant_exceptions', [ag_login_id, results])

        return [row[0] for row in results]

    def getParticipantSamples(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        barcodes = []
        con.cursor().callproc('ag_get_participant_samples', [ag_login_id, participant_name, results])
        for row in results:
            data = {'barcode':row[0], 'site_sampled':row[1], 'sample_date':row[2], 'sample_time':row[3], 
                'notes':row[4], 'status':row[5]}
            barcodes.append(data)

        return barcodes

    def getEnvironmentalSamples(self, ag_login_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        barcodes = []
        con.cursor().callproc('ag_get_environmental_samples', [ag_login_id, results])
        for row in results:
            data = {'barcode':row[0], 'site_sampled':row[1], 'sample_date':row[2], 'sample_time':row[3], 'notes':row[4], 'status':row[5]}
            barcodes.append(data)

        return barcodes

    def getAvailableBarcodes(self, ag_login_id):
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_available_barcodes', [ag_login_id, results])

        return [row[0] for row in results]

    def verifyKit(self, supplied_kit_id):
        """Set the KIT_VERIFIED for the supplied_kit_id to 'y'"""
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_verify_kit_status', [supplied_kit_id])

    def addGeocodingInfo(self, limit=None, retry=False):
        """Adds latitude, longitude, and elevation to ag_login_table

        Uses the city, state, zip, and country from the database to retrieve
        lat, long, and elevation from the google maps API.

        If any of that information cannot be retrieved, then cannot_geocode
        is set to 'y' in the ag_login table, and it will not be tried again
        on subsequent calls to this function.  Pass retry=True to retry all
        (or maximum of limit) previously failed geocodings.
        """
        con = self.getMetadataDatabaseConnection()

        # clear previous geocoding attempts if retry is True
        if retry:
            sql = (
                "select cast(ag_login_id as varchar2(100)) from ag_login "
                "where cannot_geocode = 'y'"
            )

            logins = self.dynamicMetadataSelect(sql)

            for row in logins:
                ag_login_id = row[0]
                self.updateGeoInfo(ag_login_id, '', '', '', '')

        # get logins that have not been geocoded yet
        sql = (
            'select city, state, zip, country, '
            'cast(ag_login_id as varchar2(100)) '
            'from ag_login '
            'where elevation is null '
            'and cannot_geocode is null'
        )

        logins = self.dynamicMetadataSelect(sql)

        row_counter = 0
        for row in logins:
            row_counter += 1
            if limit is not None and row_counter > limit:
                break

            ag_login_id = row[4]
            # Attempt to geocode
            address = '{0} {1} {2} {3}'.format(row[0], row[1], row[2], row[3])
            encoded_address = urllib.urlencode({'address': address})
            url = '/maps/api/geocode/json?{0}&sensor=false'.format(
                encoded_address)

            r = self.getGeocodeJSON(url)

            if r in ('unknown_error', 'not_OK'):
                # Could not geocode, mark it so we don't try next time
                self.updateGeoInfo(ag_login_id, '', '', '', 'y')
                continue
            elif r == 'over_limit':
                # If the reason for failure is merely that we are over the
                # Google API limit, then we should try again next time
                # ... but we should stop hitting their servers, so raise an
                # exception
                raise Exception, "Exceeded Google API limit"

            # Unpack it and write to DB
            lat, lon = r

            encoded_lat_lon = urllib.urlencode(
                {'locations': ','.join(map(str, [lat,lon]))})

            url2 = '/maps/api/elevation/json?{0}&sensor=false'.format(
                encoded_lat_lon)
            
            r2 = self.getElevationJSON(url2)

            if r2 in ('unknown_error', 'not_OK'):
                # Could not geocode, mark it so we don't try next time
                self.updateGeoInfo(ag_login_id, '', '', '', 'y')
                continue
            elif r2 == 'over_limit':
                # If the reason for failure is merely that we are over the
                # Google API limit, then we should try again next time
                # ... but we should stop hitting their servers, so raise an
                # exception
                raise Exception, "Exceeded Google API limit"

            elevation = r2

            self.updateGeoInfo(ag_login_id, lat, lon, elevation, '')

    def getMapMarkers(self):
        con = self.getMetadataDatabaseConnection()

        results = con.cursor()
        con.cursor().callproc('ag_get_map_markers', [results])

        # zipcode, latitude, longitude, marker_color
        return [(row[0], row[1], row[2], row[3]) for row in results]

    def getGeocodeJSON(self, url):
        conn = httplib.HTTPConnection('maps.googleapis.com')
        conn.request('GET', url)
        result = conn.getresponse()

        # Make sure we get an 'OK' status
        if result.status != 200:
            return 'not_OK'

        data = json.loads(result.read())
        conn.close()

        try:
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']
        except:
            # Unexpected format - not the data we want
            if data.get('status', None) == 'OVER_QUERY_LIMIT':
                return 'over_limit'
            else:
                return 'unknown_error'


        return (lat, lon)

    def getElevationJSON(self, url):
        """Use Google's Maps API to retrieve an elevation

        url should be formatted as described here:
        https://developers.google.com/maps/documentation/elevation/#ElevationRequests

        The number of API requests is limited to 2500 per 24 hour period.
        If this function is called and the limit is surpassed, the return value
        will be "over_limit".  Other errors will cause the return value to be
        "unknown_error".  On success, the return value is the elevation of the
        location requested in the url.
        """
        conn = httplib.HTTPConnection('maps.googleapis.com')
        conn.request('GET', url)
        result = conn.getresponse()

        # Make sure we get an 'OK' status
        if result.status != 200:
            return 'not_OK'

        data = json.loads(result.read())

        conn.close()

        try:
            elevation = data['results'][0]['elevation']
        except KeyError:
            # Unexpected format - not the data we want
            if data.get('status', None) == 'OVER_QUERY_LIMIT':
                return 'over_limit'
            else:
                return 'unknown_error'

        return elevation
        
    def updateGeoInfo(self, ag_login_id, lat, lon, elevation, cannot_geocode):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc(
            'ag_update_geo_info',
            [ag_login_id, lat, lon, elevation, cannot_geocode]
        )

    def addBruceWayne(self, ag_login_id, participant_name):
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('ag_insert_bruce_wayne', [ag_login_id, participant_name])

    def handoutCheck(self, username, password):
        con = self.getMetadataDatabaseConnection()
        is_handout = 'n'
        result = con.cursor().callproc('ag_is_handout', [is_handout, username, password])
        is_handout = result[0]

        return is_handout.strip()

    def checkBarcode(self, barcode):
        # return a tuple consists of:
        # site_sampled, sample_date, sample_time, participant_name,
        # environment_sampled, notes, etc (please refer to
        # ag_check_barcode_status.sql).
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_check_barcode_status', [barcode, results])
        barcode_details = results.fetchall()
        if barcode_details:
            return barcode_details[0]
        else: # if the barcode does not exist in database
            return ()

    def updateAGSurvey(self, ag_login_id, participant_name, field, value):
        con = self.getMetadataDatabaseConnection()
        # Make sure no single quotes get passed as it will break the sql string
        value = str(value).replace("'", "''")
        participant_name = str(participant_name).replace("'", "''")
        sql = """
        update ag_human_survey set {0} = '{1}' where ag_login_id = '{2}' and participant_name = '{3}'
        """.format(field, value, ag_login_id, participant_name)
        con.cursor().execute(sql)
        sql = ('commit')
        con.cursor().execute(sql)

    def getAGStats(self):
        # returned tuple consists of:
        # site_sampled, sample_date, sample_time, participant_name, environment_sampled, notes 
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('ag_stats', [results])
        ag_stats = results.fetchall()
        
        return ag_stats


    def updateAKB(self, barcode, moldy, overloaded, other, other_text, date_of_last_email):
        """ Update ag_kit_barcodes table.
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('update_akb', [barcode, moldy, overloaded, other, other_text, date_of_last_email])
