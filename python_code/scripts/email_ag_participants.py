#!/usr/bin/env python
# File created on 20 Mar 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeza"
__copyright__ = "Copyright 2010-2013, The QIIME WebApp project"
__credits__ = ["Yoshiki Vazquez-Baeza"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

from qiime.util import parse_command_line_parameters, make_option
from utils.mail import send_email

import logging


script_info = {}
script_info['brief_description'] = "Send emails to participants"
script_info['script_description'] = "Email a list of participants that have "+\
    "not recieved an e-mail yet."
script_info['script_usage'] = [("Test what the script would do","See the "
    "output of all the information in a log file but don't actually send any"
    "e-mail.","email_ag_participants.py -o email_log.log"),
    ("Send e-mails to the participants","Send e-mails to all of the particpants"
    ,"email_ag_participants.py -o email_log.log --really")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-o','--output_log_fp',type="new_filepath",
    help='filepath for the log file [default: %default]',
    default='email_ag_participants.log')]
script_info['optional_options'] = [\
    # Example optional option
    make_option('--really', action='store_true', help='Make the script actually'
    ' send the e-mails and not just print into stdout what it would do'
    '[default: %default]', default=False)
]
script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    really = opts.really

    # if level is set to DEBUG log messages will be written
    logging.basicConfig(filename=opts.output_log_fp, level=logging.DEBUG, \
        format='[%(asctime)s].%(levelname)s: %(message)s')

    ag_data_access = data_access_factory(ServerConfig.data_access_type,
    'american_gut')

    # cursor to update the sent e-mails
    con = ag_data_access.getMetadataDatabaseConnection()

    cursor = ag_data_access.dynamicMetadataSelect("""
        select  al.name, al.email, ak.kit_verification_code, ak.supplied_kit_id, ak.kit_password, ak.swabs_per_kit
        from ag_login al
            inner join ag_kit ak
            on al.ag_login_id = ak.ag_login_id
            where ak.verification_email_sent = 'n'
        order by al.email""")

    for entry in cursor:
        recipient_name, target_email, verification_code, supplied_kit_id,\
            kit_password, swabs_per_kit = entry

        logging.debug('\n+++++++++++++++++++++++++++++++++++++++++++++++++++\n')

        logging.debug("""recipient_name {0}, target_email {1}, """
            """verification_code {2}, supplied_kit_id {3}, kit_password {4}, """
            """swabs_per_kit {5}\n""".format(recipient_name, target_email,
            verification_code, supplied_kit_id, kit_password, swabs_per_kit))

        buffer_message = BODY_MESSAGE.format(recipient_name, supplied_kit_id, verification_code)

        try:
            logging.debug('Message is %s\n' % buffer_message)
            logging.debug('Sent to %s\n' % target_email)
            
            if really == True:
                send_email(buffer_message, SUBJECT, target_email)
                query_string = "update ag_kit set verification_email_sent = 'y' where supplied_kit_id = '{0}'".format(supplied_kit_id)
                con.cursor().execute(query_string)
                con.cursor().execute('commit')
            else:
                logging.debug('DRY RUNNING, NOT SENDING A MESSAGE\n')
        except Exception, e:
            logging.debug('Exception value is %s\n' % str(e))
            logging.debug('ERROR SENDING TO: %s' % target_email)

        logging.debug('+++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')

    # email, kit identifier, 

SUBJECT = "American Gut Website is Live!"
BODY_MESSAGE = """Hi {0}! The American Gut Participant site is now Live! Please log in with the KitID and password that you got in the mail. Your kit validation code for KitID {1} is: {2}

Go the following site to get started:

http://microbio.me/AmericanGut

Thanks!

American Gut Team!

"""

if __name__ == "__main__":
    main()
