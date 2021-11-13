# nwo.ai_task
This project is about NWO.AI company task: Semantic Search Algorithm.

The workflow of this project is that:

1. extract corpora from tweets and reddit tables associated with keyword **within a range of time**
2. process the corpora and extract enities
3. implement FP-tree algorithm to get the entities associated with the keyword


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

At this step I just count the frequency of each entity from the above part. Then return the entities based on frequency in decending order.




