#!/usr/bin/env python
# encoding: utf-8

"""
linkamafy.py

Exports a function for scanning a string of text for hyperlinks and
turning them into actual hyperlinks
"""

import re

def link_urls(val):
    r = re.compile(r"(http://[^ )]+[a-zA-Z0-9])")
    return r.sub(r'<a href="\1" target="_blank">\1</a>', val)
