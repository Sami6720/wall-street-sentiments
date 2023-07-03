from config import Config
from labelling_transformer import label_data
from cloud_interactions import get_data_from_s3, upload_data_to_s3, \
    build_s3_path

config = Config()
BUCKET_NAME = config.bucket_name

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
    preprocessed_data_path = event['preprocessorTransformer']['Payload']['pathPreprocessedData']
    top_stocks_prices_extracted_path = event['topStockPricesExtractor']['Payload']['pathTopStockPrices']

    preprocessed_data = get_data_from_s3(BUCKET_NAME, preprocessed_data_path)
    top_stocks_prices_extracted = get_data_from_s3(
        BUCKET_NAME, top_stocks_prices_extracted_path)
    labelled_data = label_data(
        preprocessed_data, top_stocks_prices_extracted)

    labelled_data_path = build_s3_path(
        LABELLED_DATA_DESTINATION_PREFIX, today, 'labelled_data')
    upload_data_to_s3(BUCKET_NAME, labelled_data_path, labelled_data)

    return {
        'status': 'success',
        'pathLabelledData': labelled_data_path
    }
