#!/usr/bin/env python

"""take barcodes and dump to a single multipage pdf, assuming barcodes are
named by their number, e.g., 000009493.jpg

Names are cast to int for sorting purposes!

Correct order is guaranteed as long as there are no more than 999 pages.

Outputs to file "squashed_barcodes.pdf"

requires GPL Ghostscript 9.05
requires PIL (Python Imaging Library). Tested with version 1.1.7
"""

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QIIME project"
__credits__ = ["Daniel McDonald", "Adam Robbins-Pianka"]
__license__ = "GPL"
__version__ = "0.1-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "daniel.mcdonald@colorado.edu"
__status__ = "Development"

from sys import argv, exit
from os import listdir, path, system, mkdir, rmdir
from math import ceil
from random import choice
from shutil import rmtree

import Image

def get_image(indir, files):
    for f in files:
        yield Image.open(path.join(indir, f))

def main(input_directory, resulting_pdf):
    # load images
    image_files = [f for f in listdir(input_directory) if f.endswith('jpg')]
    image_files.sort(key=lambda x: int(path.splitext(path.split(x)[-1])[0]))

    # 36 barcodes per page
    pages = int(ceil(len(image_files) / 36.0))

    # assuming N * 8.5in x 11in
    PAGE_WIDTH = 1275
    PAGE_HEIGHT = 1650

    # create blank pdfs
    blanks = [Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), (255,255,255)) 
              for i in range(pages)]

    # padding set empirically for 
    # Electronic Imaging Materials
    # Part #80402
    START_LEFT = 18 
    START_UPPER = 59 
    HORIZ_GAP = 23
    VERT_GAP = 17
    BOX_WIDTH = 300
    BOX_HEIGHT = 150

    # center barcode, assuming barcode images are 300x150px
    # will adjust per image if 202x100px
    SHIFT_RIGHT = 0
    SHIFT_DOWN = 0

    # set starting points
    cur_left = START_LEFT
    cur_upper = START_UPPER
    page = -1
    idx = 0
    for i in get_image(input_directory, image_files):
        # if we have 36 barcodes we have filled a page
        if idx % 36 == 0:
            page += 1
            cur_upper = START_UPPER
            cur_left = START_LEFT
        
        # verify the barcode is the expected size, shift accordingly
        width, height = i.size
        if i.size == (202, 100):
            SHIFT_RIGHT = 49
            SHIFT_DOWN = 25
        elif i.size == (300,150):
            SHIFT_RIGHT = 0
            SHIFT_DOWN = 0
        else:
            raise AttributeError, "image %s is an unsupported size" % image_files[idx]

        # shift to new row
        if cur_left + width > PAGE_WIDTH:
            cur_left = START_LEFT
            cur_upper = cur_upper + HORIZ_GAP + BOX_HEIGHT

        # paste into the image
        blanks[page].paste(i, (cur_left + SHIFT_RIGHT, cur_upper + SHIFT_DOWN))
        
        # shift right
        cur_left += BOX_WIDTH + VERT_GAP
        
        idx += 1

    # write out each page
    tmpdir = "tmp_%s" % ''.join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(5)])
    while path.exists(tmpdir):
        tmpdir = "tmp_%s" % ''.join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(5)])
    mkdir(tmpdir)

    temp_pages = "squash_barcode_page_%03d.pdf"
    for page, blank in enumerate(blanks):
        blank.save(path.join(tmpdir, temp_pages % page), quality=100)
    
    
    match_pages = path.join(tmpdir, "squash_barcode_page_*.pdf")

    # magically squash all the pages
    system('gs -r150 -q -sPAPERSIZE=a4 -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=%s %s' % (resulting_pdf, match_pages))

    print "MAKE SURE TO SET 'FILL ENTIRE PAGE' WHEN PRINTING"
    print "Final output saved as: %s" % resulting_pdf
    rmtree(tmpdir)

if __name__ == '__main__':
    if len(argv) != 2:
        print "usage: python %s <directory_of_barcodes>" % argv[0]
        exit(1)

    final_output = "squashed_barcodes.pdf"
    main(argv[1], final_output)
