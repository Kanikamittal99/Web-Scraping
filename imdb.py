# -*- coding: utf-8 -*-
"""


@author: Kanika Mittal
"""
import sqlite3

import urllib.parse, urllib.request, urllib.error
#import sys; sys.executable
from bs4 import BeautifulSoup
#allows program to access web sites that strictly enforce HTTPS
import ssl
#from requests import get
from time import sleep
from random import randint

#ignore ssl certificte errors : helps to do https sites also
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = input('enter: ')
if ( len(url) < 1 ) : url = 'https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=60PYVABN4P3VBB12N9J8&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_3'
 # Pause the loop
sleep(randint(8,15))
        
html = urllib.request.urlopen(url,context=ctx).read()
#type(html) #bytes i.e utf-8
#giving ugly 'html' to BS and it returns an object 
soup = BeautifulSoup(html,'html.parser')

movie_containers = soup.find_all('div', class_ = 'lister-item mode-advanced')
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
genres = []
for movie_container in movie_containers:
    #print(movie_container)
    name = movie_container.h3.a.text
    names.append(name)
    year_container = movie_container.h3.find('span',class_ ='lister-item-year text-muted unbold')
    year = year_container.text
    years.append(year)
    #print(year[5:9])
    #print(movie_container.p)
    genre_container = movie_container.p.find('span',class_ = 'genre')
    genre = genre_container.text
    genres.append(genre.strip())
    #print(genre.strip()
    rating = movie_container.find('span',class_ ='value')
    if rating is None:
        imdb_ratings.append(0)
    else:
        imdb_ratings.append(rating.text)
    #print(rating)
#there should not be extra space btw metascore & favourable->find()wont work
    metascore_container = movie_container.find('span',class_ ='metascore favorable')
    if metascore_container is None:
        metascore_container = movie_container.find('span',class_ ='metascore mixed') 
    if metascore_container is None:
        metascore_container = movie_container.find('span',class_ ='metascore unfavorable') 
    if metascore_container is None:
        metascores.append(0)
    else:
        metascore = metascore_container.text
        metascores.append(int(metascore))
    #print(metascore)
    votes_container = movie_container.find('span',attrs = {'name':'nv'})
    if votes_container is None:
        votes.append(0)
    else:
        votes.append(votes_container.text)
    #print(vote) #or votes_container['data-value']

import pandas as pd
test_df = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'genre':genres
})
print(test_df.info())
test_df


conn = sqlite3.connect('imdbDB.sqlite')
cur = conn.cursor()
# Do some setup

cur.executescript('''
DROP TABLE IF EXISTS Mystery;


CREATE TABLE Mystery (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    movie   TEXT UNIQUE,
    year INTEGER,
    imdb REAL,
    metascore INTEGER,
    votes INTEGER,
    genre TEXT
);
''')
conn.commit()

test_df.to_sql('Mystery', conn , if_exists = 'append',index = False)
cur.execute('''  
SELECT * FROM Mystery
          ''')



