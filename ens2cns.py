#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ens2cns.py
##
## Copyright (C) 2014 bt4baidu@pdawiki forum
## http://pdawiki.com/forum
##
## This program is a free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, version 3 of the License.
##
## You can get a copy of GNU General Public License along this program
## But you can always get it from http://www.gnu.org/licenses/gpl.txt
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.

import re
import os.path


def cvtRmn(m):
    rmn = m.group(1)
    if rmn == 'I':
        rmn = '\xE2\x85\xA0'
    elif rmn == 'II':
        rmn = '\xE2\x85\xA1'
    elif rmn == 'III':
        rmn = '\xE2\x85\xA2'
    elif rmn == 'IV':
        rmn = '\xE2\x85\xA3'
    elif rmn == 'V':
        rmn = '\xE2\x85\xA4'
    elif rmn == 'VI':
        rmn = '\xE2\x85\xA5'
    elif rmn == 'VII':
        rmn = '\xE2\x85\xA6'
    elif rmn == 'VIII':
        rmn = '\xE2\x85\xA7'
    elif rmn == 'IX':
        rmn = '\xE2\x85\xA8'
    elif rmn == 'X':
        rmn = '\xE2\x85\xA9'
    return rmn


def step3(text):
    # match IVX
    p = re.compile(r'(?<=\n) *([IVX]+) *(?=\n)')
    text = p.sub(cvtRmn, text)
    # match []
    import os
    fp = os.getcwd()+os.path.sep+'abbr.txt'
    if not os.path.exists(fp):
        print "Please put 'abbr.txt' under the same dir with this tool."
    else:
        fr = open(fp, 'rU')
        try:
            abbr = fr.read()
        finally:
            fr.close()
        abbrs = abbr.split('\n')
        rexp = ' *\[ *('
        for abbr in abbrs:
            if len(abbr) > 0:
                rexp += abbr + '|'
        rexp = rexp.rstrip('|') + ') *\] *'
        p = re.compile(rexp)
        text = p.sub('\xE3\x80\x90'+r'\1'+'\xE3\x80\x91', text)
    return text


def convert_text(text):
    text = step3(text)
    return text


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs='?', help="txt file name")
    args = parser.parse_args()

    # use GUI to select file
    if not args.filename:
        import Tkinter
        import tkFileDialog
        root = Tkinter.Tk()
        root.withdraw()
        args.filename = tkFileDialog.askopenfilename(parent=root)

    if not os.path.exists(args.filename):
        print "Please specify a valid text file"

    base, ext = os.path.splitext(args.filename)

    # read txt file
    if ext.lower() == os.path.extsep + 'txt':
        fr = open(args.filename, 'rU')
        try:
            input_txt = fr.read()
        finally:
            fr.close()
        # format txt and write out
        if (input_txt and len(input_txt)>0):
            output_txt = convert_text(input_txt)
            output_fname = ''.join([base, '_converted', os.path.extsep, 'txt'])
            fw = open(output_fname, 'w')
            try:
                fw.write(output_txt)
            finally:
                fw.close()
        else:
            print "input file is empty"
    print "Done."
