import re

def preProcessing(sample):
    sample = re.sub(r"<[^<>]+>", " html ", sample)
    sample = re.sub(r"(http|https)://[^\s]*", ' httpaddr ', sample)
    sample = re.sub(r"[^\s]+@[^\s]+", ' emailaddr ', sample)
    sample = re.sub(r"[$]+", ' dollar ', sample)
    sample = re.sub(r"[^.a-zA-Z0-9]",' ', sample)
    return (sample)