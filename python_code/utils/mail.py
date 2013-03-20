#!/usr/bin/env python
# File created on 14 Mar 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeza"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Meg Pirrung", "Adam Robbins-Pianka", "Yoshiki Vazquez-Baeza",
    "Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Yoshiki Vazquez-Baeza"]
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

FROM_EMAIL = 'info@americangut.org'

def send_email(message, subject, recipient='americangut@gmail.com'):
    """Send an email from your local host """

    # Create a text/plain message
    msg = MIMEText(message)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(FROM_EMAIL, [recipient], msg.as_string())
    s.quit()
