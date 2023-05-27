import requests
import bs4


def get_top_stocks_mentioning_user_counts(top_stock_tickers: list) -> list:
    """Get top stocks' mentioning user count by scraping Apewisdom's stocks page.

    param: top_stock_tickers
    prarm type: list

    return: top_stocks_mentioning_user_counts
    rtype: list"""
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
