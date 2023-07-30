import pandas as pd


def combine_predictions_and_preprocessed_data(predictions, preprocessed_data, model_name) -> pd.DataFrame:
    """
    Add meta data to predictions.

    :param predictions: Predictions.
    :type: pd.DataFrame
    :param preprocessed_data: Preprocessed data.
    :type: pd.DataFrame
    :param model_name: Name of model.
    :type: str

    :return: Predictions with meta data.
    :rtype: pd.DataFrame
    """

    preprocessed_data['prediction'] = predictions
    preprocessed_data['model'] = model_name

    return preprocessed_data
