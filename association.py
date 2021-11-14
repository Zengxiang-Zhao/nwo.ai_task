from collections import defaultdict
from extract_corpora import corpora
from process_text_nltk import extract_entities_nltk
from optparse import OptionParser


def compute_frequency(entis, minSupRatio = 0.05):
    """
    entis: list of list of entities
    minSup : minimal number in all entities
    rtype:
        list of entities
    """
    minSup = int(len(entis)*minSupRatio)
    remove_words = set(['people','person','day','year','gt','thing','way','time','t','[',']','...','%','something',',','anyone','one','nothing','’'])
    
    frequency = defaultdict(int)
    for ls in entis:
        for ent in ls:
            frequency[ent] += 1

    sorted_frequency = sorted([(e,f) for e,f in frequency.items() if f > minSup], key=lambda x:x[1], reverse=True)
    trends = [e for e,f in sorted_frequency if e not in remove_words] # only extract the entities
    return trends

def filter(trends):
    """
    Remove the repeat words using uppercase or lowercase
    """
    used = set()
    ans = []
    for t in trends:
        if t.lower() not in used:
            ans.append(t)
            used.add(t.lower())

    return ans
def association(keyword,date1,date2,minSupRatio=0.05):
    """
    Args:
        keyword : string
        date1,date2 : list or tuple containing year,month,day
    rtype:
        list of entities
    """
    docs = corpora(keyword,date1,date2,None)
    print(f'Got *{len(docs)}* passages associated with *{keyword}*')
    entis = extract_entities_nltk(docs)
    print(f'Extracted entites')
    trends = compute_frequency(entis,minSupRatio)
    print(f'Got the trends associated with *{keyword}*')
    trends = filter(trends)
    if trends[0].lower() == keyword.lower():
        trends = trends[1:]

    return trends

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-k', '--keyword',
                         dest='keyword',
                         help='keyword',
                         default=None)
    optparser.add_option('--date1',
                         dest='date1',
                         help='date like year,month,day',
                         default = '2020,1,1'
                         )
    optparser.add_option('--date2',
                         dest='date2',
                         help='date like year,month,day',
                         default='2021,11,11'
                         )
    (options, args) = optparser.parse_args()
    date1 = options.date1
    date2 = options.date2
    # print(f'date1 is :{date1}, date2 is {date2}')
    date1 = list(date1.split(',')) # get the date like ['2021','10','11']
    date2 = list(date2.split(','))
    date1 = [int(s) for s in date1]
    date2 = [int(s) for s in date2]
    # print(f'date1 is :{date1}, date2 is {date2}')

    trends = association(options.keyword, date1,date2)
    print(trends)

