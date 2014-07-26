#!/usr/bin/env python
# -*- coding: utf-8 -*-
## checkfile.py
## A helpful tool to check input err for ECDv2 text-translation project
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

Errs = []
Wrns = []
Infs = []


def log(errno, rexp, text):
    p = re.compile(rexp)
    l = p.findall(text)
    if l:
        if errno[0] == 'E':
            Errs.append('\xE2\x98\x85========'+errno+'========\xE2\x98\x85:\n')
            Errs.append('\n'.join(l))
        elif errno[0] == 'W':
            Wrns.append('\xE2\x96\xA0========'+errno+'========\xE2\x96\xA0:\n')
            Wrns.append('\n'.join(l))
        elif errno[0] == 'I':
            Infs.append('\xE2\x96\xB2========'+errno+'========\xE2\x96\xB2:\n')
            Infs.append('\n'.join(l))


def step1(text):
# full text mode
    #E-01
    rexp = r'(\|\| *\n *[`\.][^\n]+\n)'
    log('E-01', rexp, text)
    #E-02
    rexp = r'(?<=\n)([^\n\t\1\2\3\4\5]*[\t\1\2\3\4\5][^\n]*\n)'
    log('E-02', rexp, text)
    #E-03
    rexp = r'(\{ *\.? *\}[^\n]*\n[^\n]*\n)'
    log('E-03', rexp, text)
    #E-04
    rexp = r'(\|\| *\n *(?:[\{\[\<&\x7F-\xFF]|\([\x7F-\xFF])[^\n]*\n[^\n]*\n[^\n]*\n)'
    log('E-04', rexp, text)
    #E-05
    rexp = r'((?:II|\xE2\x85\xA1) *\n *[a-zA-Z0-9\.\,\-\'\\/~]+[^\n]*\n)'
    log('E-05', rexp, text)
    #W-01
    rexp = r"(?<=[^\}\|]\n)((?!\d{1,2}\. *)[a-zA-HJ-UWYZ0-9\-\,\'][a-zA-Z0-9\.\,\-\' ]*\n[^\n]*\n[^\n]*\n)"
    log('W-01', rexp, text)
    rexp = r"(?<=[^\}\|]\n)((?!\d{1,2}\. *)[IVX][a-zA-Z0-9\.\,\-\' ]*[a-zA-HJ-UWYZ0-9\-\.\,\']+[a-zA-Z0-9\.\,\-\' ]*\n[^\n]*\n)"
    log('W-01', rexp, text)
    #W-02
    rexp = r'((?:\n[`\.]|\|\n)[a-zA-Z0-9\.\,\-\'\{\}/ ]*(?:[\.\-] +| +[\.\-] *)[a-z0-9\.\,\-\'\{\}/]+[^\n]*\n)'
    log('W-02', rexp, text)
    #W-03
    rexp = r'((?:(?:[\]\>\)\}]|\xE3\x80\x91) *(?:\xE2\x85[\xA0-\xA9]|[IVX]+)|(?:\xE2\x85[\xA0-\xA9]|[IVX]+) *(?:[\[\<\(\{]|\xE3\x80\x90))[^\n]*\n)'
    log('W-03', rexp, text)
    #W-04
    rexp = r'((?:\xE2\x85[\xA0-\xA9]|[IVX]+) *\n *(?:\([^\n]+\)|\[[^\]\n]+\])?\s*[^\{&\n\(\)\[ a-z][^\n\)]*\n[^\n]*\n)'
    log('W-04', rexp, text)
    rexp = r'(&#1010\d; *\n *(?:\([^\n]+\)|\[[^\]\n]+\])?\s*[^\{\n\(\)\[ a-z][^\n\)]*\n[^\n]*\n)'
    log('W-04', rexp, text)
    #I-01
    rexp = r'((?:\n[`\.]|\|\n)\-?[A-Z][a-z][^\n]*\n(?!(?:[\(\<]|1\. +)?[^\0-~])[^\n\\]*\n[^\n]*\n)'
    log('I-01', rexp, text)
    #I-02
    rexp = r'((?:\n[`\.]|\|\n)[a-zA-Z0-9\.\,\'\{\}/ ]+\- *[^\n]+\n[^\n]*\n[^\n]*\n)'
    log('I-02', rexp, text)


def step2(text):
# single line mode
    idx = 0
    lns = text.split('\n')
    ibn = 0
    bw = ''
    irn = 0
    E06 = []
    E07 = []
    E08 = []
    W05 = []
    for ln in lns:
        idx += 1
        if not len(ln):
            continue
        elif ln[0] == '`' or ln[0] == '.': # new entry
            if ibn==0 or ibn==1 or ibn>10102:
                ibn = 1
            else:#E-07
                ibn = 1
                E07.append('before line '+str(idx)+': '+ln+'\n')
            if irn==0 or irn==1 or irn>0xA0:
                irn = 1
            else:#E-08
                irn = 1
                E08.append('before line '+str(idx)+': '+ln+'\n')
            ln = ln[1:].replace('.', '')
            #W-05
            pos = ln.find(',')
            if pos > 0:
                pos //= 2 +1
                p = re.compile(r'(.{'+str(pos)+'})[^,]*, *(?:[A-Z]|\\1)')
                if not p.search(ln):
                    W05.append('line '+str(idx)+': '+lns[idx-1]+'\n')
            #E-06
            ln = ln.replace('-', '').replace(' ', '').lower()
            if bw == '':
                bw = ln
            elif cmp(bw, ln) > 0:
                E06.append('line '+str(idx)+': '+lns[idx-1]+'\n')
                bw = ln
        elif ln[0] == '&': # black quan
            #E-07
            if ibn == 0:
                ibn = int(ln[2:7])
            elif ibn == 1:
                if int(ln[2:7]) == 10102:
                    ibn = 10102
                else:
                    ibn = int(ln[2:7])
                    E07.append('line '+str(idx)+': '+ln+'\n')
            elif int(ln[2:7])-ibn == 1:
                ibn += 1
            else:
                ibn = int(ln[2:7])
                E07.append('line '+str(idx)+': '+ln+'\n')
        else:
            p = re.compile(r'^\xE2\x85([\xA0-\xA9])$')
            rmn = p.findall(ln)
            #E-08
            if rmn:
                if irn == 0:
                    irn = ord(rmn[0])
                elif irn == 1:
                    if ord(rmn[0]) == 0xA0:
                        irn = 0xA0
                    else:
                        irn = ord(rmn[0])
                        E08.append('line '+str(idx)+': '+ln+'\n')
                elif ord(rmn[0])-irn == 1:
                    irn += 1
                else:
                    irn = ord(rmn[0])
                    E08.append('line '+str(idx)+': '+ln+'\n')

    if len(E06) > 0:
        Errs.append('\xE2\x98\x85========E-06========\xE2\x98\x85:\n')
        Errs.append('\n'.join(E06))
    if len(E07) > 0:
        Errs.append('\xE2\x98\x85========E-07========\xE2\x98\x85:\n')
        Errs.append('\n'.join(E07))
    if len(E08) > 0:
        Errs.append('\xE2\x98\x85========E-08========\xE2\x98\x85:\n')
        Errs.append('\n'.join(E08))
    if len(W05) > 0:
        Wrns.append('\xE2\x96\xA0========W-05========\xE2\x96\xA0:\n')
        Wrns.append('\n'.join(W05))


def docheck(text):
    step1(text)
    step2(text)
    log = '\n\n'.join(Errs)
    log += '\n\n'.join(Wrns)
    log += '\n\n'.join(Infs)
    return log


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
        # check file content and dump logs
        if (input_txt and len(input_txt)>0):
            log = docheck(input_txt)
            logfile = ''.join([os.path.dirname(base), os.path.sep, 'result', os.path.extsep, 'log'])
            fw = open(logfile, 'w')
            try:
                fw.write(log)
            finally:
                fw.close()
        else:
            print "input file is empty"
    print "Done."
