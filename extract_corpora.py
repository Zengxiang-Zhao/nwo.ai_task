from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from optparse import OptionParser
from datetime import timezone,datetime
import json

# connect to the database
credentials = service_account.Credentials.from_service_account_file(
'credential.json')
project_id = "nwo-sample"
client = bigquery.Client(credentials= credentials,project=project_id)

def corpora(keyword,date1,date2,limit):
    """extract corpora from graph.tweets and graph.reddit associated with keyword
    Parameters
    ---------
    keyword : str
        The keyword you want to search in the Database
    date1 : (int,int,int)
    date2 : (int,int,int)
        A tuple of integers like (year,month,day)
    limit : int or None
        The rows you want to extract from graph.tweets and graph.reddit respectively 
        when defining the limit as an number.
        Extract all the rows satisfying the criteria when the limit is None

    Returns
    ---------
    res : [strings] or None
        If there are some rows that satisfy the creteria then return a list of strings. Otherwise return None.

    """
    dt_date1 = datetime(date1[0],date1[1],date1[2])
    dt_date2 = datetime(date2[0],date2[1],date2[2])

    # convert utc time to datetime
    utc_timestamp1 = dt_date1.replace(tzinfo=timezone.utc).timestamp()
    utc_timestamp2 = dt_date2.replace(tzinfo=timezone.utc).timestamp()

    tweet_timestamp1 = f'{date1[0]}-{date1[1]}-{date1[2]}'
    tweet_timestamp2 = f'{date2[0]}-{date2[1]}-{date2[2]}'

    query_reddit_all_corpora = f"""
        SELECT body as corpora FROM graph.reddit
        WHERE LOWER(body) like '% {keyword.lower()} %'
        AND created_utc BETWEEN {utc_timestamp1} AND {utc_timestamp2}
        """
    query_tweet_all_corpora = f"""
        SELECT tweet as corpora FROM graph.tweets
        WHERE LOWER(tweet) like '% {keyword.lower()} %'
        AND created_at BETWEEN '{tweet_timestamp1}' AND '{tweet_timestamp2}'
        """

    if limit:
        query_reddit_all_corpora += f'\nLIMIT {limit}'
        query_tweet_all_corpora += f'\nLIMIT {limit}'

    reddit_all_corpora = (
        client.query(query_reddit_all_corpora)
        .result()
        .to_dataframe()
        )

    tweet_all_corpora = (
        client.query(query_tweet_all_corpora)
        .result()
        .to_dataframe()
        )

    keyword_corpora = pd.concat([reddit_all_corpora,tweet_all_corpora])
    if len(keyword_corpora) == 0:
        print(f'Can not find any information associated with {keyword}')
        return None

    res = keyword_corpora['corpora'].values
    return res


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-k', '--keyword',
                         dest='keyword',
                         help='keyword',
                         default=None)
    optparser.add_option('-l', '--limit',
                         dest='limit',
                         help='limit the number of output in corpora',
                         default=None,
                         type='int')
    optparser.add_option('-f', '--filePath',
                         dest='filePath',
                         help='store the result to a json file',
                         default=None)
    (options, args) = optparser.parse_args()

    corpora = corpora(options.keyword,(2020,1,1),(2021,1,1),options.limit)
    print(corpora)

    if options.filePath:
        with open(options.filePath, 'w') as f:
            json.dump(list(corpora),f)

        print('*'*20)
        print(f'The result has been saved in file:{options.filePath}')
