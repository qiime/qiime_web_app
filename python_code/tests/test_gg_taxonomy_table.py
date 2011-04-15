#!/usr/bin/env python

"""This is a functional test of the SFF.TAXONOMY table

For this test, we are making sure that we

a) have information for each prokMSA id in our test set
b) make sure we only have a single SSU_SEQUENCE_ID per test prokMSA
c) have only a single taxonomy string for a given ssu id and taxonomy name
d) make sure we have the correct taxonomy string
"""

from cogent.util.unit_test import TestCase, main
from data_access_connections import data_access_factory
from enums import ServerConfig

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Production"

qda = data_access_factory(ServerConfig.data_access_type)


class LoadDBGreenGenesTaxonomyTable(TestCase):
    def setUp(self):
        """Grab a connection"""
        self.con = qda.getSFFDatabaseConnection()
        self.cur = self.con.cursor()
    def tearDown(self):
        """Make sure to close the connection"""
        self.con.close()

    def test_verify_taxonomy_data(self):
        """Grab taxonomy strings from test prokmsas, verify correct result"""
        for prokmsa in test_mapping:
            res = self.cur.execute('SELECT SSU_SEQUENCE_ID FROM GREENGENES_REFERENCE WHERE PROKMSA_ID=%d' % prokmsa)
            all_res = list(res)
            if len(all_res) == 0:
                self.fail("No records found for prokMSA id %d" % prokmsa)
            if len(all_res) > 1:
                self.fail("Multiple records found for prokMSA id %d" % prokmsa)
            ssu_id = all_res[0][0]

            taxonomy_name, taxonomy_str = test_mapping[prokmsa]

            res = self.cur.execute("SELECT TAXONOMY_STR FROM GREENGENES_TAXONOMY WHERE prokmsa_id=%d AND TAXONOMY_NAME='%s'" % (prokmsa, taxonomy_name))
            all_res = list(res)
            if len(all_res) == 0: 
                self.fail("No records found for taxonomy %s and prokmsa %d" % (taxonomy_name, prokmsa))
            if len(all_res) > 1:
                self.fail("Multiple taxonomy strings found for taxonomy %s and prokmsa %d" % (taxonomy_name, prokmsa))
            self.assertEqual(all_res[0][0], taxonomy_str)

# the following 100 prokMSA ids were randomly (without replacement) chosen
# from the set of all prokMSA ids known as of 7/26/10

test_recs = """\
487267\tncbi_tax_string\tBacteria; environmental samples
407225\tPace_tax_string\tUnclassified
282996\tncbi_tax_string\tBacteria; environmental samples
56220\tRDP_tax_string\tBacteria; Bacteroidetes; Bacteroidetes; Bacteroidales; Porphyromonadaceae; unclassified_Porphyromonadaceae
211495\tncbi_tax_string\tBacteria; Firmicutes; Clostridia; Clostridiales; Peptostreptococcaceae; Anaerococcus; environmental samples
156205\tPace_tax_string\tUnclassified
139826\tPace_tax_string\tUnclassified
231279\tncbi_tax_string\tBacteria; environmental samples
397227\tncbi_tax_string\tBacteria; environmental samples
504439\tRDP_tax_string\tUnclassified
435574\tLudwig_tax_string\tUnclassified
439686\tHugenholtz_tax_string\tUnclassified
505539\tncbi_tax_string\tBacteria; environmental samples
350919\tHugenholtz_tax_string\tUnclassified
155867\tPace_tax_string\tUnclassified
381501\tHugenholtz_tax_string\tUnclassified
489074\tncbi_tax_string\tBacteria; environmental samples
101919\tRDP_tax_string\tBacteria; Tenericutes; Mollicutes; Acholeplasmatales; Acholeplasmataceae; Phytoplasma
125475\tPace_tax_string\tUnclassified
242759\tncbi_tax_string\tBacteria; environmental samples
""".splitlines()

test_mapping = {}
for l in test_recs:
    fields = l.strip().split('\t')
    test_mapping[int(fields[0])] = (fields[1], fields[2])

if __name__ == '__main__':
    main()
            


