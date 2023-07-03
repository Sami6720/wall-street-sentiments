import os


class Config:
    """Config class"""

    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.labelled_data_destination_prefix = os.getenv(
            "LABELLED_DATA_DESTINATION_PREFIX")
