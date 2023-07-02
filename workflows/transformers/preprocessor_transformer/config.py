import os


class Config:
    """Config class"""

    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.preprocessed_destination_path_prefix = os.getenv(
            "PREPROCESSED_DESTINATION_PATH_PREFIX")
