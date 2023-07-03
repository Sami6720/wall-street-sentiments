from top_stocks_opening_closing_prices_extractor import get_top_stocks_opening_closing_prices
import boto3
from config import Config


def lambda_handler(event, context):
    """
    Get opening and closing stock prices for the list of top
    stocks for the day. These would later be used to label 
    the data.

    param event: Event data passed to this lambda function.
    type: dict

    param context: Context data passed to this lambda function. 
    type: dict

    return stock_price_df: Dataframe of top stocks opening and closing prices.
    rtype: pd.DataFrame"""

    config = Config()
    FINHUB_API_KEY = config.finnhub_api_key
    BUCKET_NAME = config.bucket_name
    s3_client = boto3.client('s3')
    today = event['workflowStart']['today']
    top_stock_tickers = list(
        event['topStocksDataExtractor']['Payload']['topStocks'])
    top_stocks_opening_closing_prices_df = get_top_stocks_opening_closing_prices(
        top_stock_tickers, today, FINHUB_API_KEY)

    # save top_stocks_opening_closing_prices_df as csv and to s3
    key = f'extracted_data/top_stocks_opening_closing_prices/top_stocks_opening_closing_prices_{today}.csv'
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key,
                         Body=top_stocks_opening_closing_prices_df.to_csv(index=False))

    return {
        "status": "success",
        "pathTopStockPrices": key
    }
