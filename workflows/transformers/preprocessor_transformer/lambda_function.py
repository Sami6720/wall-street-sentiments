from datetime import datetime
from config import Config
import pytz
from preprocessor_transformer import create_new_feature_columns, \
    impute_values_in_columns, \
    rename_columns
from cloud_interactions import get_extracted_data, upload_preprocessed_data

config = Config()
BUCKET_NAME = config.bucket_name
TOP_STOCKS_INFO_EXTRACTED_PATH_PREFIX = config.top_stocks_info_extracted_path_prefix
PREPROCESSED_DESTINATION_PATH_PREFIX = config.preprocessed_destination_path_prefix


def lambda_handler(event, context) -> None:
    """Lambda handler function

    param event: Event data passed to function.
    type: dict
    param context: Runtime information passed to function.
    type: dict

    return: Status of lambda function execution.
    rtype: dict
    """
    timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(timezone)
    today = current_time.strftime('%m-%d-%Y')

    top_stocks_info_extracted = get_extracted_data(today,
                                                   BUCKET_NAME,
                                                   TOP_STOCKS_INFO_EXTRACTED_PATH_PREFIX)

    preprocessed_data = rename_columns(top_stocks_info_extracted)
    preprocessed_data = create_new_feature_columns(preprocessed_data)
    preprocessed_data = impute_values_in_columns(preprocessed_data)

    upload_preprocessed_data(preprocessed_data, today,
                             BUCKET_NAME, PREPROCESSED_DESTINATION_PATH_PREFIX)
