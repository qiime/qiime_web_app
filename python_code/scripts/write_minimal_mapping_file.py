#!/usr/bin/env python
# File created on 11 Jun 2010
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME WebApp project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from os import makedirs,path
import os
from qiime.util import load_qiime_config
from qiime.util import load_qiime_config
from process_sff_and_metadata_workflow import submit_processed_data_to_db


qiime_config = load_qiime_config()
options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Submit processed SFF and metadata through picking OTUs into the Oracle DB"
script_info['script_description'] = """\
This script takes an processed sff fasta file and performs the \
following steps:

    1) 
    2) 
    3) 
    4) 
"""
script_info['script_usage'] = [("Example:","This is an example of a basic use case",
"%prog -i 454_Reads.fna")]
script_info['output_description']= "There is no output from the script is puts the processed data into the Oracle DB."
script_info['required_options'] = [\
    make_option('-s','--study_id',help='This is the study id assigned from loading the metadata'),\
    options_lookup['output_dir']
]
script_info['optional_options'] = [\
    make_option('-t','--get_from_test_db',action='store_true',help='By setting this parameter, the data will be submitted to the test database.',default=False),\
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    if opts.output_dir:
        if path.exists(opts.output_dir):
            dir_path=opts.output_dir
        else:
            try:
                makedirs(opts.output_dir)
                dir_path=opts.output_dir
            except OSError:
                pass
    else:
        dir_path='./'
    
    try:
        from data_access_connections import data_access_factory
        from enums import DataAccessType
        import cx_Oracle
        if opts.get_from_test_db:
            data_access = data_access_factory(DataAccessType.qiime_test)
        else:
            data_access = data_access_factory(DataAccessType.qiime_production)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
        
    study_id=opts.study_id
    
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    #req.write(str(statement)+'<br><br>')
    run_prefixes = cur.execute('select distinct sp.RUN_PREFIX from SEQUENCE_PREP sp \
    inner join "SAMPLE" s on s.sample_id=sp.sample_id where s.study_id=%s' % (study_id))
    for run_prefix in run_prefixes:
    
        # Start building the statement for writing out the mapping file
        # THIS ORDER MUST REMAIN THE SAME SINCE CHANGES WILL AFFECT LATER FUNCTION
        statement = '("SAMPLE".sample_name||\'.\'||"SEQUENCE_PREP".run_prefix) as SampleID, \n'
        statement += '"SEQUENCE_PREP".barcode, \n'
        statement += 'concat("SEQUENCE_PREP".linker, "SEQUENCE_PREP".primer) as LinkerPrimerSequence, \n'
        statement += '"SAMPLE".study_id, \n'
        statement += '"SEQUENCE_PREP".run_prefix as RUN_PREFIX, \n'
        statement += '"SEQUENCE_PREP".experiment_title as Description \n'
    
        statement = '\n\
        select distinct \n' + statement + ' \n\
        from "STUDY" inner join user_study us on "STUDY".study_id=us.study_id \n\
        inner join "SAMPLE" on "STUDY".study_id = "SAMPLE".study_id \n\
        inner join "SEQUENCE_PREP" on "SAMPLE".sample_id = "SEQUENCE_PREP".sample_id \n\
        where "STUDY".study_id=%s and "SEQUENCE_PREP".run_prefix=\'%s\' \n' % (study_id,run_prefix[0])

        con = data_access.getMetadataDatabaseConnection()
        cur = con.cursor()
        #req.write(str(statement)+'<br><br>')
        results = cur.execute(statement)
        
        mapping_fname='study_%s_run_%s_mapping.txt' % (study_id,run_prefix[0])
        
        # Write out proper header row, #SampleID, BarcodeSequence, LinkerPrimerSequence, Description, all others....
        mapping_fp = open(path.join(dir_path,mapping_fname) ,'w')

        #req.write('http://localhost:5001/'+map_filepath)
        # All mapping files start with an opening hash
        mapping_fp.write('#')

        # Write the header row
        to_write = ''
        for column in cur.description:
            if column[0]=='SAMPLEID':
                to_write+='SampleID\t'
            elif column[0]=='BARCODE':
                to_write+='BarcodeSequence\t'
            elif column[0]=='DESCRIPTION':
                to_write+='Description\t'
            elif column[0]=='LINKERPRIMERSEQUENCE':
                to_write+='LinkerPrimerSequence\t'
            else:
                to_write += column[0] + '\t'

        mapping_fp.write(to_write[0:len(to_write)-1] + '\n')
    
        sample_to_run_prefix=[]

        samples_list=[]
        map_file_write=[]
        samples_list=[]

        for row in results:
            # Can't use something like '\t'.join(row) because not all items in list
            # are string values, hence the explicit loop structure here.
            to_write = ''
            sample_to_run_prefix.append(list((str(row[0]),str(row[4]),str(row[3]))))

            if str(row[0]) in samples_list:
                # Order of row goes as follows: SampleID, BarcodeSequence,
                # LinkerPrimerSequence,Run_Prefix, then Description is at the end
                row=list(row)
                row[0]=row[0]+'.'+str(row[4])
                row=tuple(row)
            else:    
                samples_list.append(str(row[0]))

            for i,column in enumerate(row):            
                val = str(column)
                if val == 'None':
                    val = ''
                to_write += val + '\t'
            # Write the row minus the last tab
            mapping_fp.write(to_write[0:len(to_write)-1] + '\n')

    

    
if __name__ == "__main__":
    main()
