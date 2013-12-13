#!/usr/bin/env python
# File created on 27 Nov 2013
from __future__ import division

__author__ = "Emily TerAvest"
__copyright__ = "Copyright 2011, The QIIME Web App"
__credits__ = ["Emily TerAvest"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Emily TerAvest"
__email__ = "ejteravest@gmail.com"
__status__ = "Development"


from qiime.util import parse_command_line_parameters, make_option
from data_access_connections import data_access_factory
from enums import ServerConfig

script_info = {}
script_info['brief_description'] = "this script takes in a obo file and " \
            "update the ontology database"
script_info['script_description'] = "takes an obo file downloaded from " \
            "bioportal.bioontology.org or the ontology website. This script " \
            "then parses the obo file and then adds terms not in the ontology"\
            "database to the database"
script_info['script_usage'] = [("","","")]
script_info['output_description']= "this script has no output"
script_info['required_options'] = [
    make_option('-i','--input_fp',type="existing_filepath",help='obo filepath'),
    make_option('--ontology', type="string", help='ontology short name'),
    make_option('-o', '--sql_output_fp', type="new_filepath", 
                help='sql output file'),
    make_option('-r', '--relationship_output', type="new_filepath",
                help='relationship output file')]
script_info['optional_options'] = []
script_info['version'] = __version__



def main():

    data_access = data_access_factory(ServerConfig.data_access_type)
    con = data_access.getOntologyDatabaseConnection()
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    ontology_query = "select ontology_id from ontology where shortname = '%s'" \
                    % opts.ontology
    results = con.cursor().execute(ontology_query)
    ontology_ids = [row[0] for row in results][0]
    ontology_id = ontology_ids
    
    onto_namespace = opts.ontology
    query_string = "select \"IDENTIFIER\" from  term where ontology_id ="\
                    " \'%s\'" % ontology_id 
    results = con.cursor().execute(query_string)
    exsisting_terms = [row[0] for row in results]
    obo_file = opts.input_fp
    obo = open(obo_file, "r")
    line = obo.readline()
    sqlfile = open(opts.sql_output_fp, 'w')
    relationshipfile = open(opts.relationship_output, 'w')
    count = 0

    sqlfile.write("SET ESCAPE ON;\nSET ESCAPE '\\';\n")
    while(line):
        if line == "[Term]\n":
            #read in lines and save info until blank line
            count = count + 1
            term_values = {'def': ['null'] }
            term_line = obo.readline()
            while(term_line != "\n"):
                #split the line only on the first colon
                t_key, t_value = term_line.split(': ', 1)
                if t_key in term_values and t_key != 'def':
                    term_values[t_key].append(t_value.strip())
                else:
                    term_values[t_key] = [t_value.strip()]

                term_line = obo.readline() 
            #now we need to add term_values to the database
           
            if not term_values['id'][0] in exsisting_terms:
                insert_stmt = "Insert into Term (ontology_id, term_name, " \
                    "IDENTIFIER, definition, namespace, is_obsolete, " \
                    "is_root_term, is_leaf) values ('%s', '%s', '%s', '%s', '%s', 0, 0, 0);\n" \
                    % (ontology_id, term_values['name'][0].replace('\'','\'\''), term_values['id'][0], \
                    term_values['def'][0].split('\" ')[0].strip('\"').replace('\'',\
                        '\'\'').replace('&', '\&'), onto_namespace)
                sqlfile.write(insert_stmt)
                if 'is_a' in term_values:  
                    #find the other term in the relationship
                    object_terms = [a.split(' ! ')[0] for a in term_values['is_a']]
                    #find the id of that term in the database
                    #get the id for the term we are working on now
                    for obj_term in object_terms:
                        relation_string = "%s IS_A %s\n" % (term_values['id'][0], \
                                            obj_term)
                        relationshipfile.write(relation_string) 

                if 'relationship' in term_values:
                    relations = [a.split(' ') for a in term_values['relationship']]
                    for relation in relations:
                        relation_string = "%s %s %s\n" % (term_values['id'][0], \
                                        relation[0], relation[1])
                        relationshipfile.write(relation_string)
            if 'is_obsolete' in term_values:
                update_stmt = "update term set is_obsolete = 1 where "\
                "\"IDENTIFIER\" = '%s';\n" % term_values['id'][0]
                sqlfile.write(update_stmt)   

            
        line = obo.readline()
    print count     
    obo.close()
    sqlfile.write("commit;\n")
    sqlfile.close()
    con.close()
    return

if __name__ == "__main__":
    main()