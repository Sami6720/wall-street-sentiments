import requests
import bs4
import numpy as np


def get_top_stocks_sentiments_only(top_stock_tickers: list) -> list:
    """Get top stocks' sentiment by scraping Apewisdom's stocks page.

    param: top_stock_tickers
    prarm type: list

    return: top_ten_stock_sentiment
    rtype: list"""
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
