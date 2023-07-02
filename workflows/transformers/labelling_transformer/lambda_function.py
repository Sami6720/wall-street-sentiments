from datetime import datetime
import boto3
from config import Config
import pytz
from labelling_transformer import label_data
from cloud_interactions import get_data_from_s3, upload_data_to_s3

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

    preprocessed_data = get_data_from_s3(BUCKET_NAME, PREPROCESSED_DATA_PATH_PREFIX,
                                         today, 'preprocessed_data')
    top_stocks_prices_extracted = get_data_from_s3(BUCKET_NAME, TOP_STOCKS_PRICES_EXTRACTED_PREFIX,
                                                   today, 'top_stocks_opening_closing_prices')
    labelled_data = label_data(
        preprocessed_data, top_stocks_prices_extracted)

    upload_data_to_s3(BUCKET_NAME, LABELLED_DATA_DESTINATION_PREFIX,
                      labelled_data, today, 'labelled_data')
