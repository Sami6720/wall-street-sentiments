from config import Config
from top_stock_data_extractor import get_top_stocks_raw_reddit_sentiment_info, \
    get_top_stocks_mentioning_user_counts, \
    get_top_stocks_fundamentals_df, \
    get_top_stocks_sentiments_only, \
    get_top_stock_tickers, \
    create_top_stock_info_df
import boto3


def lambda_handler(event, context):
    """
    Lambda handler for the top stock data extractor. This lambda function
    extracts metrics like upvotes, mentions etc from reddit for the top stocks. 
    It also extracts sentiment for each stock on Reddit from the website Apewisdom.io.
    and extracts fundamentals like market cap, price to earnings ratio etc for each stock.

    param event: Event data passed to this lambda function.
    type: dict

    param context: Context data passed to this lambda function.
    type: dict

    return lambda function execution status, the list of top stocks and s3
    path where the top stocks info is stored.
    rtype: dict 
    """
    config = Config()
    FINHUB_API_KEY = config.finnhub_api_key
    BUCKET_NAME = config.bucket_name
    today = event['workflowStart']['today']
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

    return {
        "status": "success",
        "topStocks": top_stock_tickers,
        "pathTopStocksData": key
    }
