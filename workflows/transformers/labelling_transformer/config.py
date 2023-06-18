import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Config class"""

    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.preprocessed_data_path_prefix = os.getenv(
            "PREPROCESSED_DATA_PATH_PREFIX")
        self.top_stocks_prices_extracted_prefix = os.getenv(
            "TOP_STOCKS_PRICES_EXTRACTED_PREFIX")
        self.labelled_data_destination_prefix = os.getenv(
            "LABELLED_DATA_DESTINATION_PREFIX")
