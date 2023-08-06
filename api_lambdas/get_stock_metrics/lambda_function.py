from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import numpy as np


from bson import json_util

from config import Config

config = Config()

client = MongoClient(config.db_connection_string,
                     server_api=ServerApi(version='1'))
db = client[config.db_name]
collection = db[config.collection_name]


def lambda_handler(event, context):
    """
    Lambda function to get the latest model performance metrics.

    :param event: Event data passed to the function. It provides the 
    list of stocks to get metrics for.
    :type event: dict
    :param context: Runtime information provided by AWS Lambda.
    :type context: LambdaContext

    :return: The latest model performance metrics and status code.
    :rtype: dict
    """

    stocks = event['queryStringParameters']['stocks'].split(',')

    data_from_db = list(collection.find(
        {
            "ticker": {"$in": stocks},
        }
    ))

    stock_metrics_df = pd.DataFrame(data_from_db)

    stock_metrics_df['dividend_exists'] = np.where(stock_metrics_df['dividend_exists'] == 1, 'Yes', 'No')

    stock_metrics_dict = {}

    for stock in stocks:
        stock_metrics_dict[stock] = {}
        stock_metrics_dict[stock]['numerical'] = (stock_metrics_df[stock_metrics_df['ticker'] == stock]
                                                  .replace(to_replace=np.nan, value=0)
                                                  .drop(['ticker', 'name', '_id'], axis=1)
                                                  .select_dtypes(include=['number'])
                                                  .to_dict(orient='list'))

        stock_metrics_dict[stock]['categorical'] = (stock_metrics_df[stock_metrics_df['ticker'] == stock]
                                                    .replace(to_replace=np.nan, value=0)
                                                    .select_dtypes(include=['object', 'bool'])
                                                    .drop(['ticker', 'name', '_id'], axis=1)
                                                    .to_dict(orient='list'))

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json_util.dumps(stock_metrics_dict)
    }
