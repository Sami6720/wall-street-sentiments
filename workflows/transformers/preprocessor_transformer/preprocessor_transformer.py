import pandas as pd
import numpy as np
from config import Config

config = Config()


def create_new_feature_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create new feature columns from existing columns. These would
    be dividend_exists, rank_percentage_change_24h and 
    mentions_percentage_change_24h.

    param data: Dataframe of extracted data.
    type: pd.DataFrame

    return: Dataframe with new feature columns.
    rtype: pd.DataFrame
    """

    data['dividend_exists'] = data['dividend_yield_annual'
                                   ].apply(lambda x: 1
                                           if x > 0 else 0)
    data['rank_percentage_change_24h'] = (
        (data['rank'] - data['rank_24h_ago']) /
        data['rank_24h_ago']
    )
    data['mentions_percentage_change_24h'] = (
        (data['mentions'] - data['mentions_24h_ago']) /
        data['mentions_24h_ago']
    )

    return data


def impute_values_in_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Impute values in columns where the values are missing a noitceable
    amount of time. This is because a lot of companies don't pay dividends.
    Also, if a company is not making any money, it's price to equity ratio
    will be non existent as well. These were initially represented as NaNs.
    They are now replaced with 0s.

    param data: Dataframe of extracted data.
    type: pd.DataFrame

    return: Dataframe with imputed values.
    rtype: pd.DataFrame
    """

    data['dividend_yield_annual'].replace(
        to_replace=np.nan, value=0, inplace=True)
    data['price_to_equity_ttm'].replace(
        to_replace=np.nan, value=0, inplace=True)

    return data


def rename_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Renaming columns of fundamental data that was extracted.

    param data: Dataframe of extracted data.
    type: pd.DataFrame

    return: Dataframe with renamed columns.
    rtype: pd.DataFrame
    """

    data.rename(
        columns={'dividendYieldIndicatedAnnual': 'dividend_yield_annual',
                 'epsTTM': 'earnings_per_share_ttm',
                 'peTTM': 'price_to_equity_ttm',
                 'roeTTM': 'return_on_equity_ttm',
                 'totalDebt/totalEquityQuarterly': 'total_debt_to_equity_quarterly',
                 'revenueGrowthTTMYoy': 'revenue_growth_ttm_yoy'
                 },
        inplace=True
    )

    return data
