
from datetime import datetime
from config import Config
from get_top_stocks_raw_reddit_sentiment_info import get_top_stocks_raw_reddit_sentiment_info
from get_top_stocks_mentioning_user_counts import get_top_stocks_mentioning_user_counts
from get_top_stocks_fundamentals_df import get_top_stocks_fundamentals_df
from get_top_stocks_sentiments_only import get_top_stocks_sentiments_only
from get_top_stock_tickers import get_top_stock_tickers
from create_top_stock_info_df import create_top_stock_info_df
import boto3
import pytz


def lambda_handler(event, context):
    """ Lambda handler for the top stock data extractor

    param: event:
    type: dict

    param: context
    type: dict

    return: None 
    """
    config = Config()
    FINHUB_API_KEY = config.finnhub_api_key
    BUCKET_NAME = config.bucket_name
    timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(timezone)
    today = current_time.strftime('%m-%d-%Y')
    top_stocks_raw_reddit_sentiment_info = get_top_stocks_raw_reddit_sentiment_info()
    top_stock_tickers = get_top_stock_tickers(
        top_stocks_raw_reddit_sentiment_info)
    top_stocks_sentiments_only = get_top_stocks_sentiments_only(
        top_stock_tickers)
    top_stocks_mentioning_user_counts = get_top_stocks_mentioning_user_counts(
        top_stock_tickers)
    top_stocks_fundamentals_df = get_top_stocks_fundamentals_df(
        top_stock_tickers, FINHUB_API_KEY)
    top_stock_info_df = create_top_stock_info_df(
        top_stocks_raw_reddit_sentiment_info, top_stocks_sentiments_only,
        top_stocks_mentioning_user_counts, top_stocks_fundamentals_df, today)

    # boto3 to put csv into S3 with today's date as filename (mm/dd/yyyy)
    s3 = boto3.client('s3')
    key = f'extracted_data/top_stocks_info/top_stocks_info_{today}.csv'
    s3.put_object(Bucket=BUCKET_NAME, Key=key,
                  Body=top_stock_info_df.to_csv(index=False))

    # return top_stock_info_df


if __name__ == '__main__':
    lambda_handler({}, {})
