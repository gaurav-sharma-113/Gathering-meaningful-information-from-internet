from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup

from modules.summary import returnSummary
from modules.textPreProcess import preProcessing

def getHitsandMiss(stream, hitsCT, hitsS, urlsCT, urlsS, entries):
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

                # Checking from the Summary
                if ("covid" in summary.lower() or "corona" in summary.lower()) and ("economy" in summary.lower() or "economic" in summary.lower()):
                    hitsS = hitsS + 1
                    print("From Summary: ", hitsS, "/", entries)
                    urlsS.append(record.rec_headers.get_header("WARC-Target-URI"))
            
                if hitsCT > 1000 or hitsS > 1000:
                    return hitsCT, hitsS, urlsCT, urlsS, entries
            except:
                pass
    
    return hitsCT, hitsS, urlsCT, urlsS, entries