This project is about NWO.AI company task: Semantic Search Algorithm.

The workflow of this project is that:

1. extract corpora from tweets and Reddit tables associated with keyword **within a range of time**. Cause all the trends are associated with a range of time. Here, I choose to use two ranges of time.
2. process the corpora and extract entities
3. compute the TF-IDF of each entity and decide which one has a strong relationship with the keyword based on the difference of TF-IDF in these two periods of time.


## Extract corpora from tweets and Reddit tables using keywords between a range of time 

```python
python extract_corpora.py -k iPhone -l 10
```

- `-k`: keyword
- `-l`: limit, limit the number of output in the SQL query.

TODO:
1. Use synonyms of keywords to extract corpora from tables when there is no keyword in the database

## Process the corpora using NLTK or Stanza

```python
python process_text_nltk.py -f text_file.json -s entities.json
```

- `-f`: JSON file containing corpora data
- `-s`: save path file to store the entities

Cons:
1. Using Stanza to extract entities is better than NLTK. But the former is slower.

TODO:
1. extract entities more accurately ，for example using the machine learning method.
1. entity disambiguation: convert the embedding of entities through bert and Spacy models and use cosine similarity to combine the same meaning of entities.

## Get the associated entities

At this step, I chose two periods of time and compare the difference of TF-IDF of each entity. Then entities will be returned based on TF-IDF difference in descending order.

When the keyword is set to 'Jeff Bezos' and the date is set from [2020,1,1]
 to [2021,1,1]. The top 10  trend entities are shown below:

 ```python
[('money', 0.0050692567642110185),
 ('world', 0.0033733516327722583),
 ('country', 0.002260528930074821),
 ('point', 0.0022593738816724376),
 ('stock', 0.002158138849534128),
 ('wealth', 0.0019373261914564762),
 ('tesla', 0.0019281190207367134),
 ('work', 0.001916325391937995),
 ('business', 0.0016910307208879054),
 ('amount', 0.0016395234455241236)]
 ```
