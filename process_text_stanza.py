import spacy,nltk
import pandas as pd
import numpy as np
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
import stanza
# from nltk import pos_tag
# from nltk import  word_tokenize
from optparse import OptionParser
import json
import re


# lemmatizer = WordNetLemmatizer()
# nlp = spacy.load('en_core_web_sm')
# nlp = stanza.Pipeline('en',processors='tokenize,pos,lemma') # initialize English neural pipeline

def connect_entities(doc):
    """
    if the NN word next to each other, then we combine them together
    doc: document style , such as doc = nlp(p)
    rtype:
        list of nouns
    """
    list_tokens = [] # convert to dictionary
    for sub_list in doc.to_dict():
        list_tokens += sub_list
    entis = [x for x in list_tokens if x['xpos'].startswith('NN')] # extract nouns

    # next procedures are to connect the nouns next to each other into one noun
    n = len(entis)
    if n == 0:
        return []
    elif n == 1:
        return [entis[0]['lemma']]
    elif n == 2:
        if entis[0]['id'] + 1 == entis[1]['id']: # next to each other
            return [entis[0]['text']+' '+ entis[1]['text']]
        else:
            return [entis[0]['lemma'], entis[1]['lemma']]
    ans = [] # to store all the nouns
    right = 1
    w = entis[0]['lemma']

    while right < n:
        if entis[right]['id'] == entis[right-1]['id']+1: # next to each other
            w += ' '+entis[right]['lemma']
        else:
            ans.append(w)
            w = entis[right]['lemma']
        
        right += 1
    ans.append(w)
    return ans


def extract_entities_stanza(docs):
    """
    docs: iteration of strings
    rtype: list of list of entities
    """
    nlp = stanza.Pipeline('en',processors='tokenize,pos,lemma') # initialize English neural pipeline

    res  = []
    for d in docs:
        # d = re.sub(r'http\S+', '', d) # remove link
        d = re.sub(r'@\S+','',d) # remove @ stuff
        # tags = pos_tag(word_tokenize(d)) # get pos tag of each word
        tags = nlp(d)
        ents = connect_entities(tags)

        # ents = [w for w,t in tags if t.startswith('NN')] # get the entities
        # ents = [lemmatizer.lemmatize(w) for w in ents] # lemmatization
        # ents = [w for w in ents if w.lower() not in all_stop_words] # get rid of stop words
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

    res = extract_entities_stanza(corpora)
    print(res)

    if options.savePath:
        with open(options.savePath,'w') as f:
            json.dump(res,f)

        print('*'*20)
        print(f'the data has been saved in file:{options.savePath}')

