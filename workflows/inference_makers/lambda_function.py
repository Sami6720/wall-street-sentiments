from cloud_interactions import get_data_from_s3, upload_data_to_s3, build_s3_path
from config import Config
from logger import logger

config = Config()


def lambda_handler(event, context):
    """
    This function is the entry point for the inference maker workflow.
    """
    logger.info("Starting inference maker workflow")

    preproceessed_data_path = event['preprocessorTransformer']['Payload']['pathPreprocessedData']
    workflow_date = event['workflowStart']['today']

    preprocessed_data = get_data_from_s3(config.bucket_name, preproceessed_data_path)

    xgboost_model_path = config.xgboost_model_path
    random_forest_model_path = config.random_forest_model_path

    xgboost_model = get_data_from_s3(config.bucket_name, xgboost_model_path)
    random_forest_model = get_data_from_s3(config.bucket_name, random_forest_model_path)

    preprocessed_data = preprocessed_data.drop(
        ['name',
         'ticker',
         'timestamp',
         'opening_price',
         'closing_price',
         'rank_24h_ago',
         'mentions_24h_ago',
         'rank', 'dividend_exists'
         ], axis=1).sort_values(
        by=['mentions'],
        ascending=False)

    xgboost_predictions = xgboost_model.predict(preprocessed_data)
    random_forest_predictions = random_forest_model.predict(preprocessed_data)

    xgboost_predictions_path = build_s3_path(config.predictions_destination_prefix, 'csv', workflow_date, 'xgboost')
    random_forest_predictions_path = build_s3_path(
        config.predictions_destination_prefix, 'csv', workflow_date, 'random_forest')

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
