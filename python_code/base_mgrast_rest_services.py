#!/usr/bin/env python

__author__ = "Doug Wendel"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Doug Wendel"]
__license__ = "GPL"
__version__ = "1.2.0-dev"
__maintainer__ = "Doug Wendel"
__email__ = "wendel@colorado.edu"
__status__ = "Development"

class BaseMGRASTRestServices(object):

    def send_data_to_mgrast(self, url_path, file_contents, host, debug):
        raise NotImplementedError('Base class method has no implementation')

