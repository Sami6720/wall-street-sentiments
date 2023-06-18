import boto3
import botocore
import pandas as pd


def get_data_from_s3(bucket_name: str, data_path_prefix: str,
                     today: str, data_type: str) -> pd.DataFrame:
    """Get data from S3

    param bucket_name: Name of S3 bucket.
    type: str
    param data_path_prefix: Path prefix to data.
    type: str
    param today: Today's date.
    type: str
    param data_type: Type of data.
    type: str

    return: Fetched data.
    rtype: pd.DataFrame
    """

    s3 = boto3.client('s3')
    key = f'{data_path_prefix}/{data_type}_{today}.csv'
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        extracted_data = pd.read_csv(obj['Body'])
        return extracted_data
    except botocore.exceptions.ClientError as error:
        raise error


def upload_data_to_s3(bucket_name: str, destination_prefix: str,
                      data: pd.DataFrame, today: str, data_type: str) -> None:
    """Upload data to S3

    param bucket_name: Name of S3 bucket.
    type: str
    param destination_prefix: Path prefix to data.
    type: str
    param data: Data to be uploaded.
    type: pd.DataFrame
    param today: Today's date.
    type: str
    param data_type: Type of data.
    type: str

    return: None
    """

    s3 = boto3.client('s3')
    key = f'{destination_prefix}/{data_type}_{today}.csv'
    s3.put_object(Bucket=bucket_name, Key=key,
                  Body=data.to_csv(index=False))
