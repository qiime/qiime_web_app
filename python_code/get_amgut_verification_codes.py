#!/usr/bin/env python

"""pull unverified emails, kit ids, verification codes from db"""

from cx_Oracle import connect
from cogent.util.misc import parse_command_line_parameters
from optparse import make_option

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald", "Doug Wendel"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdoandt@colorado.edu"
__status__ = "Development"

script_info = {}
script_info['brief_description'] = "Pull out kit verification codes"
script_info['script_description'] = """Pull out kit verification codes associated to kits and participants"""

script_info['script_usage'] = []
script_info['required_options']=[
    make_option('-u', '--user', help="Database username"),
    make_option('-p', '--password', help="Database password"),
    make_option('-d', '--dsn', help='Database DSN'),
    make_option('-o', '--outfile_fp', help='Output file')
    ]
script_info['optional_options'] = [
        make_option('-f', '--full_query', help="Pull all kit/verifications including those kits that have already been verified")
        ]
script_info['version'] = __version__

FULL_QUERY = """SELECT ag_login.name, ag_login.email, 
                       ag_kit.supplied_kit_id, ag_kit.kit_verification_code
                FROM ag_login
                INNER JOIN ag_kit 
                    ON ag_login.ag_login_id=ag_kit.ag_login_id"""
UNVER_QUERY = """SELECT ag_login.name, ag_login.email, 
                       ag_kit.supplied_kit_id, ag_kit.kit_verification_code
                 FROM ag_login
                 INNER JOIN ag_kit 
                     ON ag_login.ag_login_id=ag_kit.ag_login_id
                 WHERE ag_kit.kit_verified='n'"""

def collapse_names(records):
    """Collapse multiple kit participants"""
    mapping = {}
    for name, email, kit, code in records:
        if (name, email) not in mapping:
            mapping[(name, email)] = [[],[]]
        mapping[(name, email)][0].append(kit)
        mapping[(name, email)][1].append(code)
    
    new_recs = []
    for ((name, email), (kits, codes)) in mapping.items():
        ks = ', '.join(kits)
        cs = ', '.join(codes)
        new_recs.append((name, email, ks, cs))
    return new_recs

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    con = connect(user=opts.user, password=opts.password, dsn=opts.dsn)
    cur = con.cursor()

    if opts.full_query:
        cur.execute(FULL_QUERY)
    else:
        cur.execute(UNVER_QUERY)

    results = cur.fetchall()
    collapsed = collapse_names(results)

    f = open(opts.outfile_fp, 'w')
    f.write("#name\temail\tsupplied_kits\tverification_codes\n")
    for rec in collapsed:
        f.write('\t'.join(rec))
        f.write('\n')
    f.close()
