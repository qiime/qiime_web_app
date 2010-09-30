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
from enums import DataAccessType

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Production"

qda = data_access_factory(DataAccessType.qiime_production)


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

            res = self.cur.execute("SELECT TAXONOMY_STR FROM TAXONOMY WHERE SSU_SEQUENCE_ID=%d AND TAXONOMY_NAME='%s'" % (ssu_id, taxonomy_name))
            all_res = list(res)
            if len(all_res) == 0: 
                self.fail("No records found for taxonomy %s and ssu id %d" % (taxonomy_name, ssu_id))
            if len(all_res) > 1:
                self.fail("Multiple taxonomy strings found for taxonomy %s and ssu id %d" % (taxonomy_name, ssu_id))
            self.assertEqual(all_res[0][0], taxonomy_str)

# the following 100 prokMSA ids were randomly (without replacement) chosen
# from the set of all prokMSA ids known as of 7/26/10

test_recs = """359442\tSilva_tax_string_format_2\tBacteria; Firmicutes; Clostridia_1; Clostridiales; Lachnospiraceae; uncultured; Unclassified; otu_1373
164203\tHOMD_tax_string_format_2\tNone
260564\tHOMD_tax_string_format_2\tNone
487267\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
407225\tPace_tax_string_format_2\tUnclassified; otu_524
519829\tSilva_tax_string_format_2\tUnclassified; otu_2953
212647\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
463412\tHOMD_tax_string_format_2\tNone
485416\tSilva_tax_string_format_2\tUnclassified; otu_2953
349754\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
282996\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
56220\tRDP_tax_string_format_2\tBacteria; Bacteroidetes; Bacteroidetes; Bacteroidales; Porphyromonadaceae; unclassified_Porphyromonadaceae; otu_384
345870\tHOMD_tax_string_format_2\tNone
211495\tncbi_tax_string_format_2\tBacteria; Firmicutes; Clostridia; Clostridiales; Peptostreptococcaceae; Anaerococcus; environmental samples; otu_1718
173870\tSilva_tax_string_format_2\tBacteria; Firmicutes; Bacilli; Lactobacillales; Streptococcaceae; Streptococcus; otu_1265
535971\tSilva_tax_string_format_2\tUnclassified; otu_2953
156205\tPace_tax_string_format_2\tUnclassified; otu_524
139826\tPace_tax_string_format_2\tUnclassified; otu_524
155019\tLudwig_tax_string_format_2\tUnclassified; otu_3346
231279\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
397227\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
504439\tRDP_tax_string_format_2\tUnclassified; otu_1701
435574\tLudwig_tax_string_format_2\tUnclassified; otu_3346
439686\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
505539\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
350919\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
121436\tSilva_tax_string_format_2\tBacteria; Bacteroidetes; Bacteroidia_Bacteroidales; uncultured; otu_566
155867\tPace_tax_string_format_2\tUnclassified; otu_524
381501\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
489074\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
192496\tPace_tax_string_format_2\tUnclassified; otu_524
376833\tHOMD_tax_string_format_2\tNone
101919\tRDP_tax_string_format_2\tBacteria; Tenericutes; Mollicutes; Acholeplasmatales; Acholeplasmataceae; Phytoplasma; otu_1662
125475\tPace_tax_string_format_2\tUnclassified; otu_524
242759\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
267363\tHOMD_tax_string_format_2\tNone
175172\tHugenholtz_tax_string_format_2\tBacteria; Proteobacteria; Gammaproteobacteria; Oceanospirillales; Unclassified; otu_2104
583865\tHOMD_tax_string_format_2\tNone
246522\tSilva_tax_string_format_2\tBacteria; Firmicutes; Clostridia_1; Clostridiales; Lachnospiraceae; Catonella; otu_1349
9793\tncbi_tax_string_format_2\tBacteria; Proteobacteria; Gammaproteobacteria; Enterobacteriales; Enterobacteriaceae; Pectobacterium; otu_3171
177561\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
169110\tHugenholtz_tax_string_format_2\tBacteria; Proteobacteria; Desulfovibrionales; Desulfovibrionaceae; Desulfovibrio_acrylicus; otu_1861
119127\tSilva_tax_string_format_2\tBacteria; Bacteroidetes; Bacteroidia_Bacteroidales; Prevotellaceae; Prevotella; Unclassified; otu_556
432345\tHOMD_tax_string_format_2\tNone
239336\tHOMD_tax_string_format_2\tNone
2803\tHOMD_tax_string_format_2\tNone
499356\tHOMD_tax_string_format_2\tNone
550115\tHOMD_tax_string_format_2\tNone
563347\tLudwig_tax_string_format_2\tUnclassified; otu_3346
281059\tncbi_tax_string_format_2\tBacteria; Proteobacteria; Gammaproteobacteria; Thiotrichales; Francisellaceae; Francisella; Unclassified; otu_3401
376229\tHOMD_tax_string_format_2\tNone
166974\tPace_tax_string_format_2\tUnclassified; otu_524
203736\tHOMD_tax_string_format_2\tNone
188394\tSilva_tax_string_format_2\tBacteria; Firmicutes; Bacilli; Lactobacillales; Streptococcaceae; Streptococcus; otu_1265
248145\tPace_tax_string_format_2\tUnclassified; otu_524
390928\tSilva_tax_string_format_2\tUnclassified; otu_2953
330202\tSilva_tax_string_format_2\tBacteria; Firmicutes_Clostridia_Thermoanaerobacterales_Thermodesulfobiaceae_Coprothermobacter; otu_1575
382124\tRDP_tax_string_format_2\tUnclassified; otu_1701
46052\tPace_tax_string_format_2\tBacteria; Actinobacteria; Actinomyces A; otu_69
586316\tHOMD_tax_string_format_2\tNone
511604\tLudwig_tax_string_format_2\tUnclassified; otu_3346
141737\tRDP_tax_string_format_2\tBacteria; Proteobacteria; Betaproteobacteria; Burkholderiales; Comamonadaceae; Curvibacter; otu_1204
291443\tSilva_tax_string_format_2\tBacteria; Actinobacteria; Actinobacteridae; Actinomycetales_Micromonosporineae_Micromonosporaceae; Verrucosispora; otu_433
275787\tLudwig_tax_string_format_2\tUnclassified; otu_3346
332899\tLudwig_tax_string_format_2\tUnclassified; otu_3346
344949\tHOMD_tax_string_format_2\tNone
68840\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
311451\tPace_tax_string_format_2\tUnclassified; otu_524
181053\tPace_tax_string_format_2\tUnclassified; otu_524
190668\tSilva_tax_string_format_2\tBacteria; Firmicutes; Clostridia_1; Clostridiales; Ruminococcaceae; Incertae Sedis; otu_1406
402088\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
498068\tPace_tax_string_format_2\tUnclassified; otu_524
446554\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
167666\tSilva_tax_string_format_2\tBacteria; Firmicutes; Erysipelotrichi_Erysipelotrichales_Erysipelotrichaceae_Turicibacter; Turicibacter; otu_1523
317847\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
578371\tPace_tax_string_format_2\tUnclassified; otu_524
139596\tHugenholtz_tax_string_format_2\tBacteria; Spirochaetes; Spirochaetales; Borreliaceae; Borrelia; Unclassified; otu_2225
343208\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
263888\tHOMD_tax_string_format_2\tNone
359157\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
471331\tPace_tax_string_format_2\tUnclassified; otu_524
8736\tHOMD_tax_string_format_2\tNone
410651\tRDP_tax_string_format_2\tUnclassified; otu_1701
496420\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
537345\tLudwig_tax_string_format_2\tUnclassified; otu_3346
248395\tRDP_tax_string_format_2\tBacteria; Proteobacteria; Alphaproteobacteria; Caulobacterales; Caulobacteraceae; Caulobacter; otu_967
271353\tRDP_tax_string_format_2\tBacteria; Firmicutes; "Clostridia"; Clostridiales; "Lachnospiraceae"; unclassified_"Lachnospiraceae"; otu_762
417637\tPace_tax_string_format_2\tUnclassified; otu_524
449888\tLudwig_tax_string_format_2\tUnclassified; otu_3346
278597\tSilva_tax_string_format_2\tBacteria; Proteobacteria; Epsilonproteobacteria; Campylobacterales_Helicobacteraceae_Sulfurovum; otu_2431
27556\tRDP_tax_string_format_2\tBacteria; Firmicutes; "Bacilli"; Bacillales; Bacillaceae; "Bacillaceae 2"; Oceanobacillus; otu_687
344413\tPace_tax_string_format_2\tUnclassified; otu_524
436132\tSilva_tax_string_format_2\tUnclassified; otu_2953
33081\tncbi_tax_string_format_2\tBacteria; Proteobacteria; Alphaproteobacteria; Rhizobiales; Bradyrhizobiaceae; Bradyrhizobium; Unclassified; otu_2148
376704\tncbi_tax_string_format_2\tBacteria; environmental samples; Unclassified; otu_1343
581183\tHugenholtz_tax_string_format_2\tUnclassified; otu_2409
389512\tHOMD_tax_string_format_2\tNone
175941\tSilva_tax_string_format_2\tBacteria; Firmicutes; Clostridia_1; Clostridiales; Lachnospiraceae; Unclassified; otu_1339
339127\tRDP_tax_string_format_2\tBacteria; Tenericutes; Mollicutes; Acholeplasmatales; Acholeplasmataceae; Phytoplasma; otu_1662
206012\tLudwig_tax_string_format_2\tUnclassified; otu_3346""".splitlines()

test_mapping = {}
for l in test_recs:
    fields = l.strip().split('\t')
    test_mapping[int(fields[0])] = (fields[1], fields[2])

if __name__ == '__main__':
    main()
            


