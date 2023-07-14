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

import xml.etree.ElementTree as etree
import io



today = date.today()

blacklist = [   '[document]',   'noscript', 'header',   'html', 'meta', 'head','input', 'script',   ]

def translate(segment):
    return(segment[::-1])


parser = argparse.ArgumentParser(description='A script to convert an epub file into a text file with a light markup.')
parser.add_argument("-i", "--input_file", type=str, help="The epub input file to convert", required=True)
parser.add_argument("-o", "--output_file", type=str, help="The output text file", required=True)
parser.add_argument("-c", "--chapter", type=str, help="The tag (h1, h2, h3) that marks the title of a chapter", required=False)

args = parser.parse_args()
if not args.chapter:
    chaptermark="NoMark"
else:
    chaptermark=args.chapter
book = epub.read_epub(args.input_file)        
metadata=book.get_metadata('DC', 'title')
titol=metadata[0][0].replace("/","_")
metadata=book.get_metadata('DC', 'language')
llengua=metadata[0][0]
metadata=book.get_metadata('DC', 'creator')
autor=metadata[0][0]

sortida=codecs.open(args.output_file,"w",encoding="utf-8")

cadena="\\title "+titol
sortida.write(cadena+"\n")
cadena="\\author_firstname "+autor.split(" ")[0]
sortida.write(cadena+"\n")
cadena="\\author_lastname "+" ".join(autor.split(" ")[1:])
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
                    sortida.write(cadena+"\n")
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}h1":
                if not elem.text==None:
                    
                    if elem.tag.replace("{http://www.w3.org/1999/xhtml}","")==chaptermark:
                        cadena="\chapter "+elem.text
                        sortida.write(cadena+"\n")
                    else:
                        cadena=elem.text
                        sortida.write(cadena+"\n")
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}h2":
                if not elem.text==None:
                    if elem.tag.replace("{http://www.w3.org/1999/xhtml}","")==chaptermark:
                        cadena="\chapter "+elem.text
                        sortida.write(cadena+"\n")
                    else:
                        cadena=elem.text
                        sortida.write(cadena+"\n")
            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}h3":
                if not elem.text==None:                    
                    if elem.tag.replace("{http://www.w3.org/1999/xhtml}","")==chaptermark:
                        cadena="\chapter "+elem.text
                        sortida.write(cadena+"\n")
                    else:
                        cadena=elem.text
                        sortida.write(cadena+"\n")

            if event=="end" and elem.tag=="{http://www.w3.org/1999/xhtml}p":
                if not elem.text==None:
                    cadena=escape(elem.text)
                    sortida.write(cadena+"\n")
                



