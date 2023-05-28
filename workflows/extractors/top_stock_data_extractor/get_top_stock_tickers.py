def get_top_stock_tickers(top_stocks_raw_reddit_sentiment_info: list) -> list:
    """Get top stocks' tickers from the first page of the Apewisom API.

    param: top_ten_stock_info_on_first_page

    return: top_ten_stock_ticker
    rtype: list"""
    top_stock_tickers = []
    for stock in top_stocks_raw_reddit_sentiment_info:
        top_stock_tickers.append(stock['ticker'])
    return top_stock_tickers
