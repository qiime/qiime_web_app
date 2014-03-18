#!/usr/bin/env python
# File created on 14 Mar 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeza"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Meg Pirrung", "Adam Robbins-Pianka", "Yoshiki Vazquez-Baeza",
    "Daniel McDonald", "Emily TerAvest"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Yoshiki Vazquez-Baeza"]
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

# used in the can_send_mail function
from socket import gethostname

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

FROM_EMAIL = 'info@americangut.org'

def can_send_mail():
    """Checks whether this is a live system or not. Returns true if
    microbio.me appears in socket.gethostname()
    """
    return 'microbio.me' in gethostname()

def send_email(message, subject, recipient='americangut@gmail.com',
               sender=FROM_EMAIL):
    """Send an email from your local host """

    # Create a text/plain message
    msg = MIMEText(message)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [recipient], msg.as_string())
    s.quit()
