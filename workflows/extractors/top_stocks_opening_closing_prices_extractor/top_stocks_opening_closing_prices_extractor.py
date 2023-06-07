import requests
import pandas as pd


def get_top_stocks_opening_closing_prices(top_stock_tickers: list, today: str,
                                          FINNHUB_API_KEY: str) -> pd.DataFrame:
    """Get current stock price for the list of stock tickers.

    param: top_stock_tickers
    type: list
    param: FINNHUB_API_KEY
    type: str
    today: timestamp,
    type: str

    return: top_stocks_opening_closing_prices_df
    rtype: pd.DataFrame"""
    stock_prices_list = []
    for stock in top_stock_tickers:
        try:
            data = requests.get(
                f'https://finnhub.io/api/v1/quote?symbol={stock}&token={FINNHUB_API_KEY}',
                timeout=60).json()
            stock_opening_closing_price = {
                "timestamp": today, "stock": stock,
                "opening_price": data['o'], "closing_price": data['c']}
            stock_prices_list.append(stock_opening_closing_price)
        except Exception as e:
            print(f"For stock {stock} the error is {e}")
    top_stocks_opening_closing_prices_df = pd.DataFrame(stock_prices_list)
    return top_stocks_opening_closing_prices_df
