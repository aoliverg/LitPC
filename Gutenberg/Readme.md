# searchGutenberg.py

Install the requirements: requests

You need the Gutenberg catalog in csv format, get it writing in Terminal:

`wget https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv`

The program has the -h option that shows the help of the program:

```
python3 searchGutenberg.py -h
usage: searchGutenberg.py [-h] [-a SAUTOR] [-t STITLE] [--lang SLANG] [-o OUTPUTFILE] [-d] [-r]

searchGutenberg: a tool for searching and downloading epubs from Project Gutennberg.

options:
  -h, --help            show this help message and exit
  -a SAUTOR, --author SAUTOR
                        Authors name/surname or part of them.
  -t STITLE, --title STITLE
                        The title or part of it.
  --lang SLANG, -l SLANG
                        The 2-letter code of the language.
  -o OUTPUTFILE, --output OUTPUTFILE
                        The output file to store the information.
  -d, --download        Download the found books.
  -r, --rename          Rename the downloaded file to author+title+language.
```

For example, if you want to know all the available books of Cervantes in Spanish, you can write:

`python3 searchGutenberg.py -a Cervantes --lang es`

And you get:

```
2000    Cervantes Saavedra, Miguel de, 1547-1616        Don Quijote     es
15115   Cervantes Saavedra, Miguel de, 1547-1616        Novelas y teatro        es
16110   Cervantes Saavedra, Miguel de, 1547-1616        Viage al Parnaso
La Numancia (Tragedia) y El Trato de Argel (Comedia)    es
57955   Cervantes Saavedra, Miguel de, 1547-1616        Los entremeses  es
61202   Cervantes Saavedra, Miguel de, 1547-1616        Novelas ejemplares      es
```

You can use the -o option to store this information in a file.

You can also automatically download them with the -d option:

`python3 searchGutenberg.py -a Cervantes --lang es -d`

This command will download all these works in epub format, keeping the original name of the files: 15115.epub  16110.epub  2000.epub  57955.epub  61202.epub

You may want to rename the files with the author's name and title. To do this, you can use the -r option:

`python3 searchGutenberg.py -a Cervantes --lang es -d -r`

Now the files will be named:

```
Cervantes_Saavedra,_Miguel_de,_1547-1616-Don_Quijote-es.epub
Cervantes_Saavedra,_Miguel_de,_1547-1616-Los_entremeses-es.epub
Cervantes_Saavedra,_Miguel_de,_1547-1616-Novelas_ejemplares-es.epub
Cervantes_Saavedra,_Miguel_de,_1547-1616-Novelas_y_teatro-es.epub
'Cervantes_Saavedra,_Miguel_de,_1547-1616-Viage_al_Parnaso'$'\n''La_Numancia_(Tragedia)_y_El_Trato_de_Argel_(Comedia)-es.epub'
```

