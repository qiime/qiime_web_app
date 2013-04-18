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
from utils.psp_utils import (format_submit_form_to_fusebox_string,
    tab_delim_lines_to_table)

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

    def test_tab_delim_lines_to_table(self):
        """Tests whether the correct table is produced when given known input

        known input:
            "#comment line
            #another comment line
            Length	Count
            114.0	1830490
            124.0	1981629
            134.0	7168533
            144.0	86386729
            154.0	0
            --
            "
        """
        self.assertEqual(tab_delim_lines_to_table(histograms_lines), defaults)

        self.assertEqual(tab_delim_lines_to_table(histograms_lines, border=2,
            width='100%'), with_table_mods)

histograms_lines = '''#comment line
#another comment line
Length	Count
114.0	1830490
124.0	1981629
134.0	7168533
144.0	86386729
154.0	0
--
'''.splitlines()

with_table_mods = '''<table width=100% border=2>
<tr>
<td>Length</td>
<td>Count</td>
</tr>
<tr>
<td>114.0</td>
<td>1830490</td>
</tr>
<tr>
<td>124.0</td>
<td>1981629</td>
</tr>
<tr>
<td>134.0</td>
<td>7168533</td>
</tr>
<tr>
<td>144.0</td>
<td>86386729</td>
</tr>
<tr>
<td>154.0</td>
<td>0</td>
</tr>
<tr>
<td>--</td>
</tr>
</table>'''

defaults = '''<table >
<tr>
<td>Length</td>
<td>Count</td>
</tr>
<tr>
<td>114.0</td>
<td>1830490</td>
</tr>
<tr>
<td>124.0</td>
<td>1981629</td>
</tr>
<tr>
<td>134.0</td>
<td>7168533</td>
</tr>
<tr>
<td>144.0</td>
<td>86386729</td>
</tr>
<tr>
<td>154.0</td>
<td>0</td>
</tr>
<tr>
<td>--</td>
</tr>
</table>'''

if __name__ == "__main__":
    main()
