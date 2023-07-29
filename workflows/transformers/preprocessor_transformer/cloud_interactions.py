import boto3
import botocore
import pandas as pd


def build_s3_path(data_path_prefix: str,
                  file_extension: str,
                  today: str, data_type: str) -> str:
    """Build S3 path

    param bucket_name: Name of S3 bucket.
    type: str
    param extension: Extension of file.
    type: str
    param data_path_prefix: Path prefix to data.
    type: str
    param today: Today's date.
    type: str
    param data_type: Type of data.
    type: str

    return: S3 path.
    rtype: str
    """
    return f'{data_path_prefix}/{data_type}_{today}.{file_extension}'


def get_data_from_s3(bucket_name: str, s3_path: str) -> pd.DataFrame:
    """Get data from S3

    param bucket_name: Name of S3 bucket.
    type: str
    param s3_path: Path to data.
    type: str

    return: Fetched data.
    rtype: pd.DataFrame
    """

    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=s3_path)
        extracted_data = pd.read_csv(obj['Body'])
        return extracted_data
    except botocore.exceptions.ClientError as error:
        raise error


def upload_data_to_s3(bucket_name: str, s3_path: str, data: any) -> None:
    """Upload data to S3

    param bucket_name: Name of S3 bucket.
    type: str
    param s3_path: Path to data.
    type: str
    param data: Data to be uploaded.
    type: csv or json

    return: None
    """

    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_path,
                      Body=data)
    except botocore.exceptions.ClientError as error:
        raise error
