from datetime import datetime
import boto3
from config import Config
import pytz
from labelling_transformer import label_data
from cloud_interactions import get_data_from_s3, upload_data_to_s3, \
    build_s3_path

config = Config()
BUCKET_NAME = config.bucket_name
PREPROCESSED_DATA_PATH_PREFIX = config.preprocessed_data_path_prefix
TOP_STOCKS_PRICES_EXTRACTED_PREFIX = config.top_stocks_prices_extracted_prefix
LABELLED_DATA_DESTINATION_PREFIX = config.labelled_data_destination_prefix


def lambda_handler(event, context) -> None:
    """Lambda handler function

    param event: Event data passed to function.
    type: dict
    param context: Runtime information passed to function.
    type: dict

    return: Status of lambda function execution.
    rtype: dict
    """
    today = event['workflowStart']['today']
    preprocessed_data_path = event['transformers']['preprocessorTransformer']['pathPreprocessedData']
    top_stocks_prices_extracted_path = event['extractors']['topStocksPricesExtractor']['topStockPricesPath']

    preprocessed_data = get_data_from_s3(BUCKET_NAME, preprocessed_data_path)
    top_stocks_prices_extracted = get_data_from_s3(
        BUCKET_NAME, top_stocks_prices_extracted_path)
    labelled_data = label_data(
        preprocessed_data, top_stocks_prices_extracted)

    labelled_data_path = build_s3_path(
        LABELLED_DATA_DESTINATION_PREFIX, today, 'labelled_data')
    upload_data_to_s3(BUCKET_NAME, labelled_data_path, labelled_data)
