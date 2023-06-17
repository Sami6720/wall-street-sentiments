from datetime import datetime
import boto3
from config import Config
import pandas as pd
import pytz
from top_stock_raw_data_enrichment_transformer import create_target_column, \
    create_new_feature_columns, \
    impute_values_in_columns, \
    rename_columns
from cloud_interactions import get_file_dates_in_s3_folder, \
    get_dates_not_transformed, \
    get_data_frames_from_extraction_folders

config = Config()
BUCKET_NAME = config.bucket_name


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

    file_dates_in_extracted_data = set(get_file_dates_in_s3_folder(
        BUCKET_NAME, 'extracted_data/top_stocks_info'))
    last_date_in_transformed_data = max(get_file_dates_in_s3_folder(
        BUCKET_NAME, 'transformed_data'), default=None)
    dates_not_transformed = get_dates_not_transformed(
        last_date_in_transformed_data, file_dates_in_extracted_data)
    top_stocks_info_dfs = get_data_frames_from_extraction_folders(
        dates_not_transformed, 'top_stocks_info', BUCKET_NAME)
    top_stocks_opening_closing_prices_dfs = get_data_frames_from_extraction_folders(
        dates_not_transformed, 'top_stocks_opening_closing_prices', BUCKET_NAME)
    top_stock_info_dfs_concatanated = pd.concat(top_stocks_info_dfs,
                                                axis=0, ignore_index=True)
    top_stocks_opening_closing_prices_dfs_concatanated = pd.concat(
        top_stocks_opening_closing_prices_dfs, axis=0, ignore_index=True)
    data = pd.merge(left=top_stock_info_dfs_concatanated,
                    right=top_stocks_opening_closing_prices_dfs_concatanated,
                    on=['timestamp', 'ticker']).sort_values(by='timestamp')

    data = rename_columns(data)
    data = create_target_column(data)
    data = create_new_feature_columns(data)
    data = impute_values_in_columns(data)

    s3 = boto3.client('s3')
    key = f'transformed_data/transformed_data_{today}.csv'
    s3.put_object(Bucket=BUCKET_NAME, Key=key,
                  Body=data.to_csv(index=False))


if __name__ == '__main__':
    lambda_handler({}, {})
