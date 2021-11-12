# nwo.ai_task
This project is about NWO.AI company task: Semantic Search Algorithm.

The workflow of this project is that:

1. extract triples from the corpora of tweets and reddit posts.

2. use association rule to find the trend and the recency entities associated with the keyword.

## Build env 

1. build the Virtual Environment：`conda create -n kg python=3.6`
2. install necessary packages: `pip install -r requirement.txt`

## Extract corpora from tweets and reddit tables using keyword

```python
python extract_corpora.py -k iPhone -l 10
```

- `-k`: keyword
- `-l`: limit, limit the number of output in the sql query.
