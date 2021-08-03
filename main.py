from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
import pdb
import spacy
import csv
from bs4 import BeautifulSoup

import modules.nltkmodules
from modules.summary import returnSummary
from modules.textPreProcess import preProcessing
from modules.getResults import getHitsandMiss


def getInfoFromInternet():
    entries = 0
    hitsCT = 0
    hitsS = 0
    nlp = spacy.load("en_core_web_sm")
    urlsCT = []
    urlsS = []
    file_names = []
    with open('./filenames.txt') as csvfile:
        links = csv.reader(csvfile) 
        for names in links:
            if hitsCT > 1000 or hitsS > 1000:
                break
            for file_name in names:
                file_name = 'http://commoncrawl.s3.amazonaws.com/'+file_name
                file_names.append(file_name)
                ctr = 0
                if file_name.startswith("http://") or file_name.startswith("https://"):
                    stream = requests.get(file_name, stream=True).raw
                else:
                    stream = open(file_name, "rb")

                hitsCT, hitsS, urlsCT, urlsS, entries = getHitsandMiss(stream, hitsCT, hitsS, urlsCT, urlsS, entries)
    
                
                
    with open('finalURL.txt','a+') as filehandle:
        filehandle.write("%s\n" % url for url in urlsCT)
    print("Data samples colleceted from month of October")
    print("Score using comparison from Direct text is ", hitsCT, " out of ", entries, " entries with the URLs stored in variable urlsCT")
    print("Score using comparison from Summary text is ", hitsS, " out of ", entries, " entries with the URLs stored in variable urlsS")

if __name__ == "__main__":
    getInfoFromInternet()
