import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Config class"""

    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.top_stocks_info_extracted_path_prefix = os.getenv(
            "TOP_STOCKS_INFO_EXTRACTED_PATH_PREFIX")
        self.preprocessed_destination_path_prefix = os.getenv(
            "PREPROCESSED_DESTINATION_PATH_PREFIX")
