# nwo.ai_task
This project is about NWO.AI company task: Semantic Search Algorithm.

The workflow of this project is that:

1. extract corpora from tweets and reddit tables associated with keyword **within a range of time**. Cause all the trends are associated with a range of time.
2. process the corpora and extract enities
3. count the frequency of each entities and decide which one have a strong relationship with the keyword based on the freqency.


## Extract corpora from tweets and reddit tables using keyword between a range of time 

```python
python extract_corpora.py -k iPhone -l 10
```

- `-k`: keyword
- `-l`: limit, limit the number of output in the sql query.

TODO:
1. Use synonyms of keywords to extract corpora from tables 

## Process the corpora using NLTK or Stanza

```python
python process_text.py -f text_file.json -s entities.json
```

- `-f`: json file containing corpora data
- `-s`: save path file to store the entities

Cons:
1. Using Stanza to extract entities is better than NLTK. But the former is slower.

TODO:
1. extract entities more accurate，for example using machine learning method.
1. entity disambiguation: convert the embedding of entities through bert and Spacy models and use  cosine similarity to combine the same meaning of entities together.

## Get the associated entities

At this step I just count the frequency of each entity from the above part. Then entities will be returned based on frequency in decending order.

When the keyword is set to 'Biden' and date is set from [2021,1,1]
 to [2021,10,1] and using the default minSupRatio 0.1. The trend entities are ['Trump', 'election'].

 ```python
keyword = 'Biden'
date1 = [2021,1,1]
date2 = [2021,10,1]

trend = association(keyword,date1,date2)
#ouptput ['Trump', 'election']
 ```






