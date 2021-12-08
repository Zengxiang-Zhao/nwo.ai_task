from collections import defaultdict
from extract_corpora import corpora
from process_text_nltk import extract_entities_nltk
from optparse import OptionParser
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
idf = TfidfTransformer()

def get_corporas(keyword,date1,date2):
    """Extract the documents from the database between date1 and date2. 
    Then repeat the process decrease the year by 1.

    Parameters
    ---------
    keyword : string
        The keyword you are interested in
    date1 : (int,int,int)
    date2 : (int,int,int)
        A tuple of integers like (year,month,day)

    Returns
    ---------
    res : [[enities],[entities]]
        A list of list of entities

    """
    docs_2 = corpora(keyword,date1,date2,None)
    year_add = date2[0] - date1[0]
    if year_add == 0:
        year_add = 1
    date1_down = [date1[0]-year_add,date1[1],date1[2]] # decrease the year by 1
    
    docs_1 = corpora(keyword,date1_down,date1,None)

    entities_1 = extract_entities_nltk(docs_1)
    entities_2 = extract_entities_nltk(docs_2)

    res = [entities_1,entities_2]
    return res

def compute_tf_idf(keyword,docs,limit=10):
    """Compute the tf-idf factor of entities in the docs
    Parameters
    ---------
    keyword : string
    docs : [[entities],[entities]]
        A list of list of entities. Compute the tf-idf based on these two list of entities.
    limit : int
        The number of entities you want to show in the result. The default value is 10
    Returns
    ---------
    ans : [(entity,score),(entity,score),...]
        A list of tuples like (entity,score)


    Process
    ---------
    step-1: get the set of entities in the docs
    step-2: use defaultdict to count the frequency of each entity
    step-3: built matrix
    step-4: compute tf-idf
    """
    dic = defaultdict(lambda : defaultdict(int))

    for i,d in enumerate(docs):
        for ls in d:
            for w in ls:
                dic[i][w] += 1

    vocabulary = set([])
    for i in range(len(docs)):
        remove_words = []
        for k,v in dic[i].items():
            if v < limit:
                remove_words.append(k)
            else:
                vocabulary.add(k)
        
        for w in remove_words:
            del dic[i][w]

    # convert to the matrix
    vocabulary = list(vocabulary)
    matrix = []
    for w in vocabulary:
        column = []
        for key in dic.keys():
            column.append(dic[key][w])
        matrix.append(column)

    # compute tf
    matrix = np.array(matrix)
    matrix = np.fastCopyAndTranspose(matrix) # shape [2,n]
    tf = []
    for i in range(len(matrix)):
        tf.append(matrix[i] / (sum(matrix[i])+1))

    # compute idf
    idf_factor = idf.fit(matrix).idf_

    # compute tf-idf
    tf_idf = np.array(tf)*idf_factor

    tf_idf_diff = tf_idf[1] - tf_idf[0]

    tf_idf_diff_sort = sorted([(v,i) for i,v in enumerate(tf_idf_diff)], key= lambda x: x[0], reverse=True)

    remove_words = set(['anything', 'everyone','‘','lot','people','person','day','year','gt','thing','way','time','t','[',']','...','%','something',',','anyone','one','nothing','’'])
    remove_words |= set(keyword.split(' '))
    remove_words.add(keyword)
    ans = [] # store the trends
    for v,i in tf_idf_diff_sort:
        if v > 0 and vocabulary[i] not in remove_words:
            ans.append((vocabulary[i], v))
    
    return ans

def extract_trends(keyword,date1,date2, limit=10):
    """Extract trends from the database between date1 and date2 based on the keyword 
    with a limit number of entities

    Parameters
    ---------
    keyword : string
        The keyword you are interested in
    date1 : (int,int,int)
    date2 : (int,int,int)
        A tuple of integers like (year,month,day)
    limit : int
        Remove the entites that the frequency is smaller than limit. The default value is 10.

    Returns
    ---------
    trends : [(entity, score),...]
        A list of tupes like (entity, score)
    
    Notes
    ---------
    This function just combine get_corporas and compute_tf_idf together
    """
    docs = get_corporas(keyword,date1,date2)

    trends = compute_tf_idf(keyword,docs,limit)
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

    trends = extract_trends(options.keyword, date1,date2)
    print(trends)
