from inference_maker import combine_predictions_and_preprocessed_data
from cloud_interactions import get_data_from_s3, upload_data_to_s3, build_s3_path, get_model
from config import Config
from logger import logger
import pandas as pd
import numpy as np

config = Config()


def lambda_handler(event, context):
    """
    This function is the entry point for the inference maker workflow.
    """
    logger.info("Starting inference maker workflow")

    workflow_date = event['workflowStartDate']
    preproceessed_data_path = event['preprocessedDataPath']

    preprocessed_data = pd.read_csv(get_data_from_s3(config.bucket_name, preproceessed_data_path))

    xgboost_model_path = config.xgboost_model_path
    random_forest_model_path = config.random_forest_model_path

    xgboost_model = get_model(config.bucket_name, xgboost_model_path)
    random_forest_model = get_model(config.bucket_name, random_forest_model_path)

    feature_engineered_data = preprocessed_data.drop(
        ['name',
         'ticker',
         'timestamp',
         'rank_24h_ago',
         'mentions_24h_ago',
         'rank', 'dividend_exists'
         ], axis=1).sort_values(
        by=['mentions'],
        ascending=False)

    feature_engineered_data = feature_engineered_data.replace(to_replace=np.nan, value=0)

    xgboost_predictions = xgboost_model.predict(feature_engineered_data)
    random_forest_predictions = random_forest_model.predict(feature_engineered_data)

    xgboost_predictions = combine_predictions_and_preprocessed_data(
        xgboost_predictions, preprocessed_data.copy(), 'xgboost')
    random_forest_predictions = combine_predictions_and_preprocessed_data(
        random_forest_predictions, preprocessed_data.copy(), 'random_forest')

    xgboost_predictions_path = build_s3_path(
        config.predictions_destination_prefix, 'csv', workflow_date, 'xgboost'
    )
    random_forest_predictions_path = build_s3_path(
        config.predictions_destination_prefix, 'csv', workflow_date, 'random_forest'
    )

    upload_data_to_s3(config.bucket_name, xgboost_predictions_path, xgboost_predictions)
    upload_data_to_s3(config.bucket_name, random_forest_predictions_path, random_forest_predictions)

    logger.info("Finished inference maker workflow")

    return {
        'status': "success",
        'predictionsPaths': [
            xgboost_predictions_path,
            random_forest_predictions_path
        ]
    }
