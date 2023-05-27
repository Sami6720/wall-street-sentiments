import pandas as pd
import numpy as np
import requests


def get_top_stocks_fundamentals_df(top_stock_tickers: list, FINNHUB_API_KEY: str) -> pd.DataFrame:
    """Get fundamentals for list of top stocks.

    param: top_stock_tickers
    type: list

    param: FINNHUB_API_KEY
    type: str

    return: top_stocks_fundamentals_df
    rtype: pd.DataFrame"""
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
