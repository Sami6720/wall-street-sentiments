from config import Config
from preprocessor_transformer import create_new_feature_columns, \
    impute_values_in_columns, \
    rename_columns
from cloud_interactions import get_data_from_s3, upload_data_to_s3, \
    build_s3_path

config = Config()
BUCKET_NAME = config.bucket_name
PREPROCESSED_DESTINATION_PATH_PREFIX = config.preprocessed_destination_path_prefix


def lambda_handler(event, context) -> None:
    """
    Lambda handler function to carry out the preprocessing of data.

    param event: Event data passed to function.
    type: dict
    param context: Runtime information passed to function.
    type: dict

    return: Status of the lambda function execution and the
            s3 path where the preprocessed data is stored.
    rtype: dict
    """
    today = event['workflowStart']['today']
    top_stocks_info_extracted_path = (event['topStocksDataExtractor']
                                      ['Payload']['pathTopStocksData'])

    top_stocks_info_extracted = get_data_from_s3(
        BUCKET_NAME, top_stocks_info_extracted_path)
    preprocessed_data = rename_columns(top_stocks_info_extracted)
    preprocessed_data = create_new_feature_columns(preprocessed_data)
    preprocessed_data = impute_values_in_columns(preprocessed_data)

    preprocessed_data_csv_path = build_s3_path(
        PREPROCESSED_DESTINATION_PATH_PREFIX, "csv", today, 'preprocessed_data')
    preprocessed_data_json_path = build_s3_path(
        PREPROCESSED_DESTINATION_PATH_PREFIX, "json", today, 'preprocessed_data')

    upload_data_to_s3(BUCKET_NAME, preprocessed_data_csv_path, preprocessed_data.to_csv(index=False))
    upload_data_to_s3(BUCKET_NAME, preprocessed_data_json_path, preprocessed_data.to_json(orient='records'))

    return {
        'status': 'success',
        'pathPreprocessedData': preprocessed_data_csv_path,
        'pathPreprocessedDataJson': preprocessed_data_json_path
    }
