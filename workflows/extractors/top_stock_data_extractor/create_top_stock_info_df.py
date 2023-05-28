from datetime import datetime
import pandas as pd

# TODO: Fix the logic of the creae_top_stock_info_df function so that it is
#      consistent


def create_top_stock_info_df(top_stocks_info_on_first_page: dict, top_stocks_sentiments: list,
                             top_stocks_mentioning_user_counts: list, top_stocks_fundamentals_df: pd.DataFrame,
                             timestamp: datetime) -> pd.DataFrame:
    """Create a DataFrame for the top ten stock info.

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
