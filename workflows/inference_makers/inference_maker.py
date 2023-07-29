import pandas as pd


def add_meta_data(predictions, preprocessed_data, model_name):
    """
    Add meta data to predictions.

    :param predictions: Predictions.
    :type: pd.DataFrame
    :param preprocessed_data: Preprocessed data.
    :type: pd.DataFrame
    :param model_name: Name of model.
    :type: str
    """
    predictions = pd.concat([preprocessed_data, pd.DataFrame(predictions)], axis=1)
    predictions['model'] = model_name
