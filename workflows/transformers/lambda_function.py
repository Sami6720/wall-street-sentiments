from datetime import datetime
import boto3
from config import Config
import pandas as pd
from transformer import create_target_column, \
    create_new_feature_columns, \
    impute_values_in_columns, \
    rename_columns
import pytz
import botocore

config = Config()
BUCKET_NAME = config.bucket_name


def extract_date_from_filename(filename: str) -> str:
    """Extract date from filename

    param filename: Name of file.
    type: str

    return: Date in filename.
    rtype: str
    """

    return filename.split('_')[-1].split('.')[0]


def get_file_dates_in_s3_folder(bucket_name: str,
                                folder_path: str) -> list:
    """Get list of file names in S3 folder

    param bucket_name: Name of S3 bucket.
    type: str

    param folder_path: Path of S3 folder.
    type: str

    return: List of file names in S3 folder.
    rtype: list
    """

    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
    file_names = []
    for s3_object in response['Contents']:
        object_key = s3_object['Key']
        if object_key.endswith('/'):
            continue
        file_names.append(object_key)

    file_dates_in_s3_folder = [
        extract_date_from_filename(file) for file in file_names]

    return file_dates_in_s3_folder


def get_dates_not_transformed(last_date_in_transformed_data,
                              file_dates_in_extracted_data) -> list:
    """Get dates not transformed by selecting dates after last date in transformed data

    param last_date_in_transformed_data: Last date in transformed data.
    type: str
    param file_dates_in_extracted_data: Dates in extracted data.
    type: list

    return: Dates not transformed.
    rtype: list
    """
    if not last_date_in_transformed_data:
        return file_dates_in_extracted_data

    dates_not_transformed = []
    for date in file_dates_in_extracted_data:
        if datetime.strptime(date, "%m-%d-%Y").date() > datetime.strptime(last_date_in_transformed_data, "%m-%d-%Y").date():
            dates_not_transformed.append(date)
    return dates_not_transformed


def get_file_in_s3_folder(bucket_name: str,
                          date: str,
                          extracted_data_type: str) -> botocore.response.StreamingBody:
    """Get file in s3 folder according to date, bucket name and folder name

    param bucket_name: Name of S3 bucket.
    type: str
    param date: Date of file.
    type: str
    param folder_path: Path of S3 folder.
    type: str

    return: File in S3 folder.
    rtype: buffer
    """

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name,
                             Key=f'extracted_data/{extracted_data_type}/{extracted_data_type}_{date}.csv')
    file = response['Body']
    return file


def get_data_frames_from_extraction_folders(
        dates_not_transformed: list,
        extracted_data_type: str,
) -> list:
    """Get dataframes from extraction folders

    param dates_not_transformed: Dates not transformed.
    type: list
    param folder_path: Path of S3 folder.
    type: str

    return: Dataframes from extraction folders.
    rtype: list
    """
    dfs = []
    for date in sorted(dates_not_transformed):
        file = get_file_in_s3_folder(
            BUCKET_NAME, date, extracted_data_type)
        df = pd.read_csv(file)
        dfs.append(df)
    return dfs


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
        dates_not_transformed, 'top_stocks_info')
    top_stocks_opening_closing_prices_dfs = get_data_frames_from_extraction_folders(
        dates_not_transformed, 'top_stocks_opening_closing_prices')
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
