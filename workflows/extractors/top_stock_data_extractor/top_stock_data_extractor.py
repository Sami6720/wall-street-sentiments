import requests
import bs4
import numpy as np
import pandas as pd
from alternative_assets import alternative_assets_tickers
from datetime import datetime


def get_top_stocks_sentiment(top_stock_tickers: list) -> list:
    """
    Get top stocks' sentiment by scraping Apewisdom's stocks page. This
    is done by analyzing comments over a period of 24 hours from the morning
    when the workflow starts.

    param: top_stock_tickers
    prarm type: list

    return: top_ten_stock_sentiment
    rtype: list
    """
    top_stocks_sentiments = []
    for stock in top_stock_tickers:
        try:
            html_content = requests.get(
                f'https://apewisdom.io/stocks/{stock}/', timeout=60).text
            # soup is a BeautifulSoup object for parsing HTML
            soup = bs4.BeautifulSoup(html_content, 'html.parser')
            title_div = soup.find_all('div', class_='tile-title')
            for title in title_div:
                if title.text == 'Sentiment':
                    value_div = title.findNext('div', class_='tile-value')
                    if value_div:
                        sentiment_value = value_div.text
                        sentiment_value = float(
                            sentiment_value.replace('%', '').strip())
                        top_stocks_sentiments.append(sentiment_value)
                        break
        except Exception as error:
            top_stocks_sentiments.append(np.nan)
            print(f"For {stock} the error is {error}")
    return top_stocks_sentiments


def get_top_stocks_reddit_metrics(page_number: int = 1,
                                  required_number_of_top_stocks: int = 10) -> list:
    """
    Get top stocks' (by default 10) reddit metrics from Apewisdom API. This
    includes the following metrics: upvotes, mentions, rank, mentions_24h_ago, 
    and rank_24h_ago. These data points are calculated over a 24 hour period 
    from the morning when the workflow starts.

    param page_number: Pagination nuber for the APEWISDOM API.
    type: int
    param required_number_of_top_stocks: Number of top stocks to be returned. 
    Note we are only looking for common stocks and not alternative assets.
    type: int
    default: 10

    return: top_stocks_raw_reddit_sentiment_info
    rtype: list of dicts
    """
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


def get_top_stocks_mentioning_user_counts(top_stock_tickers: list) -> list:
    """
    Get top stocks' mentioning user count by scraping Apewisdom's stocks page.

    param: top_stock_tickers
    prarm type: list

    return: top_stocks_mentioning_user_counts
    rtype: list
    """
    top_stocks_mentioning_user_counts = []
    for stock in top_stock_tickers:
        try:
            html_content = requests.get(
                f'https://apewisdom.io/stocks/{stock}/', timeout=60).text
            soup = bs4.BeautifulSoup(html_content, 'html.parser')
            title_div = soup.find_all('div', class_='tile-title')
            for title in title_div:
                if title.text == 'mentioning users':
                    value_div = title.findNext('div', class_='tile-value')
                    if value_div:
                        mentioning_users = value_div.text
                        mentioning_users = float(
                            mentioning_users.split(' ')[0].replace(',', ''))
                        top_stocks_mentioning_user_counts.append(
                            mentioning_users)
        except Exception as error:
            print(f"For {stock} the error is {error}")

    return top_stocks_mentioning_user_counts


def get_top_stocks_fundamentals_df(top_stock_tickers: list,
                                   FINNHUB_API_KEY: str) -> pd.DataFrame:
    """
    Get financial fundamentals for list of top stocks. This inlcudes the 
    following metrics: beta, epsTTM, peTTM, roeTTM, dividendYieldIndicatedAnnual, 
    totalDebt/totalEquityQuarterly, and revenueGrowthTTMYoy.

    param: top_stock_tickers
    type: list

    param: FINNHUB_API_KEY
    type: str

    return: top_stocks_fundamentals_df
    rtype: pd.DataFrame
    """
    top_stocks_fundamentals_df = pd.DataFrame()
    METRICS = ['beta', 'epsTTM', 'peTTM', 'roeTTM', 'dividendYieldIndicatedAnnual',
               'totalDebt/totalEquityQuarterly', 'revenueGrowthTTMYoy']
    stock_fundamentals = {}
    for stock in top_stock_tickers:
        try:
            data = requests.get(
                f"https://finnhub.io/api/v1/stock/metric?symbol={stock}&metric=all&token={FINNHUB_API_KEY}",
                timeout=60).json()
            fundamentals_for_stock = {}
            metrics_in_data = data['metric'].keys()
            for metric in METRICS:
                if metric not in metrics_in_data:
                    fundamentals_for_stock[metric] = np.nan
                    continue
                fundamentals_for_stock[metric] = data['metric'][metric]
            stock_fundamentals[stock] = fundamentals_for_stock
        except Exception as error:
            print(f"For stock {stock} the error is {error}")

    top_stocks_fundamentals_df = pd.DataFrame(stock_fundamentals).T
    top_stocks_fundamentals_df = top_stocks_fundamentals_df.reset_index().rename(columns={
        'index': 'ticker'})
    return top_stocks_fundamentals_df


def get_top_stock_tickers(top_stocks_raw_reddit_sentiment_info: list) -> list:
    """
    Get top stocks' tickers from the first page of the Apewisom.io website.

    param: top_ten_stock_info_on_first_page

    return: top_ten_stock_ticker
    rtype: list
    """
    top_stock_tickers = []
    for stock in top_stocks_raw_reddit_sentiment_info:
        top_stock_tickers.append(stock['ticker'])
    return top_stock_tickers


def create_top_stock_data_df(top_stocks_info_on_first_page: dict, top_stocks_sentiments: list,
                             top_stocks_mentioning_user_counts: list,
                             top_stocks_fundamentals_df: pd.DataFrame,
                             timestamp: datetime) -> pd.DataFrame:
    """
    Create a merged dataframe containing the sentiment info, reddit metrics,
    and fundamental metrics of the top stocks.

    param: top_ten_stock_info
    type: dict

    param: top_ten_stock_sentiments
    type: dict

    param: top_ten_stock_mentioning_users
    type: dict

    return: top_stock_info_df
    rtype: pd.DataFrame"""
    top_stock_info_df = pd.DataFrame(top_stocks_info_on_first_page)
    top_stock_info_df['sentiment'] = top_stocks_sentiments
    top_stock_info_df['mentioning_users'] = top_stocks_mentioning_user_counts
    top_stock_info_df['timestamp'] = timestamp
    top_stock_info_df = top_stock_info_df[['timestamp', 'rank', 'ticker', 'name', 'mentions',
                                           'mentioning_users', 'upvotes', 'sentiment',
                                           'rank_24h_ago', 'mentions_24h_ago']]
    top_ten_stock_info_df = pd.concat(
        [top_stock_info_df, top_stocks_fundamentals_df], axis=1)
    top_ten_stock_info_df = top_ten_stock_info_df.loc[:,
                                                      ~top_ten_stock_info_df.columns.duplicated()]
    return top_ten_stock_info_df
