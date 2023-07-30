import pandas as pd

from config import Config
from logger import logger

from predictions_transformer import build_predictions_by_models_json
from cloud_interactions import upload_data_to_s3, build_s3_path

config = Config()


def lambda_handler(event, context):
    """
    This function is used to handle the lambda function. It will call the `build_predictions_by_models_json`
    function to build the `predictions_by_models_json`.

    :param `event`: event
    :type `event`: dict
    :param `context`: context
    :type `context`: dict

    :return: `predictions_by_models_json`
    :rtype: json
    """

    start_time = pd.Timestamp.now()

    logger.info("Starting predictions transformer lambda function")

    workflow_date = event["workflowStartDate"]
    predictions_paths = event['predictionsPaths']

    predictions_by_models_json = build_predictions_by_models_json(workflow_date, predictions_paths, config.bucket_name)
    predictions_upload_path = build_s3_path(
        config.transformed_predictions_destination_prefix, "json", workflow_date, 'transformed_prediction')
    upload_data_to_s3(config.bucket_name, predictions_upload_path, predictions_by_models_json)

    logger.info(f"Finished predictions_transformer lambda function in {(pd.Timestamp.now() - start_time)} seconds")

    return {
        "status": "success",
        "transformedPredictionsPath": predictions_upload_path,
    }
