import pandas as pd
import numpy as np


def create_label_column(data: pd.DataFrame) -> pd.DataFrame:
    """Create label column

    param data: Dataframe of to be labelled.
    type: pd.DataFrame

    return: Dataframe with target column.
    rtype: pd.DataFrame
    """

    data['label'] = (data['closing_price'] -
                     data['opening_price']
                     ).apply(lambda x: 1 if x > 0 else 0)
    return data


def label_data(
        top_stocks_info_extracted: pd.DataFrame,
        top_stocks_prices_extracted: pd.DataFrame) -> pd.DataFrame:
    """Merge dataframes

    param top_stocks_info_extracted: Dataframe of extracted top stocks info.
    type: pd.DataFrame
    param top_stocks_prices_extracted: Dataframe of extracted top stocks prices.
    type: pd.DataFrame

    return: Dataframe with merged dataframes.
    rtype: pd.DataFrame
    """

    data = pd.merge(left=top_stocks_info_extracted,
                    right=top_stocks_prices_extracted,
                    on=['timestamp', 'ticker']).sort_values(by='timestamp')
    data = create_label_column(data)

    return data
