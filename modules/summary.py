import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
import heapq
import warnings
warnings.filterwarnings("ignore")
nlp = spacy.load("en_core_web_sm")

def returnSummary(cleantext):
    
    # Creating dictionary of word frequency
    doc = nlp(cleantext)
    sentences = [sent.text.lower() for sent in doc.sents]
    countVectorizer = CountVectorizer(stop_words=list(STOP_WORDS))
    try:
        countVectorizerFit = countVectorizer.fit_transform(sentences)
    except:
        if not cleantext:
            return ""
    wordList = countVectorizer.get_feature_names()
    countList = countVectorizerFit.toarray().sum(axis=0)
    wordFrequency = dict(zip(wordList,countList))

    
    # Getting relative frequency of each word
    val=sorted(wordFrequency.values())
    higherFrequency = val[-1]
    for word in wordFrequency.keys():  
        wordFrequency[word] = (wordFrequency[word]/higherFrequency)

    # Making sentence rank dictionary by adding the word frequency of sentences
    # in each sentence and then finding out the 5 highest ranked sentences.
    sentenceRank = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in wordFrequency.keys():
                if sent in sentenceRank.keys():
                    sentenceRank[sent] += wordFrequency[word.text.lower()]
                else:
                    sentenceRank[sent] = wordFrequency[word.text.lower()]
    
    summarySentences = heapq.nlargest(7, sentenceRank, key=sentenceRank.get)

    # Joining final summary sentences
    summary = ""
    for sent in summarySentences:
        summary = summary + sent.text

    return summary