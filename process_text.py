import spacy,nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from nltk import pos_tag
from nltk import  word_tokenize
from optparse import OptionParser
import json
import re


lemmatizer = WordNetLemmatizer()
nlp = spacy.load('en_core_web_sm')
all_stop_words = ['many', 'us', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                  'today', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december', 'today', 'old', 'new']
all_stop_words = set(all_stop_words + list(stopwords.words('english')))

def extract_entities(docs):
    """
    docs: iteration of strings
    rtype: list of list of entities
    """
    res  = []
    for d in docs:
        d = re.sub(r'http\S+', '', d) # remove link
        d = re.sub(r'@\S+','',d) # remove @ stuff
        tags = pos_tag(word_tokenize(d)) # get pos tag of each word
        ents = [w for w,t in tags if t.startswith('NN')] # get the entities
        ents = [lemmatizer.lemmatize(w) for w in ents] # lemmatization
        ents = [w for w in ents if w.lower() not in all_stop_words] # get rid of stop words
        ents = list(set(ents))
        if len(ents) > 1:
            res.append(ents)
        
    return res


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--filePath',
                         dest='filePath',
                         help='text file path',
                         default=None)
    optparser.add_option('-s', '--savePath',
                         dest='savePath',
                         help='save file path',
                         default=None)

    (options, args) = optparser.parse_args()
    with open(options.filePath,'r') as f:
        corpora = json.load(f)

    res = extract_entities(corpora)
    print(res)

    if options.savePath:
        with open(options.savePath,'w') as f:
            json.dump(res,f)

        print('*'*20)
        print(f'the data has been saved in file:{options.savePath}')

