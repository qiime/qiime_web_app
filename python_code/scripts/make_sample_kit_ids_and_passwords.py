#!/usr/bin/env python

"""Take Indiegogo American Gut data, expand each kit and make credentials

Expects input table to have contain the following columns:

    Email
    Name
    Swabs
    State
    Zipcode

Can optionally covert US states to abbreviated codes
Can optionally force US zip codes to be 5 numbers (to correct for missing 
leading 0)
"""

from random import choice
from cx_Oracle import connect
from credentials import Credentials
from cogent.util.misc import parse_command_line_parameters
from optparse import make_option
from string import lower

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

script_info = {}
script_info['brief_description'] = "Prep Indiegogo kits"
script_info['script_description'] = ""
script_info['script_usage'] = []
script_info['required_options'] = [
        make_option('--input', '-i', help="Input table"),
        make_option('--output', '-o', help="Output table"),
        make_option('--starting_sample', help='Starting sample number', 
                    type='int')
        ]
script_info['optional_options'] = [
        make_option('--correct_us_states', action='store_true', default=False,
                    help="Abbreviate US states"),
        make_option('--pad_us_zipcodes', action='store_true', default=False,
                    help="Force US zip codes to be 5 digits")
        ]
script_info['version'] = __version__

# character sets for kit id, passwords and verification codes
KIT_ALPHA = "abcdefghijklmnopqrstuvwxyz"
KIT_ALPHA += KIT_ALPHA.upper()
KIT_PASSWD = '1234567890'
KIT_VERCODE = KIT_PASSWD

# US abbreviations including territories
US_STATES_TERRITORIES = {'delaware': 'DE', 
                         'north dakota': 'ND', 
                         'american samoa': 'AS', 
                         'national': 'NA', 
                         'washington': 'WA', 
                         'rhode island': 'RI', 
                         'tennessee': 'TN', 
                         'iowa': 'IA', 
                         'nevada': 'NV', 
                         'maine': 'ME', 
                         'colorado': 'CO', 
                         'mississippi': 'MS', 
                         'south dakota': 'SD', 
                         'new jersey': 'NJ', 
                         'oklahoma': 'OK', 
                         'wyoming': 'WY', 
                         'minnesota': 'MN', 
                         'north carolina': 'NC', 
                         'illinois': 'IL', 
                         'new york': 'NY', 
                         'arkansas': 'AR', 
                         'puerto rico': 'PR', 
                         'indiana': 'IN', 
                         'maryland': 'MD', 
                         'louisiana': 'LA', 
                         'guam': 'GU', 
                         'texas': 'TX', 
                         'district of columbia': 'DC', 
                         'arizona': 'AZ', 
                         'wisconsin': 'WI', 
                         'virgin islands': 'VI', 
                         'michigan': 'MI', 
                         'kansas': 'KS', 
                         'utah': 'UT', 
                         'virginia': 'VA', 
                         'oregon': 'OR', 
                         'connecticut': 'CT', 
                         'montana': 'MT', 
                         'california': 'CA', 
                         'new mexico': 'NM', 
                         'alaska': 'AK', 
                         'vermont': 'VT', 
                         'georgia': 'GA', 
                         'northern mariana islands': 'MP', 
                         'pennsylvania': 'PA', 
                         'florida': 'FL', 
                         'hawaii': 'HI', 
                         'kentucky': 'KY', 
                         'missouri': 'MO', 
                         'nebraska': 'NE', 
                         'new hampshire': 'NH', 
                         'idaho': 'ID', 
                         'west virginia': 'WV', 
                         'south carolina': 'SC', 
                         'ohio': 'OH', 
                         'alabama': 'AL', 
                         'massachusetts': 'MA'}
US_ABBRV = set(US_STATES_TERRITORIES.values())
US_NAMES = set(['united states', 'usa', 'us'])

BASE_PRINTOUT_TEXT = """Thank you for participating in the American Gut Project! Below you will find your sample barcodes (the numbers that anonymously link your samples to you) and your login credentials. It is very important that you login before you begin any sample collection.

Please login at: http://www.microbio.me/AmericanGut

Thanks,
The American Gut Project
"""

def verify_unique_sample_id(cursor, sample_id):
    """Verify that a sample ID does not already exist"""
    cursor.execute("select barcode from ag_kit_barcodes where barcode='%s'" % \
                sample_id)
    results = cursor.fetchall()
    return len(results) == 0

def get_used_kit_ids(cursor):
    """Grab in use kit IDs, return set of them"""
    cursor.execute("select supplied_kit_id from ag_kit")

    return set([i[0] for i in cursor.fetchall()])

def make_kit_id(obs_kit_ids, kit_id_length=5):
    """Generate a new unique kit id"""
    kit_id = ''.join([choice(KIT_ALPHA) for i in range(kit_id_length)])
    while kit_id in obs_kit_ids:
        kit_id = ''.join([choice(KIT_ALPHA) for i in range(kit_id_length)])

    obs_kit_ids.add(kit_id)

    return (obs_kit_ids, kit_id)

def make_passwd(passwd_length=8):
    """Generate a new password"""
    return ''.join([choice(KIT_PASSWD) for i in range(passwd_length)])

def make_verification_code(vercode_length=5):
    """Generate a verification code"""
    return ''.join([choice(KIT_VERCODE) for i in range(vercode_length)])

def get_printout_data(kit_passwd_map, kit_barcode_map):
    """Produce kit output text"""
    text = []
    for kit_id,passwd in kit_passwd_map:
        text.append(BASE_PRINTOUT_TEXT)
        barcodes = kit_barcode_map[kit_id]

        padding_lines = 5

        if len(barcodes) > 5:
            text.append("Sample Barcodes:\t%s" % ', '.join(barcodes[:5]))
            for i in range(len(barcodes))[5::5]:
                padding_lines -= 1
                text.append("\t\t\t%s" % ', '.join(barcodes[i:i+5]))
        else:
            text.append("Sample Barcodes:\t%s" % ', '.join(barcodes))

        text.append("Kit ID:\t\t%s" % kit_id)
        text.append("Password:\t\t%s" % passwd)

        # padding between sheets so they print pretty
        for i in range(padding_lines):
            text.append('')

    return text

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    mapping_lines = [l.strip().split('\t') for l in open(opts.input, 'U')]

    # build up new header
    outlines = [mapping_lines[0][:]]
    outlines[0].insert(0, '#SampleID')
    outlines[0].append('KIT_ID')
    outlines[0].append('KIT_PASSWORD')
    outlines[0].append('KIT_VERIFICATION_CODE')

    # get columns for the fields we care about
    index_lookup = map(lower, mapping_lines[0])
    EMAIL_IDX = index_lookup.index('email')
    NAME_IDX = index_lookup.index('name')
    ZIPCODE_IDX = index_lookup.index('zipcode')
    STATE_IDX = index_lookup.index('state')
    SWABS_IDX = index_lookup.index('swabs')
    COUNTRY_IDX = index_lookup.index('country')

    # verify columns exist
    if EMAIL_IDX == -1:
        print "Cannot find email column!"
        exit(1)

    if NAME_IDX == -1:
        print "Cannot find name column!"
        exit(1)

    if STATE_IDX == -1:
        print "Cannot find state column!"
        exit(1)

    if ZIPCODE_IDX == -1:
        print "Cannot find zipcode column!"
        exit(1)

    if SWABS_IDX == -1:
        print "Cannot find swabs column!"
        exit(1)

    if COUNTRY_IDX == -1:
        print "Cannot find country column!"
        exit(1)

    # setup DB connection
    cred = Credentials()
    con = connect(cred.liveMetadataDatabaseConnectionString)
    cursor = con.cursor()
    existing_kit_ids = get_used_kit_ids(cursor)

    kit_barcode_map = {}
    kit_passwd_map = []
    current_sample_id = opts.starting_sample
    for l in mapping_lines[1:]:
        entry = l[:]

        # determine how many samples
        try:
            number_of_samples = int(entry[SWABS_IDX])
        except ValueError:
            raise ValueError, "Could not determine samples for %s" % str(l)

        if opts.correct_us_states and entry[COUNTRY_IDX].lower() in US_NAMES:
            # if it already looks like its abbreviated, verify it
            if len(entry[STATE_IDX]) == 2: 
                if entry[STATE_IDX] not in US_ABBRV:
                    raise ValueError, "Unknown state in record: %s" % str(l)
            else:
                abbrv = US_STATES_TERRITORIES.get(entry[STATE_IDX].lower(), None)
                if abbrv is None:
                    raise ValueError, "Unknown state in record: %s" % str(l)
                entry[STATE_IDX] = abbrv

        if opts.pad_us_zipcodes and entry[COUNTRY_IDX].lower() in US_NAMES:
            # ignore if it looks like a NNNNN-NNNN PO Box zip code
            if '-' in entry[ZIPCODE_IDX] or ' ' in entry[ZIPCODE_IDX]:
                pass
            else:
                try:
                    zipcode = int(entry[ZIPCODE_IDX])
                except ValueError:
                    raise ValueError, "Invalid zipcode in record: %s " % str(l)

                if len(entry[ZIPCODE_IDX]) < 5:
                    entry[ZIPCODE_IDX] = "%0.5d" % zipcode

        existing_kit_ids, kit_id = make_kit_id(existing_kit_ids)
        passwd = make_passwd()
        vercode = make_verification_code()

        entry.append(kit_id)
        entry.append(passwd)
        entry.append(vercode)
        kit_barcode_map[kit_id] = []
        kit_passwd_map.append((kit_id, passwd))

        # add on the samples per kit
        for sample in range(number_of_samples):
            sample_id = "%0.9d" % current_sample_id

            if not verify_unique_sample_id(cursor, sample_id):
                raise ValueError, "%s is not unique!" % sample_id

            with_sample = entry[:]
            with_sample.insert(0, sample_id)
            outlines.append(with_sample)

            kit_barcode_map[kit_id].append(sample_id)

            current_sample_id += 1

    f = open(opts.output,'w')
    f.write('\n'.join(['\t'.join(l) for l in outlines]))
    f.write('\n')
    f.close()

    f = open(opts.output + '.printouts', 'w')
    f.write('\n'.join(get_printout_data(kit_passwd_map, kit_barcode_map)))
    f.write('\n')
    f.close()

if __name__ == '__main__':
    main()
