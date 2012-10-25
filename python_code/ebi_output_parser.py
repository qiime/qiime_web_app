#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

from xml.dom.minidom import parse

class EBIOutputParser(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.dom = parse(file_path)
        
    def __del__(self):
        pass
        
    def parse_samples(self):
        samples = {}
        for node in self.dom.getElementsByTagName('SAMPLE'):
            samples[node.getAttribute('alias')] = note.getAttribute('accession')
        return samples
