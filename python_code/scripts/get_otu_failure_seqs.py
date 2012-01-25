#!/usr/bin/env python
# File created on 30 Dec 2011
from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.3.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 


from qiime.util import parse_command_line_parameters, make_option
from data_access_connections import data_access_factory
from enums import ServerConfig,DataAccessType

seq_methods=['GS FLX', 'Titanium','ILLUMINA']

script_info = {}
script_info['brief_description'] = "This script takes a list of comma-separated reverse primers and comma-separated list of sequencing methods and returns a fasta containing a list of unique sequences that failed when using uclust_ref against GGs 975"
script_info['script_description'] = ""
script_info['script_usage'] = [("Example","Write a list of V2 Titanium reads that do not hit GGs.","python get_otu_failure_seqs.py -p TGCTGCCTCCCGTAGGAGT -s 'Titanium' -o test.fasta")]
script_info['output_description']= "Generates a fasta file containing unique sequences that do not hit GGs"
script_info['required_options'] = [\
 make_option('-p','--primers',type="string",
             help='comma-separated list of the rev primers to check'),\
 make_option('-s','--sequencing_method',type="string",
             help='comma-separated list of sequencing technologies to check (%s)' % ', '.join(seq_methods)),\
 make_option('-o','--output_fp',type="new_filepath",
             help='output fasta filepath]'),\
]
script_info['optional_options'] = [\
 make_option('-t','--use_test_db',action="store_true",default='False',
             help='check against the test database [default: %default]'),\
 make_option('-x','--min_samples',type="int",default=2,
             help='minimum number of samples the sequence appears in [default: %default]'),\
 make_option('-y','--min_seqs',type="int",default=20,
             help='minimum number of times the sequence appears [default: %default]'),\
]
script_info['version'] = __version__


def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    # get command-line parameters
    use_test_db=opts.use_test_db
    primers=opts.primers.split(',')
    sequencing_method=opts.sequencing_method.split(',')
    output_fp = open(opts.output_fp,'w')
    
    # create a data access object to the DB of choice
    if use_test_db == 'False':
       # Load the data into the database
       data_access = data_access_factory(ServerConfig.data_access_type)
    else:
       # Load the data into the database 
       data_access = data_access_factory(DataAccessType.qiime_test)
    
    # convert comma-separated list of primers to PL/SQL syntax
    primer_strings=[]
    for i in primers:
        primer_strings.append('sp.primer=\''+i+'\'')
        
    # convert comma-separated list of sequencing methods to PL/SQL syntax
    seq_method_strings=[]
    for i in sequencing_method:
        seq_method_strings.append('sr.instrument_code=\''+i+'\'')
    
    # write PL/SQL query statement
    statement="select distinct ss.ssu_sequence_id,ss.sequence_string from otu_picking_failures opf " +\
       "inner join ssu_sequence ss on opf.ssu_sequence_id=ss.ssu_sequence_id " +\
       "inner join analysis an on opf.otu_picking_run_id=an.otu_picking_run_id " +\
       "inner join sequencing_run sr on an.seq_run_id=sr.seq_run_id " +\
       "inner join qiime_metadata.sample sa on an.study_id=sa.study_id " +\
       "inner join qiime_metadata.sequence_prep sp on sa.sample_id=sp.sample_id " +\
       "where (%s) and (%s)" % (' or '.join(primer_strings),' or '.join(seq_method_strings))
    #print statement 
    
    # Run the statement
    con = data_access.getSFFDatabaseConnection()
    cur = con.cursor()
    count=0
    # write resulting fasta file
    results = cur.execute(statement)
    #print results
    for i in results:
        
        # pull out the sample and sequence counts based on ssu_sequence_id
        check_seq_count_statement="select count(slrm.ssu_sequence_id), " +\
                                  "count(distinct slrm.sample_name) " +\
                                  "from split_library_read_map slrm " +\
                                  "where slrm.ssu_sequence_id=\'%s\'" % \
                                  (i[0])
                                  

        # write resulting fasta file
        cur2 = con.cursor()
        results2 = cur2.execute(check_seq_count_statement) 
        
        for j in results2:
            # check if sequence appears more than 20 times or in more than 
            # 1 sample or in more than 1 study
            if (j[0]>=int(opts.min_seqs)) or (j[1]>=int(opts.min_samples)):
                output_fp.write('>%s\n%s\n' % (i[0],i[1]))
                count=count+1
                
    output_fp.close()

if __name__ == "__main__":
    main()
