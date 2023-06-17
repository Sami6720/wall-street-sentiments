import os
import pandas as pd
import numpy as np
import boto3
from config import Config

config = Config()


def create_target_column(data: pd.DataFrame) -> pd.DataFrame:
    """Create target column

    param data: Dataframe of extracted data.
    type: pd.DataFrame

    return: Dataframe with target column.
    rtype: pd.DataFrame
    """

    data['target'] = (data['opening_price'] -
                      data['closing_price']
                      ).apply(lambda x: 1 if x > 0 else 0)
    return data


def create_new_feature_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Create new feature columns

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
    """Impute values in columns

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
    """Rename columns

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


def merge_dataframes(
        top_stocks_info_dfs: list,
        top_stocks_opening_closing_prices_dfs: list) -> pd.DataFrame:
    """Merge dataframes

    param top_stocks_info_dfs: List of dataframes of top stocks info.
    type: list
    param top_stocks_opening_closing_prices_dfs: List of dataframes of top stocks opening and closing prices.
    type: list

    return: Dataframe with merged dataframes.
    rtype: pd.DataFrame
    """
    new_extracted_data_exists = len(top_stocks_info_dfs) != 0

    if not new_extracted_data_exists:
        return pd.DataFrame()

    top_stock_info_dfs_concatanated = pd.concat(top_stocks_info_dfs,
                                                axis=0, ignore_index=True)
    top_stocks_opening_closing_prices_dfs_concatanated = pd.concat(
        top_stocks_opening_closing_prices_dfs, axis=0, ignore_index=True)
    data = pd.merge(left=top_stock_info_dfs_concatanated,
                    right=top_stocks_opening_closing_prices_dfs_concatanated,
                    on=['timestamp', 'ticker']).sort_values(by='timestamp')

    return data
