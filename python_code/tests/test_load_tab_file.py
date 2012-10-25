#!/usr/bin/env python
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "QIIME-webdev"
__credits__ = ["Jesse Stombaugh","Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"

from datetime import datetime
from cogent.parse.flowgram_parser import parse_sff
from cogent.util.unit_test import TestCase, main
from load_tab_file import unzip_and_cast_to_cxoracle_types,input_set_generator,fasta_to_tab_delim, unzip_flow, flowfile_inputset_generator

type_lookup_mock = {'i':int,'f':float,'s':str, 'd':lambda x: x, 'c':str}
class MockConnection(object):
    def __init__(self):
        pass
    def connect(self, *args, **kwargs):
        return self
    def cursor(self):
        return self
    def arrayvar(self, cast_type, data):
        return map(cast_type, data)
    def commit(self):
        return self
    def close(self):
        return self
    def callproc(self, *args):
        pass
    def var(self, foo):
        return self
    def setvalue(self,foo, bar):
        return bar

class ParseAndLoadDBTests(TestCase):
    def test_unzip_and_cast_to_cxoracle_types(self):
        """Tests that we can unzip and cast"""
        input = [['1','asd','0.0'],
                 ['2','123','0.2'],
                 ['3','qwe','0.3'],
                 ['4','zxc','0.4'],
                 ['5','qaz','0.5']]
        con = MockConnection()
        cursor = con.cursor()
        types = ['i','s','f']
        obs = unzip_and_cast_to_cxoracle_types(input,cursor,types,type_lookup=type_lookup_mock)

        exp = [[1,2,3,4,5],['asd','123','qwe','zxc','qaz'],
                [0.0,0.2,0.3,0.4,0.5]]

        self.assertEqual(obs, exp)

    def test_input_set_generator(self):
        """Test that we're generating data sets to input"""
        input = """#int\tstr\tfloat
1\tasd\t0.0
2\t123\t0.2
3\t\t0.3
4\tzxc\t0.4
5\tqaz\t0.5""".splitlines()
        con = MockConnection()
        cursor = con.cursor()
        types = ['i','s','f']

        gen = input_set_generator(input,cursor,types,2,type_lookup=type_lookup_mock)
        exp1 = [[1,2],['asd','123'],[0.0,0.2]]
        exp2 = [[3,4],['','zxc'],[0.3,0.4]]
        exp3 = [[5],['qaz'],[0.5]]
        obs1 = gen.next()
        obs2 = gen.next()
        obs3 = gen.next()

        self.assertRaises(StopIteration, gen.next)

        self.assertEqual(obs1, exp1)
        self.assertEqual(obs2, exp2)
        self.assertEqual(obs3, exp3)

    def test_fasta_to_tab_delim(self):
        """make sure we can go from fasta to tab delim"""
        input = """>a RUN1 orig_bc=AAAA new_bc=AAAA bc_diffs=0
123123123
>d RUN1 orig_bc=AAAA new_bc=AAAA bc_diffs=0
atcasdad
>h RUN1 orig_bc=AAAA new_bc=AAAA bc_diffs=0
10 11 12"""
        exp = ['1\t1\ta\ta\tRUN1\tAAAA\tAAAA\t0\t9\tf5bb0c8de146c67b44babbf4e6584cc0\t123123123', '1\t1\td\td\tRUN1\tAAAA\tAAAA\t0\t8\t1fae8caaf715bdc710b99e8c3e843092\tatcasdad', '1\t1\th\th\tRUN1\tAAAA\tAAAA\t0\t8\tb4c2a347f5d0453c4fdae6d5c7b5bc78\t10 11 12']
        obs = list(fasta_to_tab_delim(input.splitlines(),1,1))
        self.assertEqual(obs, exp)

    def test_unzip_flow(self):
        """Properly unzips a flow"""
        exp = [1,
               'FIQU8OX05GCVRO',
               'tcagGCTAACTGTAACCCTCTTGGCACCCACTAAACGCCAATCTTGCTGGAGTGTTTACCAGGCACCCAGCAATGTGAATAGTCActgagcgggctggcaaggc',
               104,
               'R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford',
               datetime(2008,10,15,16,11,02),
               5,
               2489,
               3906,
               '1.06\t0.08\t1.04\t0.08\t0.05\t0.94\t0.10\t2.01\t0.10\t0.07\t0.96\t0.09\t1.04\t1.96\t1.07\t0.10\t1.01\t0.13\t0.08\t1.01\t1.06\t1.83\t2.89\t0.18\t0.96\t0.13\t0.99\t0.11\t1.94\t0.12\t0.13\t1.92\t0.21\t0.07\t0.94\t0.17\t0.03\t0.97\t2.76\t0.15\t0.05\t1.02\t1.14\t0.10\t0.98\t2.54\t1.13\t0.96\t0.15\t0.21\t1.90\t0.16\t0.07\t1.78\t0.22\t0.07\t0.93\t0.22\t0.97\t0.08\t2.02\t0.15\t0.19\t1.02\t0.19\t0.09\t1.02\t0.17\t0.99\t0.09\t0.18\t1.84\t0.16\t0.91\t0.10\t1.10\t1.00\t0.20\t0.09\t1.11\t3.01\t1.07\t1.98\t0.14\t0.22\t1.09\t0.17\t1.99\t0.15\t0.20\t0.92\t0.17\t0.07\t1.01\t2.96\t0.15\t0.07\t1.06\t0.20\t1.00\t0.10\t0.12\t1.00\t0.15\t0.08\t1.90\t0.19\t0.10\t0.99\t0.18\t0.09\t0.99\t1.08\t0.15\t0.07\t1.06\t0.14\t1.84\t0.13\t0.11\t0.95\t1.05\t0.13\t1.04\t1.10\t0.18\t0.94\t0.14\t0.10\t0.97\t1.08\t0.12\t1.08\t0.18\t0.08\t1.00\t0.13\t0.98\t0.15\t0.87\t0.13\t0.19\t1.01\t3.06\t0.17\t0.11\t1.04\t0.09\t1.03\t0.10\t0.11\t2.02\t0.16\t0.11\t1.04\t0.04\t0.09\t1.87\t0.13\t2.09\t0.13\t0.10\t0.97\t0.17\t0.08\t0.08\t0.04\t0.12\t0.05\t0.08\t0.07\t0.08\t0.05\t0.07\t0.06\t0.07\t0.03\t0.05\t0.04\t0.09\t0.04\t0.07\t0.04\t0.07\t0.06\t0.03\t0.06\t0.06\t0.06\t0.06\t0.07\t0.09\t0.04\t0.05\t0.08\t0.05\t0.04\t0.09\t0.06\t0.03\t0.02\t0.08\t0.04\t0.06\t0.05\t0.08\t0.03\t0.08\t0.05\t0.05\t0.05\t0.10\t0.05\t0.05\t0.07\t0.06\t0.04\t0.06\t0.05\t0.03\t0.04\t0.05\t0.06\t0.04\t0.04\t0.07\t0.04\t0.04\t0.05\t0.05\t0.04\t0.07\t0.06\t0.05\t0.03\t0.08\t0.05\t0.06\t0.04\t0.06\t0.05\t0.04\t0.04\t0.04\t0.05\t0.06\t0.04\t0.05\t0.04\t0.05\t0.05\t0.06\t0.05\t0.06\t0.04\t0.06\t0.07\t0.06\t0.05\t0.05\t0.05\t0.06\t0.06\t0.04\t0.05\t0.06\t0.03\t0.06\t0.04\t0.06\t0.05\t0.03\t0.06\t0.06\t0.05\t0.06\t0.04\t0.03\t0.06\t0.06\t0.06\t0.03\t0.04\t0.05\t0.05\t0.07\t0.04\t0.05\t0.06\t0.07\t0.07\t0.05\t0.07\t0.06\t0.05\t0.06\t0.05\t0.07\t0.06\t0.05\t0.06\t0.07\t0.05\t0.06\t0.04\t0.06\t0.05\t0.05\t0.06\t0.04\t0.06\t0.04\t0.03\t0.06\t0.05\t0.05\t0.04\t0.05\t0.05\t0.04\t0.04\t0.05\t0.06\t0.06\t0.04\t0.04\t0.05\t0.06\t0.04\t0.04\t0.04\t0.05\t0.05\t0.04\t0.05\t0.05\t0.03\t0.06\t0.06\t0.06\t0.04\t0.07\t0.05\t0.05\t0.04\t0.06\t0.06\t0.05\t0.05\t0.07\t0.04\t0.06\t0.06\t0.06\t0.04\t0.06\t0.03\t0.06\t0.04\t0.06\t0.04\t0.09\t0.05\t0.05\t0.05\t0.07\t0.06\t0.05\t0.05\t0.06\t0.05\t0.05\t0.05\t0.04\t0.04\t0.06\t0.05\t0.05\t0.05\t0.05\t0.04\t0.05\t0.05\t0.06\t0.04\t0.05\t0.05\t0.05\t0.05\t0.05\t0.04\t0.06\t0.04\t0.05\t0.05\t0.04\t0.05\t0.05\t0.05\t0.04',
               '1\t3\t6\t8\t8\t11\t13\t14\t14\t15\t17\t20\t21\t22\t22\t23\t23\t23\t25\t27\t29\t29\t32\t32\t35\t38\t39\t39\t39\t42\t43\t45\t46\t46\t46\t47\t48\t51\t51\t54\t54\t57\t59\t61\t61\t64\t67\t69\t72\t72\t74\t76\t77\t80\t81\t81\t81\t82\t83\t83\t86\t88\t88\t91\t94\t95\t95\t95\t98\t100\t103\t106\t106\t109\t112\t113\t116\t118\t118\t121\t122\t124\t125\t127\t130\t131\t133\t136\t138\t140\t143\t144\t144\t144\t147\t149\t152\t152\t155\t158\t158\t160\t160\t163',
               5,
               85,
               0,
               0,
               24,
               40,
               36.5,
               '37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t40\t40\t40\t40\t37\t37\t37\t37\t37\t39\t39\t39\t39\t24\t24\t24\t37\t34\t28\t24\t24\t24\t28\t34\t39\t39\t39\t39\t39\t39\t39\t39\t39\t39\t39\t39\t40\t40\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37\t37']
        obs = unzip_flow(flows[0], 1, 2)

        self.assertEqual(obs, exp)

    def test_flowfile_inputset_generator(self):
        """Make sure we are yielding the correct stuff"""
        input = test_flowgrams
        # only testing some of the fields out of the sake of sanity
        exp_names = ['FIQU8OX05GCVRO','FIQU8OX05F8ILF']
        exp_num_bases = [104,206]
        exp_run_names = ['R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford','foo']
        exp_run_dates = [datetime(2008,10,15,16,11,02),
                         datetime(2008,10,15,16,11,02)]
        exp_x = [2489, 2440]
        exp_y = [3906, 913]
        exp_qual_min = [24, 20]
        exp_qual_max = [40, 40]

        con = MockConnection()
        cur = con.cursor()
        gen = flowfile_inputset_generator(input, cur, 1, 'foo', 2, type_lookup_mock)
        res = list(gen.next())

        self.assertEqual(res[1], exp_names)
        self.assertEqual(res[3], exp_num_bases)
        self.assertEqual(res[5], exp_run_dates)
        self.assertEqual(res[7], exp_x)
        self.assertEqual(res[8], exp_y)
        self.assertEqual(res[17], exp_qual_min)
        self.assertEqual(res[18], exp_qual_max)
         

test_flowgrams = """Common Header:
  Magic Number:  0x2E736666
  Version:       0001
  Index Offset:  96099976
  Index Length:  1158685
  # of Reads:    57902
  Header Length: 440
  Key Length:    4
  # of Flows:    400
  Flowgram Code: 1
  Flow Chars:    TACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACG
  Key Sequence:  TCAG

>FIQU8OX05GCVRO
  Run Prefix:   R_2008_10_15_16_11_02_
  Region #:     5
  XY Location:  2489_3906

  Run Name:       R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford
  Analysis Name:  /data/2008_10_15/R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford/D_2008_10_15_15_12_26_FLX04070166_1548jinnescurtisstanford_FullAnalysis
  Full Path:      /data/2008_10_15/R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford/D_2008_10_15_15_12_26_FLX04070166_1548jinnescurtisstanford_FullAnalysis

  Read Header Len:  32
  Name Length:      14
  # of Bases:       104
  Clip Qual Left:   5
  Clip Qual Right:  85
  Clip Adap Left:   0
  Clip Adap Right:  0

Flowgram:	1.06	0.08	1.04	0.08	0.05	0.94	0.10	2.01	0.10	0.07	0.96	0.09	1.04	1.96	1.07	0.10	1.01	0.13	0.08	1.01	1.06	1.83	2.89	0.18	0.96	0.13	0.99	0.11	1.94	0.12	0.13	1.92	0.21	0.07	0.94	0.17	0.03	0.97	2.76	0.15	0.05	1.02	1.14	0.10	0.98	2.54	1.13	0.96	0.15	0.21	1.90	0.16	0.07	1.78	0.22	0.07	0.93	0.22	0.97	0.08	2.02	0.15	0.19	1.02	0.19	0.09	1.02	0.17	0.99	0.09	0.18	1.84	0.16	0.91	0.10	1.10	1.00	0.20	0.09	1.11	3.01	1.07	1.98	0.14	0.22	1.09	0.17	1.99	0.15	0.20	0.92	0.17	0.07	1.01	2.96	0.15	0.07	1.06	0.20	1.00	0.10	0.12	1.00	0.15	0.08	1.90	0.19	0.10	0.99	0.18	0.09	0.99	1.08	0.15	0.07	1.06	0.14	1.84	0.13	0.11	0.95	1.05	0.13	1.04	1.10	0.18	0.94	0.14	0.10	0.97	1.08	0.12	1.08	0.18	0.08	1.00	0.13	0.98	0.15	0.87	0.13	0.19	1.01	3.06	0.17	0.11	1.04	0.09	1.03	0.10	0.11	2.02	0.16	0.11	1.04	0.04	0.09	1.87	0.13	2.09	0.13	0.10	0.97	0.17	0.08	0.08	0.04	0.12	0.05	0.08	0.07	0.08	0.05	0.07	0.06	0.07	0.03	0.05	0.04	0.09	0.04	0.07	0.04	0.07	0.06	0.03	0.06	0.06	0.06	0.06	0.07	0.09	0.04	0.05	0.08	0.05	0.04	0.09	0.06	0.03	0.02	0.08	0.04	0.06	0.05	0.08	0.03	0.08	0.05	0.05	0.05	0.10	0.05	0.05	0.07	0.06	0.04	0.06	0.05	0.03	0.04	0.05	0.06	0.04	0.04	0.07	0.04	0.04	0.05	0.05	0.04	0.07	0.06	0.05	0.03	0.08	0.05	0.06	0.04	0.06	0.05	0.04	0.04	0.04	0.05	0.06	0.04	0.05	0.04	0.05	0.05	0.06	0.05	0.06	0.04	0.06	0.07	0.06	0.05	0.05	0.05	0.06	0.06	0.04	0.05	0.06	0.03	0.06	0.04	0.06	0.05	0.03	0.06	0.06	0.05	0.06	0.04	0.03	0.06	0.06	0.06	0.03	0.04	0.05	0.05	0.07	0.04	0.05	0.06	0.07	0.07	0.05	0.07	0.06	0.05	0.06	0.05	0.07	0.06	0.05	0.06	0.07	0.05	0.06	0.04	0.06	0.05	0.05	0.06	0.04	0.06	0.04	0.03	0.06	0.05	0.05	0.04	0.05	0.05	0.04	0.04	0.05	0.06	0.06	0.04	0.04	0.05	0.06	0.04	0.04	0.04	0.05	0.05	0.04	0.05	0.05	0.03	0.06	0.06	0.06	0.04	0.07	0.05	0.05	0.04	0.06	0.06	0.05	0.05	0.07	0.04	0.06	0.06	0.06	0.04	0.06	0.03	0.06	0.04	0.06	0.04	0.09	0.05	0.05	0.05	0.07	0.06	0.05	0.05	0.06	0.05	0.05	0.05	0.04	0.04	0.06	0.05	0.05	0.05	0.05	0.04	0.05	0.05	0.06	0.04	0.05	0.05	0.05	0.05	0.05	0.04	0.06	0.04	0.05	0.05	0.04	0.05	0.05	0.05	0.04
Flow Indexes:	1	3	6	8	8	11	13	14	14	15	17	20	21	22	22	23	23	23	25	27	29	29	32	32	35	38	39	39	39	42	43	45	46	46	46	47	48	51	51	54	54	57	59	61	61	64	67	69	72	72	74	76	77	80	81	81	81	82	83	83	86	88	88	91	94	95	95	95	98	100	103	106	106	109	112	113	116	118	118	121	122	124	125	127	130	131	133	136	138	140	143	144	144	144	147	149	152	152	155	158	158	160	160	163
Bases:	tcagGCTAACTGTAACCCTCTTGGCACCCACTAAACGCCAATCTTGCTGGAGTGTTTACCAGGCACCCAGCAATGTGAATAGTCActgagcgggctggcaaggc
Quality Scores:	37	37	37	37	37	37	37	37	37	37	37	37	37	40	40	40	40	37	37	37	37	37	39	39	39	39	24	24	24	37	34	28	24	24	24	28	34	39	39	39	39	39	39	39	39	39	39	39	39	40	40	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37

>FIQU8OX05F8ILF
  Run Prefix:   R_2008_10_15_16_11_02_
  Region #:     5
  XY Location:  2440_0913

  Analysis Name:  /data/2008_10_15/R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford/D_2008_10_15_15_12_26_FLX04070166_1548jinnescurtisstanford_FullAnalysis
  Full Path:      /data/2008_10_15/R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford/D_2008_10_15_15_12_26_FLX04070166_1548jinnescurtisstanford_FullAnalysis

  Read Header Len:  32
  Name Length:      14
  # of Bases:       206
  Clip Qual Left:   5
  Clip Qual Right:  187
  Clip Adap Left:   0
  Clip Adap Right:  0

Flowgram:	1.04	0.00	1.01	0.00	0.00	1.00	0.00	1.00	0.00	1.05	0.00	0.91	0.10	1.07	0.95	1.01	0.00	0.06	0.93	0.02	0.03	1.06	1.18	0.09	1.00	0.05	0.90	0.11	0.07	1.99	0.11	0.02	1.96	1.04	0.13	0.01	2.83	0.10	1.97	0.06	0.11	1.04	0.13	0.03	0.98	1.15	0.07	1.00	0.07	0.08	0.98	0.11	1.92	0.05	0.04	2.96	1.02	1.02	0.04	0.93	1.00	0.13	0.04	1.00	1.03	0.08	0.97	0.13	0.11	1.88	0.09	0.05	1.02	1.89	0.07	0.11	0.98	0.05	0.07	1.01	0.08	0.05	1.01	0.13	1.00	0.07	0.10	1.04	0.10	0.04	0.98	0.12	1.03	0.96	0.11	0.07	1.00	0.09	0.03	1.03	0.11	1.95	1.06	0.13	0.05	1.00	0.13	0.11	1.00	0.09	0.03	2.89	0.08	0.95	0.09	1.03	1.02	1.05	1.07	0.08	0.12	2.81	0.08	0.08	1.00	1.07	0.07	0.05	1.86	0.12	0.98	0.06	2.00	0.11	1.02	0.11	0.08	1.88	0.13	1.03	0.13	0.98	0.15	0.11	1.03	1.03	1.04	0.18	0.98	0.13	0.15	1.04	0.11	1.01	0.13	0.06	1.01	0.06	1.02	0.08	0.99	0.14	0.99	0.09	0.05	1.09	0.04	0.07	2.96	0.09	2.03	0.13	2.96	1.13	0.08	1.03	0.07	0.99	0.11	0.05	1.05	1.04	0.09	0.07	1.00	1.03	0.09	0.06	1.06	1.04	2.94	0.18	0.06	0.93	0.10	1.10	0.11	2.02	0.17	1.00	1.03	0.06	0.11	0.96	0.04	3.00	0.11	0.07	1.99	0.10	2.03	0.12	0.97	0.16	0.01	2.09	0.14	1.04	0.16	0.06	1.03	0.14	1.12	0.12	0.05	0.96	1.01	0.10	0.14	0.94	0.03	0.12	1.10	0.92	0.09	1.10	1.04	1.02	0.12	0.97	2.00	0.15	1.08	0.04	1.03	1.04	0.03	0.09	5.16	1.02	0.09	0.13	2.66	0.09	0.05	1.06	0.07	0.89	0.05	0.12	1.10	0.16	0.06	1.01	0.13	1.00	0.14	0.98	0.09	2.92	1.28	0.03	2.95	0.98	0.16	0.08	0.95	0.96	1.09	0.08	1.07	1.01	0.16	0.06	4.52	0.12	1.03	0.07	0.09	1.03	0.14	0.03	1.01	1.99	1.05	0.14	1.03	0.13	0.03	1.10	0.10	0.96	0.11	0.99	0.12	0.05	0.94	2.83	0.14	0.12	0.96	0.00	1.00	0.11	0.14	1.98	0.08	0.11	1.04	0.01	0.11	2.03	0.15	2.05	0.10	0.03	0.93	0.01	0.08	0.12	0.00	0.16	0.05	0.07	0.08	0.11	0.07	0.05	0.04	0.10	0.05	0.05	0.03	0.07	0.03	0.04	0.04	0.06	0.03	0.05	0.04	0.09	0.03	0.08	0.03	0.07	0.02	0.05	0.02	0.06	0.01	0.05	0.04	0.06	0.02	0.04	0.04	0.04	0.03	0.03	0.06	0.06	0.03	0.02	0.02	0.08	0.03	0.01	0.01	0.06	0.03	0.01	0.03	0.04	0.02	0.00	0.02	0.05	0.00	0.02	0.02	0.03	0.00	0.02	0.02	0.04	0.01	0.00	0.01	0.05
Flow Indexes:	1	3	6	8	10	12	14	15	16	19	22	23	25	27	30	30	33	33	34	37	37	37	39	39	42	45	46	48	51	53	53	56	56	56	57	58	60	61	64	65	67	70	70	73	74	74	77	80	83	85	88	91	93	94	97	100	102	102	103	106	109	112	112	112	114	116	117	118	119	122	122	122	125	126	129	129	131	133	133	135	138	138	140	142	145	146	147	149	152	154	157	159	161	163	166	169	169	169	171	171	173	173	173	174	176	178	181	182	185	186	189	190	191	191	191	194	196	198	198	200	201	204	206	206	206	209	209	211	211	213	216	216	218	221	223	226	227	230	233	234	236	237	238	240	241	241	243	245	246	249	249	249	249	249	250	253	253	253	256	258	261	264	266	268	270	270	270	271	273	273	273	274	277	278	279	281	282	285	285	285	285	285	287	290	293	294	294	295	297	300	302	304	307	308	308	308	311	313	316	316	319	322	322	324	324	327
Bases:	tcagAGACGCACTCAATTATTTCCATAGCTTGGGTAGTGTCAATAATGCTGCTATGAACATGGGAGTACAAATATTCTTCAAGATACTGATCTCATTTCCTTTAGATATATACCCAGAAGTGAAATTCCTGGATCACATAGTAGTTCTATTTTTATTTGATGAGAAACTTTATACTATTTTTCATAActgagcgggctggcaaggc
Quality Scores:	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	38	38	38	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	34	34	34	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	36	36	36	36	36	38	25	25	25	38	37	37	37	37	37	37	33	33	34	37	37	37	37	37	37	37	38	34	20	20	26	26	20	34	38	37	37	37	37	37	37	37	37	37	38	38	38	37	37	37	37	37	37	37	37	37	37

>FIQU8OX06G9PCS
  Run Prefix:   R_2008_10_15_16_11_02_
  Region #:     6
  XY Location:  2863_3338

  Run Name:       R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford
  Analysis Name:  /data/2008_10_15/R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford/D_2008_10_15_15_12_26_FLX04070166_1548jinnescurtisstanford_FullAnalysis
  Full Path:      /data/2008_10_15/R_2008_10_15_16_11_02_FLX04070166_adminrig_1548jinnescurtisstanford/D_2008_10_15_15_12_26_FLX04070166_1548jinnescurtisstanford_FullAnalysis

  Read Header Len:  32
  Name Length:      14
  # of Bases:       264
  Clip Qual Left:   5
  Clip Qual Right:  264
  Clip Adap Left:   0
  Clip Adap Right:  0

Flowgram:	1.04	0.05	1.01	0.07	0.05	0.99	0.03	1.05	0.04	1.05	0.05	0.06	2.05	1.13	0.03	1.00	0.08	1.07	0.09	0.05	1.02	1.11	3.06	0.09	0.04	1.03	0.13	1.97	1.02	1.07	0.06	2.10	0.05	0.05	2.04	0.10	0.03	1.06	1.05	1.01	0.07	0.09	2.07	1.01	0.93	2.88	1.06	1.95	1.00	0.05	0.05	2.97	0.09	0.00	0.93	1.01	0.06	0.05	0.99	0.09	0.98	1.01	0.03	1.02	1.92	0.07	0.01	1.03	1.01	0.01	0.05	0.96	0.09	0.05	0.98	1.07	0.02	2.02	2.05	0.09	1.87	0.12	2.15	0.05	0.13	0.92	1.05	1.96	3.01	0.13	0.04	1.05	0.96	0.05	0.05	0.95	0.12	0.01	1.00	2.02	0.03	0.03	0.99	1.01	0.05	0.06	0.98	0.13	0.06	0.97	0.11	1.01	0.08	0.12	1.02	0.12	1.02	2.19	1.03	1.01	0.08	0.11	0.96	0.09	0.08	1.01	0.08	0.06	2.10	2.11	0.12	1.04	0.13	0.09	0.94	1.03	0.08	0.05	3.06	0.12	1.00	0.03	0.09	0.95	0.10	0.03	2.09	0.21	0.99	0.06	0.11	4.06	0.10	1.04	0.04	1.05	1.05	1.04	1.02	0.97	0.13	0.93	0.10	0.12	1.08	0.12	0.99	1.06	0.10	0.11	0.98	0.10	0.02	2.01	0.10	1.01	0.09	0.96	0.07	0.11	2.03	4.12	1.05	0.08	1.01	0.04	0.98	0.14	0.12	2.96	0.13	1.98	0.12	2.08	0.10	0.12	1.99	0.13	0.07	0.98	0.03	0.93	0.86	4.10	0.13	0.10	3.99	1.13	0.07	0.06	1.07	0.09	0.05	1.03	1.12	0.13	0.05	2.01	0.08	0.80	0.05	0.11	0.98	0.13	0.04	1.01	0.07	1.02	0.07	0.11	1.07	2.19	0.06	0.97	0.11	1.03	0.05	0.11	1.05	0.14	0.06	1.03	0.13	0.10	0.97	0.16	0.13	1.00	0.13	0.06	1.02	2.15	0.02	0.16	0.95	0.09	2.06	2.12	0.07	0.07	2.08	0.12	0.97	1.00	0.03	0.99	1.02	1.01	0.03	0.15	0.90	0.07	0.01	2.00	1.01	1.00	0.06	0.11	1.08	1.00	0.03	1.99	0.03	1.00	0.02	1.85	1.93	0.14	1.97	0.91	1.83	0.06	0.04	1.97	0.05	2.08	0.04	0.06	1.05	0.05	2.13	0.16	0.09	1.17	0.01	1.01	1.07	0.09	0.14	0.91	0.06	0.08	1.03	1.04	0.08	0.05	1.05	1.03	1.16	0.06	0.05	1.01	0.06	2.15	0.06	1.99	0.13	0.04	1.08	0.97	0.11	0.07	1.05	0.08	0.07	2.13	0.14	0.09	1.10	0.15	0.00	1.02	0.07	1.05	0.05	0.95	0.09	1.00	0.15	0.95	0.08	0.15	1.11	0.07	0.12	1.05	1.06	0.09	1.03	0.07	0.11	1.01	0.05	0.05	1.05	0.98	0.00	0.93	0.08	0.12	1.85	1.11	0.10	0.07	1.00	0.01	0.10	1.87	0.05	2.14	1.10	0.03	1.06	0.10	0.91	0.10	0.06	1.05	1.02	1.02	0.07	0.06	0.98	0.95	1.09	0.06	0.14	0.97	0.04	2.44
Flow Indexes:	1	3	6	8	10	13	13	14	16	18	21	22	23	23	23	26	28	28	29	30	32	32	35	35	38	39	40	43	43	44	45	46	46	46	47	48	48	49	52	52	52	55	56	59	61	62	64	65	65	68	69	72	75	76	78	78	79	79	81	81	83	83	86	87	88	88	89	89	89	92	93	96	99	100	100	103	104	107	110	112	115	117	118	118	119	120	123	126	129	129	130	130	132	135	136	139	139	139	141	144	147	147	149	152	152	152	152	154	156	157	158	159	160	162	165	167	168	171	174	174	176	178	181	181	182	182	182	182	183	185	187	190	190	190	192	192	194	194	197	197	200	202	203	204	204	204	204	207	207	207	207	208	211	214	215	218	218	220	223	226	228	231	232	232	234	236	239	242	245	248	251	252	252	255	257	257	258	258	261	261	263	264	266	267	268	271	274	274	275	276	279	280	282	282	284	286	286	287	287	289	289	290	291	291	294	294	296	296	299	301	301	304	306	307	310	313	314	317	318	319	322	324	324	326	326	329	330	333	336	336	339	342	344	346	348	350	353	356	357	359	362	365	366	368	371	371	372	375	378	378	380	380	381	383	385	388	389	390	393	394	395	398	400	400
Bases:	tcagATTAGATACCCAGGTAGGCCACGCCGTAAACGGTGGGCGCTAGTTGTGCGAACCTTCCACGGTTTGTGCGGCGCAGCTAACGCATTAAGCGCCCTGCCTGGGGAGTACGATCGCAAGATTAAAACTCAAAGGAATTGACGGGGCCCCGCACAAGCAGCGGAGCATGCGGCTTAATTCGACGCAACGCGAAGAACCTTACCAAGGCTTGACATATACAGGAATATGGCAGAGATGTCATAGCCGCAAGGTCTGTATACAGG
Quality Scores:	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	40	37	37	37	37	37	37	37	37	37	40	40	38	38	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	37	40	40	40	37	37	37	37	37	37	37	37	38	38	40	40	40	40	40	38	38	38	38	38	40	40	38	38	38	38	38	40	40	40	40	38	38	38	38	38	38	31	30	30	30	32	31	32	31	32	31	31	28	25	21	20

""".split('\n')
flows, head = parse_sff(test_flowgrams)
flows = list(flows)

if __name__ == "__main__":
    main()

