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
    make_option('-f','--write_full_mapping',action='store_true',help='By setting this parameter, you can write out all metadata for study.',default=False),\
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
    write_full_mapping=opts.write_full_mapping
    
    con = data_access.getMetadataDatabaseConnection()
    cur = con.cursor()
    column_table=data_access.getMetadataFields(study_id)
    new_cat_column_table=[]
    new_tables=[]
    for i in column_table:
        col_name=i[1]+'.'+i[0]
        if col_name not in ['"SEQUENCE_PREP".RUN_PREFIX',\
                            '"SEQUENCE_PREP".BARCODE','"SEQUENCE_PREP".LINKER', \
                            '"SEQUENCE_PREP".PRIMER','"SAMPLE".STUDY_ID',\
                            '"SEQUENCE_PREP".RUN_PREFIX',\
                            '"SEQUENCE_PREP".EXPERIMENT_TITLE',
                            '"SAMPLE".PUBLIC']:
            new_cat_column_table.append(i[1]+'.'+i[0])
        if i[1] not in ['"STUDY"', '"USER_STUDY"','"SAMPLE"','"SEQUENCE_PREP"']\
            and i[1] not in new_tables:
            new_tables.append(i[1])
    
    #req.write(str(statement)+'<br><br>')
    run_prefixes = cur.execute('select distinct sp.RUN_PREFIX from SEQUENCE_PREP sp \
    inner join "SAMPLE" s on s.sample_id=sp.sample_id where s.study_id=%s' % (study_id))
    for run_prefix in run_prefixes:
    
        # Start building the statement for writing out the mapping file
        # THIS ORDER MUST REMAIN THE SAME SINCE CHANGES WILL AFFECT LATER FUNCTION
        statement = '("SAMPLE".SAMPLE_NAME||\'.\'||"SEQUENCE_PREP".ROW_NUMBER) as SampleID, \n'
        statement += '"SEQUENCE_PREP".BARCODE, \n'
        statement += 'concat("SEQUENCE_PREP".LINKER, "SEQUENCE_PREP".PRIMER) as LinkerPrimerSequence, \n'
        statement += '"SAMPLE".STUDY_ID, \n'
        statement += '"SEQUENCE_PREP".RUN_PREFIX as RUN_PREFIX, \n'
        
        if write_full_mapping:
            for col_tab in new_cat_column_table:
                statement += '%s, \n' % (col_tab)
        
        statement += '"SEQUENCE_PREP".EXPERIMENT_TITLE as Description_new \n'
    
        statement = '\n\
        select distinct \n' + statement + ' \n\
        from "STUDY" \
        inner join "USER_STUDY" us on "STUDY".study_id=us.study_id \n\
        inner join "SAMPLE" on "STUDY".study_id = "SAMPLE".study_id \n\
        inner join "SEQUENCE_PREP" on "SAMPLE".sample_id = "SEQUENCE_PREP".sample_id \n'
        
        if write_full_mapping:
            # Handle Common fields table
            if '"COMMON_FIELDS"' in new_tables:
                new_tables.remove('"COMMON_FIELDS"')
                statement += '\
                inner join "COMMON_FIELDS" \n\
                on "SAMPLE".sample_id = "COMMON_FIELDS".sample_id \n'

            # Deal with the rest of the tables. They should all be assocaiated by sample id.
            for table in new_tables:
                if table=='"HOST"':
                    try:
                        new_tables.remove('"HOST_SAMPLE"')
                    except:
                        pass
                    statement += '\
                    inner join "HOST_SAMPLE" \n\
                    on "SAMPLE".sample_id = "HOST_SAMPLE".sample_id\n'
                    statement += '\
                    inner join ' + table + '\n\
                    on "HOST_SAMPLE".host_id = ' + table + '.host_id\n '
                else:
                    statement += '\
                    inner join ' + table + '\n\
                    on "SAMPLE".sample_id = ' + table + '.sample_id\n '
                    
        statement += '\n\
        where "STUDY".study_id=%s and "SEQUENCE_PREP".run_prefix=\'%s\' \n' % (study_id,run_prefix[0])
        
        #print statement
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
                to_write+='Description_duplicate\t'
            elif column[0]=='DESCRIPTION_NEW':
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
