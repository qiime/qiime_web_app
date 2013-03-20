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


from data_access import ag_data_access
from qiime.util import parse_command_line_parameters, make_option
from utils.mail import send_mail

import logging

# if level is set to DEBUG log messages will be written
logging.basicConfig(filename='email_ag_participants.log', level=logging.DEBUG, \
                    format='[%(asctime)s].%(levelname)s: %(message)s')


script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = []
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

    ag_data_access = data_access_factory(ServerConfig.data_access_type,
    'american_gut')

    cursor = ag_data_access.dynamicMetadataSelect("""
        select  al.name, al.email, ak.kit_verification_code, ak.supplied_kit_id, ak.kit_password, ak.swabs_per_kit
        from ag_login al
            inner join ag_kit ak
            on al.ag_login_id = ak.ag_login_id
        order by al.email""")

    for entry in cursor:
        recipient_name, target_email, verification_code, supplied_kit_id,\
            kit_password, swabs_per_kit = entry

        logging.debug('\n+++++++++++++++++++++++++++++++++++++++++++++++++++'\n)

        logging.debug("""recipient_name {0}, target_email {1}, """
            """verification_code {2}, supplied_kit_id {3}, kit_password {4}, """
            """swabs_per_kit {5}\n""".format(recipient_name, target_email,
            verification_code, supplied_kit_id, kit_password, swabs_per_kit))

        buffer_message = BODY_MESSAGE % (recipient_name, verification_code)

        try:
            logging.debug('Message is %s\n' % buffer_message)
            logging.debug('Sent to %s\n' % target_email)
            
            if really == True:
                send_mail(buffer_message, SUBJECT, target_email)
            else:
                logging.debug('DRY RUNNING, NOT SENDING A MESSAGE\n')
        except Exception, e:
            logging.debug('Exception value is %s\n' % str(e))

        logging.debug('+++++++++++++++++++++++++++++++++++++++++++++++++++'\n\n)

    # email, kit identifier, 

SUBJECT = "American Gut Website is Live!"
BODY_MESSAGE = """Hi {1}! The American Gut Participant site is now Live! Please log in with the KitID and password that you got in the mail. Your kit validation code is {2}.

Go the following site to get started:

http://microbio.me/AmericanGut

Thanks!

American Gut Team!

"""

if __name__ == "__main__":
    main()