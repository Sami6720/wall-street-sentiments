import requests
from alternative_assets import alternative_assets_tickers


def get_top_stocks_raw_reddit_sentiment_info(page_number: int = 1,
                                             required_number_of_top_stocks: int = 10) -> list:
    """Get top stock (by default) info from Apewisdom API.

    param: page_number
    type: int

    param: Finnhub API key
    type: str

    param: required_number_of_top_stocks
    type: int
    default: 10

    return: top_stocks_raw_reddit_sentiment_info
    rtype: list"""
    FILTER = 'all-stocks'
    top_stocks_raw_reddit_sentiment_info = []
    try:
        data = requests.get(
            f'https://apewisdom.io/api/v1.0/filter/{FILTER}/page/{page_number}',
            timeout=60).json()
        data = data['results']
        common_stock_count = 0
        data_index = 0
        while common_stock_count < required_number_of_top_stocks:
            ticker = data[data_index]['ticker']
            if ticker not in alternative_assets_tickers:
                common_stock_count += 1
                top_stocks_raw_reddit_sentiment_info.append(
                    data[data_index])
            data_index += 1
    except Exception as error:
        # TODO: add np.nan rows to the dataframe
        print(f'The error is {error}')

    return top_stocks_raw_reddit_sentiment_info
