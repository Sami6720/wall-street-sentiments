import pandas as pd
import json

from cloud_interactions import get_data_from_s3

predictions_by_models = []


def build_predictions_by_models_json(workflow_date: str, predictions_paths: list, bucket_name: str):
    """
    This function is used to build the `predictions_by_models_json`. There will be
    one entry for each model. Each entry will contain the `workflow_date`, and `model_name`. 
    It will also contain the `company_name`, `ticker`, `prediction` adn `features` for each 
    stock.

    :param `workflow_date`: workflow date
    :type `workflow_date`: str
    :param `predictions_paths`: predictions paths
    :type `predictions_paths`: list
    :param `bucket_name`: bucket name
    :type `bucket_name`: str

    :return: `predictions_by_models`
    :rtype: json
    """

    for path in predictions_paths:

        predictions = get_data_from_s3(path)

        predictions_dict_for_model = {}
        predictions_dict_for_model["workflow_date"] = workflow_date
        predictions_dict_for_model["model"] = predictions["model"][0]

        predictions_by_models.append(
            add_prediction_and_features_for_each_stock(predictions, predictions_dict_for_model)
        )

    return json.dumps(predictions_by_models)


def add_prediction_and_features_for_each_stock(predictions: pd.DataFrame,
                                               predictions_dict_for_model: pd.DataFrame) -> dict:
    """
    This function is used to add the `prediction` and the `features` for each stock
    from the `predictions` dataframe to the `predictions_dict_for_model`.

    :param `predictions`: predictions dataframe
    :type `predictions`: pandas.DataFrame
    :param `predictions_dict_for_model`: predictions_dict_for_model
    :type `predictions_dict_for_model`: dict

    :return: `predictions_dict_for_model`
    :rtype: dict
    """

    predictions_dict_for_model["predictions"] = []
    for record in predictions.to_dict(orient='records'):
        record.pop("model", None)
        predictions_dict_for_model["predictions"].append(
            {
                "prediction": record.pop("prediction", None),
                "ticker": record.pop("ticker", None),
                "company_name": record.pop("name", None),
                "features": record
            })

    return predictions_dict_for_model
