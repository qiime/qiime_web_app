#!/usr/bin/env python

from cogent.util.unit_test import TestCase, main
from parse_and_load_db import unzip_and_cast_to_cxoracle_types, \
        input_set_generator, MockConnection

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2010, Qiime Web Analysis"
__credits__ = ["Daniel McDonald", "Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0.dev"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Production"

class MockConnectionTests(TestCase):
    def test_connect(self):
        mc = MockConnection()
        con = mc.connect(user='asd',password='asd',dsn='asd')
        self.assertSameObj(mc, con)

    def test_cursor(self):
        mc = MockConnection()
        con = mc.connect()
        cur = con.cursor()
        self.assertSameObj(mc, cur)

    def test_arrayvar(self):
        mc = MockConnection()
        obs = mc.arrayvar(int, ['1','2','3'])
        exp = [1,2,3]
        self.assertEqual(obs, exp)

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
        obs = unzip_and_cast_to_cxoracle_types(input,cursor,types)
        
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

        gen = input_set_generator(input,cursor,types,2)
        exp1 = [[1,2],['asd','123'],[0.0,0.2]]
        exp2 = [[3,4],['','zxc'],[0.3,]]
        exp3 = [[5],['qaz'],[0.5]]
        obs1 = gen.next()
        obs2 = gen.next()
        obs3 = gen.next()

        self.assertRaises(StopIteration, gen.next)

        self.assertEqual(obs1, exp1)
        self.assertEqual(obs2, exp2)
        self.assertEqual(obs3, exp3)
if __name__ == '__main__':
    main()
