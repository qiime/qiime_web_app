#!/usr/bin/env python
# File created on 07 Feb 2014

from __future__ import division

"""Gets the American Gut metadata associated with set of barcodes"""

__author__ = "Adam Robbins-Pianka"
__copyright__ = "Copyright 2014, The QIIME-DB Project"
__credits__ = ["Adam Robbins-Pianka"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Adam Robbins-Pianka"
__email__ = "adam.robbinspianka@colorado.edu"
__status__ = "Development"


import cx_Oracle

from qiime.util import parse_command_line_parameters, make_option

from data_access_connections import data_access_factory
from enums import ServerConfig, DataAccessType

script_info = {}
script_info['brief_description'] = (
    "Query the database and retrieve metadata for a set of barcodes in the "
    "American Gut Project"
)

script_info['script_description'] = (
    "Connects to the QIIME metadata database using the web app's "
    "ag_data_access.AGGetBarcodeMetadata. This function is called once per "
    "barcodes in the input file."
)

script_info['script_usage'] = [("","","")]

script_info['output_description']= (
    "Results are written to an output file, one line per barcode. Column "
    "headers are written by default, but can be omitted by passing -H."
)

script_info['required_options'] = [
    make_option('-i', '--input_barcodes_file', type='existing_filepath',
                help="The input file containing barcodes, one per line"),
    make_option('-o', '--output_file', type='new_filepath',
                help="The output file, to which metadata will be written")

]

script_info['optional_options'] = [
    make_option('-H', '--omit_headers', action='store_true',
                help="Do not print column headers as the first line")
]

script_info['version'] = __version__

def get_ag_metadata_bulk(barcodes):
    """Calls ag_get_barcode_metadata on a list of barcodes

    The input, barcodes, should be an iterable list of barcodes (or an open
    file that has one barcode per line)
    """
    ag_data_access = data_access_factory(ServerConfig.data_access_type,
                                         'american_gut')

    results = []
    for line in barcodes:
        bc = line.strip()
        metadata = ag_data_access.AGGetBarcodeMetadata(bc)
        if len(metadata) != 1:
            print ("FAILED barcode %s; %d results were returned (should be 1)"
                   % (bc, len(metadata)))
        else:
            yield metadata[0]

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    input_fp = opts.input_barcodes_file
    output_fp = opts.output_file
    print_headers = not opts.omit_headers

    # this is the order of the columns to write.
    headers = [
        'SAMPLE_NAME', 'ANONYMIZED_NAME', 'COLLECTION_DATE', 'public',
        'DEPTH', 'DESCRIPTION', 'SAMPLE_TIME', 'ALTITUDE',
        'ASSIGNED_FROM_GEO', 'TITLE', 'SITE_SAMPLED', 'HOST_SUBJECT_ID',
        'TAXON_ID', 'HOST_TAXID', 'COMMON_NAME', 'HOST_COMMON_NAME',
        'BODY_HABITAT', 'BODY_SITE', 'BODY_PRODUCT', 'ENV_BIOME',
        'ENV_FEATURE', 'ENV_MATTER', 'CITY', 'STATE', 'ZIP', 'COUNTRY',
        'LATITUDE', 'LONGITUDE', 'ELEVATION', 'AGE_UNIT', 'AGE',
        'ACNE_MEDICATION', 'ACNE_MEDICATION_OTC', 'ALCOHOL_FREQUENCY',
        'FAT_PER', 'CARBOHYDRATE_PER', 'PROTEIN_PER', 'ANIMAL_PER',
        'PLANT_PER', 'ANTIBIOTIC_CONDITION', 'ANTIBIOTIC_SELECT',
        'APPENDIX_REMOVED', 'ASTHMA', 'BIRTH_DATE', 'CAT', 'CHICKENPOX',
        'COMMUNAL_DINING', 'CONDITIONS_MEDICATION', 'CONTRACEPTIVE',
        'COSMETICS_FREQUENCY', 'COUNTRY_OF_BIRTH', 'CSECTION',
        'CURRENT_RESIDENCE_DURATION', 'DECEASED_PARENT', 'DEODORANT_USE',
        'DIABETES', 'DIABETES_DIAGNOSE_DATE', 'DIABETES_MEDICATION',
        'DIET_TYPE', 'DOG', 'DRINKING_WATER_SOURCE', 'EXERCISE_FREQUENCY',
        'EXERCISE_LOCATION', 'FIBER_GRAMS', 'FLOSSING_FREQUENCY',
        'FLU_VACCINE_DATE', 'FOODALLERGIES_OTHER',
        'FOODALLERGIES_OTHER_TEXT', 'FOODALLERGIES_PEANUTS',
        'FOODALLERGIES_SHELLFISH', 'FOODALLERGIES_TREENUTS', 'FRAT', 'SEX',
        'GLUTEN', 'DOMINANT_HAND', 'HEIGHT_IN', 'HEIGHT_OR_LENGTH', 'IBD', 
        'LACTOSE', 'LAST_TRAVEL', 'LIVINGWITH', 'MAINFACTOR_OTHER_1',
        'MAINFACTOR_OTHER_2', 'MAINFACTOR_OTHER_3', 'MIGRAINE',
        'MIGRAINEMEDS', 'MIGRAINE_AGGRAVATION', 'MIGRAINE_AURA',
        'MIGRAINE_FACTOR_1', 'MIGRAINE_FACTOR_2', 'MIGRAINE_FACTOR_3',
        'MIGRAINE_FREQUENCY', 'MIGRAINE_NAUSEA', 'MIGRAINE_PAIN',
        'MIGRAINE_PHONOPHOBIA', 'MIGRAINE_PHOTOPHOBIA',
        'MIGRAINE_RELATIVES', 'MULTIVITAMIN', 'NAILS',
        'NONFOODALLERGIES_BEESTINGS', 'NONFOODALLERGIES_DANDER',
        'NONFOODALLERGIES_DRUG', 'NONFOODALLERGIES_NO',
        'NONFOODALLERGIES_POISONIVY', 'NONFOODALLERGIES_SUN',
        'PERCENTAGE_FROM_CARBS', 'PKU', 'POOL_FREQUENCY', 'PREGNANT',
        'PREGNANT_DUE_DATE', 'PRIMARY_CARB', 'PRIMARY_VEGETABLE', 'RACE',
        'RACE_OTHER', 'ROOMMATES', 'SEASONAL_ALLERGIES', 'SHARED_HOUSING',
        'SKIN_CONDITION', 'SLEEP_DURATION', 'SMOKING_FREQUENCY',
        'SOFTENER', 'SPECIAL_RESTRICTIONS', 'SUPPLEMENTS', 'TANNING_BEDS',
        'TANNING_SPRAYS', 'TEETHBRUSHING_FREQUENCY', 'TONSILS_REMOVED',
        'TYPES_OF_PLANTS', 'WEIGHT_CHANGE', 'TOT_MASS', 'WEIGHT_LBS',
        'BMI', 'ANTIBIOTIC_MEDS', 'DIABETES_MEDICATIONS', 
        'DIET_RESTRICTIONS', 'GENERAL_MEDS', 'MIGRAINE_MEDICATIONS',
        'PETS', 'PET_CONTACT', 'PET_LOCATIONS', 'RELATIONS',
        'SUPPLEMENTS_FIELDS', 'MACRONUTRIENT_PCT_TOTAL', 'QUINOLINE',
        'NITROMIDAZOLE', 'PENICILLIN', 'SULFA_DRUG', 'CEPHALOSPORIN'
    ]

    with open(output_fp, 'w') as out_file:
        if print_headers:
            out_file.write('\t'.join(headers) + '\n')

        for metadata in get_ag_metadata_bulk(open(input_fp, 'U')):
            line = '\t'.join([str(metadata[header]) for header in headers])
            line += '\n'
            out_file.write(line)

if __name__ == '__main__':
    main()
