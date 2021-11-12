from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from optparse import OptionParser
import json

# connect to the database
credentials = service_account.Credentials.from_service_account_file(
'credential.json')
project_id = "nwo-sample"
client = bigquery.Client(credentials= credentials,project=project_id)

def corpora(keyword,limit):
    """
    extract corpora from graph.tweets and graph.reddit associated with keyword
    args:
        keyword: string
        limit: int or None
    rtype:
        list of strings
    """
    query_reddit_all_corpora = f"""
        SELECT body as corpora FROM graph.reddit
        WHERE body like '% {keyword} %'
        """
    query_tweet_all_corpora = f"""
        SELECT tweet as corpora FROM graph.tweets
        WHERE tweet like '% {keyword} %'
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

    return keyword_corpora['corpora'].values


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

    corpora = corpora(options.keyword, options.limit)
    print(corpora)

    if options.filePath:
        with open(options.filePath, 'w') as f:
            json.dump(list(corpora),f)

        print('*'*20)
        print(f'The result has been saved in file:{options.filePath}')
