#    fb22segmentedtext
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
import sys
import codecs
import os
import zipfile
from lxml import etree
from io import BytesIO
import re
import html
import os

import srx_segmenter



def remove_tags(segment):
    segmentnotags=re.sub('<[^>]+>',' ',segment).strip()
    segmentnotags=re.sub(' +', ' ', segmentnotags)
    return(segmentnotags)

def unescape_html(segment):
    segmentUN=html.unescape(segment)
    return(segmentUN)

def segmenta(cadena):
    segmenter = srx_segmenter.SrxSegmenter(rules[srx_lang],cadena)
    segments=segmenter.extract()
    for segment in segments[0]:
        print(segment)
        sortida.write(segment+"\n")

parser = argparse.ArgumentParser(description='A script to convert a fb2 file into a text file.')
parser.add_argument("-i", "--input_file", type=str, help="The fb2 input file to convert", required=True)
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

if args.input_file.endswith(".zip"):
    sortida=codecs.open(args.output_file,"w",encoding="utf-8")
    zip = zipfile.ZipFile(args.input_file)
    for filename in zip.namelist(  ):
        bytes = zip.read(filename).decode("utf-8")
        text=remove_tags(bytes)
        text=unescape_html(text)
        linies=text.split("\n")
        for linia in linies:
            linia=linia.strip()
            if len(linia)>0:
                segmenta(linia)            
    sortida.close()
else:
    entrada=codecs.open(args.input_file,"r",encoding="utf-8")
    sortida=codecs.open(args.output_file,"w",encoding="utf-8")
    for linia in entrada:
        linia=linia.strip()
        if len(linia)>0:
            linia=remove_tags(linia)
            linia=unescape_html(linia)
            linia=linia.strip()
            if len(linia)>0:
                segmenta(linia)
    sortida.close()
