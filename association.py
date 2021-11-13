from collections import defaultdict
from extract_corpora import corpora
from process_text_nltk import extract_entities_nltk

def compute_frequency(entis, minSup = 1):
    """
    entis: list of list of entities
    minSup : minimal number in all entities
    rtype:
        list of tuple(entity,frequency)
    """

    frequency = defaultdict(int)
    for ls in entis:
        for ent in ls:
            frequency[ent] += 1

    sorted_frequency = sorted([(e,f) for e,f in frequency.items() if f > minSup], key=lambda x:x[1], reverse=True)
    return sorted_frequency

def association(keyword,date1,date2):
    docs = corpora(keyword,date1,date2,None)
    entis = extract_entities_nltk(docs)
    freq = compute_frequency(entis)

    return freq

