#!/usr/bin/env python
# -*- coding: utf-8 -*-
## format_tool.py
## A helpful tool to format OCR text for ECDv2 text-translation project
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


WORDETY = "[a-zA-Z][a-zA-Z0-9\*\. \,'\-]*[a-zA-Z0-9\.\-]"
LSWORD = '[a-zA-Z][ -\.0-;\?-Z\^_a-z]*[a-zA-Z0-9\.\)\^_\-]'
ENP = "([^\0-~]{,3}[ -Z\^-z~])+[\!-'\)-\.;\?-Z\^-z~]"


def tolower(m):
    return m.group(1).lower()


def toupper(m):
    return m.group(1).upper()


def step1(text):
# full text mode: Add \r\n before special patterns, do f-h change and add some marks
    # replace full ' to half
    p = re.compile(r'\s*\xE2\x80[\x98\x99]')
    text = p.sub("'", text)
    # replace full , to half
    p = re.compile(r'\s*(\,|\xEF\xBC\x8C)\s*')
    text = p.sub(', ', text)
    # replace full ; to half
    p = re.compile(r'\s*(;|\xEF\xBC\x9B)\s*')
    text = p.sub('; ', text)
    # replace full ~ to half
    p = re.compile(r'\s*\xE3\x80\x9C\s*')
    text = p.sub(' ~ ', text)
    # replace full ( to half
    p = re.compile(r'\xEF\xBC\x88')
    text = p.sub('(', text)
    # replace full ) to half
    p = re.compile(r'\xEF\xBC\x89')
    text = p.sub(')', text)
    # replace full < to half
    p = re.compile(r'\xE3\x80\x88')
    text = p.sub('<', text)
    # replace full > to half
    p = re.compile(r'\xE3\x80\x89')
    text = p.sub('>', text)
    # replace full : to half
    p = re.compile(r'\s*\xEF\xBC\x9A')
    text = p.sub(':', text)
    # replace full / to half
    p = re.compile(r'\xEF\xBC\x8F')
    text = p.sub('/', text)
    # replace full = to half
    p = re.compile(r'\xEF\xBC\x9D')
    text = p.sub('=', text)
    # replace full !? to half
    p = re.compile(r'(?<=[\!-~])\s*\xEF\xBC\x81')
    text = p.sub('!', text)
    p = re.compile(r'(?<=[\!-~])\s*\xEF\xBC\x9F')
    text = p.sub('?', text)
    # replace full " to half
    p = re.compile(r'\s*\xE2\x80\x9C\s*(?=[\!-~])')
    text = p.sub(' "', text)
    p = re.compile(r'(?<=[\!-~])\s*\xE2\x80\x9D\s*')
    text = p.sub('" ', text)
    # replace middle-dot to . after digit
    p = re.compile(r'(?<=\d)(\s*\xE2\x80\xA2)')
    text = p.sub(r'.', text)
    # replace middle-dot to * in entry-header
    p = re.compile(r'(?<=[a-zA-Z])(\s*(\xE2\x80\xA2|\xC2\xBB|\*)\s*)(?=[a-zA-Z])')
    text = p.sub(r'.', text)#1
    # replace full | to half
    p = re.compile(r'\s*\xE4\xB8\xA8')
    text = p.sub('|', text)
    # remove unnecessary spaces between chinese chars
    p = re.compile(r'(?<![ -~]) +(?![\ -~])')
    text = p.sub('', text)
    # remove unnecessary spaces between english chars
    p = re.compile(r'(?<=[a-zA-Z]) {2,}(?=[a-zA-Z])')
    text = p.sub(' ', text)
    # remove unnecessary spaces between <>
    p = re.compile(r'(?<=\<)[ \t]*([^ -~]*)[ \t]*(?=\>)')
    text = p.sub(r'\1', text)
    # remove unnecessary spaces around (),numbers in ch sentence
    p = re.compile(r'(?<=[^\0-~])[ \t]*([\(\)]|\d+)[ \t]*(?=[^\0-~])')
    text = p.sub(r'\1', text)
    # remove unnecessary CR and translate \n to \r\n
    p = re.compile(r'[\r\n]+')
    text = p.sub('\r\n', text)
    #---------------------
    # match digit+"." => explainations
    p = re.compile(r'(\d{1,2}\.)\s*(\D)')
    text = p.sub('\r\n'+r'\1 '+r'\2', text)
    # match ":" => examples
    p = re.compile(r'(?<![a-zA-Z0-9])\s*(:|\xef\xbc\x9a)\s*(?=[\ -~])')
    text = p.sub(':\r\n', text)
    # match quan1~quan10 only
    # (black quan1~quan10 not supported as it can't be OCRed correctly)
    p = re.compile(r'(\xE2\x91[\xA0-\xA9])\s*')
    text = p.sub('\r\n'+r'\1', text)
    # match "II" "||" "|I" "I|" => usages start
    p = re.compile(r'\s*[I\|] *[I\|]\s*(?=[\!-HJ-z\{\}~])')
    text = p.sub('\r\n||\r\n', text)
    # match "III"
    p = re.compile(r'\s*([I\|]\s*){3}\s*(?=[\!-HJ-z\{\}~])')
    text = p.sub('\r\nIII\r\n', text)
    # match "/<> /[]" => entry-header
    p = re.compile(r'(?<=/)[ \t]*(?=[\[\<][^>\r\n\<\[\]]+[>\]])')
    text = p.sub('\r\n', text)
    # match "/" => idioms or example's spliter
    p = re.compile(r'(?<![ -~])(\s*\)?)\s*/\s*(?='+ENP+')')
    text = p.sub(r'\1'+'\r\n/', text)
    # remove unnecessary CRs in english sentence
    # not finished words
    p = re.compile(r'(?<=\d\-)[\r\n]+\s*(?=[a-zA-Z0-9])')
    text = p.sub('', text)
    p = re.compile(r'(?<=[a-zA-Z])\-[\r\n]+\s*(?=[a-zA-Z0-9])')
    text = p.sub('', text)
    # en sentence with numbers in the end
    p = re.compile(r'(?<=:\r\n|\r\n/)\s*([\ -~]+)\r\n(\d{1,2}\.\s+\D)')
    text = p.sub(r'\1\2', text)
    # not finished examples
    p = re.compile(r'(?<=:\r\n|\r\n/)\s*([\ -~]+)\r\n([a-zA-Z]{2,})')
    text = p.sub(r'\1 \2', text)
    # not finished chinese sentence
    p = re.compile(r'([^\0-~][ -~]{0,3})[ \t]*\r\n([\(\)]?[^\0-~])')
    text = p.sub(r'\1\2', text)
    #------------------------
    # add {} to the characteristic or property
    prop = r'comb[\,\.] *form(?=\s|[^a-zA-Z\.])'
    text = p.sub('comb. form', text)
    prop = r'(n\.|vt\.|vi\.|v\.aux\.|a\.|ad\.|art\.|pron\.|prep\.|conj\.|int\.|pref\.|comb\. form|suf\.|abbr\.)\s*'
    p = re.compile(r'\s+'+prop+r'(?=[^a-zA-Z])')
    text = p.sub(r' {\1} ', text)
    # add CR before{ and between } and explanation
    p = re.compile(r'\s*(\{[a-z\.\ ]+\})\s*(\d{1,2}\.\s+\D|[\(\[\<]?[^\0-~])')
    text = p.sub('\r\n'+r'\1'+'\r\n'+r'\2', text)
    # add CR  between } and alphabet => new entry begin
    p = re.compile(r'(\s*\{[a-z\.\ ]+\})[ \t]*('+WORDETY+')\s*([\r\n]+|[\(\[\<]?[^\0-~])')
    text = p.sub(r'\1'+'\r\n'+r'\2'+r'\3', text)
    # deal with the rest props
    p = re.compile(prop+'(?=\r\n\d{1,2}\.\s+\D)')
    text = p.sub('\r\n'+r'{\1}', text)
    #-------------------------
    # match "||{" =>try to correct OCR error
    p = re.compile(r'\|\|\s*(?=\{)')
    text = p.sub('II\r\n', text)
    # match "||O{" =>try to correct OCR error => replace to black quan1
    p = re.compile(r'\s*(\|\||[IVX]+)\s*([O0@]|\xC2\xA9)\s*(?=\{)', re.I)
    text = p.sub('\r\n'+r'\1'+'\r\n&#10102;\r\n', text)
    # match "O-CR-{, 0-CR-x." =>try to correct OCR error => replace to black quan1
    p = re.compile(r'([^\0-~][\)\]]?|\))\s*([O0@]|\xC2\xA9) *[^\.]{,4}(\.)\s*(?=1\.\s+\D|[\[\<\(]?[^\0-~])', re.I)
    text = p.sub(r'\1'+'\r\n&#10102;\r\n{'+r'\3'+'}\r\n', text)
    p = re.compile(r'\s*([O0@]|\xC2\xA9)[ \t]*[\r\n]+\s*(?=\{)', re.I)
    text = p.sub('\r\n&#10102;\r\n', text)
    # match || x. \d,cn
    p = re.compile(r'\s*(\|\||[IVX]+)\s*[^\.]{1,4}(\.)\s*(?=1\.\s+\D|[\[\<\(]?[^\0-~])')
    text = p.sub('\r\n'+r'\1'+'\r\n{'+r'\2'+'}\r\n', text)
    # loose
    p = re.compile(r'(?<=[^\0-~])\s*(\|\||[IVX]+)\s*[^\.]{1,4}(\.)\s*(?=1\.\s+\D|[\[\<\(]?[^\0-~])', re.I)
    text = p.sub('\r\n'+r'\1'+'\r\n{'+r'\2'+'}\r\n', text)
    # match || (,cn
    p = re.compile(r'\|\|(?=\s*([\(\{]|[^\0-~]|&#10102;))')
    text = p.sub('II', text)
    # match ",ve" =>try to correct OCR error
    p = re.compile(r'\,[ \t]*(ve|ll|s|d|ed) ')
    text = p.sub(r"'\1 ", text)
    # match "~ 5 " =>try to correct OCR error
    p = re.compile(r'(?<=~)( +5 +)')
    text = p.sub('s ', text)
    # match "T." =>try to correct OCR error
    p = re.compile(r'(?<=[^\0-~]) *T\.|T\.? *(?=[^\0-~])')
    text = p.sub('\xE5\xB7\xA5', text)
    p = re.compile('\xE4\xB8\xA1')
    text = p.sub('\xE7\x94\xBB', text)
    #-------------------------
    # format entry-header
    p = re.compile(r'(?<=[a-zA-Z])[\.|\*]\s+(?='+WORDETY+'\s*/[^/]{2,}/)')
    text = p.sub('.', text)#2
    p = re.compile(r'(?<=[a-z][\.|\*])([A-Z]+)(?=[\.|\*][a-z])')
    text = p.sub(tolower, text)
    # remove phonetic
    PHONTC = '[ -\.0-;>-z\|]'
    # match en /xx/ <>,{},I,|,[,ch[,(
    p = re.compile(r'(?<='+PHONTC+r')\s*/'+PHONTC+'{2,}/\s*(?=[\{\(\[\<]|\xE3\x80\x90)')
    text = p.sub('\r\n', text)
    p = re.compile(r'(?<='+PHONTC+r')(\s*/'+PHONTC+'{2,}/)\s*[I\|]\s*(?=[^\.]+\.)')
    text = p.sub(r'\1'+'\r\nI'+'\r\n', text)
    # match en /xx/ cn
    p = re.compile(r'(?<='+PHONTC+r')\s*/'+PHONTC+'{2,}/\s*(?=[^\0-~])')
    text = p.sub(' ', text)
    # match en /xx/ x. <>,1.
    p = re.compile(r'(?<='+PHONTC+r')\s*/'+PHONTC+'{2,}/\s*([I\s]*)[^\.]{,4}(\.)\s*(?=(1\.\s+\D|[\[\<\(]?[^\0-~]))', re.I)
    text = p.sub('\r\n'+r'\1'+'{'+r'\2'+'}\r\n', text)
    # match en /xx/ I
    p = re.compile(r'(?<='+PHONTC+r')\s*/'+PHONTC+'{2,}/\s*(?=I\r\n)')
    text = p.sub('\r\n', text)
    # match en /xx/ en
    p = re.compile(r'(?<='+PHONTC+r') */'+PHONTC+'{2,}/ *(?='+PHONTC+')')
    text = p.sub(' ', text)
    # add CR after etymology
    p = re.compile(r'\s*(\[[^\<\]]*\<[^\]]+\])\s*')
    text = p.sub(r' \1'+'\r\n', text)
    # match xxx) xxx]
    p = re.compile(r'(?<=[\?\!\)\]\}])[ \t]*('+WORDETY+')[ \t]*(?=\r\n)')
    text = p.sub('\r\n'+r'\1', text)
    # match cn-en-I{,<,[,1.
    p = re.compile(r'(?<=[^\0-~])([^a-zA-Z])?[ \t]*('+WORDETY+
        ')[ \t]*(?=\r\n[ \t]*([\[\<\(]*[^\0-~]|I\s*\{|1\.\s+\D))')
    text = p.sub(r'\1'+'\r\n'+r'\2', text)
    # match cn-en-{}-1.,<[ch,
    p = re.compile(r'(?<=[^\0-~])([^a-zA-Z])?[ \t]*('+WORDETY+
        ')[ \t]*(?=\r\n[ \t]*\{[a-z\.\ ]+\}\s*(1\.\s+\D|[\[(\<]*[^\0-~]|\=))')
    text = p.sub(r'\1'+'\r\n'+r'\2', text)
    # match "/" => idioms or example's spliter
    p = re.compile(r'(?<=\r\n/)([^/\r\n]+)/(?=[^/\r\n]{10,})')
    while 1:
        text, times = p.subn(r'\1'+'\r\n/', text)
        if not times:
            break
    #-------------------------
    # remove unnecessary spaces around =
    p = re.compile(r'\s*\=\s*')
    text = p.sub(' = ', text)
    # remove unnecessary spaces around ,
    p = re.compile(r'\s*\,\s*')
    text = p.sub(', ', text)
    # remove unnecessary spaces around ~
    p = re.compile(r'(?<=\-)( +)(?=~)')
    text = p.sub('', text)
    p = re.compile(r'(?<=~)( +)(?=(e?[sd]|ing)[ \]\)\.\,\?\;\!]|[\)\.;\,\?\-\!\]])')
    text = p.sub('', text)
    # remove unnecessary spaces between alphabet and (
    p = re.compile(r'(?<=[a-z])( +\([ \t]*)(?=[a-zA-Z])')
    text = p.sub('(', text)
    # remove unnecessary CR in word-entry
    p = re.compile(r'\s*(\{[a-z\.\ ]+\} */)\s*')
    text = p.sub(r' \1 ', text)
    p = re.compile(r"(?<=\|\|)\s*([a-zA-Z][a-zA-Z\*\.\{\} /']*[a-zA-Z0-9])\s*(?=\{[a-z\.\ ]+\})")
    text = p.sub('\r\n'+r'\1 ', text)
    #-------------------------
    # mark entry-header
    p = re.compile(r'(?<=[^\|:IVX])[\r\n]+\s*(\-? *'+WORDETY+')\s*(?=\r\n)')
    text = p.sub('\r\n`'+r'\1', text)
    p = re.compile(r'`([IVX]+)(?=\r\n)', re.I)
    text = p.sub(toupper, text)
    p = re.compile(r'(?<=\r\n)([IVX]+|\|\|)\s+` *('+WORDETY+'\s*)')
    text = p.sub(r'\1'+'\r\n'+r'\2', text)
    p = re.compile(r'(` *'+WORDETY+'\s*)` *('+WORDETY+') *')
    text = p.sub(r'\1\2', text)
    # remove unnecessary CR in word-entry
    p = re.compile(r'(\r\n\|\|\r\n[ -_a-~]+[^/]|&)[ \t]*[\r\n]+(?=\{)')
    text = p.sub(r'\1 ', text)
    # match =
    p = re.compile(r'(?<=[^\|:IVX]\r\n)[ \t]*('+WORDETY+')[ \t]*(?=\=)')
    text = p.sub('\r\n'+r'`\1'+'\r\n', text)
    #-------------------------
    # allow one ch char in english part
    # match /xxx-CR-1. => idiom
    p = re.compile(r'(?<=\r\n)/[ \t]*('+ENP+')\s*(?=1\.\s+\D)')
    text = p.sub(r'\1 \\ \r\n', text)
    p = re.compile(r'(?<=\|\|\r\n)[ \t]*('+ENP+')\s*(?=1\.\s+\D)')
    text = p.sub(r'\1 \\ \r\n', text)
    # avoid : in []
    p = re.compile(r'([\[\(][^\r\n\]\):]+:)\r\n')
    text = p.sub('\r\n'+r'\1 ', text)
    # match /xxx: => idiom
    p = re.compile(r'(?<=\r\n)(/[ \t]*'+ENP+'[ \t]*(\d+ *|\()?[^\0-~]{3,}[^\r\n:]*:)[ \t]*(?=[^\r\n])')
    text = p.sub(r'\1'+'\r\n', text)
    p = re.compile(r'(?<=\r\n)/[ \t]*('+ENP+')[ \t]*(?=(\d+ *|[\<\(])?[^\0-~]{3,}[^\r\n:]*:\r\n)')
    text = p.sub(r'\1 \\ ', text)
    # match /xxx<> or /xxx= => idiom
    p = re.compile(r'(?<=\r\n)/[ \t]*('+ENP+')[ \t]*(?=(\<[^>\r\n\<]+>|\=)[^\r\n]*\r\n)')
    text = p.sub(r'\1 \\ ', text)
    EXAMP = ENP+')[ \t]*(?=(\d+ *|\()?([^\0-~]{4,}|[^\0-~]{3,}[^\r\n]*\r\n)'
    # match "/" => idioms or example's spliter loose
    p = re.compile(r'([^\0-~]{5,}[ -~]{,3})\s*/\s*(?='+ENP+')')
    text = p.sub(r'\1'+'\r\n/', text)
    # match \d. xxx:exm
    p = re.compile(r'(?<=[^:]\r\n)(\s*\d{1,2}\. +\D[^\r\n:]*:)[ \t]*('+EXAMP+')')
    text = p.sub(r'\1'+'\r\n'+r'\2', text)
    # match :\r\n => example
    p = re.compile(r'(?<=:\r\n)[ \t]*('+EXAMP+')')
    text = p.sub(r'\1 / ', text)
    # match ||xxx/ => idiom
    p = re.compile(r'(?<=\|\|\r\n)[ \t]*('+ENP+r')[ \t]*(?=(\d+ *|[\<\(])?[^\0-~]{3,}[^\r\n`/]*\r\n[ \t]*/)')
    text = p.sub(r'\1 \\ ', text)
    # remove unnecessary CR and translate \n to \r\n
    p = re.compile(r'[\r\n]+')
    text = p.sub('\r\n', text)
    #-------------------------
    # match ||...^`, add mark for step2
    p = re.compile(r'(?<=\|\|\r\n)([^\r\n]+)(?=\r\n *[^`/])')
    text = p.sub('\1'+r'\1', text)
    # match ||\r\n => idiom
    p = re.compile(r'(?<=\|\|\r\n)[ \t]*((?!\d{1,2}\. )[^\r\n]+)(?=\r\n *`)')
    text = p.sub('\2'+r'\1', text)
    # encn type explainations, add mark to avoid formating
    p = re.compile(r'(?<=\r\n)((`'+LSWORD+'|[IVX]+|[^\r\n:]+:) *\r\n)[ \t]*(?=[a-zA-Z0-9])')
    text = p.sub(r'\1'+'\5', text)
    # example or idiom
    p = re.compile(r'(?<=\r\n)([^\r\n/\\]+[/\\][ \t]*)(?=(\d+ *|[\<\(])?[^\0-~]{3,})')
    text = p.sub('\5'+r'\1', text)
    # match CR-en-cn loosen
    p = re.compile(r'(?<=\r\n)[ \t]*('+LSWORD+r')[ \t]*(?=([\[\(\<]?[^\0-~]{3,}))')
    while 1:
        text, times = p.subn(r'`\1'+'\r\n', text)
        if not times:
            break
    # match =en-CR-I{,<,[,1., add mark for step2
    p = re.compile(r'(?<=\r\n)([^\r\n\=]*[^\r\n\=> ] *\= *'+WORDETY+
        ')[ \t]*(?=\r\n *([\[\<\(]?[^\0-~]|I\s*\{|1\.\s+\D))')
    text = p.sub('\3'+r'\1', text)
    # match =en-CR-{}-1.,<([ch, add mark for step2
    p = re.compile(r'(?<=\r\n)([^\r\n\=]*[^\r\n\=> ] *\= *'+WORDETY+
        ')[ \t]*(?=\r\n *\{[a-z\.\ ]+\}\s*(1\.\s+\D|[\[\(\<]?[^\0-~]))')
    text = p.sub('\3'+r'\1', text)
    p = re.compile('\5')
    text = p.sub('', text)
    # remove etymology
    p = re.compile(r'\s*\[[^\<\]\{]*\<[^\[\]>]+\]\s*')
    text = p.sub('\r\n', text)
    return text


PTN = None
SPT = ''
SPL = ' \\ '


def fmtgrp(m):
    ln = ''
    for grp in m.groups():
        if grp[0] != '(' and grp[0] != '[':
            grp = PTN.sub(SPT, grp)
        ln += grp
    return ln


def add_spliter(m):
    en = m.group(1)
    if en[-1]=='.' or en[-1]=='?' or en[-1]=='!' or en[-1]=="'":
        return m.group(1) + ' / '
    else:
        return m.group(1) + SPL


def split_entry(cch, ln):
    # split cn-en-cn-$
    match = 0
    if PTN.search(ln):
        pg = re.compile(r'([\(\[\]\)]?[^\(\)\[\]]+)')
        ln = pg.sub(fmtgrp, ln)
        match = 1
    return ln, match


def split_cn_en_cn(cch, ln):
    global PTN, SPT
    PTN = re.compile(r'([^\0-~]{3,}|[\)\]])[ \t]*('+cch+LSWORD
        +')[ \t]*(?=([\[\<\(]?[^\0-~].+)\s*)', re.I)
    SPT = r'\1'+'\r\n'+r'`\2'+'\r\n'
    ln, match = split_entry(cch, ln)
    if match:
        p = re.compile(r'([^\0-~]{3,}|[\)\]])[ \t]*('+cch+LSWORD
            +')[ \t]*(?=[\[\(][^\0-~])', re.I)
        ln = p.sub(r'\1'+'\r\n'+r'`\2'+'\r\n', ln)
    return ln, match


def step2(text):
# single line mode: do a little lexical analysis
    global PTN, SPT, SPL
    l_fmted = []
    bsnb = 10102 # black quan
    cch = ' '
    lns = text.split('\r\n')
    for ln in lns:
        if not len(ln):
            continue
        elif ln[0] == '/':
            # split EN-CN in examples and idioms by "/" or "\"
            p = re.compile(r'/[ \t]*('+ENP+')[ \t]*(?=(\d+ *|[\<\(])?([^\0-~]{4,}|[^\0-~]{3,}[^\r\n]*))')
            ln = p.sub(add_spliter, ln)
            # match cn-en-cn-$
            ln = split_cn_en_cn(cch, ln)[0]
        elif ln[0] == '`': # new entry
            SPL = ' \\ '
            bsnb = 10102
            cch = ln[1]
            # replace 0 to o
            p = re.compile(r'(?<=[^\d])\s*(0)\s*(?=[^\d])')
            ln = p.sub('o', ln)
        elif ln == '||':
            SPL = ' \\ '
        elif ln == '&#10102;': # format black quan
            ln = '&#'+str(bsnb)+';'
            bsnb += 1
        elif ln[0]=='\1' or ln[0]=='\2':
            mark = ln[0]
            ln = ln[1:]
            # en-en-cn
            PTN = re.compile(' *('+cch+LSWORD+')'+' +('+cch+LSWORD+
                ')[ \t]*(?=((\d+ *|[\<\(])?([^\0-~]{4,}|[^\0-~]{3,}[^\r\n]*))|$)', re.I)
            SPT = r'\1'+'\r\n'+r'`\2'+'\r\n'
            ln, match = split_entry(cch, ln)
            # add spliter
            p = re.compile(r'^(\s*'+ENP+')[ \t]*(?=(\d+ *|[\<\(])?([^\0-~]{3,}[^\r\n]*))')
            ln = p.sub(add_spliter, ln)
            # cn-en-cn-$
            ln = split_cn_en_cn(cch, ln)[0]
            # SP-cn-en-$
            if mark == '\1':
                PTN = re.compile(r'(?<=[\\/])([^\r\n]+) +('+cch+LSWORD+')$', re.I)
                SPT = r'\1'+'\r\n`'+r'\2'
                ln = split_entry(cch, ln)[0]
        elif ln[0] == '\3':
            ln = ln[1:]
            PTN = re.compile(r'^([^\r\n]+) +('+cch+LSWORD+')$', re.I)
            SPT = r'\1'+'\r\n`'+r'\2'
            ln = split_entry(cch, ln)[0]
            # match =
            p = re.compile(r'(?<=\r\n)[ \t]*(`'+LSWORD+')[ \t]*(?=\=.+)')
            ln = p.sub(r'\1'+'\r\n', ln)
        else:
            if len(ln)<4 and re.search(r'^[IVX]+$', ln):
                bsnb = 10102
            else:
                if ln[-1] == ':':
                    SPL = ' / '
                # match cn-en=en
                p = re.compile(r'([^\0-~]{3,}|[\)\]])[ \t]*('+cch+LSWORD+')[ \t]*(?=\=.+)')
                ln = p.sub(r'\1'+'\r\n`'+r'\2'+'\r\n', ln)
                # match =en-en-cn
                p = re.compile(r'(\= *'+LSWORD+') +('+cch+LSWORD+
                    ')[ \t]*(?=((\d+ *|[\<\(])?([^\0-~]{4,}|[^\0-~]{3,}[^\r\n]*))|$)')
                ln = p.sub(r'\1'+'\r\n`'+r'\2'+'\r\n', ln)
                # match =en en=
                p = re.compile(r'(\= *'+LSWORD+')[ \t]*('+cch+LSWORD+')[ \t]*(?=\=)')
                ln = p.sub(r'\1'+'\r\n'+r'`\2'+'\r\n', ln)
                # match cn-en-cn-$
                ln = split_cn_en_cn(cch, ln)[0]
        l_fmted.append(ln.strip())
    return '\r\n'.join(l_fmted)


def format_text(text):
    text = step1(text)
    text = step2(text)
    return text


if __name__ == '__main__':
    import os.path
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
        fr = open(args.filename, 'r')
        try:
            input_txt = fr.read()
        finally:
            fr.close()
        # format txt and write out
        if (input_txt and len(input_txt)>0):
            output_txt = format_text(input_txt)
            output_fname = ''.join([base, '_formated', os.path.extsep, 'txt'])
            fw = open(output_fname, 'wb')
            try:
                fw.write(output_txt)
            finally:
                fw.close()
        else:
            print "input file is empty"
    print "Done."
