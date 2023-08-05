import pandas as pd
import numpy as np

from logger import logger
from cloud_interactions import get_data_from_s3


def get_aggregated_metrics_by_models_df(collection, aggregate_pipeline,
                                        perf_metrics_by_models_column_names) -> pd.DataFrame:
    """
    Gets the aggreagated metrics for each model from the database. The aggregation is
    done over the following features: net_buy_profits, not_buy_saves, good_day and total_days.
    If the collection is empty, an empty dataframe is returned. 

    :param collection: Collection to query.
    :type: pymongo.collection.Collection
    :param aggregate_pipeline: Pipeline to aggregate the data.
    :type: list
    :param perf_metrics_by_models_column_names: Column names for the dataframe to be returned.
    :type: list

    :return: Aggregated metrics for each model.
    :rtype: pd.DataFrame
    """

    aggregated_metrics_by_models = list(collection.aggregate(aggregate_pipeline))

    if len(aggregated_metrics_by_models) == 0:
        logger.warning(
            "Length of the returned aggregated metrics by model list is 0. "
            "A reason for this could be the collection is empty."
        )

        return pd.DataFrame(columns=perf_metrics_by_models_column_names)

    aggregated_metrics_by_models = pd.DataFrame(aggregated_metrics_by_models)
    aggregated_metrics_by_models.columns = perf_metrics_by_models_column_names

    logger.info("Finished executing get_aggregated_metrics_by_models")

    return aggregated_metrics_by_models


def build_todays_metrics_by_models_df(predictions_data_file_paths, labelled_data_file_path,
                                      workflow_start_date, bucket_name) -> pd.DataFrame:
    """
    Builds a dataframe containing the metrics for each model for today. The metrics are
    calculated by comparing the predictions made by the models with the labelled data.

    :param predictions_data_file_paths: File paths to the predictions data.
    :type: list
    :param labelled_data_file_path: File path to the labelled data.
    :type: str
    :param workflow_start_date: Start date of the workflow.
    :type: str

    :return: Dataframe containing the metrics for each model for today.
    :rtype: pd.DataFrame
    """

    labelled_data = get_data_from_s3(bucket_name, labelled_data_file_path)

    non_aggregated_metrics_by_models: [dict] = []

    for file_path in predictions_data_file_paths:

        predictions = get_data_from_s3(bucket_name, file_path)
        predictions_and_labelled_data = pd.merge(labelled_data, predictions, on=['ticker'])

        non_aggregated_metrics_by_models.append(
            build_todays_metrics_dict_for_model(
                predictions_and_labelled_data, workflow_start_date
            )
        )

    logger.info("Finished executing build_todays_metrics_by_models_df")

    return pd.DataFrame(non_aggregated_metrics_by_models)


def build_todays_metrics_dict_for_model(predictions_and_labelled_data,
                                        workflow_start_date) -> dict:
    """
    Builds a dictionary containing the metrics for a model for today. The metrics are
    calculated by comparing the predictions made by the model with the labelled data.

    :param predictions_and_labelled_data: Dataframe containing the predictions made by the model
        and the labelled data.
    :type: pd.DataFrame
    :param workflow_start_date: Start date of the workflow.
    :type: str

    :return: Dictionary containing the metrics for a model for today.
    :rtype: dict
    """

    BUY = 1
    NOT_BUY = 0

    predictions_and_labelled_data['price_change'] = (predictions_and_labelled_data['closing_price']
                                                     - predictions_and_labelled_data['opening_price'])

    radom_predictions_and_labelled_data = predictions_and_labelled_data.copy()
    radom_predictions_and_labelled_data['prediction'] = np.random.randint(
        0, 2, size=len(radom_predictions_and_labelled_data))

    # -1 becuase if money was saved by model's not buy predictions, we want to show that as a positive number.
    buy_predictions_profit = calculate_todays_net_profit_or_save(predictions_and_labelled_data, BUY)
    not_buy_predictions_save = calculate_todays_net_profit_or_save(predictions_and_labelled_data, NOT_BUY) * -1
    random_buy_predictions_profit = calculate_todays_net_profit_or_save(radom_predictions_and_labelled_data, BUY)
    random_not_buy_predictions_save = calculate_todays_net_profit_or_save(radom_predictions_and_labelled_data,
                                                                          NOT_BUY) * -1

    model = predictions_and_labelled_data['model'].iloc[0]

    model_metrics = {}
    model_metrics['timestamp'] = workflow_start_date
    model_metrics['model'] = model
    model_metrics['buy_predictions_count'] = get_predicted_category_count(predictions_and_labelled_data, BUY)
    model_metrics['not_buy_predictions_count'] = get_predicted_category_count(
        predictions_and_labelled_data, NOT_BUY)
    model_metrics['buy_predictions_profit'] = buy_predictions_profit
    model_metrics['not_buy_predictions_save'] = not_buy_predictions_save
    model_metrics['good_day'] = (1 if (not_buy_predictions_save > random_not_buy_predictions_save)
                                 and (buy_predictions_profit > random_buy_predictions_profit)
                                 else 0)

    logger.info(f"Finished executing build_todays_metrics_dict_for_model for model: {model}")

    return model_metrics


def calculate_todays_net_profit_or_save(predictions_and_labelled_data, prediction) -> float:
    """
    Calculates the net profit or save for today for a model. Profit is made when the model
    predicts a buy and the price goes up. Save is made when the model predicts a not buy
    and the price goes down.

    :param predictions_and_labelled_data: Dataframe containing the predictions made by the model
        and the labelled data.
    :type: pd.DataFrame
    :param prediction: Prediction made by the model.
    :type: int

    :return: Net profit or save for today for a model.
    :rtype: float
    """

    return (
        predictions_and_labelled_data
        [predictions_and_labelled_data['prediction'] == prediction]
        ['price_change'].sum()
    )


def get_predicted_category_count(predictions_and_labelled_data, prediction) -> int:
    """
    Calculates the number of BUY or NOT_BUY predictions made by the model.

    :param predictions_and_labelled_data: Dataframe containing the predictions made by the model
        and the labelled data.
    :type: pd.DataFrame
    :param prediction: Prediction made by the model.
    :type: int

    :return: Number of predictions made by the model.
    :rtype: int
    """

    return len(predictions_and_labelled_data[predictions_and_labelled_data['prediction'] == prediction])


def build_combined_metrics_by_models_json(todays_metrics_by_models_df,
                                          aggregated_metrics_by_models_df):
    """
    Builds a list containing the metrics for each model for today and the aggregated metrics for each model.
    The data is ontainted in ditctionaries for each model.

    :param todays_metrics_by_models_df: Dataframe containing the metrics for each model for today.
    :type: pd.DataFrame
    :param aggregated_metrics_by_models_df: Dataframe containing the aggregated metrics for each model.
    :type: pd.DataFrame

    :return: List containing the metrics for each model for today and the aggregated metrics for each model.
    :rtype: [jsonType]
    """

    metrics_by_models = pd.merge(left=todays_metrics_by_models_df,
                                 right=aggregated_metrics_by_models_df, on='model', how='left')

    metrics_by_models = replace_nan_values(metrics_by_models)
    metrics_by_models = update_aggregated_columns_with_todays_data(metrics_by_models)

    logger.info("Finished executing build_combined_metrics_by_models_json")

    return metrics_by_models.to_json(orient='records')


def replace_nan_values(metrics_by_models):
    """
    Replaces the null values in the metrics_by_models df with 0. A reason for this could be that a new model was
    introduced and no previous records for this model existed in the collection.

    :param metrics_by_models: Dataframe containing the metrics for each model for today and the aggregated metrics
        for each model.
    :type: pd.DataFrame

    :return: Dataframe containing the metrics for each model for today and the aggregated metrics for each model
        with null values replaced by 0.
    :rtype: pd.DataFrame
    """

    if metrics_by_models.isna().values.any():
        logger.warning(
            "The metrics_by_models df contains null values. These null values will be replaced by 0. "
            "A reason for this could be that a new model was introduced and no previous records "
            "for this model  existed in the collection"
        )
        metrics_by_models.replace(to_replace=np.nan, value=0, inplace=True)

    logger.info("Finished executing replace_nan_values")

    return metrics_by_models


def update_aggregated_columns_with_todays_data(metrics_by_models):
    """
    Updates the aggregated columns with the data for today. The aggregated columns are the sum of the
    buy_predictions_profit, not_buy_predictions_save and good_day columns.

    :param metrics_by_models: Dataframe containing the metrics for each model for today and the aggregated metrics
        for each model.
    :type: pd.DataFrame

    :return: Dataframe containing the metrics for each model for today and the aggregated metrics for each model
        with the aggregated columns updated with the data for today.
    :rtype: pd.DataFrame
    """

    metrics_by_models['historic_buy_predictions_profit'] += metrics_by_models['buy_predictions_profit']
    metrics_by_models['historic_not_buy_predictions_save'] += metrics_by_models['not_buy_predictions_save']
    metrics_by_models['total_good_days'] += metrics_by_models['good_day']
    metrics_by_models['total_days'] += 1

    logger.info("Finished executing update_aggregated_columns_with_todays_data")

    return metrics_by_models
