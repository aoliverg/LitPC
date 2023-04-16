#Copyright: Antoni Oliver (2023)
#version 2023-04-16

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

import codecs
import re
import csv
import argparse
import requests


def loadcatalog(catalogfile):
    data={}
    with open(catalogfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cont=0
        for row in csv_reader:
            cont+=1
            ident=row[0]
            title=row[3]
            language=row[4]
            author=row[5]
            data[cont]={}
            data[cont]["ident"]=ident
            data[cont]["title"]=title
            data[cont]["language"]=language
            data[cont]["author"]=author
    return(data)
  
def info(dataclau):
    cadena=dataclau["ident"]+"\t"+dataclau["author"]+"\t"+dataclau["title"]+"\t"+dataclau["language"]
    return(cadena)
        
data=loadcatalog("pg_catalog.csv")


parser = argparse.ArgumentParser(description='searchGutenberg: a tool for searching and downloading epubs from Project Gutennberg.')
parser.add_argument('-a','--author', dest='sautor', help='Authors name/surname or part of them.', action='store',required=False)
parser.add_argument('-t','--title', dest='stitle', help='The title or part of it.', action='store',required=False)
parser.add_argument('--lang', '-l', dest='slang', help='The 2-letter code of the language.', action='store',required=False)
parser.add_argument('-o','--output', dest='outputfile', help='The output file to store the information.', action='store',required=False)
parser.add_argument('-d','--download', dest='download', help='Download the found books.', action='store_true',required=False)
parser.add_argument('-r','--rename', dest='rename', help='Rename the downloaded file to author+title+language.', action='store_true',required=False)



args = parser.parse_args()

sautor=args.sautor
slang=args.slang
stitle=args.stitle

escriu=False
if not args.outputfile==None:
    sortida=codecs.open(args.outputfile,"w",encoding="utf-8")
    escriu=True
descarrega=False
if args.download:
    descarrega=True
reanomena=False
if args.rename:
    reanomena=True
print(args.download,args.rename,descarrega,reanomena)
for clau in data:
    include=True
    if not sautor==None and not data[clau]["author"].find(sautor)>-1:
        include=False
    if not slang==None and not data[clau]["language"].find(slang)>-1:
        include=False
    if not stitle==None and not data[clau]["title"].find(stitle)>-1:
        include=False
    
    if include:
        information=info(data[clau])
        print(information)
        if escriu:
            sortida.write(information+"\n")
        if descarrega:
            #https://www.gutenberg.org/ebooks/730.epub.noimages https://www.gutenberg.org/ebooks/730.epub3.images
            url="https://www.gutenberg.org/ebooks/"+str(data[clau]["ident"])+".epub.noimages"
            r = requests.get(url, allow_redirects=True)
            filename=str(data[clau]["ident"])+".epub"
            if reanomena:
                filename=data[clau]["author"]+"-"+data[clau]["title"]+"-"+data[clau]["language"]
                filename=filename.replace(" ","_")
                filename=filename+".epub"
        
            open(filename, 'wb').write(r.content)
            
if escriu:
    sortida.close()
