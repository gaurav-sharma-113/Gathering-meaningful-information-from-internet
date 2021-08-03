from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
import pdb
from bs4 import BeautifulSoup
import spacy
import nltkmodules
import csv
from summary import returnSummary
from textPreProcess import preProcessing

def getHitsandMiss(stream, hitsCT, hitsS, missCT, missS, urlsCT, urlsS, entries):
    for record in ArchiveIterator(stream):
        if record.rec_type == "warcinfo":
            continue
        if not ".com/" in record.rec_headers.get_header("WARC-Target-URI"):
            continue

        contents = (
            record.content_stream()
            .read()
            .decode("utf-8", "replace")
        )
    
        if contents:
            entries = entries + 1
            try:
                soup = BeautifulSoup(contents, 'html.parser')
                cleantext = preProcessing(soup.get_text())
                cleantext = " ".join(cleantext.split())
                summary = returnSummary(cleantext)
            
                # Checking from the Text directly
                if ("covid" in cleantext.lower() or "corona" in cleantext.lower()) and ("economy" in cleantext.lower() or "economic" in cleantext.lower()):
                    hitsCT = hitsCT + 1
                    print("From Text: ", hitsCT, "/", entries)
                    urlsCT.append(record.rec_headers.get_header("WARC-Target-URI"))
                else:
                    missCT = missCT - 1 

                # Checking from the Summary
                if ("covid" in summary.lower() or "corona" in summary.lower()) and ("economy" in summary.lower() or "economic" in summary.lower()):
                    hitsS = hitsS + 1
                    print("From Summary: ", hitsS, "/", entries)
                    urlsS.append(record.rec_headers.get_header("WARC-Target-URI"))
                else:
                    missS = missS - 1 
            
                if hitsCT > 1000 or hitsS > 1000:
                    return hitsCT, hitsS, missCT, missS, urlsCT, urlsS, entries
            except:
                pass
    
    return hitsCT, hitsS, missCT, missS, urlsCT, urlsS, entries


def getInfoFromInternet():
    entries = 0
    matching_entries = 0
    hitsCT = 0
    missCT = 0
    hitsS = 0
    missS = 0
    nlp = spacy.load("en_core_web_sm")
    urlsCT = []
    urlsS = []
    file_names = []
    with open('./filenames.txt') as csvfile:
        links = csv.reader(csvfile) 
        ctr = 0
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

                hitsCT, hitsS, missCT, missS, urlsCT, urlsS, entries = getHitsandMiss(stream, hitsCT, hitsS, missCT, missS, urlsCT, urlsS, entries)
                
                
    with open('finalURL.txt','a+') as filehandle:
        filehandle.write("%s\n" % url for url in urlsCT)
    print("Data samples colleceted from month of October")
    print("Score using comparison from Direct text is ", hitsCT, " out of ", entries, " entries with the URLs stored in variable urlsCT")
    print("Score using comparison from Summary text is ", hitsS, " out of ", entries, " entries with the URLs stored in variable urlsS")

if __name__ == "__main__":
    getInfoFromInternet()
