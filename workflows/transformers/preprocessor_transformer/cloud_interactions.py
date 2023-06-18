import boto3
import botocore
import pandas as pd


def get_extracted_data(today: str, bucket_name: str, extracted_data_path_prefix: str) -> pd.DataFrame:
    """Get extracted data

    param today: Today's date.
    type: str
    param bucket_name: Name of S3 bucket.
    type: str
    param extracted_data_path_prefix: Path prefix to extracted data.
    type: str

    return: Dataframe of extracted data.
    rtype: pd.DataFrame
    """

    s3 = boto3.client('s3')
    key = f'{extracted_data_path_prefix}/top_stocks_info_{today}.csv'
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        extracted_data = pd.read_csv(obj['Body'])
        return extracted_data
    except botocore.exceptions.ClientError as error:
        raise error


def upload_preprocessed_data(preprocessed_data: pd.DataFrame, today: str,
                             bucket_name: str, preprocessed_destination_path_prefix: str) -> None:
    """Upload preprocessed data

    param preprocessed_data: Dataframe of preprocessed data.
    type: pd.DataFrame
    param today: Today's date.
    type: str
    param bucket_name: Name of S3 bucket.
    type: str
    param preprocessed_destination_path_prefix: Path prefix to preprocessed data.
    type: str

    return: None
    rtype: None
    """

    s3 = boto3.client('s3')
    key = f'{preprocessed_destination_path_prefix}/preprocessed_data_{today}.csv'
    s3.put_object(Bucket=bucket_name, Key=key,
                  Body=preprocessed_data.to_csv(index=False))
