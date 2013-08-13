
"""
Centralized database access for the Qiime web app
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

class QiimeDataAccess(object):
    """
    Data Access implementation for all the Qiime web appliation
    
    This is the data access class for all Qiime web app applications. It can be used
    for production or testing depending on the connection class that's passed in.
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
    
    def convertToOracleHappyName(self, date_string):
        """ Oracle is picky about dates. This function takes a previously validated
        date format and returns a formatted string for inserting into database
        """
        formatted_date = ''
        
        # First handle the date portion since it must exist for a valid submission
        if date_string.find(' ') == -1:
            # Date only
            formatted_date = 'to_date(\'%s\', \'%s\')' % (date_string, 'MM/DD/YYYY')
        else:
            # Date and time exist
            formatted_date = 'to_date(\'%s\', \'%s\')' % (date_string, 'MM/DD/YYYY HH24:MI:SS')
        
        return formatted_date
        
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

    def deactivateWebAppUser( self, username, activation_code ):
        """ Attempts to deactivate user's account

        Attempt to deactivate the user account. If successful, returns True. 
        If not, the function returns False. Note: in the tests, this is part
        of the tearDown procedure.
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('deactivate_user_account', [username,activation_code])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def authenticateWebAppUser( self, username, password ):
        """ Attempts to validate authenticate the supplied username/password
        
        Attempt to authenticate the user against the list of users in
        web_app_user table. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getMetadataDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('qiime_assets.authenticate_user', [username, crypt_pass, user_data])
            row = user_data.fetchone()
            if row:
                user_data = {'web_app_user_id':row[0], 'email':row[1], 'password':row[2], \
                    'is_admin':row[3], 'is_locked':row[4], 'last_login':row[5],'verified':row[6]}
                return user_data
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getUserDetails(self, user_id):
        """ Gets the user data from the web_app_user table
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_user_details', [user_id, results])
            row = results.fetchone()
            if row:
                user_data = {'email':row[0], 'is_admin':row[1], 'is_locked':row[2], 'last_login':row[3]}
                return user_data
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def verifyActivationCode( self, username, activation_code ):
        """ Verify the user's activation code is correct.
        """
        try:
            con = self.getMetadataDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('verify_user_activation_code', [username, activation_code, user_data])
            row = user_data.fetchone()
            if row:
                return True
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def activateWebAppUser( self, username, activation_code ):
        """ Attempts to activate user's account

        Attempt to activate the user account. If successful, returns True. 
        If not, the function returns False.
        """
        try:
            con = self.getMetadataDatabaseConnection()
            user_data = con.cursor()

            con.cursor().callproc('verify_user_activation_code', [username, activation_code, user_data])
            row = user_data.fetchone()
            if row:
                con.cursor().callproc('activate_user_account', [username])
                return True
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def checkWebAppUserAvailability(self, username):
        """ Checks the availability of the supplied username
        """
        try:
            con = self.getMetadataDatabaseConnection()
            availability = con.cursor()
            con.cursor().callproc('check_username_availability', [username, availability])
            row = availability.fetchone()
            if row:
                return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def registerWebAppUser(self, username, password ,activation_code):
        """ Attempts to register a new user using the supplied username/password

        Attempt to register the user. If successful, a dict with user innformation is
        returned. If not, the function returns False.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getMetadataDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('web_app_user_insert', [username, crypt_pass, activation_code])
            return self.authenticateWebAppUser(username, password)
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def updateWebAppUserPwd( self, username, password ):
        """ Attempts to update the users password.
        """
        try:
            crypt_pass = crypt(password, username)
            con = self.getMetadataDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('update_web_app_user_password', [username, crypt_pass])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False  

    #####################################
    # Study
    #####################################

    def getSampleIDsFromStudy(self, study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_sample_ids_from_study', [study_id, results])
            metadata_fields = []
            for row in results:
                metadata_fields.append(row[0])
            return metadata_fields
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    #
    
    def createStudy(self, user_id, study_name, investigation_type, miens_compliant, submit_to_insdc, 
        portal_type, study_title, study_alias, pmid, study_abstract, study_description,
        principal_investigator, principal_investigator_contact, lab_person, lab_person_contact,
        includes_timeseries):
        """ Creates a study.
        """
        con = self.getMetadataDatabaseConnection()
        study_id = 0
        results = con.cursor().callproc('qiime_assets.study_insert', 
            [study_id, user_id, study_name, investigation_type, miens_compliant, submit_to_insdc, 
            portal_type, study_title, study_alias, pmid, study_abstract, study_description,
            principal_investigator, principal_investigator_contact, lab_person, lab_person_contact,
            includes_timeseries])
            
        return results[0]
            
    def updateStudy(self, study_id, study_name, investigation_type, miens_compliant, submit_to_insdc, 
        portal_type, study_title, study_alias, pmid, study_abstract, study_description,
        principal_investigator, principal_investigator_contact, lab_person, lab_person_contact,
        includes_timeseries):
        """ Updates a study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_update', 
                [study_id, study_name, investigation_type, miens_compliant, submit_to_insdc, 
                portal_type, study_title, study_alias, pmid, study_abstract, study_description,
                principal_investigator, principal_investigator_contact, lab_person, lab_person_contact,
                includes_timeseries])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def deleteStudy(self, study_id, full_delete):
        """ Removes a study from the database
        
        study_id: the numeric identifier for the study in the database
        full_delete: an integer value:
            0 = delete all BUT the study entry
            1 = delete all metadata including sample and sequence prep ids
            2 = delete everything including the study
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('qiime_assets.study_delete', [study_id, full_delete])
        
    def getStudyNames(self):
        """ Returns a list of study names
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_names', [results])
            study_name_list = []
            for row in results:
                if row[0] is None:
                    continue
                else:
                    study_name_list.append(row)
            return study_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getUserStudyNames(self, user_id, is_admin, portal_type):
        """ Returns a list of User's study names
        """
        try:
            con = self.getMetadataDatabaseConnection()
            study_names = con.cursor()
            con.cursor().callproc('qiime_assets.get_user_study_names', [user_id,
                                            is_admin, portal_type, study_names])
            study_name_list = []
            for row in study_names:
                if row[0] is None:
                    continue
                else:
                    study_name_list.append((row[0], row[1], row[2], row[3]))
            return study_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getUserAndPublicStudyNames(self, user_id, is_admin, portal_type):
        """ Returns a list of user's private studies along with all public 
            studies for the current portal type
        """
        public_studies = self.getUserStudyNames(0, is_admin, portal_type)
        all_studies = self.getUserStudyNames(user_id, is_admin, portal_type)
        if not public_studies and not all_studies:
            return
        elif public_studies:
            for item in public_studies:
                if item not in all_studies:
                    all_studies.append(item)
                
        return sorted(all_studies, key=lambda item: str(item[1]).lower())
        
    def getAllUserAndPublicStudyNames(self, user_id, is_admin):
        """ Returns a list of user's private studies along with all public 
            studies for all portal types
        """
        emp_public_studies = self.getUserStudyNames(0, is_admin, 'emp')
        qiime_public_studies = self.getUserStudyNames(0, is_admin, 'qiime')
        all_studies = self.getUserStudyNames(user_id, is_admin, portal_type)
        if not emp_public_studies and not qiime_public_studies and not all_studies:
            return

        for item in emp_public_studies:
            if item not in all_studies:
                all_studies.append(item)
                
        for item in qiime_public_studies:
            if item not in all_studies:
                all_studies.append(item)                

        return sorted(all_studies, key=lambda item: str(item[1]).lower())
    
    def getStudyInfo(self, study_id, web_app_user_id):
        """ Returns a list of metadata values based on a study type and list
        """
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('qiime_assets.get_study_info', [study_id, web_app_user_id, results])
        study_info = {}
        for row in results:
            study_info['submit_to_insdc'] = row[0]
            study_info['investigation_type'] = row[1]
            study_info['project_name'] = row[2]
            study_info['experimental_factor'] = row[3]
            study_info['study_alias'] = row[4]
            study_info['study_title'] = row[5]
            study_info['study_type'] = row[6]
            study_info['study_abstract'] = row[7]
            study_info['study_description'] = row[8]
            study_info['center_name'] = row[9]
            study_info['center_project_name'] = row[10]
            study_info['project_id'] = row[11]
            study_info['pmid'] = row[12]
            study_info['metadata_complete'] = row[13]
            study_info['sff_complete'] = row[14]
            study_info['mapping_file_complete'] = row[15]
            study_info['miens_compliant'] = row[16]
            study_info['can_delete'] = row[17]
            study_info['avg_emp_score'] = row[18]
            study_info['user_emp_score'] = row[19]
            study_info['number_samples_promised'] = row[20]
            study_info['number_samples_collected'] = row[21]
            study_info['principal_investigator'] = row[22]
            study_info['sample_count'] = row[23]               
            study_info['lab_person'] = row[24] 
            study_info['lab_person_contact'] = row[25]
            study_info['emp_person'] = row[26]
            study_info['first_contact'] = row[27]
            study_info['most_recent_contact'] = row[28]
            study_info['sample_type'] = row[29]
            study_info['has_physical_specimen'] = row[30]
            study_info['has_extracted_data'] = row[31]
            study_info['timeseries'] = row[32]
            study_info['spatial_series'] = row[33]
            study_info['principal_investigator'] = row[34]
            study_info['principal_investigator_contact'] = row[35]
            study_info['default_emp_status'] = row[36]
            study_info['funding'] = row[37]
            study_info['includes_timeseries'] = row[38]
            study_info['sample_count'] = row[39]
            study_info['ebi_study_accession'] = row[40]
            study_info['locked'] = row[41]
        return study_info

    def saveTimeseriesData(self, study_id, timeseries_file, req):
        con = self.getMetadataDatabaseConnection()
        
        # Delete a table if it exists already
        try:
            statement = 'drop table study_{0}_timeseries'.format(str(study_id))
            con.cursor().execute(statement)
        except:
            # If the table doesn't exist, this may toss an exception. We don't care,
            # just want to delete the table whether or not it exists
            pass
                
        # Dict for assigning data types:
        data_types = {}
        data_types['event_date_time'] = 'varchar2(50)'
        data_types['event_description'] = 'varchar2(2000)'
        data_types['event_duration'] = 'varchar2(100)'
        data_types['hours_since_experiment_start'] = 'varchar2(50)'
        data_types['sample_names'] = 'varchar2(4000)'
        data_types['host_subject_ids'] = 'varchar2(4000)'
        
        # Iterate over the remaining columns and create
        columns = []
        f = open(timeseries_file, 'rU')
        reader = csv.reader(f, delimiter='\t')        
        headers = reader.next()
        for column in headers:
            if column in data_types:
                data_type = data_types[column]
            else:
                data_type = 'varchar2(1000)'
            columns.append('{0} {1}'.format(column, data_type))

        # Create the new table based on file headers
        table_name = 'study_{0}_timeseries'.format(str(study_id))
        statement = 'create table {0} ({1})'.format(table_name, ','.join(columns))
        #req.write(statement)
        con.cursor().execute(statement)
            
        # Load the data rows
        for row in reader:
            values = ','.join(['\'' + item + '\'' for item in row])
            statement = 'insert into {0} values ({1})'.format(table_name, values)
            #req.write(statement)
            con.cursor().execute(statement)
            con.cursor().execute('commit')
            
        f.close()
        
        

    def getStudyPlatform(self,study_id):
        """ Returns a Run Prefix for Sample
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            db_output=[]
            con.cursor().callproc('qiime_assets.get_study_platform',\
                                                    [study_id,results])
                                                                
            run_prefix = ''
            for row in results:
                if row[0] is None:
                    continue
                else:
                    study_platform=row[0]
            return study_platform
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False


    #####################################
    # Metadata and EMP Stuff
    #####################################
    def createEMPStudy(self, user_id, study_name, investigation_type, miens_compliant, submit_to_insdc, 
        portal_type, study_title, study_alias, pmid, study_abstract, study_description,
        number_samples_collected, number_samples_promised , lab_person,
        lab_person_contact, emp_person, first_contact, most_recent_contact, sample_type, 
        has_physical_specimen, has_extracted_data, timeseries, spatial_series,
        principal_investigator, principal_investigator_contact, default_emp_status, funding,
        includes_timeseries):
        """ Creates an EMP study
        """
        con = self.getMetadataDatabaseConnection()
        study_id = 0
        results = con.cursor().callproc('qiime_assets.emp_study_insert', 
            [study_id, user_id, study_name,
            investigation_type, miens_compliant, submit_to_insdc, portal_type, 
            study_title, study_alias, pmid, study_abstract, study_description,
            number_samples_collected, number_samples_promised , lab_person,
            lab_person_contact, emp_person, first_contact, most_recent_contact, sample_type, 
            has_physical_specimen, has_extracted_data, timeseries, spatial_series,
            principal_investigator, principal_investigator_contact, default_emp_status, funding,
            includes_timeseries])
        return results[0]
        
    def updateEMPStudy(self, study_id, study_name, investigation_type, miens_compliant, submit_to_insdc, 
        portal_type, study_title, study_alias, pmid, study_abstract, study_description,
        number_samples_collected, number_samples_promised , lab_person,
        lab_person_contact, emp_person, first_contact, most_recent_contact, sample_type, 
        has_physical_specimen, has_extracted_data, timeseries, spatial_series,
        principal_investigator, principal_investigator_contact, default_emp_status, funding,
        includes_timeseries):
        """ Creates an EMP study
        """
        con = self.getMetadataDatabaseConnection()
        results = con.cursor().callproc('qiime_assets.emp_study_update', 
            [study_id, study_name, investigation_type, miens_compliant, submit_to_insdc, portal_type, 
            study_title, study_alias, pmid, study_abstract, study_description,
            number_samples_collected, number_samples_promised , lab_person,
            lab_person_contact, emp_person, first_contact, most_recent_contact, sample_type, 
            has_physical_specimen, has_extracted_data, timeseries, spatial_series,
            principal_investigator, principal_investigator_contact, default_emp_status, funding,
            includes_timeseries])

    def createStudyPackage(self, study_id, env_package):
        """ 
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_packages_insert', [study_id, env_package])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def clearStudyPackages(self, study_id):
        """ 
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.study_packages_delete', [study_id])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getStudyPackages(self, study_id):
        """ Returns a list env_package types associated to this study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_packages', [study_id, results])
            env_packages = []
            for row in results:
                env_packages.append(row[0])
            return env_packages
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def updateMetadataFlag(self, study_id, status):
        """ Updates the status of the metadata submission flag (y/n)
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.update_metadata_flag', [study_id, status])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def calcAgeInYears(self, study_id):
        """ Calculates a normalized age in years
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('calc_age_in_years', [study_id])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addSeqFile(self, study_id, file_path, file_type):
        """ adds a new SFF file to the study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_seq_file', [study_id, file_path, file_type])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
            
    def addSFFFileInfo(self, start_job, sff_filename, number_of_reads,header_length,
                    key_length, number_of_flows, flowgram_code, flow_characters,
                    key_sequence, md5_checksum, seq_run_id):
        """ appends the SFF info into the SFF_FILE table
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('add_sff_file',
                                                [sff_filename, number_of_reads,
                                                 header_length,key_length, 
                                                 number_of_flows, flowgram_code, 
                                                 flow_characters, key_sequence, 
                                                 md5_checksum,seq_run_id])
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False            

    def addMappingFile(self, study_id, mapping_file_path):
        """ adds a new mapping file to the study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_mapping_file', [study_id, mapping_file_path])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def addTemplateFile(self, study_id, template_file_path):
        """ adds a new mapping file to the study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_template_file', [study_id, template_file_path])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def clearStudyTemplates(self, study_id):
        """ adds a new mapping file to the study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.clear_study_templates', [study_id])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getEMPStudyList(self):
        """ Returns a list of emp studies
        """
        try:
            studies = []
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_emp_study_list', [results])
            for row in results:
                # study_id, sample_id, sample_name, project_name, study_title, email, sample_count, metadata_complete,
                # study_score, sample_score, s.number_samples_promised, s.number_samples_in_freezer, 
                # s.principal_investigator
                studies.append((row[0], row[1], row[2], row[3], row[4], row[5],
                    row[6], row[7], row[8], row[9], row[10], row[11], row[12]))
            return studies
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)

    def getPublicEMPDownloadLinks(self):
        """ Returns a list of emp studies
        """
        try:
            studies = []
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_public_emp_studies', [results])
            for row in results:
                # study_id, project_name, file_path, study_abstract
                studies.append((row[0], row[1], row[2], row[3]))
            return studies
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            
    def getEMPSampleList(self, study_id, web_app_user_id):
        """ Returns a list of emp studies
        """
        samples = []
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('qiime_assets.get_emp_sample_list', [study_id, web_app_user_id, results])
        for row in results:
            # sample_id, avg_emp_score, user_emp_score, sample_name, emp_status, sample_location, 
            # sample_progress, description, altitude, samp_size,
            # temp, samp_store_temp, country, depth, elevation, env_biome, env_feature, 
            # env_matter, ph, latitude, longitude, chem_administration, samp_store_loc
            samples.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
            row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], 
            row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22]))
            
            
        return samples
            
    def updateEMPSampleData(self, sample_id, sample_score, emp_status, web_app_user_id):
        """ Updates the sample emp database fields
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('qiime_assets.update_emp_sample_data', [sample_id, sample_score, emp_status, web_app_user_id])
            
    def updateEMPStudyData(self, study_id, study_score, web_app_user_id):
        """ Updates the emp database fields
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('qiime_assets.update_emp_study_data', [study_id, study_score, web_app_user_id])
    
    def getListFieldValue(self, vocab_value_id):
        """ Returns a list env_package types associated to this study
        """
        try:
            value = ''
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_list_field_value', [vocab_value_id, results])
            for row in results:
                value = row[0]
            return value
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)

    def verifySampleNames(self, study_id, file_sample_name_list):
        all_samples_present = True
        
        # Get the list of sample names for this study:
        database_sample_name_list = self.getSampleList(study_id)
        # Chop off the sample_id from the tuple - only want names for comparison
        database_sample_name_list = zip(*database_sample_name_list.items())[1]

        # If all samples in file are not present in list in database, need to reload
        common_names = set(file_sample_name_list).intersection(set(database_sample_name_list))
        
        # If any samples that used to exist in the database are missing...
        if len(common_names) < len(database_sample_name_list):
            return False
        
        # If the entire list is not a subset of what's in the database
        #if not set(file_sample_name_list).issubset(set(database_sample_name_list)):
        #    all_samples_present = False

        return all_samples_present

    def getSampleColumnValue(self, sample_id, table_name, column_name):
        """ Returns a field value
        """
        try:
            table_name = table_name.upper()
            column_name_upper = column_name.upper()
                
            value = None
            statement = ''
            
            if table_name == 'HOST':
                statement = 'select %s from host h inner join host_sample hs on h.host_id = hs.host_id inner join sample s on hs.sample_id = s.sample_id where s.sample_id = %s' %\
                    (column_name_upper, sample_id)
            elif table_name == 'HOST_SAMPLE':
                statement = 'select %s from host_sample hs inner join sample s on hs.sample_id = s.sample_id where s.sample_id = %s' %\
                    (column_name_upper, sample_id)
            else:
                statement = 'select "%s" from "%s" where sample_id = %s' % \
                    (column_name_upper, table_name, sample_id)

            con = self.getMetadataDatabaseConnection()
            results = con.cursor().execute(statement).fetchone()
            if not results:
                return None
            else:
                value = results[0]
            
            # Figure out if this is a list column. If so, do a reverse-lookup to get the text value
            field_details = self.getFieldDetails(column_name)
            database_data_type = field_details[1]
            if database_data_type == 'list':
                value = self.getListFieldValue(value)
            
            return value
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            print 'table_name: %s, column_name: %s, sample_id: %s' % (table_name, column_name, sample_id)
            return False
            
    def getPrepColumnValue(self, sample_id, row_number, table_name, column_name):
        """ Returns a field value
        """
        try:
            table_name = table_name.upper()
            column_name = column_name.upper()
                
            value = None
            statement = 'select "%s" from "%s" where sample_id = %s and row_number = %s' % \
                (column_name, table_name, sample_id, row_number)
            #print statement
            con = self.getMetadataDatabaseConnection()
            results = con.cursor().execute(statement).fetchone()
            value = results[0]
            
            # Figure out if this is a list column. If so, do a reverse-lookup to get the text value
            field_details = self.getFieldDetails(column_name)
            database_data_type = field_details[1]
            if database_data_type == 'list':
                value = self.getListFieldValue(value)

            return value
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getMetadataFields(self, study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_metadata_fields', [study_id, results])
            metadata_fields = []
            for row in results:
                metadata_fields.append((row[0], row[1]))
            return metadata_fields
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getSampleList(self, study_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_sample_list', [study_id, results])
            sample_list = {}
            for sample_name, sample_id in results:
                sample_list[sample_id] = sample_name
            return sample_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getSampleDetailList(self, study_id):
        """ Returns a list of metadata fields
        """
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('get_sample_detail_list', [study_id, results])
        sample_details = []
        for sample_name, sample_id, public, collection_date, run_prefix, sequence_count, otu_count, otu_percent_hit in results:
            sample_details.append((sample_name, sample_id, public, collection_date, run_prefix, sequence_count, otu_count, otu_percent_hit))
        return sample_details
            
    def getPrepList(self, sample_id):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_prep_list', [sample_id, results])
            sample_row_list = []
            for sample_id, row_number, num_sequences in results:
                sample_row_list.append((sample_id, row_number, num_sequences))
            return sample_row_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def removeStudyActualColumn(self, study_id, column_name):
        """ inserts a selected metadata column name into the database
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.remove_study_actual_column', [study_id, column_name])
        except Exception, e:            
            raise Exception('Exception caught in removeStudyActualColumns(): %s.\nThe error is: %s' % (type(e), e))

    def addStudyActualColumn(self, study_id, column_name, table_name):
        """ inserts a selected metadata column name into the database
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.add_study_actual_column', [study_id, column_name, table_name])
        except Exception, e:            
            raise Exception('Exception caught in addStudyActualColumns(): %s.\nThe error is: %s' % (type(e), e))
            
    def getStudyActualColumns(self, study_id):
        """ inserts a selected metadata column name into the database
        """
        try:
            con = self.getMetadataDatabaseConnection()
            extra_columns = {}
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_study_actual_columns', [study_id, results])
            #for row in results:
            for column_name, table_name in results:
                #extra_columns[row[0]] = row[1]
                extra_columns[column_name] = table_name
            
            return extra_columns
        except Exception, e:            
            raise Exception('Exception caught in addStudyActualColumns(): %s.\nThe error is: %s' % (type(e), e))
            
    def findExtraColumnMatch(self, column_name):
        """ Searches for a match in 'extra' tables
        """
        column_name = column_name.upper()
        con = self.getMetadataDatabaseConnection()
        matches = []
        results = con.cursor()
        con.cursor().callproc('qiime_assets.find_extra_column_match', [column_name, results])
        #for row in results:
        for row in results:
            matches.append(row[0])
        
        return matches
        
    def addCommonExtraColumn(self, req, study_id, found_extra_table, column_name, data_type, description):
        """ Factors an extra column into the common table
        """
        debug = False
        common_extra_table_name = None
        min_column_count = None
        quoted_column_name = '"{0}"'.format(column_name.upper())
        
        if 'SAMPLE' in found_extra_table:
            common_extra_table_name = 'COMMON_EXTRA_SAMPLE'
            min_column_count = 2
        elif 'PREP' in found_extra_table:
            common_extra_table_name = 'COMMON_EXTRA_PREP'
            min_column_count = 3
            
        if common_extra_table_name == None:
            raise Exception('Error: Could not determine the common extra table name. The found extra table is: %s' % found_extra_table)
            
        # Set the database data type:
        database_data_type = ''
        if data_type == 'text' or database_data_type == 'range':
            database_data_type = 'varchar2(4000)'
        elif data_type == 'numeric':
            database_data_type = 'int'
        elif data_type == 'date':
            database_data_type = 'date'
            
        if database_data_type == '':
            raise Exception('Could not determine common extra column data type.')

        # Create the column if it doesn't already exist
        statement = """
        select  count(*) 
        from    all_tab_columns 
        where   column_name = '{0}' 
                and table_name = '{1}'
        """.format(column_name.upper(), common_extra_table_name)
        if debug:
            req.write('<pre>' + statement + '</pre><br/>')
        con = self.getMetadataDatabaseConnection()
        results = con.cursor().execute(statement).fetchone()
        if results[0] == 0:
            statement = 'alter table %s add %s %s' % (common_extra_table_name, quoted_column_name, database_data_type)
            if debug:
                req.write('<pre>' + statement + '</pre><br/>')
            con.cursor().execute(statement)
        
        # Copy the data found in the found extra_table
        if common_extra_table_name == 'COMMON_EXTRA_SAMPLE':
            statement = """
            MERGE INTO common_extra_sample e
            USING (
                    SELECT  sample_id, {0}
                    FROM    {1}
                  ) x
                  ON (e.sample_id = x.sample_id)
            WHEN MATCHED THEN 
              UPDATE SET e.{0} = x.{0}
            WHEN NOT MATCHED THEN 
              INSERT (e.sample_id, e.{0})
              VALUES (x.sample_id, x.{0})
            """.format(quoted_column_name, found_extra_table)
        else:
            statement = """
            MERGE INTO common_extra_prep e
            USING (
                    SELECT  sample_id, row_number, {0}
                    FROM    {1}
                  ) x
                  ON (e.sample_id = x.sample_id and e.row_number = x.row_number)
            WHEN MATCHED THEN 
              UPDATE SET e.{0} = x.{0}
            WHEN NOT MATCHED THEN 
              INSERT (e.sample_id, e.row_number, e.{0})
              VALUES (x.sample_id, x.row_number, x.{0})
            """.format(quoted_column_name, found_extra_table)
        
        if debug:
            req.write('<pre>' + statement + '</pre><br/>')
        con.cursor().execute(statement)
        statement = 'commit'
        if debug:
            req.write('<pre>' + statement + '</pre><br/>')
        con.cursor().execute(statement)
        
        # Remove the column from the found extra table. If it's the last custom column in the table, remove the table
        statement = "select count(*) from all_tab_columns where table_name = '%s'" % (found_extra_table)
        if debug:
            req.write('<pre>' + statement + '</pre><br/>')
        results = con.cursor().execute(statement).fetchone()
        if results[0] <= min_column_count:
            statement = 'drop table %s' % (found_extra_table)
            if debug:
                req.write('<pre>' + statement + '</pre><br/>')
            con.cursor().execute(statement)
        else:
            statement = 'alter table %s drop column %s' % (found_extra_table, quoted_column_name)
            if debug:
                req.write('<pre>' + statement + '</pre><br/>')
            con.cursor().execute(statement)
        
        # Clean up references in study_actual_columns
        extra_table_study_id = found_extra_table.split('_')[2]

        statement = """
        update  study_actual_columns 
        set     table_name = '"{0}"' 
        where   study_id = {1} 
                and table_name = '"{2}"'
        """.format(common_extra_table_name, extra_table_study_id, found_extra_table)
        if debug:
            req.write('<pre>' + statement + '</pre><br/>')
        con.cursor().execute(statement)
        statement = 'commit'
        if debug:
            req.write('<pre>' + statement + '</pre><br/>')
        con.cursor().execute(statement)
            
    def addExtraColumnMetadata(self, study_id, table_level, column_name, description, data_type):
        """ inserts metadata for an "extra" column
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.extra_column_metadata_insert', [study_id, table_level, 
                column_name, description, data_type])
        except Exception, e:            
            raise Exception('Exception caught in addExtraColumnMetadata(): {0}.\nThe error is: {1}.\nstudy_id: \
                {2}\ntable_level: {3}\ncolumn_name: {4}\ndescription: {5}\n data_type: {6}'.format(type(e), e, \
                str(study_id), str(table_level), str(column_name), str(description), str(data_type)))
            
    def getExtraColumnMetadata(self, study_id):
        """ Retrieves all metadata for extra columns
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            extra_columns = {}
            con.cursor().callproc('qiime_assets.get_study_extra_columns', [study_id, results])
            for row in results:
                extra_columns[row[1]] = {'table_level':row[0], 'description':row[2], 'data_type':row[3]}
            return extra_columns
        except Exception, e:            
            raise Exception('Exception caught in getExtraColumnMetadata(): %s.\nThe error is: %s' % (type(e), e))
            
    def deleteExtraColumnMetadata(self, study_id):
        """ Deletes all metadata for extra columns
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.delete_study_extra_columns', [study_id])
        except Exception, e:            
            raise Exception('Exception caught in deleteExtraColumnMetadata(): %s.\nThe error is: %s' % (type(e), e))
    
    def getColumnDictionary(self):
        """ Returns the full column dictionary
        """
        try:
            column_dictionary = []
            con = self.getMetadataDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('qiime_assets.get_column_dictionary', [column_values])
            for row in column_values:
                # Skip if no column name is found
                if row[0] is None:
                    continue

                # Some variables to allow for re-assignment should any of them be None
                column_name = row[0].lower()
                expected_values = row[1]
                description = row[2]
                data_type = row[3]
                max_length = row[4]
                min_length = row[5]
                active = row[6]
                
                if row[1] == None:
                    expected_values == ''
                elif row[2] == None:
                    description == ''
                elif row[3] == None:
                    data_type = ''
                elif row[4] == None:
                    max_length = ''
                elif row[5] == None:
                    min_length = ''
                elif row[6] == None:
                    min_length = ''
                    
                list_item = (column_name, expected_values, description, data_type, max_length, min_length, active)
                column_dictionary.append(list_item)
            return column_dictionary
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getCustomColumnDetails(self, column_name):
        """ Returns details about a user-defined column
        """
        column_info = {}
        con = self.getMetadataDatabaseConnection()
        found = False
        column_name = column_name.upper()
        
        # Init some variables
        description = ''
        extra_table_name = ''
        common_table_name = ''
        data_type = ''
        
        # Figure out if exists in "Extra" table
        statement = """select table_name from all_tab_columns where column_name = '%s' and table_name like 'EXTRA_%%'"""\
            % column_name
        try:
            results = con.cursor().execute(statement).fetchone()
            extra_table_name = results[0]
            found = True
        except:
            extra_table_name = None
            
        # Figure out if exists in a factored table
        statement = """select table_name from all_tab_columns where column_name = '%s' and table_name like 'COMMON_EXTRA_%%'"""\
            % column_name
        try:
            results = con.cursor().execute(statement).fetchone()
            common_table_name = results[0]
            found = True
        except:
            common_table_name = None
        
        if found:
            try:
                statement = """select data_type, description from extra_column_metadata where upper(column_name) = '%s'""" % column_name
                results = con.cursor().execute(statement).fetchone()
                data_type = results[0]
                description = results[1]
            except:
                data_type = None
                description = None
        else:
            data_type = None
        
        column_info['description'] = description
        column_info['extra_table_name'] = extra_table_name
        column_info['common_table_name'] = common_table_name
        column_info['data_type'] = data_type
        
        return column_info
        
    def getPackageColumns(self, package_type_id):
        """ Returns the full package column dictionary
        """
        try:
            package_columns = []
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_package_columns', [package_type_id, results])

            for row in results:
                package_columns.append((row[0], row[1], row[2], row[3], row[4]))

            return package_columns

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getImmutableDatabaseFields(self, study_id):
        """ Returns the immutable metadata fields for a study
        """
        fields = []
        con = self.getMetadataDatabaseConnection()
        results = con.cursor()
        con.cursor().callproc('qiime_assets.get_immutable_database_fields', [study_id, results])
        for row in results:
            fields.append((row[0], row[1], row[2], row[3], row[4], row[5]))
        return fields
    
    fields = {}
    def findMetadataTable(self, field_name, field_type, log, study_id, lock):
        """ Finds the target metadata table for the supplied column name
        
        Determines which table a column belongs to based on field_name and type.
        """
        
        # log passed in from writeMetadataValue() - it's a list. At end of function, 
        # exception handler will output contents of log to web for viewing if error
        # occurrs.
        
        try:
            table = ''
            field_name = field_name.upper()
            field_name.replace('"', '')

            # Fill out the field list if it's the first call
            log.append('Length of fields is: {0}'.format(str(len(self.fields))))
            if len(self.fields) == 0:
                log.append('Filling out field list for table lookup. Current field is "{0}"'.format(field_name))
                lock.acquire()
                con = self.getMetadataDatabaseConnection()
                results = con.cursor()
                con.cursor().callproc('qiime_assets.find_metadata_table', [results])
                for tab_name, col_name in results:
                    if col_name not in self.fields:
                        self.fields[col_name] = []
                    self.fields[col_name].append(tab_name)
                lock.release()
            
            log.append('field{} successfully filled out')
            
            if field_name in self.fields:
                # If there's only one hit we can assign it
                tables = self.fields[field_name]
                log.append('Type of variable is: %s' % str(tables))
                if len(self.fields[field_name]) == 1:
                    table = self.fields[field_name][0]
                    log.append('Field only in one table: %s' % table)
                
                # More than one table was found with this column name. Find the correct one
                # based on the study id
                else:
                    log.append('Field in multiple tables(%s): %s' % (len(self.fields[field_name]), str(self.fields[field_name])))
                    log.append('Study is is: %s' % study_id)
                    for table_name in self.fields[field_name]:
                        if str(study_id) in table_name:
                            table = table_name
                            
            # If table is not found, assume user-defined column
            else:
                """ Code may look bizarre... but here's why:
                1. To streamline access and prevent blocking, we first check to see if the field
                does exist in the field list. If it does, we do not have to lock and can simply
                look up the table name.
                
                2. If field is not in list, it must be a new column. In this case we must lock the 
                code that handles new column creation. The catch is that if two threads both hit the lock
                with the same field name, one will get in and the other will block. Once the initial thread 
                exists, it will have handled the new column, gotten the appropriate table name, and returned. 
                The 2nd thread will now enter the critical section, however if we don't again check to see 
                if the field is now in the field list, it will attempt to create the same column again and 
                fail. Thus we check a 2nd time to see if the field exists and if so, simply read it from the 
                field list.                
                """
                lock.acquire()                
                if field_name in self.fields:
                    log.append('Field now exists. Pulling from local list.')
                    table = self.fields[field_name][0]
                    log.append('Table name exists. Using "%s".' % table)
                else:
                    log.append('Entities do not exist. Creating...')
                    table = self.handleExtraData(study_id, field_name, field_type, log)
                    log.append('Entities created. Table name is "%s"' % table)
                    if field_name not in self.fields:
                        self.fields[field_name] = [table]
                    else:
                        self.fields[field_name].append(table)
                lock.release()
           
            log.append('Returning from findMetadataTable with value: %s' % str(table))
            return table

        except Exception, e:
            lock.release()
            log.append('Exception caught: %s' % str(e))
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception('\n'.join(log))

    def getFieldDetails(self, field_name):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            value_list = []
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_field_details', [field_name, results])

            for row in results:
                # column_name, data_type, desc_or_value, definition, active
                value_list.append((row[0], row[1], row[2], row[3], row[4]))
                
            if len(value_list) == 0:
                # If not found in the dictionary, assume this is a user-created column
                value_list.append((field_name, 'text', '', ''))
                
            return value_list[0]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def getTableCategory(self, table_name):
        table_category = ''
        table_name = table_name.upper()
        if '"' not in table_name:
            table_name = '"%s"' % table_name
        
        if table_name == '"STUDY"' or 'EXTRA_STUDY_' in table_name:
            table_category = 'study'
        elif table_name in ['"AIR"', '"COMMON_FIELDS"', '"MICROBIAL_MAT_BIOFILM"', '"OTHER_ENVIRONMENT"', \
            '"SAMPLE"', '"SEDIMENT"', '"SOIL"', '"WASTEWATER_SLUDGE"', '"WATER"', \
            '"HOST_ASSOC_VERTIBRATE"', '"HOST_ASSOCIATED_PLANT"', '"HOST_SAMPLE"', '"HUMAN_ASSOCIATED"'] \
            or 'EXTRA_SAMPLE_' in table_name or 'EXTRA_PREP_' in table_name:
            table_category = 'sample'
        elif table_name in ['"HOST"']:
            table_category = 'host'
        elif table_name == '"SEQUENCE_PREP"' or 'EXTRA_PREP_' in table_name:
            table_category = 'prep'
            
        return table_category

    def createSampleKey(self, study_id, sample_name):
        """ Writes a sample key row to the database
        """
        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.sample_insert', [study_id, sample_name])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def createPrepKey(self, study_id, sample_name, row_number, barcode, linker, primer, run_prefix):
        """ Writes a prep key row to the database
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('qiime_assets.prep_insert', [study_id, sample_name, row_number, barcode, linker, primer, run_prefix])

    def createHostKey(self, study_id, sample_name, host_subject_id):
        """ Writes a host key row to the database
        """
        try:
            host_subject_id = '{0}:{1}'.format(str(study_id), host_subject_id)
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.host_insert', [study_id, sample_name, host_subject_id])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def handleExtraData(self, study_id, field_name, field_type, log):
        
        # Get our database connection
        con = self.getMetadataDatabaseConnection()
        
        # Define the names of the 'extra' tables
        extra_table = ''
        key_table = ''
        
        # Other required values
        schema_owner = 'QIIME_METADATA'
        statement = ''
        
        # Figure out which table we're talking about
        if field_type == 'study':
            extra_table = str('extra_study_' + str(study_id)).upper()
            key_table = 'study'
        elif field_type == 'sample':
            extra_table = str('extra_sample_' + str(study_id)).upper()
            key_table = 'sample'
        elif field_type == 'prep':
            extra_table = str('extra_prep_' + str(study_id)).upper()
            key_table = 'sample'
        else:
            # Error state
            raise Exception('Could not determine "extra" table name. field_type is "%s"' % (field_type))        
        try:
            # Does table exist already?
            log.append('Checking if table %s exists...' % extra_table)
            named_params = {'schema_owner':schema_owner, 'extra_table':extra_table}
            statement = 'select * from all_tables where owner = :schema_owner and table_name = :extra_table'
            statement = str(statement)
            log.append(statement)
            log.append('schema_owner: %s' % schema_owner)
            log.append('extra_table: %s' % extra_table)
            results = con.cursor().execute(statement, named_params).fetchone()
            log.append('Table search results: %s' % str(results))
        
            # Create if it doesn't exist already
            if not results:
                log.append('Creating "extra" table %s...' % extra_table)
                statement = 'create table %s (%s_id int not null, \
                    constraint fk_%s_sid foreign key (%s_id) references %s (%s_id))' % \
                    (extra_table, key_table, extra_table, key_table, key_table, key_table)
                statement = str(statement)
                log.append(statement)
                results = con.cursor().execute(statement)

                # If it's a prep table, must create row_number column
                if field_type == 'prep':
                    log.append('Adding row_number to extra_prep table...')                        
                    statement = 'alter table %s add row_number integer' % (extra_table)
                    statement = str(statement)
                    log.append(statement)
                    results = con.cursor().execute(statement)

                if field_type == 'prep':
                    statement = 'alter table %s add constraint pk_%s primary key (%s_id, row_number)'\
                        % (extra_table, extra_table, key_table)
                else:
                    statement = 'alter table %s add constraint pk_%s primary key (%s_id)'\
                        % (extra_table, extra_table, key_table)
                statement = str(statement)
                log.append(statement)
                results = con.cursor().execute(statement)
                    
                # In the study case, we must also add the first (and only) row for the subsequent updates to succeed.
                if field_type == 'study':
                    log.append('Inserting study extra row...')                        
                    statement = 'insert into %s (study_id) values (%s)' % (extra_table, study_id)
                    statement = str(statement)
                    log.append(statement)
                    results = con.cursor().execute(statement)
                    con.cursor().execute('commit')
            else:
                log.append('Extra table already exists.')
                            
            # Check if the column exists
            log.append('Checking if extra column exists: %s' % field_name)
            named_params = {'schema_owner':schema_owner, 'extra_table_name':extra_table, 'column_name':field_name.upper()}
            statement = 'select * from all_tab_columns where owner = :schema_owner and table_name = :extra_table_name and column_name = :column_name'
            statement = str(statement)
            log.append(statement)
            log.append('schema_owner: %s, extra_table_name: %s, column_name: %s' %
                (schema_owner, extra_table, field_name))
            results = con.cursor().execute(statement, named_params).fetchone()
            log.append('Results are: %s' % (str(results)))

            # If column doesn't exist, add it:
            if not results:
                log.append('Column does not exist. Creating extra column: %s' % field_name)
                statement = 'alter table %s add "%s" varchar2(4000) default \'\'' % (extra_table, field_name.upper())
                statement = str(statement)
                log.append(statement)
                results = con.cursor().execute(statement)
                log.append('Column added. Results are: %s. Extra table is: %s' % (str(results), extra_table))
            else:
                log.append('Column already exists.')

            # Return the proper table name
            log.append('Returning extra table as %s' % extra_table)
            return extra_table
        except Exception, e:
            log.append('Exception caught creating entities. Exception was: "%s"' % str(e))
            raise Exception(str(e))
    
    def writeMetadataValue(self, field_type, key_field, field_name, field_value, \
        study_id, host_key_field, row_num, lock):
        """ Writes a metadata value to the database
        """
        
        # This is a mess and it's slow right now. In need of serious speed improvements and cleanup.
        
        statement = ''
        log = []
        pk_name = ''

        try:
            #lock.acquire()
            
            # Get our database connection
            con = self.getMetadataDatabaseConnection()
            
            # Set the timeout
            #con.cursor().execute('alter session set ddl_lock_timeout=100')            
                        
            # Find the table name
            log.append('Locating table name...')
            table_name = None
            table_name = self.findMetadataTable(field_name, field_type, log, study_id, lock)
            log.append('Successfully found table name. Table name is "%s"' % str(table_name))
            
            #if field_name == 'dw1':
            #    raise Exception('asdf')

            # Double-quote for database safety
            log.append('Adding quotes to table name...')
            table_name = '"' + table_name + '"' 
            log.append('Quoted table name is %s' % table_name)
            log.append('Table name found: %s' % (table_name))
            
            # Store the field name in the database. These are the field names which will
            # be used later to generate a mapping file. We collect the names here because
            # it's an expensive operation to determine post-commit which fields were
            # actually submitted to the database.
            log.append('Attempting to store values in study_actual_columns: %s, %s, %s'\
                % (study_id, field_name, table_name))
            self.addStudyActualColumn(study_id, field_name, table_name);
            
            # Get extended field info from the database
            log.append('Loading field details...')
            field_details = self.getFieldDetails(field_name)
            log.append(str(field_details))
            if field_details == None:
                log.append('Could not obtain detailed field information. Skipping.')
                raise Exception
            else:
                database_data_type = field_details[1]
                log.append('Read field database data type as "%s"' % database_data_type)
            
            # If the field value is 'unknown', switch to 'null' (empty string is the same as null)
            #pass_values = 
            if str(field_value).upper() == 'UNKNOWN':
                field_value = ''
            # Figure out if this needs to be an integer ID instead of a text value
            elif database_data_type == 'list':
                log.append('Field is of type list. Looking up integer value...')
                named_params = {'field_value':field_value.upper()}
                statement = 'select vocab_value_id from controlled_vocab_values where upper(term) = :field_value'
                statement = str(statement)
                log.append(statement)
                results = con.cursor().execute(statement, named_params).fetchone()
                if results != None:
                    # If found, set the field_value to its numeric identifier for storage
                    log.append('Value found in controlled_vocab_values. Old field value: "%s", new field value: "%s".'\
                        % (field_value, results[0]))
                    field_value = results[0]
                else:
                    log.append('Could not determine inteteger value for list term "%s" with value "%s". Skipping.'\
                        % (field_name, field_value))
                    raise Exception
            
            # Set the field_name to it's quoted upper-case name to avoid key-work issues with Oracle
            field_name = '"%s"' % field_name.upper()
            
            ########################################
            ### For STUDY
            ########################################
            
            # Study is special - handle separately since row is guaranteed to exist and there can only be one row
            if table_name == '"STUDY"' or 'EXTRA_STUDY_' in table_name:
                log.append('Updating study field...')
                named_params = {'field_value':field_value, 'study_id':study_id}
                statement = 'update %s set %s = :field_value where study_id = :study_id' % (table_name, field_name)
                statement = str(statement)
                log.append(statement)
                log.append('field_value = "%s", study_id = "%s"' % (field_value, study_id))
                results = con.cursor().execute(statement, named_params)
                con.cursor().execute('commit')
                log.append('Study updated.')
                #raise Exception
                return
            
            ########################################
            ### For other tables
            ########################################
            
            if table_name in ['"AIR"', '"COMMON_FIELDS"', '"MICROBIAL_MAT_BIOFILM"', '"OTHER_ENVIRONMENT"', \
            '"SAMPLE"', '"SEDIMENT"', '"SOIL"', '"WASTEWATER_SLUDGE"', '"WATER"', '"SEQUENCE_PREP"', \
            '"HOST_ASSOC_VERTIBRATE"', '"HOST_ASSOCIATED_PLANT"', '"HOST_SAMPLE"', '"HUMAN_ASSOCIATED"',
            '"COMMON_EXTRA_SAMPLE"', '"COMMON_EXTRA_SAMPLE_2"', '"COMMON_EXTRA_PREP"'] \
            or 'EXTRA_SAMPLE_' in table_name or 'EXTRA_PREP_' in table_name:
                named_params = {'key_field':key_field, 'study_id':study_id}
                statement = 'select sample_id from "SAMPLE" where sample_name = :key_field and study_id = :study_id'
                statement = str(statement)
                key_column = 'sample_id'
                key_table = '"SAMPLE"'
            elif table_name in ['"HOST"']:
                named_params = {'key_field':'{0}:{1}'.format(str(study_id), host_key_field)}
                statement = 'select host_id from "HOST" where host_subject_id = :key_field'
                statement = str(statement)
                key_column = 'host_id'
                key_table = '"HOST"'
            else:
                return 'Unknown table found - no action taken. Table name was: "%s". Column name was: "%s"'\
                    % (table_name, field_name)
            
            # Find the assocaited key column
            log.append('Determining if required key row exists...')
            log.append(statement + '", key_field is ' + key_field + ', study_id is ' + str(study_id))
            results = con.cursor().execute(statement, named_params).fetchone()
            if results != None:
                key_column_value = results[0]
                log.append('Found key_column_value: %s' % str(key_column_value))
            else:
                log.append('Could not determine key. Skipping write for field %s with value "%s".'\
                    % (field_name, field_value))
                raise Exception











            ####### to speed up access, create local storage for all items already seen



            # If it ain't there, create it
            log.append('Checking if row already exists...')
            
            # Must append row_num if sequence table
            if table_name == '"SEQUENCE_PREP"' or table_name == '"COMMON_EXTRA_PREP"' or 'EXTRA_PREP_' in table_name:
                named_params = {'key_column_value':key_column_value, 'row_number':row_num}
                statement = 'select 1 from %s where %s = :key_column_value and row_number = :row_number'\
                    % (table_name, key_column)
            else:
                named_params = {'key_column_value':key_column_value}
                statement = 'select 1 from %s where %s = :key_column_value' % (table_name, key_column)
            statement = str(statement)
            log.append(statement)
            results = con.cursor().execute(statement, named_params).fetchone()
                
            if results == None:
                log.append('No row found, inserting new row')
                if table_name == '"SEQUENCE_PREP"' or table_name == '"COMMON_EXTRA_PREP"' or 'EXTRA_PREP_' in table_name:
                    log.append('Row number is %s' % (str(row_num)))
                    named_params = {'key_column_value':key_column_value, 'row_number':row_num}
                    statement = 'insert into %s (%s, row_number) values (:key_column_value, :row_number)'\
                        % (table_name, key_column)
                else:
                    named_params = {'key_column_value':key_column_value}
                    statement = 'insert into %s (%s) values (:key_column_value)' % (table_name, key_column)
                statement = str(statement)
                log.append(statement)
                con.cursor().execute(statement, named_params)






            
            # Attempt to write the metadata field
            log.append('Writing metadata value...')
            
            # If it's a date, must not put quotes around the oracle to_date function.
            if database_data_type == 'date':
                field_value = self.convertToOracleHappyName(field_value)
                if table_name == '"SEQUENCE_PREP"' or table_name == '"COMMON_EXTRA_PREP"' or 'EXTRA_PREP_' in table_name:
                    statement = 'update %s set %s = %s where %s = %s and row_number = %s'\
                        % (table_name, field_name, field_value, key_column, key_column_value, row_num)
                else:  
                    statement = 'update %s set %s = %s where %s = %s'\
                        % (table_name, field_name, field_value, key_column, key_column_value)            
            else:            
                if table_name == '"SEQUENCE_PREP"' or table_name == '"COMMON_EXTRA_PREP"' or 'EXTRA_PREP_' in table_name:
                    statement = 'update %s set %s = \'%s\' where %s = %s and row_number = %s'\
                        % (table_name, field_name, field_value, key_column, key_column_value, row_num)
                else:  
                    statement = 'update %s set %s = \'%s\' where %s = %s'\
                        % (table_name, field_name, field_value, key_column, key_column_value)
            statement = str(statement)
            log.append(statement)
            results = con.cursor().execute(statement)
            
            # Finally, commit the changes
            results = con.cursor().execute('commit')

            #if field_name == '"DW1"':
            #    raise Exception('Found DW1: Dumping log')
            
        except Exception, e:
            call_string = 'writeMetadataValue("%s", "%s", "%s", "%s", "%s")'\
                % (field_type, key_field, field_name, field_value, study_id)
            log_string = '<br/>'.join(log)
            error_msg = 'Exception caught attempting to store field "%s" with value "%s" into \
                table "%s".<br/>Method signature: %s<br/>Full error log:<br/>%s<br/>Oracle says: %s' % \
                (field_name, field_value, table_name, call_string, log_string, str(e))
            raise Exception(error_msg)
        finally:
            # Release the lock
            #lock.release()
            log.append('Lock released')

            
    #####################################
    # Jobs
    #####################################
    def createTorqueJob(self, job_type, job_input, user_id, study_id, job_state_id=-1):
        """ submits a job to the queue and returns the job_id
        """
        con = self.getSFFDatabaseConnection()
        job_id = 0
        job_id = con.cursor().callproc('create_torque_job', [job_type, job_input, user_id, study_id, job_state_id,job_id])
        return job_id[5]
    

    def updateTorqueJob(self, job_id, new_state,job_notes):
        """ updates a torque job and returns the job_id
        """
        try:
            con = self.getSFFDatabaseConnection()
            job_id = con.cursor().callproc('update_torque_job', [job_id, new_state, job_notes[-4000:]])
            return job_id[0]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            
    
    def clearTorqueJob(self, job_id):
        """ Removes a job from the torque_jobs table
        """
        
        try:
            con = self.getSFFDatabaseConnection()
            con.cursor().callproc('clear_torque_job', [job_id])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception(str(e))
    #
    def getJobInfo(self, study_id,job_type):
        """ returns job information
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            jobs = []
            con.cursor().callproc('get_job_info', [study_id,job_type,results])
            for row in results:
                jobs.append({'job_id':row[0], 'job_type_name':row[1], 'job_arguments':row[2], \
                    'user_id':row[3], 'job_state_name':row[4], 'job_notes':row[5],'job_type_id':row[6]})
            return jobs
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    #####################################
    # Ontologies and Lists
    #####################################
    
    def getAllControlledVocabs(self):
        """ Returns all controlled vocabularies
        """
        controlled_vocabs = {}
        
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_controlled_vocab_list_all', [results])
            for row in results:
                controlled_vocabs[row[0]] = row[1]
            
            return controlled_vocabs
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getControlledVocabs(self, column_name):
        """ Returns controlled vocabularies associated to the supplied column name
        """
        controlled_vocabs = []
        
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_controlled_vocab_list', [results, column_name])
            for row in results:
                controlled_vocabs.append(row[0])

            return controlled_vocabs
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
        
    def getControlledVocabValueList(self, controlled_vocab_id):
        """ Returns the controlled vocabulary values
        """
        vocab_items = {}

        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_controlled_vocab_values', [controlled_vocab_id, results])
            for row in results:
                vocab_items[row[0]] = row[1]

            return vocab_items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getOntologies(self, column_name):
        """ Returns a list of Ontologies
        """
        ontologies = []
        
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_ontology_list', [results, column_name])
            for row in results:
                ontologies.append(row[0])

            return ontologies
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getListValues(self, list_name):
        """ Returns list values
        """
        try:
            list_values = []
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_list_values', [results, list_name])
            
            for row in results:
                list_values.append((row[0], row[1]))
                    
            return list_values
            
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    def validateListValue(self, list_name, list_value):
        """ validates a list value
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = 0
            results = con.cursor().callproc('qiime_assets.validate_list_value', [list_name, list_value, results])
            return results[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    def getOntologyValues(self, ontology_name):
        """ Returns ontology values
        """
        try:
            ontology_values = []
            con = self.getOntologyDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_ontology_values', [results, ontology_name])

            for row in results:
                ontology_values.append(row[0])

            return ontology_values

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def validateOntologyValue(self, ontology_name, identifier_value):
        """ validates an ontology value
        """
        try:
            con = self.getOntologyDatabaseConnection()
            results = 0
            results = con.cursor().callproc('validate_ontology_value', [ontology_name, identifier_value, results])
            return results[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def get_column_ontology_details(self, column_name):
        """ Returns ontology details for a particular column
        """
        ontology_details = []
        
        try:
            con = self.getMetadataDatabaseConnection()
            ontologies = con.cursor()
            con.cursor().callproc('qiime_assets.get_column_ontologies', [column_name, ontologies])
            query_results=[]
            for row in ontologies:
                # row[0] = short_name
                # row[1] = bioportal_id
                # row[2] = ontology_branch_id
                ontology_details.append((row[0], row[1], row[2]))
            return ontology_details
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    def getTermMatches(self, column_name, term_value):
        """ Finds close term matches for columns of type ontology or list
        """
        try:
            # Handle the ontology prefix:
            term_parts = term_value.split(':')
            if len(term_parts) > 1:
                term_value = term_parts[1]
            
            details = self.getFieldDetails(column_name)
            if len(details) == 0:
                return None
            
            matches = []
            column_type = details[1]
            
            if column_type == 'list':
                con = self.getMetadataDatabaseConnection()
                results = con.cursor()
                con.cursor().callproc('qiime_assets.get_list_matches', [column_name, term_value, results])
                for row in results:
                    matches.append(row[1])
            elif column_type == 'ontology':
                con = self.getMetadataDatabaseConnection()
                ontologies = con.cursor()
                con.cursor().callproc('qiime_assets.get_column_ontologies', [column_name, ontologies])
                for row in ontologies:
                    con_tology = self.getOntologyDatabaseConnection()
                    results = con_tology.cursor()
                    con_tology.cursor().callproc('get_ontology_terms', 
                        ['\'' + row[0] + '\'', term_value.upper(), results])
                    for row in results:
                        matches.append(row[1])
            else:
                # Do nothing for all other types
                return None
            
            return matches
        
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def get_list_of_ontologies(self):
        """ Returns a list of metadata values based on a study type and list
        """
        try:
            con = self.getOntologyDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('get_list_of_ontologies', [column_values])
            query_results=[]
            for row in column_values:
                if row[0] is None:
                    continue
                query_results.append(row)
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def get_ontology_terms(self, ontology, query):
        """ Returns a list of ontology terms if the term contains query as a
            substring.
            
            Note: ontology can be a list of ontologies, and as such the value, whether
            singular or multiple, must be quoted: e.g. '\'FMA\'', or '\'FMA\', \'OBI\''
        """
        try:
            con = self.getOntologyDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('get_ontology_terms', [ontology, query, column_values])
            query_results=[]
            for row in column_values:
                if row[1] is None:
                    continue
                query_results.append(row[1])
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def validity_of_ontology_term(self, ontology, query):
        """ Returns a list of ontology terms if the query is exactly equal to 
            the term.
        """
        try:
            con = self.getOntologyDatabaseConnection()
            column_values = con.cursor()
            con.cursor().callproc('validity_of_ontology_term', [ontology, query, column_values])
            query_results=[]
            for row in column_values:
                if row[1] is None:
                    continue
                query_results.append(row[1])
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                
    #####################################
    # Loading
    #####################################
    
    def getSFFFiles(self, study_id):
        """ Gets a list of SFF files for this study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            items = []
            con.cursor().callproc('qiime_assets.get_sff_files', [study_id, results])
            for row in results:
                items.append(row[0])
            return items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getMappingFiles(self, study_id):
        """ Gets a list of mapping files for this study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            items = []
            con.cursor().callproc('qiime_assets.get_mapping_files', [study_id, results])
            for row in results:
                items.append(row[0])
            return items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getStudyTemplates(self, study_id):
        """ Gets a list of template files for this study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            items = []
            con.cursor().callproc('qiime_assets.get_study_templates', [study_id, results])
            for row in results:
                items.append(row[0])
            return items
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False        



    def getSplitLibrariesMappingFileData(self, study_id):
        """ Returns a collection of data sets, one for each run_prefix in the study

        This funciton generates a collection of result sets for producing the minimal
        mapping file required by split_libraries.py. There will be one result set for
        each run_prefix found in the study. Each result set consists of only the few 
        required fields for split_libraries.py to run.
        """

        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            result_sets = {}
            con.cursor().callproc('qiime_assets.get_split_libarary_data', [study_id, results])

            mapping_file_header = '#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tRunPrefix\tDescription'
            #for column in results.description:
            #    mapping_file_header += column[0] + '\t'

            for row in results:
                linker = row[2]
                primers = row[3]
                run_prefix = row[4]
                linker_primer_list = ''
                    
                # handles null linkers
                if linker is None:
                    linker=''
                if primers is None:
                    primers=''
                # Create a comma-separated list of linker+primer sequences
                if ',' in primers:
                    primer_list = primers.split(',')
                    for primer in primer_list:
                        linker_primer_list += '{0}{1},'.format(linker, primer)
                
                    # Strip the trailing comma
                    linker_primer_list = linker_primer_list[:-1]
                else:
                    linker_primer_list = linker + primers

                # Adjust the row contents
                newrow = (row[0], row[1], linker_primer_list, row[4], row[5])

                # If this is the first time we've seen this run_prefix, create a new list 
                # to hold the rows
                if run_prefix not in result_sets:
                    result_sets[run_prefix] = []

                # Add the row to the right run_prefix heading
                result_sets[run_prefix].append(newrow)

            #raise Exception(str(result_sets))

            return mapping_file_header, result_sets
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception(str(e))

    def clearSplitLibrariesMappingFiles(self, study_id):
        """ Clears split lib mapping files by study id
        """

        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.clear_split_lib_map_files', [study_id])
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception(str(e))


    def checkRunPrefixBarcodeLengths(self, study_id, run_prefix):
        """ Checks to make sure all barcode lengths are the same for a given run_prefix
        """

        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_run_prefix_bc_lengths', [study_id, run_prefix, results])
            barcode_length = 0

            # Make sure we get only one result back. If more than one length is returned, we must
            # raise an error:
            rows = results.fetchall()
            if len(rows) == 0:
                raise ValueError('No barcodes were found for the given run prefix: %s' % run_prefix)
            
            # we now allow for variable barcode lengths
            if len(rows) > 1:
                #raise ValueError('All barcodes must be of the same length for a given run_prefix. Multiple barcode lengths found for run prefix: %s' % run_prefix)
                barcode_length = 'variable_length'
            else:
                # Figure out if the length is one of the expected barcde lengths:
                barcode_length = rows[0][0]
                # If barcode is null, set length to 0
                if not barcode_length:
                    barcode_length = 0
                
            acceptable_barcode_lengths = ['0', '4', '5', '6', '7', '8', '9', '10', '11', '12','13','14','15','variable_length']
            if str(barcode_length) not in acceptable_barcode_lengths:
                raise ValueError('Barcode lengths must be one of the following: ' + ', '.join(acceptable_barcode_lengths))
            
            # Looks like we're good! Return the length
            return barcode_length

        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception(str(e))



    def clearMetaFiles(self, meta_id,fpath):
        """ Removes a job from the torque_jobs table
        """

        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('clear_meta_analysis_files', [meta_id,fpath])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception(str(e))

    def clearSFFFile(self, study_id, sff_file):
        """ Removes an sff file from the database
        """

        try:
            con = self.getMetadataDatabaseConnection()
            con.cursor().callproc('qiime_assets.clear_sff_file', [study_id, sff_file])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            raise Exception(str(e))
    
    def loadSplitLibInfo(self, start_job, analysis_id, run_date, cmd, svn_version,
                            log_str, hist_str, md5_input_file):
        """ uploads the information related to the split_libraries run to the DB
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            split_lib_run_id=1
            if start_job:
                db_output=con.cursor().callproc('register_split_library_run',
                                        [analysis_id,run_date, cmd, svn_version,\
                                         log_str, hist_str, md5_input_file,\
                                         split_lib_run_id,error_flag])
                if db_output[8]==0:
                    return True,db_output[7]
                else:
                    return False,db_output[7]
            else:
                return True,0
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False,0
    

    def loadAllOTUInfo(self, start_job, otu_run_set_id, run_date,
                    pOTUs_method, pOTUs_threshold, svn_version, pick_otus_cmd, 
                    otus_log_str,split_lib_seqs_md5,ref_set_name,
                    ref_set_threshold, analysis_id):
        """ loads the information pertaining to an OTU picking runs
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            otu_picking_run_id=0
            if start_job:
                db_output=con.cursor().callproc(\
                        'REGISTER_OTU_PICK_RUN_ALL',[analysis_id, otu_run_set_id, run_date, \
                                pOTUs_method, \
                                pOTUs_threshold, svn_version, pick_otus_cmd, \
                                otus_log_str,split_lib_seqs_md5,ref_set_name, \
                                ref_set_threshold, error_flag, \
                                otu_picking_run_id])
                if db_output[11]==0:
                    return True,db_output[1],db_output[12]
                else:
                    return False,db_output[1],db_output[12]
            else:
                return True,0
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    

    def getTestFlowData(self, start_job,analysis_id, sample_id):
        """ Returns the FLOW TEST Data from DB
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_flow_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getTestSplitLibData(self, start_job,analysis_id, sample_id):
        """ Returns the SPLIT_LIBRARY TEST Data
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_split_lib_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getTestOTUData(self, start_job,analysis_id, sample_id):
        """ Returns the OTU TEST DATA
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_otu_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getTestOTUFailureData(self, start_job,analysis_id, sample_id):
        """ Returns the OTU FAILURE TEST DATA
        """
        analysis_data = []
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_test_otu_failure_data', 
                                        [analysis_id, sample_id,results])
                for row in results:
                    analysis_data.append(row)
                return analysis_data[0]
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
                    
    def deleteTestAnalysis(self, start_job,analysis_id):
        """ Removes rows from the DB given an analysis id
        """
        analysis_data = []
        error_flag = 1
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('delete_test_analysis', 
                                        [analysis_id, error_flag])
                if db_output[1]==0:
                    return True
                else:
                    return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def deleteAllAnalysis(self, study_id):
        """ Removes rows from the DB given a study_id
        """
        error_flag = 1
        
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor().execute('select analysis_id from analysis where study_id = %s' % study_id)
            for result in results:
                db_output = con.cursor().callproc('delete_test_analysis', [result[0], error_flag])
                if db_output[1] == 0:
                    continue
                else:
                    return 'Could not remove analysis results from analysis_id: %s' % str(analysis_id)
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def loadOTUFailuresAll(self, start_job, input_set):
        """ starts process of importing failed otus
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_otu_failures_all_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def checkIfSFFExists(self, md5_checksum):
        """ determine if the SFF is already in the DB
        """
        try:
            con = self.getSFFDatabaseConnection()
            sff_exists=0
            db_output=con.cursor().callproc('check_if_sff_file_exists',
                                            [str(md5_checksum),sff_exists])
            if db_output[1] > 0:
                return True
            else:
                return False
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def getSeqRunIDUsingMD5(self, md5_checksum):
        """ returns the SEQ_RUN_ID given an md5_checksum
        """
        try:
            con = self.getSFFDatabaseConnection()
            seq_run_id=0
            db_output=con.cursor().callproc('get_seq_run_id_using_md5', [md5_checksum,seq_run_id])
            return db_output[1]
        except Exception, e:
            return False

    def createAnalysis(self, study_id):
        """ creates a row in the ANALYSIS table 
        """
        try:
            con = self.getSFFDatabaseConnection()
            analysis_id=0
            db_output=con.cursor().callproc('create_analysis',
                                            [study_id,analysis_id])
            return db_output[1]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def createSequencingRun(self,start_job,instrument_code,version,seq_run_id):
        """ creates a row in the sequencing_run table
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('create_sequencing_run',
                                                [instrument_code, version,
                                                 seq_run_id])
                return db_output[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def loadSFFData(self, start_job, input_set):
        """ loads the flow data into the READ_454 table
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_flow_data.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def loadFNAFile(self, start_job, input_set):
        """ starts process of importing fna file data
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag = 1
            if start_job:
                db_output=con.cursor().callproc('load_fna_file_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def updateAnalysisWithSeqRunID(self, start_job, analysis_id,seq_run_id):
        """ updates the ANALYSIS table with the SEQ_RUN_ID
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                con.cursor().callproc('update_analysis_w_seq_run_id',
                                                [analysis_id,seq_run_id])
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    def loadOTUMapAll(self, start_job, input_set):
        """ starts process of importing otus
        """
        try:
            #print str(input_set)
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('load_otu_map_all_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False  
                  
    def loadSeqToSourceMap(self, start_job, input_set):
        """ loads the sequence to source map...for greengenes seqs
        """
        try:
            con = self.getSFFDatabaseConnection()
            if start_job:
                db_output=con.cursor().callproc('load_seq_to_source_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    '''DEPRECATED - Maybe keep
    def getOTUMap(self,sample_name,study_id,otu_threshold,otu_method,\
                  source_name,ref_threshold):
        """ Gets a list otus for a samples
        """
        try:
            con = self.getSFFDatabaseConnection()
            user_data = con.cursor()
            con.cursor().callproc('get_otu_map', [sample_name,study_id,\
                                                  otu_threshold,otu_method,\
                                                  source_name,ref_threshold,\
                                                  user_data])
            
            return user_data
        except Exception, e:
            return 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    '''
    
    def getOTUTable(self,start_job,sample_name,otu_method,otu_threshold,\
                  source_name,ref_threshold):
        """ Gets a list otus for a samples
        """
        try:
            con = self.getSFFDatabaseConnection()
            user_data = con.cursor()
            if start_job:
                con.cursor().callproc('get_otu_table', [sample_name,\
                                                  otu_method,otu_threshold,\
                                                  source_name,ref_threshold,\
                                                  user_data])
                return user_data
            else:
                return False
        except Exception, e:
            return 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def checkIfStudyIdExists(self, study_id):
        """ Check if the study id already exists
        """
        try:
            con = self.getSFFDatabaseConnection()
            study_id_cnt=0
            db_output=con.cursor().callproc('check_if_study_id_exists',
                                            [study_id,study_id_cnt])
            if db_output[1]==0:
                return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            

    def checkIfColumnControlledVocab(self, column_name):
        """ checks if column is a controlled column
        """
        try:
            con = self.getMetadataDatabaseConnection()
            valid_controlled_column=0
            db_output=con.cursor().callproc('check_if_column_controlled',
                                            [column_name.upper(),\
                                             valid_controlled_column])
            if db_output[1]==0:
                return False
            else:
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    #
    #
    def getValidControlledVocabTerms(self,column_name):
        """ get controlled vocab values
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_valid_control_vocab_terms', \
                                     [column_name.upper(), results])
            valid_terms = []
            for row in results:
                valid_terms.append(row)
            return valid_terms
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getPublicColumns(self, user_id):
        """ get public columns for specified user
        """
        try:
            user_details = self.getUserDetails(user_id)
            is_admin = user_details['is_admin']
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_public_study_columns', [user_id, is_admin, results])
            public_cols = []
            for row in results:
                public_cols.append(row)
            return public_cols
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    #
    def getFieldReferenceInfo(self,column_name):
        """ Returns a list of metadata fields
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_field_reference_info', \
                                     [column_name,results])
            field_reference = []
            for row in results:
                field_reference.append(row)
            return field_reference
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def loadBetaDivDistances(self, start_job, input_set):
        """ loads beta-diversity distances
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_beta_distance_matrix.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    #
    def loadOTUTable(self, start_job, input_set):
        """ loads the OTU table
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('load_otu_table_package.array_insert',
                                                input_set)
                return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    def getBetaDivDistances(self, start_job, sample_name1,sample_name2,metric,\
                             rarefied):
        """ gets the beta-div distance for 2 samples
        """
        try:
            con = self.getSFFDatabaseConnection()
            distance=0.0000
            if start_job:
                db_output=con.cursor().callproc('get_beta_div_distance', \
                                                [sample_name1,sample_name2,\
                                                metric,rarefied,distance])
                if db_output[4]==None:
                    return 'not_found'
                else:
                    return db_output[4]
                    
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    #
    def getBetaDivDistancesArray(self, start_job, input_set):
        """ starts process of importing failed otus
        """
        try:
            con = self.getSFFDatabaseConnection()
            error_flag=1
            if start_job:
                db_output=con.cursor().callproc('get_bdiv_distances_package.array_get',
                                                input_set)
                return db_output
                
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
            
    def getFoundOTUArray(self, md5_list):
        """ Gets a list of found OTU ids based on a list of input sequence MD5s
        """
        try:
            con = self.getSFFDatabaseConnection()
            cur = con.cursor()
            
            # Convert input list to proper type:
            input_array = cur.arrayvar(cx_Oracle.FIXED_CHAR, md5_list)
            otu_results = cur.arrayvar(cx_Oracle.STRING , len(md5_list))
            md5_results = cur.arrayvar(cx_Oracle.FIXED_CHAR , len(md5_list))
            results = cur.callproc('otu_check.check_existing_otus', [input_array, otu_results, md5_results])
            return results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    def getQiimeSffSamples(self, study_id,seq_run_id):
        """ Gets a list of SFF samples
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_qiime_sff_samples', \
                                    [study_id,seq_run_id,results])
            return results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def getQiimeSffReadCounts(self,seq_run_id):
        """ Gets the read counts for a sequencing run
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_qiime_sff_read_counts', \
                                    [seq_run_id,results])
            return results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False

    def getQiimeSffSamplesCount(self,sample):
        """ Gets the sample count
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = 0
            query_results=con.cursor().callproc('get_qiime_sff_samples_count', \
                                    [str(sample),results])
            return query_results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    def getQiimeSffDbSummary(self,study_id):
        """ Gets the summary info for an SFF
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_qiime_sff_db_summary', \
                                    [study_id,results])
            return results
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    def getGGTaxonomy(self, start_job, prokmsa,tax_name):
        """ gets the gg taxonomy for a prokmsa
        """
        try:
            con = self.getSFFDatabaseConnection()
            results = con.cursor()
            if start_job:
                con.cursor().callproc('get_gg_taxonomy',
                                        [str(prokmsa),str(tax_name),results])
                for row in results:
                    return row[0]
                    
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return False
    
    #####################################
    # Meta-Analysis
    #####################################
    
    def addMetaAnalysisFiles(self, start_job, meta_analysis_id, \
                                    fpath, meta_type,run_date,ftype):
        """  add meta-analysis files
        """
        try:
            con = self.getMetadataDatabaseConnection()
            if start_job:
                con.cursor().callproc('add_meta_analysis_files', 
                                                    [meta_analysis_id,\
                                                    fpath,meta_type,
                                                    run_date,ftype])  
            return True
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    def getMetaAnalysisFilepaths(self, meta_analysis_id):
        """ gets meta-analysis files
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results=con.cursor()
            con.cursor().callproc('get_meta_analysis_filepaths', 
                                                    [meta_analysis_id,\
                                                    results])
            fpaths=[]
            for row in results:
                if row[0] is None:
                    continue
                else:
                    fpaths.append(row)
            return fpaths
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
            
    def createMetaAnalysis(self,web_app_user_id,inv_name):
        """ creates a meta-analysis
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            db_output=[]
            inv_id=0
            db_output=con.cursor().callproc('create_meta_analysis', 
                                                    [web_app_user_id, \
                                                     inv_name,inv_id])
                                                                
            return db_output[2]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False

    def getRunPrefixes(self, study_id):
        """ get the run prefixes for the study
        """
        try:
            con = self.getMetadataDatabaseConnection()
            run_prefixes = []
            results = con.cursor()
            con.cursor().callproc('GET_RUN_PREFIXES', \
                                      [study_id, results])
            for row in results:
                if row[0] == None:
                    continue
                run_prefixes.append(row[0])
            return run_prefixes
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), str(e))
            return []

    def getMetaAnalysisNames(self,web_app_user_id):
        """ Returns a list of meta-analysis names
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('get_meta_analysis_names', [web_app_user_id,\
                                                                results])
            meta_analysis_name_list = []
            for row in results:
                if row[0] is None:
                    continue
                else:
                    meta_analysis_name_list.append(row)
            return meta_analysis_name_list
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    #
    def getSampleCount(self,study_id):
        """ Returns a list of meta-analysis names
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            count=0
            results=con.cursor().callproc('get_sample_count', [study_id,\
                                                                count])
            
            return results[1]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False
    
    #####################################
    # MG-RAST Stuff
    #####################################
    
    def getSequencesFullDatabase(self):
        """ Returns a list of all sequences in DB
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_sequences_for_fasta_fulldb', [results])
            for row in results:
                # sequence_name, sequence_string, md5_checksum
                yield [row[0], row[1], row[2]]
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            
    def getSequencesFromSample(self, study_id, sample_id):
        """ Returns a list of seqs for a given sample
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('qiime_assets.get_sequences_for_fasta', [study_id, sample_id, results])
            seqs = {}
            for row in results:
                seqs[row[0]] = row[1]
            return seqs            
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False    
    
    
    def getAllSampleFields(self, sample_id, study_id):
        """ Finds all filled in sample fields for a given sample_id
        """
        sample_tables = []
        sample_tables.append('sample')
        sample_tables.append('common_fields')
        sample_tables.append('extra_sample_')
        sample_tables.append('air')
        sample_tables.append('other_environment')
        sample_tables.append('sediment')
        sample_tables.append('soil')
        sample_tables.append('wastewater_sludge')
        sample_tables.append('water')
        sample_tables.append('host_assoc_vertibrate')
        sample_tables.append('host_associated_plant')
        sample_tables.append('human_associated')
        sample_tables.append('host_sample')
        sample_tables.append('host')
      
        filled_fields = {}
        
        con = self.getMetadataDatabaseConnection()
        cursor = con.cursor()
        
        for table in sample_tables:
            if 'extra_sample_' in table:
                statement = 'select * from %s%s where sample_id = %s' % (table, study_id, sample_id)
            elif table == 'host':
                statement = 'select * from host h inner join host_sample hs on h.host_id = hs.host_id where sample_id = %s' % sample_id
            else:
                statement = 'select * from %s where sample_id = %s' % (table, sample_id)
            
            try:
                cursor.execute(statement)
            except Exception, e:
                print str(e)
                print 'Error running query:\n'
                print statement
                print 'Running next query...\n'
                
                continue
                
            data = cursor.fetchall()

            # Get the column names
            col_names = []
            for i in range(0, len(cursor.description)):
                col_names.append(cursor.description[i][0])
        
            # Find the rows with data
            for row in data:
                i = 0
                for field in row:
                    if field != None and field != '':
                        filled_fields[col_names[i]] = field
                    i += 1
        
        return filled_fields
    
    def insertAmericanGutConsent(self, input_values):
        """ Inserts a record into the american gut consent table
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('american_gut_consent_submit', input_values)

    def updateSeqOtuCounts(self, sequence_prep_id, num_sequences, num_otus, otu_percent_hit):
        """ Updates sequence and otu counts for a prep entry
        """
        try:
            con = self.getMetadataDatabaseConnection()
            results = con.cursor()
            con.cursor().callproc('update_seq_otu_counts', [sequence_prep_id, num_sequences, num_otus, otu_percent_hit])
        except Exception, e:
            print 'Exception caught: %s.\nThe error is: %s' % (type(e), e)
            return False  

    def updateBarcodeStatus(self, status, postmark, scan_date, barcode):
        """ Updates a barcode's status
        """
        con = self.getMetadataDatabaseConnection()
        con.cursor().callproc('update_barcode_status', [status, postmark, scan_date, barcode])
