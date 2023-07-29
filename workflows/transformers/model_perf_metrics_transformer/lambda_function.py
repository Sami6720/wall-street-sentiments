import pandas as pd

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import Config

from cloud_interactions import upload_data_to_s3, build_s3_path
from model_perf_metrics_transformer import (get_aggregated_metrics_by_models_df,
                                            build_todays_metrics_by_models_df,
                                            build_combined_metrics_by_models_json)

from logger import logger

config = Config()

client = MongoClient(config.db_connection_string,
                     server_api=ServerApi(version='1'))
db = client[config.db_name]
collection = db[config.db_collection_name]


def lambda_handler(event, context):
    """
    Lambda handler function.

    :param event: Event data passed to function.
    :type: dict

    :param context: Runtime information passed to function.
    :type: dict

    :return: Status of lambda function execution and s3 path where 
             model performance metrics for the day is stored.
    :rtype: dict
    """

    start_time = pd.Timestamp.now()
    logger.info("The model performance metrics transformer lambda function has started.")

    workflow_start_date = event['workflowStart']['today']

    model_metrics_dict = build_combined_metrics_by_models_json(
        get_aggregated_metrics_by_models_df(collection, config.aggregation_pipeline,
                                            config.aggregated_metrics_by_models_column_names),
        build_todays_metrics_by_models_df(
            event['predictions']['Payload']['predictionsFilePath'],
            event['labellingTransformer']['Payload']['pathLabelledData'],
            workflow_start_date,
            config.bucket_name
        )
    )

    model_perf_metrics_path = build_s3_path(
        config.model_perf_metrics_destination_prefix, "json", workflow_start_date, 'model_perf_metrics')
    upload_data_to_s3(config.bucket_name, model_perf_metrics_path, model_metrics_dict)

    logger.info(
        f"The model performance metrics transformer lambda function took {pd.Timestamp.now() - start_time} to finish."
    )

    return {
        'status': 'success',
        'modelPerfMetricsPath': model_perf_metrics_path
    }
