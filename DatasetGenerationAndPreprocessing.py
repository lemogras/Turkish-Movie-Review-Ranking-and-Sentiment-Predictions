from bs4 import BeautifulSoup
import urllib
import requests
import re
import numpy as np
import string
import os
import socket
import xlwt
os.chdir("/Users/baki/Documents/Python")
ids = []
with open('filmler_sirali.txt') as inputfile:
    for line in inputfile:
        ids.append(line.strip())
exclude = set(string.punctuation)

review_all_txt = open("reviews_all.txt","w")

ratings_all = []
reviews_all= []


count=0
count_of_movie_considered = 0
for movie_id in ids:
    count+=1
    try:
        movie_url = 'http://www.beyazperde.com/filmler/film-' + movie_id+ '/kullanici-elestirileri'
        r = urllib.request.urlopen(movie_url,timeout=0x02)
        soup = BeautifulSoup(r)
        reviews = soup.findAll("p",{"itemprop":"description"})
        ratings = soup.findAll("span",{"class" : "stareval-note"})
        numberofComments= soup.find("span",{"class" : "js-follow-unfollow"})
        count_of_movie_considered +=1
        if(numberofComments is not None):
            numberofComments_=np.int(numberofComments['data-totalreviews'])
            if(numberofComments_>10):
                numberofComments_=10   
            reviews_np = list(range(numberofComments_))
            ratings_np = list(range(numberofComments_))
            for i in range(numberofComments_):
                if(ratings[i].string.count("?") > 0):
                    ratings[i].string=ratings[i].string.replace("?","0")
                ratings_np[i]=np.double(ratings[i].string[-3:].replace(",","."))
                reviews_np[i]=reviews[i].get_text()
                if("\t" in reviews_np[i]):
                    reviews_np[i]=reviews_np[i][reviews_np[i].index("\t")+3:]
                else:
                    reviews_np[i]=reviews_np[i][reviews_np[i].index("\n")+3:]
                if("\n\n" in reviews_np[i]):
                    reviews_np[i]=reviews_np[i][:reviews_np[i].index("\n\n")]
                reviews_np[i]=reviews_np[i].replace("\n","")
                for ch in exclude:
                    reviews_np[i]=reviews_np[i].replace(ch," ")
                reviews_np[i] = reviews_np[i].replace("  "," ").replace("I","i")
                reviews_np[i] = reviews_np[i].replace("ö","o").replace("ü","u").replace("ı","i").replace("ğ","g").replace("ş","s").replace("ç","c")
                reviews_np[i] = reviews_np[i].lower()
                try:
                    review_all_txt.write(reviews_np[i] + "\n")
                except UnicodeEncodeError:
                    reviews_np[i] = reviews_np[i].encode('ascii','ignore').decode('ascii')
                    review_all_txt.write(reviews_np[i] + "\n")
            ratings_all = np.concatenate((ratings_all,ratings_np))
            reviews_all = np.concatenate((reviews_all,reviews_np))
    except socket.timeout:
        print(np.str(movie_id) + "is timeout. Number of ids =" + np.str(np.size(ids)))
        ids.remove(movie_id)
    except urllib.error.URLError:
        print(np.str(movie_id) + "is 404 NOT found. Number of ids =" + np.str(np.size(ids)))
        ids.remove(movie_id)
    
    if(count%20==0):
        print("Hold On Babe")
        print("Percentage of loading:" + np.str((count/np.size(ids))*100))
review_all_txt.close()
ratings_all.tofile('ratings_all_19.csv',sep=',',format='%10.5f')
reviews_all.tofile('reviews_all_19.csv',sep=',',format='%10.5f')

ReviewWorkbook = xlwt.Workbook()
ReviewWorksheet = ReviewWorkbook.add_sheet('Reviews')
RatingWorksheet = ReviewWorkbook.add_sheet('Ratings')
for i in range(reviews_all.size):
    if(i!= 30044):
	    ReviewWorksheet.write(i,0,reviews_all[i])
	    RatingWorksheet.write(i,0,ratings_all[i])


#print(ratings_all)
    
