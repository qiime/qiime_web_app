#!/usr/bin/env python

import urllib
import Image
from StringIO import StringIO
from sys import argv, exit
from time import sleep
import os
from hashlib import md5

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2009-2013, QIIME Web Analysis"
__credits__ = ["Daniel McDonald"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = ["Daniel McDonald"]
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

URL = "http://barcode.tec-it.com/barcode.ashx?code=Code128&modulewidth=fit&data=%s&dpi=96&imagetype=jpg&rotation=0&color=&bgcolor=&fontcolor=&quiet=0&qunit=mm&download=true"

def get_barcode(id_, attempts=20, sleep_duration=2):
    """Obtain a barcode
    
    If attemps is > 1 , retry N times if a non 200-code is returned

    "Barcode generated with TEC-IT Barcode Software"
    """
    barcode = None
    while attempts > 0 and barcode is None:
        if sleep_duration is not None:
            sleep(sleep_duration)
        
        try:
            data = urllib.urlopen(URL % id_)
        except Exception, e:
            attempts -= 1
            continue

        if data.code != 200:
            attempts -= 1
            if sleep_duration is not None:
                sleep_duration += 10
            continue
        
        barcode = Image.open(StringIO(data.read()))

        if barcode.size != (202, 100):
            if sleep_duration is not None:
                sleep_duration += 10
            attempts -= 1
            continue

    if barcode.size != (202, 100):
        raise ValueError, "Failed despite attempts!"

    if barcode is None:
        raise ValueError, "Unable to obtain barcode!"

    if barcode.mode != "RGB":
        barcode = barcode.convert("RGB")

    return barcode

def crop_barcode(barcode):
    """Crop lower 20px off image (TEC-IT.COM tag)"""
    left = 0; upper = 0
    right, lower = barcode.size
    return barcode.crop((0, 0, right, lower - 20))

def hash_from_image(data):
    """Compute the MD5 of a written image"""
    wrapper = StringIO()
    data.save(wrapper, format='JPEG')
    return md5(wrapper.getvalue()).hexdigest()

if __name__ == '__main__':
    if len(argv) != 4:
        print "usage: %s <input_metadata_table> <output_metadata_table> <output_barcode_directory>" % argv[0]
        exit(1)

    in_table = [l.strip().split('\t') for l in open(argv[1],'U')]
    out_barcode_dir = argv[3]

    if os.path.exists(out_barcode_dir):
        print "Output directory already exists!"
        exit(1)
    else:
        os.mkdir(out_barcode_dir)

    if os.path.exists(argv[2]):
        print "Output table already exists!"
        exit(1)
    else:
        out_table = open(argv[2],'w')
    
    if in_table[0][0] != '#SampleID':
        print "The first column in the metadat file is not SampleID!"
        exit(1)

    out_lines = [in_table[0][:]]
    out_lines[0].append('SampleBarcodeFile')
    out_lines[0].append('SampleBarcodeFileMD5')
    out_table.write('\t'.join(out_lines[0]))
    out_table.write('\n')
    for record in in_table[1:]:
        new_record = record[:]
        sample_id = new_record[0]
        
        barcode_filename = "%s.jpg" % sample_id
        barcode_path = os.path.join(out_barcode_dir, barcode_filename)

        barcode = crop_barcode(get_barcode(sample_id))
        barcode_hash = hash_from_image(barcode)

        barcode.save(barcode_path)
        os.chmod(barcode_path, 0444) # read-only

        new_record.append(barcode_filename)
        new_record.append(barcode_hash)
        out_lines.append(new_record)

        out_table.write('\t'.join(new_record))
        out_table.write('\n')
    
    out_table.close()
