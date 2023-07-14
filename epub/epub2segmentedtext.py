#    epub2text
#    Copyright (C) 2023  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import ebooklib
from ebooklib import epub
import html2text
import sys
import re
import codecs
import nltk
import glob
import os
from bs4 import BeautifulSoup
from datetime import date
from xml.sax.saxutils import escape
import srx_segmenter


import xml.etree.ElementTree as etree
import io

#IMPORTS FOR YAML
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def segmenta(cadena):
    segmenter = srx_segmenter.SrxSegmenter(rules[srx_lang],cadena)
    segments=segmenter.extract()
    for segment in segments[0]:
        print(segment)
        sortida.write(segment+"\n")


today = date.today()

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script',   ]

def translate(segment):
    return(segment[::-1])


parser = argparse.ArgumentParser(description='A script to convert an epub file into a text file with a light markup.')
parser.add_argument("-i", "--input_file", type=str, help="The epub input file to convert", required=True)
parser.add_argument("-o", "--output_file", type=str, help="The output text file", required=True)
parser.add_argument("-s", "--srx_file", type=str, help="The srx file to be used. By default segment.srx", required=False)
parser.add_argument("-l", "--srx_lang", type=str, help="The language as stated in the SRX file. By default English", required=False)
parser.add_argument("-p", "--paragraph_mark", type=str, help="Add the <p> mark to paragraph. Useful to align with Hunalign. Default True", required=False, default="True")


args = parser.parse_args()

if not args.srx_file:
    srx_file="segment.srx"
else:
    srx_file=args.srx_file
if not args.srx_lang:
    srx_lang="English"
else:
    srx_lang=args.srx_lang
    
paragraph_mark=args.paragraph_mark

if paragraph_mark=="False":
    paragraph_mark=False
else:
    paragraph_mark=True



rules = srx_segmenter.parse(srx_file)

book = epub.read_epub(args.input_file)        
metadata=book.get_metadata('DC', 'title')
titol=metadata[0][0].replace("/","_")
metadata=book.get_metadata('DC', 'language')
llengua=metadata[0][0]
metadata=book.get_metadata('DC', 'creator')
autor=metadata[0][0]

sortida=codecs.open(args.output_file,"w",encoding="utf-8")

cadena=titol
sortida.write(cadena+"\n")

segmentcount=1
contchapter=1
inChapter=False
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        xmlstring=item.get_content().decode("utf-8")

        f = io.StringIO(xmlstring)
        for event, elem in etree.iterparse(f, events=("start", "end")):            
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}title":
                if not elem.text==None:
                    cadena=elem.text                    
                    if paragraph_mark: sortida.write("<p>\n")
                    segmenta(cadena)
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}h1":
                if not elem.text==None:
                    cadena=elem.text
                    if paragraph_mark: sortida.write("<p>\n")
                    segmenta(cadena)
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}h2":
                if not elem.text==None:
                    cadena=elem.text
                    if paragraph_mark: sortida.write("<p>\n")
                    segmenta(cadena)
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}h3":
                if not elem.text==None:                    
                    cadena=elem.text
                    if paragraph_mark: sortida.write("<p>\n")
                    segmenta(cadena)
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}p":
                if not elem.text==None:
                    cadena=escape(elem.text)
                    if paragraph_mark: sortida.write("<p>\n")
                    segmenta(cadena)


