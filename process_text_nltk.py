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

def combine_nouns(tags):
    """
    tags: pos_tag of NLTK
    rtype:
        list of nouns
    """
    ents = [(lemmatizer.lemmatize(w.strip().lower()),i) for i, (w,t) in enumerate(tags) if t.startswith('NN')] # extract nouns

    n = len(ents)
    if n == 0:
        return []
    elif n == 1:
        return [ents[0][0]]

    # screen the nuons and connect the nouns next to each other together
    right = 1
    res = [] # store the nouns
    sub = ents[0][0]
    while right < n:
        if ents[right][1] == ents[right-1][1]+1:
            sub += ' '+ ents[right][0]
        else:
            res.append(sub)
            sub = ents[right][0]

        right += 1

    res.append(sub)
    return res

def extract_entities_nltk(docs):
    """
    docs: iteration of strings
    rtype: list of list of entities
    """
    res  = []
    for d in docs:
        d = re.sub(r'http\S+', '', d) # remove link
        d = re.sub(r'@\S+','',d) # remove @ stuff
        tags = pos_tag(word_tokenize(d)) # get pos tag of each word
        
        ents = combine_nouns(tags)
        
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

    res = extract_entities_nltk(corpora)
    print(res)

    if options.savePath:
        with open(options.savePath,'w') as f:
            json.dump(res,f)

        print('*'*20)
        print(f'the data has been saved in file:{options.savePath}')

