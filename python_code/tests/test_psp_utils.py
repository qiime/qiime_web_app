#!/usr/bin/env python
# File created on 15 Mar 2013
from __future__ import division

__author__ = "Adam Robbins-Pianka"
__copyright__ = "Copyright 2009-2013, QIIME web analysis"
__credits__ = ["Adam Robbins-Pianka"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Adam Robbins-Pianka"
__email__ = "adam.robbinspianka@colorado.edu"
__status__ = "Production"


from cogent.util.unit_test import TestCase, main
from utils.psp_utils import format_submit_form_to_fusebox_string

class ToplevelTests(TestCase):
    def test_format_submit_form_to_fusebox_string(self):
        """
        """
        change_page_only = ('\n    <form action="fusebox.psp" name="redirect" '
        'id="redirect" method="post">\n    \n        <input type="hidden" '
        'name="page" id="page" value="portal.psp">\n        '
        '</form>\n    <script>document.forms[\'redirect\'].submit()'
        '</script>\n    ')

        change_form_name = ('\n    <form action="fusebox.psp" '
        'name="something_else" id="something_else" '
        'method="post">\n    \n        <input type="hidden" name="page" '
        'id="page" value="portal.psp">\n        </form>\n    '
        '<script>document.forms[\'something_else\'].submit()</script>\n    ')

        self.assertEqual(format_submit_form_to_fusebox_string(
            form_name='something_else', page='portal.psp'), change_form_name)

        self.assertEqual(format_submit_form_to_fusebox_string(
            page='portal.psp'), change_page_only)

if __name__ == "__main__":
    main()
