#    fb22text
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



def remove_tags(segment):
    segmentnotags=re.sub('<[^>]+>',' ',segment).strip()
    segmentnotags=re.sub(' +', ' ', segmentnotags)
    return(segmentnotags)

def unescape_html(segment):
    segmentUN=html.unescape(segment)
    return(segmentUN)

parser = argparse.ArgumentParser(description='A script to convert a fb2 file into a text file.')
parser.add_argument("-i", "--input_file", type=str, help="The fb2 input file to convert", required=True)
parser.add_argument("-o", "--output_file", type=str, help="The output text file", required=True)

args = parser.parse_args()

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
                print(linia)
                sortida.write(linia+"\n")            
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
                print(linia)
                sortida.write(linia+"\n")
    sortida.close()
