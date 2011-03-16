#!/usr/bin/env python
# File created on 16 Mar 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME-webdev project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
from os import path

def write_mapping_file(study_id,write_full_mapping,dir_path,get_from_test_db):
    
    try:
        from data_access_connections import data_access_factory
        from enums import DataAccessType
        import cx_Oracle
        if get_from_test_db:
            data_access = data_access_factory(DataAccessType.qiime_test)
        else:
            data_access = data_access_factory(DataAccessType.qiime_production)
    except ImportError:
        print "NOT IMPORTING QIIMEDATAACCESS"
        pass
    
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
    run_prefix_list=[]
    run_prefixes = cur.execute('select distinct sp.RUN_PREFIX from SEQUENCE_PREP sp \
    inner join "SAMPLE" s on s.sample_id=sp.sample_id where s.study_id=%s' % (study_id))
    for run_prefix in run_prefixes:
        run_prefix_list.append(run_prefix[0])
        # Start building the statement for writing out the mapping file
        # THIS ORDER MUST REMAIN THE SAME SINCE CHANGES WILL AFFECT LATER FUNCTION
        statement = '("SAMPLE".SAMPLE_NAME||\'.\'||"SEQUENCE_PREP".SEQUENCE_PREP_ID) as SampleID, \n'
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

    return run_prefix_list