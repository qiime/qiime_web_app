#!/usr/bin/env python
# encoding: utf-8
from __future__ import division

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2012, The QIIME-webdev project"
__credits__ = [" Doug Wendel","Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
"""
linkamafy.py

Exports a function for scanning a string of text for hyperlinks and
turning them into actual hyperlinks
"""

import re

def link_urls(val):
    r = re.compile(r"(http://[^ )]+[a-zA-Z0-9])")
    return r.sub(r'<a href="\1" target="_blank">\1</a>', val)
